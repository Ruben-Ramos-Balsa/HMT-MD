#!/usr/bin/env python3
"""Compile the local Article IV REV02 draft and record technical provenance.

Python standard library only. --check-only never invokes TeX or writes files.
This driver requires and rebinds a real hmt-md-precompile-receipt-v2.
It does not issue that receipt, certify mathematics or perform visual review.
Origin: the Article VII driver; IV REV02 adapts the authored root and output.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT
PDF_NAME = "ARTICULO_IV_MOONSHINE_DUALIDAD_TEORIA_M_REV02.pdf"
PREFLIGHT_SCHEMA = "hmt-md-precompile-receipt-v2"
PREFLIGHT_STATUS = "PASS_HMT_MD_PRECOMPILE"
TEX_COMMAND_RE = re.compile(
    r"\\(?P<cmd>input|include|subfile|includepdf|includegraphics|"
    r"addbibresource|bibliography|usepackage|documentclass)"
    r"(?:\s*\[[^\]]*\])?\s*\{(?P<arg>[^{}]+)\}", re.MULTILINE)
TEX_IMPORT_RE = re.compile(
    r"\\(?P<cmd>import|subimport)\s*\{(?P<dir>[^{}]+)\}\s*\{(?P<arg>[^{}]+)\}",
    re.MULTILINE)
TEX_SINGLE_FILE_RE = re.compile(
    r"\\(?P<cmd>lstinputlisting|VerbatimInput|verbatiminput)"
    r"(?:\s*\[[^\]]*\])?\s*\{(?P<arg>[^{}]+)\}", re.MULTILINE)
TEX_MINTED_RE = re.compile(
    r"\\inputminted(?:\s*\[[^\]]*\])?\s*\{[^{}]+\}\s*\{(?P<arg>[^{}]+)\}",
    re.MULTILINE)
DYNAMIC_TEX_RE = re.compile(
    r"\\(?:write18|directlua|openin|read\b|@@input|scantokens|"
    r"CatchFileDef|InputIfFileExists|ShellEscape)\b", re.IGNORECASE)
EXTENSIONS = {
    "input": ("", ".tex"), "include": ("", ".tex"), "subfile": ("", ".tex"),
    "import": ("", ".tex"), "subimport": ("", ".tex"),
    "includepdf": ("", ".pdf"),
    "includegraphics": ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg"),
    "addbibresource": ("", ".bib"), "bibliography": ("", ".bib"),
    "usepackage": ("", ".sty"), "documentclass": ("", ".cls"),
    "lstinputlisting": ("", ".tex", ".py", ".json", ".txt", ".csv"),
    "VerbatimInput": ("", ".tex", ".py", ".json", ".txt", ".csv"),
    "verbatiminput": ("", ".tex", ".py", ".json", ".txt", ".csv"),
    "inputminted": ("", ".tex", ".py", ".json", ".txt", ".csv"),
}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return h.hexdigest()


def local(path):
    return path.resolve().is_relative_to(ROOT.resolve())


def relative(path):
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def record(path):
    return {"path": relative(path), "sha256": digest(path),
            "bytes": path.stat().st_size}


def canonical_json(payload):
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def payload_digest(payload):
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def strip_comments(text):
    # Same even/odd backslash treatment as precompile_hmt_md.py.
    lines = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            slashes, cursor = 0, index - 1
            while cursor >= 0 and line[cursor] == "\\":
                slashes += 1
                cursor -= 1
            if slashes % 2 == 0:
                cut = index
                break
        lines.append(line[:cut])
    return "\n".join(lines)


def tex_commands(path):
    """Reproduce the literal import scan of the real preflight producer."""
    text = strip_comments(path.read_text(encoding="utf-8"))
    if DYNAMIC_TEX_RE.search(text):
        raise ValueError("Dynamic TeX dependency in " + relative(path))
    result = []
    for match in TEX_COMMAND_RE.finditer(text):
        command, argument = match.group("cmd"), match.group("arg")
        if command in {"bibliography", "usepackage"}:
            result.extend((command, item.strip()) for item in argument.split(",")
                          if item.strip())
        else:
            result.append((command, argument))
    result.extend((m.group("cmd"), str(Path(m.group("dir")) / m.group("arg")))
                  for m in TEX_IMPORT_RE.finditer(text))
    result.extend((m.group("cmd"), m.group("arg"))
                  for m in TEX_SINGLE_FILE_RE.finditer(text))
    result.extend(("inputminted", m.group("arg"))
                  for m in TEX_MINTED_RE.finditer(text))
    return result


def resolve_tex(importer, command, argument):
    argument = argument.strip()
    if not argument or any(x in argument for x in ("\\", "#", "$", "|")):
        raise ValueError("Dynamic/invalid dependency: " + argument)
    raw = Path(argument).expanduser()
    if command in {"usepackage", "documentclass"} and "/" not in argument and not raw.suffix:
        candidates = [base / (argument + ext)
                      for base in (importer.parent, MANUSCRIPT)
                      for ext in EXTENSIONS[command]]
        if not any(p.exists() for p in candidates):
            return None  # Runtime package, not an authored package.
    bases = [Path("/")] if raw.is_absolute() else [importer.parent, MANUSCRIPT]
    for base in bases:
        stem = raw if raw.is_absolute() else base / raw
        for extension in EXTENSIONS[command]:
            candidate = stem if extension == "" or stem.suffix else Path(str(stem) + extension)
            if candidate.exists():
                if candidate.is_symlink() or not candidate.is_file() or not local(candidate):
                    raise ValueError("Nonlocal or nonregular dependency: " + str(candidate))
                return candidate.resolve()
    raise ValueError("Missing dependency: " + relative(importer) + " -> " + argument)


def source_graph():
    files, images, edges, errors = {}, {}, [], []
    labels = collections.defaultdict(list)
    inclusions = collections.Counter()

    def walk(path, stack):
        key = relative(path)
        inclusions[key] += 1
        if key in stack:
            errors.append("Cyclic inclusion: " + " -> ".join(stack + [key]))
            return
        if key in files:
            return
        files[key] = record(path)
        content = strip_comments(path.read_text(encoding="utf-8"))
        for name in re.findall(r"\\label\s*\{([^{}]+)\}", content):
            labels[name].append(key)
        try:
            commands = tex_commands(path)
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
            return
        for command, name in commands:
            try:
                child = resolve_tex(path, command, name)
            except (ValueError, OSError) as exc:
                errors.append(str(exc))
                continue
            if child is not None:
                child_key = relative(child)
                edges.append({"from": key, "to": child_key,
                              "command": command, "sha256": digest(child)})
                if command in {"input", "include", "subfile", "import", "subimport",
                               "usepackage", "documentclass"}:
                    walk(child, stack + [key])
                else:
                    images[child_key] = record(child)

    entry = MANUSCRIPT / "main.tex"
    if entry.is_file():
        walk(entry.resolve(), [])
    else:
        errors.append("Missing main.tex")
    result = {
        "entry": "main.tex",
        "tex": sorted(files.values(), key=lambda x: x["path"]),
        "images": sorted(images.values(), key=lambda x: x["path"]),
        "images_field_scope": "All non-TeX authored assets, including bibliography/listings",
        "edges": edges,
        "label_count": len(labels),
        "duplicate_labels_in_sources": {k: v for k, v in labels.items()
                                        if len(v) > 1},
        "repeated_inclusions": {k: n for k, n in inclusions.items() if n > 1},
        "errors": errors,
    }
    result["active_graph_sha256"] = payload_digest({
        "entry": result["entry"], "tex": result["tex"], "assets": result["images"],
        "edges": result["edges"]})
    return result


def verify_preflight(receipt_path, graph):
    """Consume a genuine producer receipt; never create scientific approval."""
    if not receipt_path.is_file():
        raise ValueError("Preflight receipt not found: " + str(receipt_path))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("schema_version") != PREFLIGHT_SCHEMA or receipt.get("status") != PREFLIGHT_STATUS:
        raise ValueError("A real PASS_HMT_MD_PRECOMPILE v2 receipt is required")
    if receipt.get("phase") != "preflight":
        raise ValueError("Wrong preflight phase")
    body = {k: v for k, v in receipt.items() if k != "receipt_payload_sha256"}
    if receipt.get("receipt_payload_sha256") != payload_digest(body):
        raise ValueError("Preflight payload checksum mismatch")
    artifact = receipt["artifact"]
    original_source = Path(artifact["source_root"])
    if not original_source.is_absolute():
        raise ValueError("Preflight source_root must be an absolute article directory")
    original_root = original_source

    def rebound(raw, base=None):
        p = Path(raw).expanduser()
        if not p.is_absolute():
            p = (base or original_root) / p
        if p.is_relative_to(original_root):
            return (ROOT / p.relative_to(original_root)).resolve()
        return p.resolve()

    entrypoint = rebound(artifact["entrypoint"], original_source)
    if entrypoint != (MANUSCRIPT / "main.tex").resolve():
        raise ValueError("Preflight entrypoint does not identify this main.tex")
    if rebound(artifact["output_pdf"]) != (ROOT / "output" / "pdf" / PDF_NAME).resolve():
        raise ValueError("Preflight output_pdf does not identify the requested IV REV02 output")

    verified_bindings, historical_external = [], []

    def binding(spec, name, must_local=False):
        if not isinstance(spec, dict) or "path" not in spec or "sha256" not in spec:
            raise ValueError("Malformed preflight binding: " + name)
        p = rebound(spec["path"])
        if local(p):
            if not p.is_file() or p.is_symlink() or digest(p) != spec["sha256"]:
                raise ValueError("Stale or missing preflight binding: " + name + ": " + str(p))
            verified_bindings.append({"name": name, **record(p)})
        elif must_local:
            raise ValueError("Portable local preflight binding required: " + name)
        else:
            historical_external.append({"name": name, "path": spec["path"],
                                        "sha256": spec["sha256"],
                                        "scope": "Historical preflight execution; not rerun by compiler"})
        return p

    contract_path = binding(receipt["contract"], "contract", True)
    ledger_path = binding(receipt["editorial_ledgers"]["manuscript"], "manuscript", True)
    binding(receipt["wrapper"], "preflight_producer")
    binding(receipt["claims_registry"], "claims_registry")
    for name in ("matrix", "canvas", "manuscript_manifest"):
        binding(receipt["editorial_ledgers"][name], name, True)
    for name in ("application", "physical", "physical_evidence_registry",
                 "physical_certificate_manifest"):
        spec = receipt["dossiers"][name]
        binding(spec, name)
        if "gate" in spec and "gate_sha256" in spec:
            binding({"path": spec["gate"], "sha256": spec["gate_sha256"]}, name + "_gate")
    for index, spec in enumerate(receipt["evidence"]):
        binding(spec, "evidence[" + str(index) + "]")
    for index, spec in enumerate(receipt["frozen_artifacts"]):
        binding(spec, "frozen[" + str(index) + "]")
        if rebound(spec["path"]) == (ROOT / "output" / "pdf" / PDF_NAME).resolve():
            raise ValueError("The selected output is a frozen artifact")
    for index, certificate in enumerate(receipt["certificates"]):
        binding({"path": certificate["program"], "sha256": certificate["program_sha256"]},
                "certificate[" + str(index) + "]")
        for j, spec in enumerate(certificate["inputs"]):
            binding(spec, "certificate_input[" + str(index) + "," + str(j) + "]")
    for index, spec in enumerate(receipt["separation"].get("peer_ledgers", [])):
        binding(spec, "peer_ledger[" + str(index) + "]")
    authorization = receipt["separation"].get("authorization")
    if authorization is not None:
        binding(authorization, "separation_authorization")

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    files, items = {}, []
    for index, spec in enumerate(ledger["source_files"]):
        p = rebound(spec["path"], original_source)
        if not p.is_relative_to(MANUSCRIPT.resolve()) or p.is_symlink() or not p.is_file():
            raise ValueError("Nonlocal or missing ledger source: " + str(p))
        if p in files:
            raise ValueError("Duplicate ledger source: " + str(p))
        actual = digest(p)
        if actual != spec["sha256"]:
            raise ValueError("Stale ledger source: " + relative(p))
        files[p] = actual
        items.append({"path": p.relative_to(MANUSCRIPT.resolve()).as_posix(), "sha256": actual})
    if entrypoint not in files or not files:
        raise ValueError("The ledger must include main.tex")
    merkle = payload_digest(sorted(items, key=lambda x: x["path"]))
    if merkle != receipt["source_merkle_sha256"] or len(files) != receipt["source_files"]:
        raise ValueError("Preflight source Merkle or count mismatch")
    for folder in (ROOT / 'sections', ROOT / 'figures'):
        for p in folder.rglob('*'):
            if p.is_symlink():
                raise ValueError("Symlink in authored source tree: " + str(p))
    active_files = graph["tex"] + graph["images"]
    if any((ROOT / x["path"]).resolve() not in files for x in active_files):
        raise ValueError("An active dependency is not bound by the preflight ledger")

    imports = []
    for importer in sorted((p for p in files if p.suffix.lower() in {".tex", ".sty", ".cls"}),
                           key=str):
        for command, argument in tex_commands(importer):
            target = resolve_tex(importer, command, argument)
            if target is not None:
                if target not in files:
                    raise ValueError("Import outside the source ledger: " + str(target))
                imports.append({"from": relative(importer), "command": command,
                                "to": relative(target), "sha256": digest(target)})
    received_imports = []
    for item in receipt["separation"]["imports"]:
        from_path, to_path = rebound(item["from"]), rebound(item["to"])
        if not local(from_path) or not local(to_path):
            raise ValueError("This portable manuscript requires local authored imports")
        received_imports.append({"from": relative(from_path), "command": item["command"],
                                 "to": relative(to_path), "sha256": item["sha256"]})
    if imports != received_imports:
        raise ValueError("Current literal TeX imports differ from the preflight graph")
    return {
        "status": "VALIDATED_PREFLIGHT_BINDING",
        "receipt": {"path": str(receipt_path.resolve()), "sha256": digest(receipt_path)},
        "producer_schema": PREFLIGHT_SCHEMA, "producer_status": PREFLIGHT_STATUS,
        "source_merkle_sha256": merkle,
        "active_graph_sha256": graph["active_graph_sha256"],
        "imports_sha256": payload_digest(imports), "imports": len(imports),
        "verified_local_bindings": verified_bindings,
        "external_execution_provenance": historical_external,
        "scientific_gates_reexecuted": False,
        "mathematical_validity_certified_by_this_driver": False,
    }


def warning_report(log):
    folded = re.sub(r"\s+", " ", log)
    return {
        "missing_reference_warnings": log.count("LaTeX Warning: Reference "),
        "missing_citation_warnings": log.count("LaTeX Warning: Citation "),
        "duplicate_label_warnings": len(re.findall(
            r"LaTeX Warning: Label [\x60'][^']*' multiply defined", folded)),
        "overfull_hbox": log.count("Overfull \\hbox"),
        "overfull_vbox": log.count("Overfull \\vbox"),
        "underfull_hbox": log.count("Underfull \\hbox"),
        "underfull_vbox": log.count("Underfull \\vbox"),
        "missing_glyph_warnings": log.count("Missing character:"),
        "undefined_references_summary": "There were undefined references" in folded,
        "duplicate_labels_summary": "There were multiply-defined labels" in folded,
        "rerun_warning": "Rerun to get cross-references right" in folded,
    }


def fls_dependencies(path):
    deps, external, missing = {}, set(), set()
    cwd = MANUSCRIPT.resolve()
    if not path.is_file():
        return {"local": [], "external_runtime_count": 0,
                "external_runtime_paths": [], "missing": ["main.fls"]}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("PWD "):
            cwd = Path(line[4:]).resolve()
        elif line.startswith("INPUT "):
            p = Path(line[6:])
            if not p.is_absolute():
                p = cwd / p
            p = p.resolve()
            if local(p):
                if p.is_file():
                    deps[relative(p)] = record(p)
                else:
                    missing.add(relative(p))
            else:
                external.add(str(p))
    return {
        "local": sorted(deps.values(), key=lambda x: x["path"]),
        "external_runtime_count": len(external),
        "external_runtime_paths": sorted(external),
        "missing": sorted(missing),
        "external_files_copied_or_hashed": False,
    }


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true",
                        help="Read-only source graph; do not compile or create files")
    parser.add_argument("--preflight", type=Path,
                        help="Real PASS_HMT_MD_PRECOMPILE v2 receipt; mandatory for compilation")
    parser.add_argument("--lualatex", default="lualatex",
                        help="LuaLaTeX executable or its full path")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Maximum seconds per pass; default 300")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    before = source_graph()
    engine = shutil.which(args.lualatex)
    preflight, preflight_errors = None, []
    if args.preflight is not None:
        try:
            preflight = verify_preflight(args.preflight.resolve(), before)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            preflight_errors.append(str(exc))
    elif not args.check_only:
        preflight_errors.append("--preflight is mandatory; this driver never issues approval")
    if args.check_only:
        print(json.dumps({"status": "SOURCE_GRAPH_CHECK_ONLY",
                          "lualatex": engine, "source_graph": before,
                          "preflight": preflight,
                          "preflight_errors": preflight_errors,
                          "preflight_supplied": args.preflight is not None,
                          "compilation_authorized": not before["errors"] and
                                                   not preflight_errors and preflight is not None,
                          "mathematical_validity_certified": False,
                          "files_written": False, "tex_invoked": False},
                         ensure_ascii=False, indent=2))
        return 0 if not before["errors"] and not preflight_errors else 1
    if before["errors"] or preflight_errors or engine is None:
        print(json.dumps({"status": "FAIL_PREPARACION_COMPILACION_IV_REV02",
                          "errors": before["errors"] + preflight_errors +
                          ([] if engine else ["LuaLaTeX executable not found"]),
                          "files_written": False, "tex_invoked": False},
                         ensure_ascii=False, indent=2))
        return 1

    started = datetime.datetime.now(datetime.timezone.utc)
    run_id = started.strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    build = ROOT / "tmp" / "build" / run_id
    cache = ROOT / "tmp" / "texcache"
    receipts = ROOT / "technical" / "compilacion" / run_id
    output = ROOT / "output" / "pdf"
    for p in (build, cache, receipts, output):
        if not local(p):
            raise ValueError("Output directory escapes the package: " + str(p))
        p.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TEXMFVAR"] = str(cache)
    env["TEXMFCACHE"] = str(cache)
    cmd = [engine, "-no-shell-escape", "-interaction=nonstopmode",
           "-halt-on-error", "-file-line-error", "-recorder",
           "-output-directory=" + str(build), "main.tex"]
    passes, errors = [], []
    for number in range(1, 4):
        try:
            current_graph = source_graph()
            if current_graph["errors"] or current_graph["active_graph_sha256"] != before["active_graph_sha256"]:
                errors.append("Source graph changed before pass " + str(number))
                break
            current_preflight = verify_preflight(args.preflight.resolve(), current_graph)
            if current_preflight["receipt"]["sha256"] != preflight["receipt"]["sha256"]:
                errors.append("Preflight receipt changed before pass " + str(number))
                break
            result = subprocess.run(cmd, cwd=MANUSCRIPT, env=env,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=args.timeout,
                                    check=False)
            captured, exit_code = result.stdout, result.returncode
        except subprocess.TimeoutExpired as exc:
            captured, exit_code = exc.stdout or b"", None
            errors.append("Pass " + str(number) + " exceeded timeout")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            captured, exit_code = str(exc).encode("utf-8"), None
            errors.append("Pass execution failed: " + str(exc))
        (build / ("pass-" + str(number) + ".txt")).write_bytes(captured)
        log_path = build / "main.log"
        log = (log_path.read_text(encoding="utf-8", errors="replace")
               if log_path.is_file() else captured.decode("utf-8", errors="replace"))
        passes.append({"pass": number, "exit_code": exit_code,
                       "stdout": relative(build / ("pass-" + str(number) + ".txt")),
                       "warnings": warning_report(log)})
        if exit_code != 0:
            errors.append("Pass " + str(number) + " failed")
            break

    after = source_graph()
    before_hashes = {x["path"]: x["sha256"] for x in
                     before["tex"] + before["images"]}
    after_hashes = {x["path"]: x["sha256"] for x in
                    after["tex"] + after["images"]}
    changed = sorted(k for k in before_hashes.keys() | after_hashes.keys()
                     if before_hashes.get(k) != after_hashes.get(k))
    if changed or after["errors"]:
        errors.append("Authored sources changed or became unreadable during compilation")
    if before["active_graph_sha256"] != after["active_graph_sha256"]:
        errors.append("Active source graph changed during compilation")
    try:
        final_preflight = verify_preflight(args.preflight.resolve(), after)
        if final_preflight["receipt"]["sha256"] != preflight["receipt"]["sha256"]:
            errors.append("Preflight receipt changed during compilation")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        final_preflight = None
        errors.append("Preflight no longer valid: " + str(exc))
    dependencies = fls_dependencies(build / "main.fls")
    fls_paths = {x["path"] for x in dependencies["local"]}
    unrecorded = sorted(set(before_hashes) - fls_paths)
    undeclared = sorted(
        x["path"] for x in dependencies["local"]
        if (x['path'] == 'main.tex' or x['path'].startswith(('sections/', 'figures/')))
        and x["path"] not in before_hashes)
    if unrecorded:
        errors.append("Authored sources not present in recorder inputs")
    if undeclared:
        errors.append("Recorder found manuscript inputs outside the preflight graph")
    if dependencies["missing"]:
        errors.append("Recorder local dependencies are missing")
    log_path = build / "main.log"
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    warnings = warning_report(log)
    pdf = build / "main.pdf"
    valid_pdf = False
    if pdf.is_file() and pdf.stat().st_size > 5:
        with pdf.open("rb") as stream:
            valid_pdf = stream.read(5) == b"%PDF-"
    if not valid_pdf:
        errors.append("No nonempty PDF with PDF header")
    if len(passes) != 3:
        errors.append("Three successful passes were not completed")
    if (warnings["missing_reference_warnings"] or warnings["missing_citation_warnings"]
            or warnings["undefined_references_summary"] or warnings["duplicate_labels_summary"]
            or warnings["duplicate_label_warnings"] or warnings["rerun_warning"]):
        errors.append("Cross-references/citations did not settle without conflicts")
    page_match = re.search(r"Output written on .*?\((\d+) pages?,", log, re.S)
    manifest = {
        "schema": "HMT_ARTICLE_IV_REV02_COMPILATION_MANIFEST_V1",
        "run_id": run_id, "active_sources_before": before,
        "active_sources_after": after, "changed_authored_sources": changed,
        "consumed_preflight": preflight, "preflight_after": final_preflight,
        "fls_dependencies": dependencies, "authored_sources_missing_from_fls": unrecorded,
        "undeclared_manuscript_inputs_in_fls": undeclared,
        "recorder": record(build / "main.fls") if (build / "main.fls").is_file() else None,
        "build_files": [record(p) for p in sorted(build.iterdir()) if p.is_file()],
        "mathematical_validity_certified": False,
    }
    manifest_path = receipts / "MANIFIESTO_COMPILACION.json"
    write_json(manifest_path, manifest)
    final_pdf, previous_pdf = None, None
    if not errors:
        destination = output / PDF_NAME
        if destination.exists():
            if destination.is_symlink() or not destination.is_file():
                raise ValueError("Existing output is not a regular PDF: " + str(destination))
            archive = output / "historial" / run_id
            archive.mkdir(parents=True, exist_ok=True)
            previous = archive / PDF_NAME
            shutil.copy2(destination, previous)
            if digest(previous) != digest(destination):
                raise ValueError("Preserved previous PDF differs from the existing output")
            previous_pdf = record(previous)
        staging = output / (PDF_NAME + "." + run_id + ".tmp")
        shutil.copy2(pdf, staging)
        if digest(staging) != digest(pdf):
            raise ValueError("Staged PDF differs from the compiled PDF")
        os.replace(staging, destination)
        final_pdf = record(destination)
        final_pdf["pages_from_log"] = int(page_match.group(1)) if page_match else None
    status = ("FAIL_COMPILACION_IV_REV02" if errors else
              "BORRADOR_COMPILADO_CON_AVISOS" if any(warnings.values()) or
              before["duplicate_labels_in_sources"] else "BORRADOR_COMPILADO")
    receipt = {
        "schema": "HMT_ARTICLE_IV_REV02_COMPILATION_RECEIPT_V1",
        "status": status, "run_id": run_id,
        "started_utc": started.isoformat(),
        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "driver": record(Path(__file__)),
        "source_cwd": ".", "build_directory": relative(build),
        "fontcache": relative(cache), "command": cmd, "passes": passes,
        "final_warnings": warnings, "errors": errors,
        "consumed_preflight": preflight,
        "manifest": record(manifest_path), "pdf": final_pdf,
        "previous_pdf_preserved": previous_pdf,
        "mathematical_validity_certified": False, "visual_review_performed": False,
        "semantic_gates": "Real preflight consumed and local bindings rechecked; scientific gates not rerun",
        "source_documents_modified": False,
        "external_files_copied_or_hashed": False,
    }
    receipt_path = receipts / "RECIBO_COMPILACION.json"
    write_json(receipt_path, receipt)
    print(json.dumps({"status": status, "receipt": relative(receipt_path),
                      "manifest": relative(manifest_path), "pdf": final_pdf,
                      "warnings": warnings, "errors": errors},
                     ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
