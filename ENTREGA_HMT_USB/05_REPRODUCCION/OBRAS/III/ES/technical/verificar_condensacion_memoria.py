#!/usr/bin/env python3
"""Control estático del delta de memoria; no compila ni certifica matemáticas."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def uncomment(text):
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def closure(start, root):
    seen = set()
    missing = []

    def visit(path):
        path = path.resolve()
        if path in seen:
            return
        seen.add(path)
        content = uncomment(path.read_text())
        for target in re.findall(r"\\input\{([^}]+)\}", content):
            if "#" in target or "\\" in target:
                missing.append({"source": str(path), "dynamic_input": target})
                continue
            name = target if Path(target).suffix else target + ".tex"
            options = [root / name, root / "base_articulo_II" / name,
                       root / "base_articulo_I" / name, path.parent / name]
            found = next((p for p in options if p.is_file()), None)
            if found is None:
                missing.append({"source": str(path), "input": target})
            else:
                visit(found)
    visit(start)
    return sorted(seen), missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    base = (args.base or root.parent / "ARTICULO_III_VACIO_ELECTROMAGNETICO_20260909").resolve()
    receipt = args.receipt or root / "technical/CONTROL_CONDENSACION_MEMORIA.json"
    checks = {}
    details = {}

    original_hashes = {}
    original_differences = []
    for directory in ("base_articulo_I", "base_articulo_II"):
        paths_a = {p.relative_to(base) for p in (base / directory).rglob("*") if p.is_file()}
        paths_b = {p.relative_to(root) for p in (root / directory).rglob("*") if p.is_file()}
        for rel in sorted(paths_a | paths_b):
            a, b = base / rel, root / rel
            if not a.is_file() or not b.is_file():
                original_differences.append({"path": str(rel), "base_exists": a.is_file(), "root_exists": b.is_file()})
                continue
            ha, hb = sha(a), sha(b)
            original_hashes[str(rel)] = hb
            if ha != hb:
                original_differences.append({"path": str(rel), "base_sha256": ha, "root_sha256": hb})
    checks["bases_immutable_byte_identical"] = not original_differences
    details["original_differences"] = original_differences

    original = (root / "base_articulo_II/sections/03_actualizacion.tex").read_text()
    derived = (root / "manuscrito/sections/02_actualizacion_ii.tex").read_text()
    old_input = r"\input{sections/03b_memoria_resolvente.tex}"
    new_input = r"\input{manuscrito/sections/02_memoria_ii.tex}"
    checks["actualizacion_only_input_changed"] = original.count(old_input) == 1 and derived == original.replace(old_input, new_input)

    wrapper_original = (root / "base_articulo_II/INCLUIR_DEPENDENCIAS_II.tex").read_text()
    wrapper_path = root / "manuscrito/INCLUIR_DEPENDENCIAS_II_REV02.tex"
    wrapper = wrapper_path.read_text()
    expected = wrapper_original.replace(
        r"\clearpage\input{base_articulo_II/sections/03_actualizacion.tex}",
        r"\clearpage\input{manuscrito/sections/02_actualizacion_ii.tex}")
    removed = []
    expected_lines = []
    for line in expected.splitlines(keepends=True):
        match = re.search(r"HMTIILabel@(mem:[^\\]+)\\endcsname", line)
        if match and match.group(1) not in {"mem:balance", "mem:identidad-finita"}:
            removed.append(match.group(1))
        else:
            expected_lines.append(line)
    checks["wrapper_only_input_and_reference_table_changed"] = wrapper == "".join(expected_lines)
    details["memory_reference_prefixes_removed"] = removed

    mem_i = (root / "base_articulo_I/sections/memoria_resolvente.tex").read_text()
    mem_ii = (root / "base_articulo_II/sections/03b_memoria_resolvente.tex").read_text()
    mem_new = (root / "manuscrito/sections/02_memoria_ii.tex").read_text()
    marker = r"\Needspace{20\baselineskip}"
    prefix, repeated = mem_ii.split(marker, 1)
    common = mem_i.split(marker, 1)[1]
    checks["finite_identity_full_prefix_byte_preserved"] = mem_new.startswith(prefix)
    checks["removed_suffix_exact_common_copy_after_reference_substitution"] = repeated.replace(r"\eqref{eq:eta}", r"\eqref{mem:actualizacion}") == common
    checks["finite_terminal_term_preserved"] = r"-u^{N+1}Ry_N" in mem_new
    checks["index_correspondence_explicit"] = r"E^{(I)}_{m+1}=I_m=E^{(II)}_m" in mem_new

    sources, missing = closure(wrapper_path, root)
    checks["all_derived_wrapper_inputs_resolve"] = not missing
    details["missing_inputs"] = missing
    labels = set()
    for path in sources:
        labels.update("hmtII:" + key for key in re.findall(r"\\label\{([^}]+)\}", uncomment(path.read_text())) if "#" not in key)
    # El AUX precedente acredita las anclas comunes ya incluidas, no una compilación nueva.
    aux = base / "build/main.aux"
    if not aux.is_file():
        raise SystemExit("No existe el AUX previo del PDF140: " + str(aux))
    common_labels = {k for k in re.findall(r"\\newlabel\{([^}]+)\}", aux.read_text()) if not k.startswith("hmtII:")}
    labels.update(common_labels)
    prefix_table = set(re.findall(r"HMTIILabel@([^\\]+)\\endcsname", wrapper))
    unresolved = []
    refs = []
    for path in sources:
        content = uncomment(path.read_text())
        for match in re.finditer(r"\\(ref|eqref|autoref|cref|Cref|HMTIIRefOriginal)\*?\{([^}]+)\}", content):
            command, values = match.groups()
            if "#" in values:
                continue
            for key in values.split(","):
                key = key.strip()
                resolved = key if command == "HMTIIRefOriginal" or key not in prefix_table else "hmtII:" + key
                item = {"source": str(path.relative_to(root)), "line": content.count("\n", 0, match.start()) + 1,
                        "command": command, "key": key, "resolved": resolved}
                refs.append(item)
                if resolved not in labels:
                    unresolved.append(item)
    checks["all_references_in_derived_II_closure_resolve_statically"] = not unresolved
    details["unresolved_references"] = unresolved
    details["reference_count"] = len(refs)
    details["reference_checks"] = refs
    details["source_closure"] = [{"path": str(p.relative_to(root)), "sha256": sha(p)} for p in sources]
    details["common_aux"] = {"path": str(aux), "sha256": sha(aux)}
    result = {"scope": "Delta editorial de memoria; control estático, sin nueva compilación, sin dictamen matemático global",
              "root": str(root), "base": str(base), "checks": checks, "all_checks_true": all(checks.values()),
              "preserved_file_count": len(original_hashes), "preserved_sha256": original_hashes, "details": details}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"all_checks_true": result["all_checks_true"], "checks": checks,
                      "preserved_files": len(original_hashes), "references": len(refs),
                      "receipt": str(receipt), "unresolved": unresolved}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["all_checks_true"] else 1)


if __name__ == "__main__":
    main()
