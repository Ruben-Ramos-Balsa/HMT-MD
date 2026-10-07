#!/usr/bin/env python3
"""Check cumulative source preservation, independently of proof coverage."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def lean_rows(document):
    return [r for r in document["files"] if r["path"].endswith(".lean")]


def checked_rows(document, root):
    root = root.resolve()
    rows = lean_rows(document)
    if not rows:
        raise ValueError("No Lean sources in candidate manifest")
    paths = set()
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe manifest path: " + str(relative))
        if str(relative) in paths:
            raise ValueError("Duplicate manifest path: " + str(relative))
        paths.add(str(relative))
        target = (root / relative).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError("Missing or external Lean source: " + str(relative))
        data = target.read_bytes()
        if sha(data) != row["sha256"] or len(data) != row["bytes"]:
            raise ValueError("Source does not match manifest: " + str(relative))
    return rows


def check(baseline, candidate, root):
    rows = checked_rows(candidate, root)
    if not baseline["files"]:
        raise ValueError("Empty preservation baseline")
    available = {r["sha256"] for r in rows}
    absent = [r["path"] for r in baseline["files"] if r["sha256"] not in available]
    if absent:
        raise ValueError("Prior sources lost; retain archived bytes: " + ", ".join(absent))
    return {"status": "PASS_LEAN_SOURCE_PRESERVATION",
            "baseline_unique_sources": len({r["sha256"] for r in baseline["files"]}),
            "candidate_unique_sources": len(available),
            "meaning": "Byte preservation only; no new proof-coverage claim."}


def self_test():
    with tempfile.TemporaryDirectory(prefix="hmt-lean-preservation-") as folder:
        root = Path(folder)
        content = b"theorem preserved : True := True.intro\n"
        (root / "A.lean").write_bytes(content)
        row = {"path": "A.lean", "sha256": sha(content), "bytes": len(content)}
        base = {"files": [row]}
        assert check(base, base, root)["status"] == "PASS_LEAN_SOURCE_PRESERVATION"
        # Renaming or moving to an archive keeps the exact old source.
        (root / "archive.lean").write_bytes(content)
        moved = {"files": [{**row, "path": "archive.lean"}]}
        check(base, moved, root)
        # Removing both the source and its manifest row must not hide the loss.
        other = b"theorem newer : True := True.intro\n"
        (root / "B.lean").write_bytes(other)
        replaced = {"files": [{"path": "B.lean", "sha256": sha(other), "bytes": len(other)}]}
        failures = 0
        for candidate in (replaced, {"files": [row, row]}):
            try:
                check(base, candidate, root)
            except ValueError:
                failures += 1
        (root / "A.lean").write_bytes(other)
        try:
            check(base, base, root)
        except ValueError:
            failures += 1
        (root / "A.lean").unlink()
        try:
            check(base, base, root)
        except ValueError:
            failures += 1
        assert failures == 4
    print("PASS_LEAN_PRESERVATION_SELF_TEST: intact, relocated, removal, duplicate, alteration, missing")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.baseline or not args.manifest or not args.root:
        parser.error("--baseline, --manifest and --root are required")
    document_bytes = args.manifest.read_bytes()
    candidate = json.loads(document_bytes)
    if args.capture:
        rows = checked_rows(candidate, args.root)
        baseline = {"schema": "hmt.lean.preservation.v1",
                    "source_manifest_sha256": sha(document_bytes),
                    "files": [{k: r[k] for k in ("path", "sha256", "bytes")} for r in rows]}
        # A baseline is immutable: creation never silently replaces it.
        with args.baseline.open("x") as handle:
            json.dump(baseline, handle, indent=2)
            handle.write("\n")
    else:
        baseline = json.loads(args.baseline.read_bytes())
    result = check(baseline, candidate, args.root)
    result["baseline_sha256"] = sha(args.baseline.read_bytes())
    result["candidate_manifest_sha256"] = sha(document_bytes)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit("FAIL_LEAN_SOURCE_PRESERVATION: " + str(error))
