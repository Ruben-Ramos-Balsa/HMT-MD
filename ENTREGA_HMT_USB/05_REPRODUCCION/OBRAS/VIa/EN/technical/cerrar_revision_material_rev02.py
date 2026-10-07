#!/usr/bin/env python3
"""Registra el corte revisado REV02. No certifica autonomía matemática."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((ROOT / "technical" / name).read_text(encoding="utf-8"))


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    names = [
        ("ARTICULO_VI_PARTICULAS_PERSISTENCIA_ESPECTRO_MASAS.pdf", 121,
         "c9f65a439a1011d92cc7cc92838b5eb3daa9625e5b9404a61f09e2964f1a8512"),
        ("ARTICULO_VI_CATALOGO_ESTRUCTURAL_Y_METROLOGICO.pdf", 608,
         "f8e08f34fd852b2bddd9e4d92191bdf56032165e5b7cd945c355d7ed4d5263e8"),
    ]
    rows = []
    for name, pages, expected in names:
        p = ROOT / "output/pdf" / name
        require(digest(p) == expected, "PDF distinto del corte revisado: " + name)
        rows.append({"path": "output/pdf/" + name, "pages": pages,
                     "sha256": expected, "bytes": p.stat().st_size})
    qa = read("qa_main_rev02_final/QA_TECNICO.json")
    require(qa["sha256"] == rows[0]["sha256"] and qa["pages"] == 121,
            "QA del manuscrito desactualizado")
    require(not any(p["outside_page"] for p in qa["geometry"]),
            "Texto fuera de página")
    require(not any("Overfull" in w["text"] or "Missing character" in w["text"]
                    or "undefined" in w["text"] for w in qa["log_findings"]),
            "Advertencia de composición no resuelta")
    diff = read("COMPARACION_VISUAL_FINAL_REV02.json")
    require([p["page"] for p in diff["changed"]] == [63, 64]
            and len(diff["identical"]) == 119, "Cambio visual adicional")
    nav = read("NAVEGACION_CATALOGO_REV02.json")
    require(nav["pdf_sha256"] == rows[1]["sha256"]
            and nav["all_visible_index_pages_match_destinations"]
            and nav["all_route_titles_with_first_data_row"],
            "Navegación de catálogo no verificada")
    controls = read("RECIBO_PAQUETE_PORTABLE_VI.json")
    require(controls["successful_count"] == 7
            and controls["core"]["all_six_match"], "Controles locales pendientes")
    correction = read("CONTROL_ANTIUNITARIEDAD_FOCK_VI_REV02.json")
    for name, sha in correction["source_hashes"].items():
        require(digest(ROOT / name) == sha, "Control de correcciones desactualizado")
    k = read("CONTROL_PERIODO_CONJUGACION_K_VI_REV02.json")
    require(digest(ROOT / k["source"]) == k["source_sha256"],
            "Control K desactualizado")
    report = {
        "schema": "HMT.VI.REV02.MATERIAL_READING_REVIEW.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "LECTURA_REVISADA_NO_CIERRE_CIENTIFICO",
        "material_review_completed": True,
        "scientific_autonomy_certified": False,
        "canonical_E108_produced": False,
        "canonical_gates_modified": False,
        "original_edition_preserved": True,
        "pdfs": rows,
        "main_visual_review": {
            "all_pages_rendered": 121,
            "focal_contact_pages_reviewed": 54,
            "individual_pages_reviewed": 12,
            "final_corrected_pages_reviewed_by_editor": [63, 64],
            "final_unchanged_page_images": 119,
            "conclusions_reviewed": [99, 100],
            "scope": "Revisión focal y comparación de píxeles; no nueva lectura científica de las 121 páginas.",
        },
        "catalogue_visual_review": {
            "focal_pages_reviewed": 17,
            "all_route_bookmarks_checked": 324,
            "all_cell_bookmarks_checked": 81,
            "all_continuation_identifiers_checked": 324,
            "literal_route_fields_preserved": 324 * 65,
            "external_records_preserved": 855,
            "scope": "Revisión visual focal y controles completos de navegación; no inspección visual individual de las 608 páginas.",
        },
        "focal_checks": {
            "portable_controls": 7,
            "antiunitarity_fock_units": correction["checks_count"],
            "k_period_and_conjugation": k,
        },
        "autonomy_scope": "La reconstrucción de K está incluida. La selección canónica del libro previo no ha quedado reunida ni ejecutada en esta revisión.",
    }
    destination = ROOT / "technical/REVISION_MATERIAL_ENTREGA_VI.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": report["status"], "pdfs": rows,
                      "scientific_autonomy_certified": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
