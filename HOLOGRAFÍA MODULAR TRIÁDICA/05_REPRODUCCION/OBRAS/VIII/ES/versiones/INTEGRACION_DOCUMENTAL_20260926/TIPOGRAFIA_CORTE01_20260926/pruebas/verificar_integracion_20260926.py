#!/usr/bin/env python3
"""Control documental sucesor de VIII (directorio técnico VII), 26/09/2026.

Contrasta una instantánea del 21/09 y deltas explícitos, sin reemplazar la
evidencia REV04/REV05. Analiza inclusiones literales y condicionales booleanos
TeX; no es un intérprete TeX ni una certificación matemática o física.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

MANIFEST = "gestion/MANIFIESTO_INTEGRACION_VIII_20260926.json"
PROOF = re.compile(r"\\begin\{proof\}[\s\S]*?\\end\{proof\}")
COMMAND = re.compile(r"\\[A-Za-z@]+|\\.")
STRUCTURAL = re.compile(
    r"\\(?:input|include|label|ref|eqref|cref|Cref|pageref|autoref|begin|end)\b")
EVENT = re.compile(
    r"\\(input|include|label|ref|eqref|cref|Cref|pageref|autoref|begin|end)"
    r"\s*\{([^}]+)\}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def uncomment(text):
    lines = []
    for line in text.splitlines(keepends=True):
        for i, char in enumerate(line):
            if char != "%":
                continue
            backslashes, j = 0, i - 1
            while j >= 0 and line[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                line = line[:i] + ("\n" if line.endswith("\n") else "")
                break
        lines.append(line)
    return "".join(lines)


def active_text(original, file, errors, exclusions, layout_conditions):
    """Conserve unknown layout conditions only when structurally inert."""
    source = uncomment(original)
    stack, result, last = [], [], 0

    def enabled():
        return all(item["branch"] is not False for item in stack)

    def emit(chunk):
        if enabled():
            result.append(chunk)

    for match in COMMAND.finditer(source):
        token = match.group()
        if token not in (r"\iffalse", r"\iftrue", r"\else", r"\fi") and not token.startswith(r"\if"):
            continue
        emit(source[last:match.start()])
        if token in (r"\else", r"\fi"):
            if not stack:
                errors.append({"conditional_unmatched": token, "file": file})
            elif token == r"\else":
                top = stack[-1]
                if top["else"]:
                    errors.append({"conditional_second_else": file})
                top["else"] = True
                if top["branch"] is not None:
                    top["branch"] = not top["branch"]
            else:
                top = stack.pop()
                body = source[top["start"]:match.start()]
                if top["kind"] == r"\iffalse":
                    exclusions.append({"file": file, "start_line": top["line"],
                                       "end_line": source.count("\n", 0, match.start()) + 1})
                elif top["branch"] is None:
                    if STRUCTURAL.search(body):
                        errors.append({"unevaluated_structural_condition": top["kind"],
                                       "file": file, "line": top["line"]})
                    else:
                        layout_conditions.append({"file": file, "condition": top["kind"],
                                                  "line": top["line"]})
        else:
            stack.append({"kind": token, "branch": False if token == r"\iffalse" else
                          True if token == r"\iftrue" else None,
                          "start": match.end(), "line": source.count("\n", 0, match.start()) + 1,
                          "else": False})
        last = match.end()
    emit(source[last:])
    if stack:
        errors.append({"unclosed_conditionals": [x["kind"] for x in stack], "file": file})
    return "".join(result)


def scan(manuscript):
    errors, exclusions, conditions, edges = [], [], [], []
    labels, references, inventory, active = {}, [], {}, []
    environment_stack, proof_hashes = [], {}

    def visit(relative):
        if relative in active:
            errors.append({"include_cycle": active + [relative]})
            return
        path = manuscript / relative
        try:
            path.resolve().relative_to(manuscript.resolve())
        except ValueError:
            errors.append({"input_outside_manuscript": relative})
            return
        if not path.is_file():
            errors.append({"missing_input": relative})
            return
        active.append(relative)
        source = active_text(path.read_text(encoding="utf-8"), relative,
                             errors, exclusions, conditions)
        inventory[relative] = digest(path)
        proof_hashes[relative] = [text_hash(x) for x in PROOF.findall(source)]
        for match in EVENT.finditer(source):
            command, value = match.groups()
            if command in ("input", "include"):
                if any(x in value for x in ("\\", "#", "{")):
                    errors.append({"dynamic_input_not_supported": value, "file": relative})
                    continue
                child = value if value.endswith(".tex") else value + ".tex"
                edges.append({"from": relative, "to": child})
                visit(child)
            elif command == "label":
                labels.setdefault(value, []).append(relative)
            elif command in ("begin", "end"):
                if command == "begin":
                    environment_stack.append((value, relative))
                elif not environment_stack or environment_stack[-1][0] != value:
                    errors.append({"environment_mismatch": value, "file": relative})
                else:
                    environment_stack.pop()
            else:
                references.extend((relative, x.strip()) for x in value.split(","))
        active.pop()

    visit("main.tex")
    if environment_stack:
        errors.append({"unclosed_environments": environment_stack})
    return {"files": inventory, "edges": edges, "proofs": proof_hashes,
            "label_count": len(labels),
            "duplicate_labels": {k: v for k, v in labels.items() if len(v) > 1},
            "unresolved_references": [{"file": f, "label": k}
                                      for f, k in references if k not in labels],
            "errors": errors, "excluded_false_blocks": exclusions,
            "unevaluated_layout_conditions": conditions}


def proof_blocks(path):
    errors = []
    text = active_text(path.read_text(encoding="utf-8"), path.name, errors, [], [])
    if errors:
        raise ValueError(str(errors))
    return PROOF.findall(text)


def check_proof_lineage(old, new, file):
    """Match every antecedent in order, with one declared notation substitution."""
    result, cursor = [], 0
    for index, block in enumerate(old):
        mapped = block
        if file == "81_propagacion_bidireccional.tex":
            for subscript in ("ret", "adv", "sym", "rad"):
                mapped = mapped.replace("G_{\\rm " + subscript + "}",
                                        "\\mathsf{G}_{\\rm " + subscript + "}")
        found = None
        for j in range(cursor, len(new)):
            if new[j] in (block, mapped):
                found = j
                break
        if found is None:
            result.append({"old_index": index, "old_sha256": text_hash(block),
                           "status": "MISSING_OR_CHANGED"})
        else:
            result.append({"old_index": index, "new_index": found,
                           "old_sha256": text_hash(block), "new_sha256": text_hash(new[found]),
                           "status": "IDENTICAL" if new[found] == block else "EXPLICIT_GREEN_NOTATION_CHANGE"})
            cursor = found + 1
    return result


def verify(base):
    manifest = json.loads((base / MANIFEST).read_text(encoding="utf-8"))
    errors, lineage = [], []
    for section in ("baseline_files", "current_files", "evidence_files", "control_files"):
        for item in manifest[section]:
            path = base / item["path"]
            actual = digest(path) if path.is_file() else None
            if actual != item["sha256"]:
                errors.append({"hash_mismatch": item["path"], "group": section,
                               "expected": item["sha256"], "actual": actual})
    expected = {x["path"] for x in manifest["current_files"]}
    actual = {str(x.relative_to(base)) for x in (base / "manuscrito").rglob("*.tex")
              if "reproduccion_gravitatoria_20260926" not in x.parts}
    if actual != expected:
        errors.append({"tex_inventory_delta": {"added": sorted(actual - expected),
                                               "missing": sorted(expected - actual)}})
    baseline = base / manifest["baseline_root"]
    current = base / "manuscrito"
    for item in manifest["baseline_files"]:
        relative = item["manuscript_path"]
        old_path, new_path = baseline / relative, current / relative
        if not (old_path.is_file() and new_path.is_file()):
            continue
        blocks = check_proof_lineage(proof_blocks(old_path), proof_blocks(new_path), relative)
        for block in blocks:
            if block["status"] == "MISSING_OR_CHANGED":
                errors.append({"antecedent_proof_changed": relative, "proof": block})
        lineage.append({"file": relative, "proofs": blocks})
    if lineage != manifest["proof_lineage_20260921_to_20260926"]:
        errors.append({"lineage_does_not_match_reviewed_delta": True})
    current_scan = scan(current)
    baseline_scan = scan(baseline)
    errors.extend(current_scan["errors"])
    if baseline_scan["errors"]:
        errors.append({"baseline_scan_errors": baseline_scan["errors"]})
    if current_scan["edges"] != manifest["active_include_edges"]:
        errors.append({"active_include_graph_changed": True})
    removed_active = sorted(set(baseline_scan["files"]) - set(current_scan["files"]))
    if removed_active:
        errors.append({"previous_active_sources_removed": removed_active})
    duplicates, unresolved = current_scan["duplicate_labels"], current_scan["unresolved_references"]
    statuses = Counter(p["status"] for f in lineage for p in f["proofs"])
    success = not (errors or duplicates or unresolved)
    return {"schema": "hmt.viii.documentary_integration.20260926.v1",
            "status": "PASS_INTEGRACION_DOCUMENTAL_VIII_20260926" if success else
                      "FAIL_INTEGRACION_DOCUMENTAL_VIII_20260926",
            "language": manifest["language"], "baseline_date": "2026-09-21",
            "scope": manifest["scope"], "file_count": len(current_scan["files"]),
            "label_count": current_scan["label_count"],
            "proof_environment_count": sum(len(p) for p in current_scan["proofs"].values()),
            "antecedent_proofs": dict(statuses), "proof_lineage": lineage,
            "reviewed_deltas": manifest["reviewed_deltas"],
            "historical_discrepancies": manifest["historical_discrepancies"],
            "errors": errors, "duplicate_labels": duplicates, "unresolved_references": unresolved,
            "active_include_edges": current_scan["edges"],
            "excluded_false_blocks": current_scan["excluded_false_blocks"],
            "unevaluated_layout_conditions": current_scan["unevaluated_layout_conditions"],
            "pdf_compiled": False, "physical_amplitude_certified": False,
            "global_mathematical_certification": False,
            "script_sha256": digest(Path(__file__)), "manifest_sha256": digest(base / MANIFEST)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = verify(Path(__file__).resolve().parents[1])
    if args.receipt:
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    keys = ("status", "file_count", "label_count", "proof_environment_count", "antecedent_proofs",
            "errors", "duplicate_labels", "unresolved_references", "excluded_false_blocks",
            "physical_amplitude_certified")
    print(json.dumps({k: result[k] for k in keys}, ensure_ascii=False))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
