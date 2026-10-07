#!/usr/bin/env python3
"""Create the deterministic distribution archive for the English edition."""

from __future__ import annotations

import hashlib
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.parent / (ROOT.name + ".zip")
FIXED_TIME = (2026, 9, 14, 0, 0, 0)


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if "build" in relative.parts:
        return False
    if path.name == ".DS_Store" or path.suffix == ".olean":
        return False
    return path.is_file() and not path.is_symlink()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    files = sorted(
        (path for path in ROOT.rglob("*") if included(path)),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    temporary = ARCHIVE.with_suffix(".zip.tmp")
    with zipfile.ZipFile(
        temporary,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for path in files:
            relative = Path(ROOT.name) / path.relative_to(ROOT)
            info = zipfile.ZipInfo(relative.as_posix(), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
    temporary.replace(ARCHIVE)
    print(
        "PASS_DETERMINISTIC_ENGLISH_EDITION_ZIP "
        f"files={len(files)} sha256={sha256(ARCHIVE)}"
    )


if __name__ == "__main__":
    main()
