#!/usr/bin/env python3
"""Copia mecánica, sin edición, del cierre TeX común del artículo I.

Este programa conserva archivos; no compila ni certifica sus demostraciones.
La bibliografía se conserva íntegra, aunque el cierre utilice siete claves.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


DEFAULT_SOURCE = Path(
    "/Users/ruben/Documents/New project/output/"
    "CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/"
    "ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909"
)
ROOTS = tuple(
    f"sections/{name}.tex"
    for name in ("nucleo", "extension", "generacion", "registro_k", "alpha")
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_tex(text: str) -> str:
    return "\n".join(re.split(r"(?<!\\)%", line, 1)[0]
                     for line in text.splitlines())


def closure(source: Path) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    def visit(relative: str) -> None:
        if relative in graph:
            return
        path = (source / relative).resolve()
        if source not in path.parents or not path.is_file():
            raise SystemExit(f"Dependencia ausente o externa: {relative}")
        text = active_tex(path.read_text(encoding="utf-8"))
        includes = re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text)
        dependencies = [name if Path(name).suffix else name + ".tex"
                        for name in includes]
        graph[relative] = dependencies
        for name in dependencies:
            visit(name)

    for root in ROOTS:
        visit(root)
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--destination", type=Path,
                        default=Path(__file__).resolve().parents[1]
                        / "base_articulo_I")
    args = parser.parse_args()
    source, destination = args.source.resolve(), args.destination.resolve()
    if source == destination or source in destination.parents:
        raise SystemExit("La copia debe quedar fuera del artículo I original.")
    graph = closure(source)
    if len(graph) != 28:
        raise SystemExit(f"El cierre cambió: se esperaban 28 TeX; hay {len(graph)}.")
    files = sorted(set(graph) | {"sections/bibliografia.tex"})
    for relative in files:
        src, dst = source / relative, destination / relative
        if dst.exists() and src.read_bytes() != dst.read_bytes():
            raise SystemExit(f"Se preserva el destino divergente: {dst}")
    records = []
    for relative in files:
        src, dst = source / relative, destination / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(src, dst)
        src_sha, dst_sha = sha256(src), sha256(dst)
        if src_sha != dst_sha:
            raise SystemExit(f"La copia no es idéntica: {relative}")
        records.append({"source": str(src), "destination": str(dst),
                        "relative_path": relative, "bytes": src.stat().st_size,
                        "sha256_source": src_sha, "sha256_destination": dst_sha})
    manifest = {
        "scope": "BYTE_IDENTICAL_SOURCE_COPY_ONLY_NOT_COMPILATION_OR_MATHEMATICAL_CERTIFICATION",
        "source_root": str(source), "destination_root": str(destination),
        "entry_points": list(ROOTS), "tex_closure_count": len(graph),
        "copied_file_count": len(files), "graph": dict(sorted(graph.items())),
        "bibliography_copied_in_full": True,
        "required_citation_keys": ["hmtholonomia", "hmtintegral", "mustovicary",
                                   "delascuevas2023", "delascuevas2020",
                                   "hmtedicionsintesis", "hmtedicionintegral"],
        "unresolved_cross_references_without_exceptional_section": {
            "exc:doble-lectura": "sections/excepcional.tex:41",
            "inc-ampl-cuaterna": "sections/incidencia_bandera.tex:21"
        },
        "preamble_source_not_copied": str(source / "main.tex"),
        "preamble_source_sha256": sha256(source / "main.tex"),
        "files": records,
    }
    manifest_path = destination / "MANIFIESTO_COPIA_NUCLEO.json"
    encoded = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    if manifest_path.exists() and manifest_path.read_bytes() != encoded:
        raise SystemExit("El manifiesto anterior difiere; no se sobrescribe.")
    if not manifest_path.exists():
        manifest_path.write_bytes(encoded)
    print(json.dumps({"status": "PASS_COPIA_IDENTICA", "files": len(files),
                      "manifest": str(manifest_path),
                      "manifest_sha256": sha256(manifest_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
