#!/usr/bin/env python3
"""Conserva copias literales; no convierte preservación en prueba."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path("/Users/ruben/Documents/New project")
INTEGRAL = PROJECT / "output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente"
WORKING = PROJECT / "output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente"
COORD = PROJECT / "output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906"
CORE = PROJECT / "PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910"

OWNERS = [
    "colaboracion/parte_iii/source/public_final/dependencies/10_producto_nativo_body.tex",
    "colaboracion/parte_iii/source/public_final/base_83/c44_body.tex",
    "colaboracion/parte_iii/source/public_final/constantes/c34_euler_kronecker_primos.tex",
    "colaboracion/parte_iii/source/public_final/constantes/c35_bendersky_glaisher.tex",
    "manuscrito/sections/hmt/18_funcionales_espectrales_triadicos.tex",
    "manuscrito/sections/hmt/19a_constantes_torre_triadica_rev6.tex",
    "manuscrito/sucesor_102/deltas_ley9/10b_prueba_espectral_polar_riemann_weil_rectificacion_probatoria_20260903.tex",
    "manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex",
    "colaboracion/partes_iv_v/tex/residencias/94_cierre_espectral_parte_v.tex",
]
JOINT = "manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core"
OWNERS += [
    f"{JOINT}/04b1_estado_arbol_medida_comun.tex",
    f"{JOINT}/04b2_operaciones_intrinsecas_correlativas.tex",
    f"{JOINT}/04b3_terminal_naturalidad_limite.tex",
]
INSERTIONS = [
    "05a_lector_telescopia_correlativa.tex",
    "05a_retorno_memoria_correlativa.tex",
    "05b_balance_memoria_correlativa.tex",
    "05c_incidencia_curvatura_correlativa.tex",
    "05d_totalizacion_cohomologica_correlativa.tex",
    "05e_aw_nervio_correlativo.tex",
    "05e_smith_bockstein_correlativo.tex",
]
OWNERS += [f"manuscrito/incorporaciones/v2_global_20260823/{p}" for p in INSERTIONS]
COORD_OWNERS = [
    "TRAZA_GENERATIVA_COORDINADA.md",
    "OVERLEAF/PLIEGUE_HOJAS_RETORNO_Y_OCUPACION.md",
    "OVERLEAF/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md",
    "OVERLEAF/RECIBO_CAUSAL_RED_LECTORES.json",
    "OVERLEAF/CONTROL_EULER_KRONECKER.json",
    "OVERLEAF/resolver_discrepancia_ek.py",
    "ACLARAR/verificar_composiciones_momentos_y_accion.py",
]
PYTHON_OWNERS = [
    "pruebas/python/a9_native.py",
    "pruebas/python/generar_certificado_producto_nativo.py",
    "pruebas/python/auditar_producto_nativo.py",
    "pruebas/python/verificar_funcionales_espectrales.py",
    "certificados/producto_nativo_generador.json",
    "certificados/producto_nativo_auditoria.json",
    "certificados/funcionales_espectrales.json",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, destination, role, rows):
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and digest(destination) != digest(source):
        raise RuntimeError(f"No se sobreescribe una copia distinta: {destination}")
    shutil.copy2(source, destination)
    rows.append({
        "source": str(source), "copy": str(destination.relative_to(ROOT)),
        "sha256": digest(source), "copy_sha256": digest(destination),
        "role": role, "incorporated_in_manuscript": False,
        "proof_verified_by_copy": False,
    })


def main():
    rows = []
    for relative in OWNERS:
        source = INTEGRAL / relative
        role = "propietario_literal_integral_2249"
        if not source.is_file():
            source = WORKING / relative
            role = "propietario_ensamblado_no_incluido_en_copia_fls_integral"
        copy(source, ROOT / "antecedentes/integral" / relative, role, rows)
    for relative in COORD_OWNERS:
        copy(COORD / relative, ROOT / "antecedentes/ampliacion_coordinada" / relative,
             "desarrollo_posterior", rows)
    for relative in PYTHON_OWNERS:
        copy(WORKING / relative, ROOT / "antecedentes/ejecutables" / relative,
             "fuente_o_recibo_heredado_no_reescrito", rows)
    core_manifest = json.loads((CORE / "MANIFIESTO.json").read_text())
    for item in core_manifest["files"]:
        source = CORE / item["path"]
        if digest(source) != item["sha256"]:
            raise RuntimeError(f"Núcleo común distinto del manifiesto: {source}")
        copy(source, ROOT / "nucleo_comun" / item["path"],
             "nucleo_comun_identico_no_abreviado", rows)
    copy(CORE / "MANIFIESTO.json", ROOT / "nucleo_comun/MANIFIESTO.json",
         "manifiesto_nucleo_comun", rows)
    result = {
        "schema": "HMT.articulo_VIII.procedencia.v1",
        "status": "COPIAS_LITERALMENTE_VERIFICADAS",
        "integral_authorial_pages": 2249,
        "source_files": rows, "count": len(rows),
        "scope": "Preservación documental. No certifica autonomía ni teoremas.",
        "generated_by": "gestion/REUNIR_FUENTES.py",
    }
    (ROOT / "gestion/MANIFIESTO_FUENTES.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"COPIAS_VERIFICADAS={len(rows)} NUCLEO_COMUN=6/6")


if __name__ == "__main__":
    main()
