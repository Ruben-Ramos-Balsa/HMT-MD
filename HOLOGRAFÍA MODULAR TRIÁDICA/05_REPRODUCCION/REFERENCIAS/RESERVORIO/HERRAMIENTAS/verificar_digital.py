#!/usr/bin/env python3
"""Read-only, standard-library verification of hmt.digital.v1 deliveries.

The JSON report must be outside the delivery. This program never executes
scientific code, TeX, Lean, installers or network operations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata

SCHEMA = "hmt.digital.v1"
BAD_WINDOWS = re.compile(r'[<>:"\\|?*\x00-\x1f]')
RESERVED_WINDOWS = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])$", re.I)
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def canonical(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def relative_path(value, *, allow_root=False) -> str:
    """Validate a portable, unambiguous POSIX-relative manifest locator."""
    if not isinstance(value, str) or not value:
        raise ValueError("Expected a nonempty relative path string")
    if allow_root and value == ".":
        return value
    if value.startswith("/") or "\\" in value:
        raise ValueError("Absolute paths and backslashes are forbidden")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("Empty components, '.' and '..' are forbidden")
    for part in parts:
        if BAD_WINDOWS.search(part):
            raise ValueError("Windows-incompatible filename character")
        if part.endswith((".", " ")):
            raise ValueError("A path component ends in dot or space")
        if RESERVED_WINDOWS.fullmatch(part.split(".", 1)[0]):
            raise ValueError("Reserved Windows device name")
    return value


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("Duplicate JSON key: " + key)
        obj[key] = value
    return obj


def digest_file(path: Path) -> tuple[int, str]:
    """Reject leaf symlinks and files altered during hashing."""
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("Not a regular file")
        digest = hashlib.sha256()
        count = 0
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            count += len(chunk)
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    final_path = path.lstat()
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
    if any(getattr(before, field) != getattr(after, field) for field in fields):
        raise ValueError("File changed during hashing")
    if (not stat.S_ISREG(final_path.st_mode) or
            any(getattr(after, field) != getattr(final_path, field) for field in fields)):
        raise ValueError("File path was replaced during hashing")
    if count != after.st_size:
        raise ValueError("File size changed during hashing")
    return count, digest.hexdigest()


def verify(root: Path, manifest_name="MANIFEST.json", long_path=240) -> dict:
    report = {
        "schema": "hmt.digital.report.v1", "status": "FAIL",
        "root": str(root.absolute()), "manifest": manifest_name,
        "errors": [], "warnings": [], "checked_files": 0, "checked_units": 0,
        "scientific_execution": False, "package_modified": False,
    }

    def issue(code, path, message, warning=False):
        report["warnings" if warning else "errors"].append(
            {"code": code, "path": str(path), "message": str(message)})

    try:
        manifest_name = relative_path(manifest_name)
        if root.is_symlink():
            raise ValueError("The delivery root must not be a symlink")
        root = root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("The delivery root must be a directory")
    except (OSError, ValueError) as exc:
        issue("ROOT_OR_MANIFEST_PATH", root, exc)
        return report

    report["root"] = str(root)
    files, directories, actual_keys = {}, set(), {}

    def scan(directory: Path):
        try:
            entries = sorted(os.scandir(directory), key=lambda e: e.name)
        except OSError as exc:
            issue("SCAN_ERROR", directory, exc)
            return
        for entry in entries:
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            try:
                relative_path(rel)
            except ValueError as exc:
                issue("UNSAFE_INVENTORY_NAME", rel, exc)
            key = canonical(rel)
            if key in actual_keys and actual_keys[key] != rel:
                issue("INVENTORY_COLLISION", rel, "NFC/casefold collision with " + actual_keys[key])
            actual_keys[key] = rel
            if len(rel) >= long_path or len(str(path)) >= long_path:
                issue("LONG_PATH", rel, "Long path; target-system limits may require a shorter extraction location", True)
            try:
                info = entry.stat(follow_symlinks=False)
                if (stat.S_ISLNK(info.st_mode) or
                        getattr(info, "st_file_attributes", 0) &
                        getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)):
                    issue("SYMLINK", rel, "Symbolic links and Windows reparse points are forbidden")
                elif stat.S_ISDIR(info.st_mode):
                    directories.add(rel)
                    scan(path)
                elif stat.S_ISREG(info.st_mode):
                    files[rel] = path
                else:
                    issue("SPECIAL_FILE", rel, "Only ordinary files and directories are allowed")
            except OSError as exc:
                issue("SCAN_ERROR", rel, exc)

    scan(root)
    if manifest_name not in files:
        issue("MANIFEST_MISSING", manifest_name, "Manifest is not an ordinary local file")
        return report
    try:
        manifest = json.loads(files[manifest_name].read_text(encoding="utf-8"),
                              object_pairs_hook=unique_object)
    except (OSError, ValueError) as exc:
        issue("MANIFEST_JSON", manifest_name, exc)
        return report
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        issue("SCHEMA", manifest_name, "Expected schema " + SCHEMA)
        return report

    expected_files, expected_dirs, manifest_keys = set(), set(), {}

    def register(locator, label, allow_root=False):
        try:
            rel = relative_path(locator, allow_root=allow_root)
        except ValueError as exc:
            issue("UNSAFE_MANIFEST_PATH", label, exc)
            return None
        if rel == ".":
            return rel
        parts = rel.split("/")
        for length in range(1, len(parts) + 1):
            prefix = "/".join(parts[:length])
            key = canonical(prefix)
            old = manifest_keys.get(key)
            if old is not None and old != prefix:
                issue("MANIFEST_COLLISION", prefix, "NFC/casefold collision with " + old)
            manifest_keys[key] = prefix
        expected_dirs.update("/".join(parts[:n]) for n in range(1, len(parts)))
        return rel

    register(manifest_name, "manifest")
    records = manifest.get("files")
    if not isinstance(records, list) or not records:
        issue("EMPTY_FILES", manifest_name, "files must be a nonempty list")
        records = []
    for index, record in enumerate(records):
        label = "files[" + str(index) + "]"
        if not isinstance(record, dict):
            issue("FILE_RECORD", label, "Expected an object")
            continue
        rel = register(record.get("path"), label)
        if rel is None:
            continue
        if rel == manifest_name:
            issue("MANIFEST_SELF_REFERENCE", rel, "The manifest is excluded from its own files list")
            continue
        if rel in expected_files:
            issue("DUPLICATE_FILE", rel, "Duplicate file record")
        expected_files.add(rel)
        size, digest = record.get("size"), record.get("sha256")
        if type(size) is not int or size < 0 or not isinstance(digest, str) or not SHA256.fullmatch(digest):
            issue("FILE_RECORD", rel, "size must be a nonnegative integer and sha256 a 64-digit hex string")
            continue
        if rel not in files:
            issue("FILE_MISSING", rel, "Expected ordinary local file not found")
            continue
        try:
            # resolve also protects against a directory link substituted after scanning.
            target = files[rel].resolve(strict=True)
            if not target.is_relative_to(root):
                raise ValueError("Resolved file escapes delivery")
            current = root
            for component in rel.split("/"):
                current = current / component
                if current.is_symlink():
                    raise ValueError("Path changed into a symbolic link")
            actual_size, actual_hash = digest_file(files[rel])
            report["checked_files"] += 1
            if actual_size != size:
                issue("SIZE_MISMATCH", rel, "Expected " + str(size) + "; received " + str(actual_size))
            if actual_hash != digest.lower():
                issue("HASH_MISMATCH", rel, "SHA-256 mismatch")
        except (OSError, ValueError) as exc:
            issue("FILE_READ", rel, exc)

    units = manifest.get("units")
    if not isinstance(units, list) or not units:
        issue("EMPTY_UNITS", manifest_name, "units must be a nonempty list")
        units = []
    unit_ids = set()
    unit_paths = set()
    for index, unit in enumerate(units):
        label = "units[" + str(index) + "]"
        if not isinstance(unit, dict):
            issue("UNIT_RECORD", label, "Expected an object")
            continue
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or not unit_id.strip():
            issue("UNIT_ID", label, "Expected a nonempty id")
        elif canonical(unit_id) in unit_ids:
            issue("DUPLICATE_UNIT_ID", label, "Duplicate normalized unit id")
        else:
            unit_ids.add(canonical(unit_id))
        unit_path = register(unit.get("path"), label, allow_root=True)
        if unit_path is None:
            continue
        if canonical(unit_path) in unit_paths:
            issue("DUPLICATE_UNIT_PATH", unit_path, "Two units use the same directory")
        unit_paths.add(canonical(unit_path))
        if unit_path != ".":
            expected_dirs.add(unit_path)
            if unit_path not in directories:
                issue("UNIT_MISSING", unit_path, "Unit directory not found")
        required = unit.get("required")
        if not isinstance(required, list) or not required:
            issue("EMPTY_REQUIRED", label, "Every unit needs a nonempty required list")
            required = []
        locators = [(item, "required", False) for item in required]
        locators += [(unit[key], key, True) for key in ("pdf", "readme") if key in unit]
        for item, role, file_only in locators:
            try:
                local = relative_path(item)
            except ValueError as exc:
                issue("UNSAFE_MANIFEST_PATH", label + "." + role, exc)
                continue
            full = local if unit_path == "." else unit_path + "/" + local
            register(full, label + "." + role)
            if full in files:
                if full not in expected_files:
                    issue("UNIT_FILE_UNLISTED", full, "Unit file is absent from files inventory")
                if role == "pdf" and PurePosixPath(full).suffix.casefold() != ".pdf":
                    issue("PDF_EXTENSION", full, "pdf locator must name a .pdf file")
            elif full in directories and not file_only:
                expected_dirs.add(full)
            else:
                issue("UNIT_REQUIRED_MISSING", full, "Expected local " + ("file" if file_only else "file or directory"))
        report["checked_units"] += 1

    for rel in sorted(set(files) - expected_files - {manifest_name}):
        issue("EXTRA_FILE", rel, "File is absent from manifest")
    for rel in sorted(directories - expected_dirs):
        issue("EXTRA_DIRECTORY", rel, "Directory is absent from inventory structure and unit requirements")
    if not report["errors"]:
        report["status"] = "PASS"
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", default="MANIFEST.json", help="Relative manifest locator")
    parser.add_argument("--report", type=Path, required=True, help="JSON output outside --root")
    parser.add_argument("--long-path-warning", type=int, default=240)
    args = parser.parse_args(argv)
    if args.long_path_warning < 1:
        parser.error("--long-path-warning must be positive")
    target = args.report.resolve()
    base = args.root.resolve()
    if target == base or target.is_relative_to(base) or args.report.is_symlink():
        parser.error("--report must be an external, non-symlink file")
    report = verify(args.root, args.manifest, args.long_path_warning)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        print("FAIL: cannot write external report: " + str(exc), file=sys.stderr)
        return 2
    print(report["status"] + " hmt.digital.v1: " + str(report["checked_files"]) +
          " files; " + str(report["checked_units"]) + " units; " +
          str(len(report["errors"])) + " errors; " + str(len(report["warnings"])) + " warnings")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
