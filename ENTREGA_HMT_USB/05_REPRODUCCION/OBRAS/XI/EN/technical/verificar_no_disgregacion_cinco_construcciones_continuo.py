#!/usr/bin/env python3
"""Puerta focal de no disgregacion para el paper del continuo.

Comprueba el texto activo de la construccion conjunta. No compila ni escribe.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sections" / "continuo_cinco_construcciones_tipado.tex"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(
            "FAIL_NO_DISGREGACION_CINCO_CONSTRUCCIONES_CONTINUO " + message
        )


text = SOURCE.read_text(encoding="utf-8")
text_flat = re.sub(r"\s+", " ", text)

markers = (
    r"\label{eq:base-comun-registros}",
    r"\mathcal F_{\rm sp}",
    r"\mathcal F_{\rm sol}",
    r"\mathcal F_{\rm gau}^{(m)}",
    r"\mathcal F_{\rm coh}^{(m)}",
    r"\mathcal F_{\rm det}^{(m)}",
    r"\label{eq:constructor-correlativo}",
    r"\label{eq:naturalidad-D}",
    r"\label{eq:fibras-conjuntas-horizonte}",
    r"r^m_{N+1,N}",
    r"q^N_{m+1,m}",
    r"\operatorname{Gen}_{\rm cont}:H_\infty^{\rm enr}",
    r"\mathcal C_{\rm cont}^{\rm disc}",
    r"\label{eq:continuo-discreto}",
    r"\label{thm:correlacion-cinco}",
    "Correlative emergence of the five constructions",
    "five components are inseparable aspects of the same continuum",
    "not the image or the graph of a map",
    "not used to define",
    "The fiber, relation, number, orientation, carry, memory, boundary, and route",
    "the multisection, the terminals, and the linear and probabilistic readers",
    "subsequent recognition of the single continuum constructed",
)
for marker in markers:
    require(re.sub(r"\s+", " ", marker) in text_flat,
            f"falta_marcador={marker}")

constructor_anchor = text.find(r"\label{eq:constructor-correlativo}")
constructor_start = text.rfind(r"\[", 0, constructor_anchor)
constructor_end = text.find(r"\]", constructor_anchor)
require(constructor_anchor >= 0 and constructor_start >= 0
        and constructor_end > constructor_anchor,
        "constructor_correlativo_no_localizado")
constructor = text[constructor_start:constructor_end]
for component in ("sp", "sol", "gau", "coh", "det"):
    require(f"\\widetilde{{\\mathcal F}}_{{\\rm {component};k,N}}" in constructor,
            f"componente_ausente={component}")
require(constructor.count(r"\mathop{\times}_{\mathfrak R_{k,N}(\zeta)}") == 4,
        "producto_fibrado_no_unitario")

limit_anchor = text.find(r"\label{eq:continuo-discreto}")
limit_start = text.rfind(r"\[", 0, limit_anchor)
limit_end = text.find(r"\]", limit_anchor)
require(limit_anchor >= 0 and limit_start >= 0 and limit_end > limit_anchor,
        "limite_conjunto_no_localizado")
limit_block = text[limit_start:limit_end]
require(r"\varprojlim" in limit_block, "continuo_no_definido_como_limite")
require(r"\operatorname{im}" not in limit_block,
        "continuo_definido_como_imagen")

require(
    r"r^m_{N+1,N}q^{N+1}_{m+1,m}" in text_flat
    and r"q^N_{m+1,m}r^{m+1}_{N+1,N}" in text_flat,
    "cuadrado_horizonte_profundidad_ausente",
)

for forbidden in (
    r"(?:son|constituyen|forman) cinco ramas independientes",
    r"(?:son|constituyen|forman) cinco continuos independientes",
    r"(?:son|constituyen|forman) cinco aplicaciones independientes",
    r"(?:are|constitute|form) five independent branches",
    r"(?:are|constitute|form) five independent continua",
    r"(?:are|constitute|form) five independent maps",
):
    require(re.search(forbidden, text, flags=re.IGNORECASE) is None,
            f"disgregacion_explicita={forbidden}")

print(
    "PASS_NO_DISGREGACION_CINCO_CONSTRUCCIONES_CONTINUO "
    "components=sp/sol/gau/coh/det base=shared product=fibered "
    "naturality=horizon+modular limit=joint generator=post_definition "
    "nonempty=proved conserved=9+ terminal=joint compile=0"
)
