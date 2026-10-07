#!/usr/bin/env python3
"""Reúne fragmentos completos de antecedentes y registra las extracciones.

La copia íntegra de cada propietario queda conservada. Las selecciones son
cortes de exposición; no se presentan como certificación de autonomía global.
"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = ROOT.parent / "CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910_REV02"
ARCHIVE = ROOT / "antecedentes/lectura_articulo_I"
DEST = ROOT / "gestion/lectura_antecedentes"
PLAN = {
    "sections/extension.tex": [(1,97),(107,132),(172,179)],
    "sections/aritmetica_historias.tex": [(1,199)],
    "sections/revision_emrh.tex": [(1,114)],
    "sections/generacion.tex": [(1,176),(197,257)],
    "sections/revision_monodromia.tex": [(256,304)],
    "sections/registro_k.tex": [(1,567)],
    "sections/revision_k.tex": [(1,43)],
    "sections/k_reversibilidad.tex": [(1,65)],
    "figures/monodromia_regional_ampliacion.tex": None,
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    for relative, ranges in PLAN.items():
        original = ORIGIN / relative
        archived = ARCHIVE / relative
        if not archived.exists():
            archived.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, archived)
        if original.exists() and sha(original) != sha(archived):
            raise RuntimeError("Ha cambiado el propietario: " + relative)
        raw = archived.read_text()
        lines = raw.splitlines(keepends=True)
        if ranges is None:
            ranges = [(1, len(lines))]
        selected = "\n".join("".join(lines[a-1:b]) for a,b in ranges)
        substitutions = []
        for src,dst in [
            (r"\input{sections/revision_k.tex}", r"\input{gestion/lectura_antecedentes/revision_k.tex}"),
            (r"\input{sections/k_reversibilidad.tex}", r"\input{gestion/lectura_antecedentes/k_reversibilidad.tex}"),
            (r"\input{figures/monodromia_regional_ampliacion.tex}", r"\input{gestion/lectura_antecedentes/monodromia_regional_ampliacion.tex}"),
            (r"\ref{exc:doble-lectura}", r"8.1 del Artículo I (procedencia del corredor excepcional, conservada en el registro técnico)"),
            (r"\eqref{inc-ampl-cuaterna}", r"(8.12) del Artículo I (procedencia de la prolongación excepcional, conservada en el registro técnico)"),
            (r"\cite{hmtintegral,hmtholonomia}", r"\textup{(procedencia conservada en el registro técnico)}"),
            (r"\cite{hmtintegral}", r"\textup{(procedencia conservada en el registro técnico)}"),
        ]:
            count = selected.count(src)
            if count:
                selected = selected.replace(src,dst)
                substitutions.append({"before":src,"after":dst,"count":count})
        dst = DEST / Path(relative).name
        dst.write_text("% Fragmento conservado; véase MANIFIESTO_ANTECEDENTES_LECTURA.json.\n" + selected + "\n")
        records.append({"source":str(original),"archive":str(archived.relative_to(ROOT)),
                        "source_sha256":sha(archived),"source_lines":len(lines),
                        "ranges_inclusive":ranges,"output":str(dst.relative_to(ROOT)),
                        "output_sha256":sha(dst),"editorial_substitutions":substitutions})
    result = {"scope":"Antecedentes demostrativos conservados y reunidos; no dictamen científico global",
              "source_article":"Artículo I, revisión de helicidad REV02",
              "selection":"Emisión y calendario; historias compatibles y varianzas; completación cúbica; generación y cilindros; regiones; registro dodecafásico y reversibilidad. Las extensiones electrónicas y el corredor excepcional no se importan como pruebas esenciales del VIII.",
              "records":records}
    (ROOT / "gestion/MANIFIESTO_ANTECEDENTES_LECTURA.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"owners":len(records),"copied_sources_identical":True},ensure_ascii=False))

if __name__ == "__main__":
    main()
