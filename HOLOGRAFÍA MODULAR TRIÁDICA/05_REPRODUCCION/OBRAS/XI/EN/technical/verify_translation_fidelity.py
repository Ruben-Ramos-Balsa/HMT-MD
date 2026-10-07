#!/usr/bin/env python3
"""Structural fidelity gate for the English successor of the approved REV14.

The gate does not assess the mathematics.  It proves that translation has
preserved the active TeX graph, cross-reference graph, environment structure,
formula delimiters, and numerical sequence of every compiled source unit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys


INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
COMMAND_RE = re.compile(r"\\([A-Za-z@]+|.)")
NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+(?:[.,]\d+)?)")
LAYOUT_ONLY_RE = re.compile(
    r"\\looseness\s*=\s*-?\d+|"
    r"\\enlargethispage\{[^{}]*\\baselineskip\}"
)
ENV_RE = re.compile(r"\\(begin|end)\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REFERENCE_RE = re.compile(
    r"\\(?:ref|eqref|cref|Cref|pageref|autoref)\{([^}]+)\}"
)
CITE_RE = re.compile(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}")
FORMULA_DELIMITER_RE = re.compile(
    r"(?<!\\)\$\$|(?<!\\)\$|\\\(|\\\)|\\\[|\\\]"
)
STRUCTURAL_ENVS = {
    "equation",
    "equation*",
    "align",
    "align*",
    "gather",
    "gather*",
    "multline",
    "multline*",
    "theorem",
    "lemma",
    "proposition",
    "corollary",
    "definition",
    "axiom",
    "remark",
    "proof",
    "figure",
    "table",
    "longtable",
    "tikzpicture",
}
STRUCTURAL_COMMANDS = {
    "input",
    "include",
    "includegraphics",
    "label",
    "ref",
    "eqref",
    "cref",
    "Cref",
    "pageref",
    "autoref",
    "cite",
    "tag",
    "begin",
    "end",
    "section",
    "subsection",
    "subsubsection",
    "paragraph",
    "clearpage",
    "newpage",
    "footnote",
    "href",
}


def fail(message: str) -> None:
    raise SystemExit("FAIL_ACADEMIC_ENGLISH_TRANSLATION_FIDELITY " + message)


def active_tex_graph(root: Path) -> list[Path]:
    pending = [Path("main.tex")]
    ordered: list[Path] = []
    seen: set[Path] = set()
    while pending:
        rel = pending.pop(0)
        if rel in seen:
            continue
        path = root / rel
        if not path.is_file():
            fail(f"missing_active_source={rel.as_posix()}")
        seen.add(rel)
        ordered.append(rel)
        text = path.read_text(encoding="utf-8")
        for raw in INPUT_RE.findall(text):
            child = Path(raw if raw.endswith(".tex") else raw + ".tex")
            if child not in seen:
                pending.append(child)
    return ordered


def sequence(pattern: re.Pattern[str], text: str) -> list[object]:
    values: list[object] = []
    for match in pattern.finditer(text):
        values.append(match.groups() if len(match.groups()) > 1 else match.group(1))
    return values


def compare_file(source: Path, target: Path, rel: Path) -> None:
    src = source.read_text(encoding="utf-8")
    dst = target.read_text(encoding="utf-8")

    exact_sequences = {
        "inputs": sequence(INPUT_RE, src),
        "labels": sequence(LABEL_RE, src),
        "references": sequence(REFERENCE_RE, src),
        "citations": sequence(CITE_RE, src),
    }
    target_sequences = {
        "inputs": sequence(INPUT_RE, dst),
        "labels": sequence(LABEL_RE, dst),
        "references": sequence(REFERENCE_RE, dst),
        "citations": sequence(CITE_RE, dst),
    }
    for name, expected in exact_sequences.items():
        if target_sequences[name] != expected:
            fail(f"{name}_changed={rel.as_posix()}")

    src_env = [entry for entry in sequence(ENV_RE, src) if entry[1] in STRUCTURAL_ENVS]
    dst_env = [entry for entry in sequence(ENV_RE, dst) if entry[1] in STRUCTURAL_ENVS]
    if dst_env != src_env:
        fail(f"environment_sequence_changed={rel.as_posix()}")

    if FORMULA_DELIMITER_RE.findall(dst) != FORMULA_DELIMITER_RE.findall(src):
        fail(f"formula_delimiters_changed={rel.as_posix()}")

    # Pagination controls may contain integers (for example, a paragraph
    # looseness or an enlarged text block).  They are typography, not
    # mathematical data, and are removed symmetrically before the numerical
    # sequence comparison.
    src_numbers = NUMBER_RE.findall(LAYOUT_ONLY_RE.sub("", src))
    dst_numbers = NUMBER_RE.findall(LAYOUT_ONLY_RE.sub("", dst))
    if dst_numbers != src_numbers:
        fail(f"numerical_sequence_changed={rel.as_posix()}")

    src_commands = Counter(
        command for command in COMMAND_RE.findall(src)
        if command in STRUCTURAL_COMMANDS
    )
    dst_commands = Counter(
        command for command in COMMAND_RE.findall(dst)
        if command in STRUCTURAL_COMMANDS
    )
    if dst_commands != src_commands:
        missing = src_commands - dst_commands
        added = dst_commands - src_commands
        fail(
            f"command_multiset_changed={rel.as_posix()} "
            f"missing={dict(missing)} added={dict(added)}"
        )

    for side, text in (("source", src), ("target", dst)):
        if text.count("{") != text.count("}"):
            fail(f"brace_count={side}:{rel.as_posix()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    package_root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--source",
        type=Path,
        default=package_root / "evidence" / "spanish-argument-revision-20260915",
    )
    parser.add_argument("--target", type=Path, default=package_root)
    args = parser.parse_args()
    source = args.source.resolve()
    target = args.target.resolve()

    source_graph = active_tex_graph(source)
    target_graph = active_tex_graph(target)
    if target_graph != source_graph:
        fail("active_tex_graph_changed")
    for rel in source_graph:
        compare_file(source / rel, target / rel, rel)

    theorem_counts: Counter[str] = Counter()
    for rel in target_graph:
        text = (target / rel).read_text(encoding="utf-8")
        for direction, env in sequence(ENV_RE, text):
            if direction == "begin" and env in STRUCTURAL_ENVS:
                theorem_counts[env] += 1
    details = " ".join(f"{key}={theorem_counts[key]}" for key in sorted(theorem_counts))
    print(
        "PASS_ACADEMIC_ENGLISH_TRANSLATION_FIDELITY "
        f"active_tex_files={len(target_graph)} {details}"
    )


if __name__ == "__main__":
    main()
