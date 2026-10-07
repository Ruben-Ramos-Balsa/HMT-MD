#!/usr/bin/env python3
"""Verify the derived GitHub transport using Python's standard library only.

Usage (after extracting the complete Release ZIP):
    python3 -I -B -S verificar_edicion.py --root "/path/to/HOLOGRAFÍA MODULAR TRIÁDICA"

For the intentionally smaller browsable repository copy, add --view.
The pinned original manifest remains unchanged, including its excluded Finder row.
This program verifies transported bytes; it does not validate scientific results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys


ORIGINAL_MANIFEST = "06_VERIFICACION/MANIFIESTO.json"
ORIGINAL_MANIFEST_SHA256 = "3bc8a5aad20d7de02f511d0eddd731524c2767734b93c3e4e8e853886d7fd03f"
ORIGINAL_SCHEMA = "HMT_PUBLIC_DELIVERY_FILES_V1"
ORIGINAL_RECORD_COUNT = 29014
EXCLUDED_RECORD = {
    "path": ".DS_Store",
    "bytes": 8196,
    "sha256": "2e806d78415b0dcb357b02a69eb20444cd387490a4dd31450e1e119f6bca42c1",
}
ARCHIVE_ROOT = "HOLOGRAFÍA MODULAR TRIÁDICA"
CHUNK_SIZE = 1024 * 1024
SCOPE = (
    "Integrity of the derived transport only: retained original-manifest files "
    "and the unchanged original manifest. No mathematical validation, new "
    "scientific computation, Lean compilation or native Windows execution."
)
CAVEAT = (
    "The original manifest includes a Finder .DS_Store record. That single "
    "record is excluded from this derivative and is not repaired or removed "
    "from the original manifest. PASS_TRANSPORT_CONTENT does not mean "
    "PASS_FILE_INTEGRITY for the original delivery."
)


class TransportError(Exception):
    """A fail-closed validation error suitable for a public report."""


def valid_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise TransportError("Invalid relative path in manifest")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value:
        raise TransportError("Non-canonical manifest path: " + value)
    if any(part in ("", ".", "..") or ":" in part for part in path.parts):
        raise TransportError("Unsafe manifest path: " + value)
    return value


def is_git_metadata(path: str) -> bool:
    return ".git" in PurePosixPath(path).parts


def is_finder_metadata(path: str) -> bool:
    return PurePosixPath(path).name == ".DS_Store"


def open_regular(path: Path):
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise TransportError("Not a regular file: " + str(path))
        # O_NOFOLLOW is not implemented on every supported platform.
        if path.is_symlink():
            raise TransportError("Symbolic links are not allowed: " + str(path))
        return os.fdopen(descriptor, "rb"), info
    except BaseException:
        os.close(descriptor)
        raise


def unchanged(before, after) -> bool:
    return (
        before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
        stat.S_IMODE(before.st_mode),
    ) == (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
        stat.S_IMODE(after.st_mode),
    )


def hash_regular(path: Path) -> dict:
    stream, before = open_regular(path)
    digest = hashlib.sha256()
    total = 0
    with stream:
        while True:
            chunk = stream.read(CHUNK_SIZE)
            if not chunk:
                break
            total += len(chunk)
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    if not unchanged(before, after) or total != before.st_size:
        raise TransportError("File changed while being read: " + str(path))
    return {
        "bytes": total,
        "sha256": digest.hexdigest(),
        "unix_mode": stat.S_IMODE(before.st_mode),
    }


def read_manifest(root: Path):
    path = root / ORIGINAL_MANIFEST
    stream, before = open_regular(path)
    with stream:
        raw = stream.read()
        after = os.fstat(stream.fileno())
    if not unchanged(before, after) or len(raw) != before.st_size:
        raise TransportError("Original manifest changed during reading")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != ORIGINAL_MANIFEST_SHA256:
        raise TransportError("Original manifest SHA256 does not match the pinned delivery")
    manifest = json.loads(raw)
    if manifest.get("schema") != ORIGINAL_SCHEMA:
        raise TransportError("Unexpected original manifest schema")
    records = manifest.get("files")
    if not isinstance(records, list) or len(records) != ORIGINAL_RECORD_COUNT:
        raise TransportError("Unexpected original manifest record count")
    entries = {}
    for item in records:
        if not isinstance(item, dict) or set(item) != {"path", "bytes", "sha256"}:
            raise TransportError("Unexpected original file-record structure")
        relative = valid_relative_path(item["path"])
        if relative in entries or relative == ORIGINAL_MANIFEST:
            raise TransportError("Duplicate or self-referential manifest record: " + relative)
        if type(item["bytes"]) is not int or item["bytes"] < 0:
            raise TransportError("Invalid file size: " + relative)
        value = item["sha256"]
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise TransportError("Invalid SHA256: " + relative)
        entries[relative] = dict(item)
    if entries.get(".DS_Store") != EXCLUDED_RECORD:
        raise TransportError("The sole permitted original-manifest exclusion changed")
    if any(is_finder_metadata(p) for p in entries if p != ".DS_Store"):
        raise TransportError("Unexpected additional Finder record in original manifest")
    if manifest.get("count") != len(entries) or manifest.get("bytes") != sum(e["bytes"] for e in entries.values()):
        raise TransportError("Original manifest totals do not match its records")
    selected = {p: e for p, e in entries.items() if p != ".DS_Store"}
    selected[ORIGINAL_MANIFEST] = {
        "path": ORIGINAL_MANIFEST, "bytes": len(raw), "sha256": digest,
    }
    return manifest, selected


def scan_tree(root: Path):
    if root.is_symlink() or not root.is_dir():
        raise TransportError("Root must be an existing directory, not a symbolic link")
    files = {}
    directories = set()
    failures = []
    pending = [(root, "")]
    while pending:
        directory, prefix = pending.pop()
        with os.scandir(directory) as scan:
            children = sorted(scan, key=lambda item: item.name)
        for child in children:
            relative = prefix + child.name
            info = child.stat(follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                failures.append({"path": relative, "issue": "symbolic_link"})
            elif stat.S_ISDIR(info.st_mode):
                directories.add(relative)
                pending.append((Path(child.path), relative + "/"))
            elif stat.S_ISREG(info.st_mode):
                files[relative] = {"bytes": info.st_size, "unix_mode": stat.S_IMODE(info.st_mode)}
            else:
                failures.append({"path": relative, "issue": "non_regular_file"})
    return files, directories, failures


def required_directories(paths) -> set:
    directories = set()
    for relative in paths:
        parent = PurePosixPath(relative).parent
        while parent != PurePosixPath("."):
            directories.add(parent.as_posix())
            parent = parent.parent
    return directories


def verify_tree(root: Path, view: bool = False) -> dict:
    root = Path(root)
    manifest, complete = read_manifest(root)
    expected = {p: e for p, e in complete.items() if not (view and is_git_metadata(p))}
    actual, directories, failures = scan_tree(root)
    allowed_directories = required_directories(expected)
    ignored = []
    for relative in sorted(actual):
        if relative in expected:
            continue
        if is_finder_metadata(relative):
            ignored.append({"path": relative, "bytes": actual[relative]["bytes"]})
        else:
            failures.append({"path": relative, "issue": "unexpected_file"})
    # A directory is not an allowed extra merely because it contains a .DS_Store.
    for relative in sorted(directories - allowed_directories):
        failures.append({"path": relative, "issue": "unexpected_directory"})
    verified = 0
    verified_bytes = 0
    for relative, item in sorted(expected.items()):
        if relative not in actual:
            failures.append({"path": relative, "issue": "missing_file"})
            continue
        try:
            observed = hash_regular(root / relative)
        except (OSError, TransportError) as error:
            failures.append({"path": relative, "issue": "read_failed", "detail": str(error)})
            continue
        if observed["bytes"] != item["bytes"] or observed["sha256"] != item["sha256"]:
            failures.append({
                "path": relative, "issue": "content_mismatch",
                "expected_bytes": item["bytes"], "actual_bytes": observed["bytes"],
                "expected_sha256": item["sha256"], "actual_sha256": observed["sha256"],
            })
        else:
            verified += 1
            verified_bytes += observed["bytes"]
    return {
        "status": "FAIL_TRANSPORT_CONTENT" if failures else "PASS_TRANSPORT_CONTENT",
        "mode": "browsable_view" if view else "complete_extraction",
        "scope": SCOPE,
        "caveat": CAVEAT,
        "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
        "original_edition": manifest.get("edition"),
        "excluded_original_record": dict(EXCLUDED_RECORD),
        "expected_files": len(expected),
        "expected_bytes": sum(e["bytes"] for e in expected.values()),
        "verified_files": verified,
        "verified_bytes": verified_bytes,
        "git_metadata_files_omitted_for_view": sorted(p for p in complete if view and is_git_metadata(p)),
        "ignored_finder_metadata": ignored,
        "failure_count": len(failures),
        "failures": failures,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Path to the extracted edition directory")
    parser.add_argument("--view", action="store_true", help="Verify only the repository view, which excludes .git components")
    args = parser.parse_args(argv)
    try:
        result = verify_tree(args.root, args.view)
    except (OSError, TransportError, ValueError, TypeError) as error:
        result = {
            "status": "FAIL_TRANSPORT_CONTENT",
            "mode": "browsable_view" if args.view else "complete_extraction",
            "scope": SCOPE, "caveat": CAVEAT,
            "failure_count": 1,
            "failures": [{"issue": "validation_error", "detail": str(error)}],
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS_TRANSPORT_CONTENT" else 1


if __name__ == "__main__":
    sys.exit(main())
