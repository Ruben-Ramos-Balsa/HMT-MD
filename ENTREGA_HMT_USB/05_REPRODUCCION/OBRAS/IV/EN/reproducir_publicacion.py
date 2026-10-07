#!/usr/bin/env python3
"""Reproduce IV or V locally; stdlib only, no scientific certification.

Install this file at the source-package root, beside main.tex (IV) or
manuscrito/ (V). No historical receipt or private path is required.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

PROFILES = {
    "IV": ("main.tex", "DISCRETE_CONTINUUM_MOONSHINE_T_DUALITY_AND_M_THEORY_EN.pdf"),
    "V": ("manuscrito/main.tex", "QUANTUM_STATISTICS_AND_RADIATION_EN.pdf"),
}
DEFAULT_EPOCH = 946684800  # 2000-01-01 00:00:00 UTC; fixed for every pass.
LUAOTFLOAD_CONFIG = "[db]\nlocation-precedence = texmf\nscan-local = false\n"
SYSTEM_TEX_TREES = ("TEXMFDIST", "TEXMFLOCAL", "TEXMFSYSVAR", "TEXMFSYSCONFIG")
FONTS = (
    "STIXTwoText-Regular.otf", "STIXTwoText-Bold.otf",
    "STIXTwoText-Italic.otf", "STIXTwoText-BoldItalic.otf",
    "STIXTwoMath-Regular.otf",
)
AUX_SUFFIXES = {".aux", ".toc", ".out", ".log", ".fls", ".synctex", ".xdv"}
IMPORT = re.compile(
    r"\\(?P<kind>input|include|includegraphics)\*?\s*"
    r"(?:\[[^\]]*\]\s*)?\{(?P<name>[^{}]+)\}"
)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inside(path, directory):
    return Path(path).resolve().is_relative_to(Path(directory).resolve())


def strip_comments(text):
    result = []
    for line in text.splitlines():
        for i, char in enumerate(line):
            if char == "%":
                backslashes = len(line[:i]) - len(line[:i].rstrip("\\"))
                if backslashes % 2 == 0:
                    line = line[:i]
                    break
        result.append(line)
    return "\n".join(result)


def source_graph(root, entry):
    """Literal input/include/graphics used by these two active manuscripts.

    The recorder check complements this scan with every actual TeX input.
    This is not a general-purpose parser of arbitrary TeX or Lua programs.
    """
    root, entry = root.resolve(), entry.resolve()
    files, errors, visiting = {}, [], set()

    def walk(path):
        path = path.resolve()
        if path in visiting:
            errors.append("Cyclic input: " + str(path))
            return
        key = path.relative_to(root).as_posix()
        if key in files:
            return
        files[key] = digest(path)
        if path.suffix != ".tex":
            return
        visiting.add(path)
        for match in IMPORT.finditer(strip_comments(path.read_text(encoding="utf-8"))):
            kind, name = match.group("kind", "name")
            if Path(name).is_absolute() or any(c in name for c in "\\#$|"):
                errors.append("Nonportable/dynamic input: " + key + " -> " + name)
                continue
            suffixes = ("", ".tex") if kind != "includegraphics" else (
                "", ".pdf", ".png", ".jpg", ".jpeg", ".eps")
            # TeX resolves these manuscript-relative paths from the main directory.
            candidates = [entry.parent / (name + ext) for ext in suffixes]
            target = next((p for p in candidates if p.is_file()), None)
            if target is None or not inside(target, root):
                errors.append("Missing/nonlocal input: " + key + " -> " + name)
            else:
                walk(target)
        visiting.remove(path)

    walk(entry)
    return {"files": dict(sorted(files.items())), "errors": errors}


def validate_log(text):
    """Fatal publication diagnostics; underfull boxes are recorded, not hidden."""
    folded = re.sub(r"\s+", " ", text)
    patterns = {
        "tex_errors": r"(^!|^.*:\d+: (?:LaTeX|Package .*|Undefined control).*|"
                      r"Emergency stop|Fatal error occurred)",
        "undefined_reference_or_citation": r"(?:Reference|Citation).*?undefined|"
                                            r"There were undefined references",
        "duplicate_labels": r"multiply[- ]defined|multiply defined",
        "rerun_required": r"Rerun to get cross-references right|"
                          r"Rerun to get /PageLabels entry|"
                          r"Please \(re\)run (?:Biber|BibTeX)|"
                          r"Package rerunfilecheck Warning: File .*? has changed",
        "overfull_hbox": r"Overfull \\hbox",
        "overfull_vbox": r"Overfull \\vbox",
        "missing_glyphs": r"Missing character:",
    }
    counts = {}
    for name, pattern in patterns.items():
        haystack = text if name == "tex_errors" else folded
        counts[name] = len(re.findall(pattern, haystack, re.M))
    return {
        "blocking": counts,
        "underfull_hbox": text.count("Underfull \\hbox"),
        "underfull_vbox": text.count("Underfull \\vbox"),
        "warnings": [line for line in text.splitlines() if "Warning:" in line],
        "errors": [name + ": " + str(n) for name, n in counts.items() if n],
    }


def validate_fls(text, root, cwd, work, runtime_roots, expected=()):
    """Reject private dependencies, stale auxiliaries and outputs in sources.

    External runtime is allowed only inside the queried installation trees,
    never merely because a path is outside the source package.
    """
    root, cwd, work = root.resolve(), cwd.resolve(), work.resolve()
    local, runtime, generated, outputs, errors = set(), set(), set(), set(), []
    entries = 0
    for line in text.splitlines():
        if line.startswith("PWD "):
            cwd = Path(line[4:]).resolve()
        elif line.startswith(("INPUT ", "OUTPUT ")):
            kind, raw = line.split(" ", 1)
            p = Path(raw)
            p = (p if p.is_absolute() else cwd / p).resolve()
            entries += 1
            if kind == "OUTPUT":
                outputs.add(str(p))
                if not inside(p, work):
                    errors.append("TeX output outside work directory: " + str(p))
            elif inside(p, work):
                generated.add(str(p))
            elif not p.is_file():
                errors.append("Missing recorder input: " + str(p))
            elif inside(p, root):
                if p.suffix in AUX_SUFFIXES:
                    errors.append("Stale auxiliary outside work directory: " + str(p))
                local.add(p.relative_to(root).as_posix())
            elif any(inside(p, r) for r in runtime_roots):
                runtime.add(str(p))
            else:
                errors.append("External input outside declared TeX runtime: " + str(p))
    if not entries:
        errors.append("Empty/missing recorder data")
    for key in sorted(set(expected) - local):
        errors.append("Expected source not recorded: " + key)
    return {
        "local_inputs": sorted(local), "runtime_inputs": sorted(runtime),
        "generated_inputs": sorted(generated), "outputs": sorted(outputs),
        "errors": errors,
    }


def run_text(command, env, cwd):
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=30, check=False)
    if result.returncode:
        raise ValueError("Command failed: " + " ".join(command) + "\n" + result.stderr)
    return result.stdout.strip()


def clean_environment(work, epoch):
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(("TEX", "BIB", "BST", "LUAINPUTS", "LUAFONTS",
                           "OPENTYPEFONTS", "TTFONTS", "T1FONTS", "AFMFONTS",
                           "OSFONTDIR")):
            del env[key]
    for key, folder in (("TEXMFVAR", "var"), ("TEXMFCACHE", "cache"),
                        ("TEXMFCONFIG", "config"), ("TEXMFHOME", "empty-texmfhome")):
        p = work / folder
        p.mkdir()
        env[key] = str(p)
    # Luaotfload's fresh database otherwise scans personal/system font folders.
    # Its documented location-precedence also controls which locations are
    # scanned, not merely the lookup order (luaotfload 3.28 database.lua).
    # XDG configuration is found before ~/.luaotfloadrc. The caller rejects
    # working-directory configurations, which have still higher precedence.
    config_dir = work / "config" / "luaotfload"
    config_dir.mkdir()
    (config_dir / "luaotfload.conf").write_text(LUAOTFLOAD_CONFIG, encoding="utf-8")
    env["XDG_CONFIG_HOME"] = str(work / "config")
    # TEXMF scanning itself expands font search paths containing OSFONTDIR.
    # Use an existing empty directory, not an unset variable/default fallback.
    env["OSFONTDIR"] = str(work / "empty-texmfhome")
    env.update(SOURCE_DATE_EPOCH=str(epoch), FORCE_SOURCE_DATE="1",
               TZ="UTC", max_print_line="1000", openout_any="p")
    return env


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raiz", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--articulo", choices=PROFILES)
    parser.add_argument("--salida", type=Path, default=Path("reproduccion_publicacion"),
                        help="New directory inside source root; existing files are never replaced")
    parser.add_argument("--lualatex", default="lualatex")
    parser.add_argument("--kpsewhich", default="kpsewhich")
    parser.add_argument("--source-date-epoch", type=int, default=DEFAULT_EPOCH)
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per TeX pass")
    parser.add_argument("--solo-compilar", action="store_true",
                        help="Three passes and candidate PDF only; no FLS/log publication validation")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.source_date_epoch < 0:
        parser.error("timeout must be positive and SOURCE_DATE_EPOCH nonnegative")
    root = args.raiz.resolve()
    candidates = [k for k, (p, _) in PROFILES.items() if (root / p).is_file()]
    profile = args.articulo or (candidates[0] if len(candidates) == 1 else None)
    if profile is None:
        parser.error("Specify --articulo IV or V for this source root")
    relative_entry, pdf_name = PROFILES[profile]
    entry = (root / relative_entry).resolve()
    if not entry.is_file() or not inside(entry, root):
        parser.error("Missing/nonlocal entry point: " + relative_entry)
    for filename in ("luaotfload.conf", "luaotfloadrc"):
        if (entry.parent / filename).exists():
            parser.error("Working-directory " + filename +
                         " would override the isolated TeX-only font configuration")
    output = (root / args.salida).resolve()
    if not inside(output, root) or output == root:
        parser.error("--salida must be a proper subdirectory of --raiz")
    protected = [root / p for p in ("manuscrito", "sections", "figures", "antecedentes")]
    if any(inside(output, p) for p in protected if p.is_dir()):
        parser.error("--salida cannot be inside authored source directories")
    if output.exists():
        parser.error("--salida already exists; choose a fresh directory (no overwrites)")
    engine, kpse = shutil.which(args.lualatex), shutil.which(args.kpsewhich)
    if not engine or not kpse:
        parser.error("LuaLaTeX and kpsewhich must be available")
    graph = source_graph(root, entry)
    if graph["errors"]:
        print(json.dumps({"status": "FAIL_SOURCE_GRAPH", **graph}, ensure_ascii=False, indent=2))
        return 1
    output.mkdir(parents=True)
    work = output / "tex"
    work.mkdir()
    receipt = {
        "schema": "HMT_PUBLICATION_REPRODUCTION_V1", "article": profile,
        "entry": relative_entry, "source_date_epoch": args.source_date_epoch,
        "mode": "compile_only" if args.solo_compilar else "compile_and_validate",
        "scientific_checks_run": False, "mathematical_validity_certified": False,
        "visual_review_performed": False, "sources_before": graph["files"],
        "passes": [], "errors": [], "pdf": None,
    }
    errors = receipt["errors"]
    try:
        env = clean_environment(work, args.source_date_epoch)
        font_config = work / "config" / "luaotfload" / "luaotfload.conf"
        receipt["font_scan_policy"] = {
            "locations": ["texmf"], "scan_local": False,
            "osfontdir": (work / "empty-texmfhome").relative_to(root).as_posix(),
            "configuration": font_config.relative_to(root).as_posix(),
            "configuration_sha256": digest(font_config),
        }
        receipt["engine_version"] = run_text([engine, "--version"], env, root)
        runtime = []
        for name in SYSTEM_TEX_TREES:
            raw = run_text([kpse, "-var-value=" + name], env, root)
            if raw:
                p = Path(raw).resolve()
                if not p.is_dir() or p == Path(p.anchor) or p == Path.home():
                    raise ValueError("Unusable TeX runtime tree " + name + ": " + raw)
                runtime.append(p)
        if not runtime:
            raise ValueError("No TeX installation trees discovered with kpsewhich")
        receipt["tex_runtime_roots"] = [str(p) for p in runtime]
        receipt["fonts"] = {}
        for font in FONTS:
            raw = run_text([kpse, font], env, root)
            if not raw or not Path(raw).is_file():
                raise ValueError("Required TeX font not found: " + font)
            p = Path(raw).resolve()
            if not any(inside(p, r) for r in runtime) and not inside(p, root):
                raise ValueError("Required font resolves outside package/runtime: " + str(p))
            receipt["fonts"][font] = {"path": str(p), "sha256": digest(p)}
        # LuaTeX's default trailer ID also depends on the temporary output path.
        # Bind this non-content identifier to authored sources and the fixed epoch.
        trailer_material = json.dumps(
            {"sources": graph["files"], "epoch": args.source_date_epoch},
            sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
        trailer_id = hashlib.sha256(trailer_material).hexdigest()[:32].upper()
        receipt["pdf_trailer_id"] = {
            "value": trailer_id,
            "policy": "First 128 bits of SHA-256 of sorted source hashes and epoch",
        }
        tex_entry = (r"\pdfvariable trailerid {[<" + trailer_id + "><" +
                     trailer_id + r">]}\input{main.tex}")
        command = [
            engine, "-no-shell-escape", "-interaction=nonstopmode",
            "-halt-on-error", "-file-line-error", "-recorder",
            "-jobname=main", "-output-directory=" + str(work), tex_entry,
        ]
        receipt["command"] = command
        for number in range(1, 4):
            if source_graph(root, entry) != graph:
                raise ValueError("Authored source graph changed before pass " + str(number))
            try:
                result = subprocess.run(command, cwd=entry.parent, env=env,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        timeout=args.timeout, check=False)
                captured, code = result.stdout, result.returncode
            except subprocess.TimeoutExpired as exc:
                captured, code = exc.stdout or b"", None
                errors.append("Pass " + str(number) + " exceeded timeout")
            (work / ("pass-" + str(number) + ".stdout.txt")).write_bytes(captured)
            for suffix in ("log", "fls"):
                p = work / ("main." + suffix)
                if p.is_file():
                    shutil.copyfile(p, work / ("pass-" + str(number) + "." + suffix))
            receipt["passes"].append({"pass": number, "returncode": code})
            if code != 0:
                errors.append("TeX pass " + str(number) + " failed; inspect saved stdout/log")
                break
        if len(receipt["passes"]) != 3:
            errors.append("Three completed TeX passes are required")
        after = source_graph(root, entry)
        receipt["sources_after"] = after["files"]
        if after != graph:
            errors.append("Authored source graph changed during compilation")
        pdf = work / "main.pdf"
        if not pdf.is_file() or pdf.stat().st_size < 6:
            errors.append("Missing/empty PDF")
        elif pdf.open("rb").read(5) != b"%PDF-":
            errors.append("Invalid PDF header")
        if not args.solo_compilar:
            receipt["fls_checks"] = []
            for number in range(1, len(receipt["passes"]) + 1):
                fls = work / ("pass-" + str(number) + ".fls")
                report = validate_fls(
                    fls.read_text(encoding="utf-8", errors="replace") if fls.is_file() else "",
                    root, entry.parent, work, runtime, graph["files"])
                receipt["fls_checks"].append(report)
                errors.extend("Pass " + str(number) + ": " + s for s in report["errors"])
            log = work / "main.log"
            diagnostics = validate_log(
                log.read_text(encoding="utf-8", errors="replace") if log.is_file() else "")
            receipt["final_log"] = diagnostics
            errors.extend(diagnostics["errors"])
            if not log.is_file():
                errors.append("Missing final TeX log")
        if not errors:
            destination = output / pdf_name
            shutil.copyfile(pdf, destination)
            receipt["pdf"] = {"path": destination.relative_to(root).as_posix(),
                              "sha256": digest(destination), "bytes": destination.stat().st_size}
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        errors.append(str(exc))
    receipt["status"] = ("FAIL" if errors else "COMPILED_NOT_VALIDATED"
                         if args.solo_compilar else "PASS_TECHNICAL_REPRODUCTION")
    (output / "RECIBO_REPRODUCCION.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"],
                      "receipt": (output / "RECIBO_REPRODUCCION.json").relative_to(root).as_posix(),
                      "pdf": receipt["pdf"], "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
