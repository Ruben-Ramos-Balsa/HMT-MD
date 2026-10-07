#!/usr/bin/env python3
"""Control aritmético posterior de las comparaciones del artículo II.

Sólo biblioteca estándar. No reconstruye el generador APP--TRIT--TPK:
recibe sus coordenadas publicadas, separadas de las referencias externas.
La evaluación de pi por una identidad analítica es un lector de control,
no la definición ni el selector de la coordenada pi_HMT del manuscrito.
Uso: python3 -I -S verificar_comparaciones_II.py [--receipt RUTA.json]
"""
from __future__ import annotations

if not __debug__:
    raise RuntimeError('Este control requiere aserciones activas; ejecutar sin -O.')

import argparse
from decimal import Decimal as D, localcontext
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
TEX = ROOT / "manuscrito/sections/18_comparacion_cuantitativa_II.tex"
INTERNAL = {
    "hbar_pre_coefficient": "1.0545718176461544696",
    "hbar_ret_coefficient": "1.0545718169150390611",
    "gamma": "0.27400767269445927474725526077398041940",
    "delta_S90": "2.95169439297457621139847987861e-4",
    "delta_S120": "1.96835112502951720093738706217e-5",
    "gamma_angular": "0.270485322934140078465586458790",
    "theta12_deg": "13.003313589509",
    "theta23_deg": "2.398056157332",
    "theta13_deg": "0.213977382244",
    "delta_deg": "65.676173123554",
    "J_published": "3.1189723326632974e-5",
}
# Referencias terminales; ningún constructor interno recibe este diccionario.
EXTERNAL = {
    "h_SI": "6.62607015e-34", "kB_SI": "1.380649e-23",
    "G_CODATA2022": "6.67430e-11", "G_standard_uncertainty": "0.00015e-11",
    "PDG2025": {
        "s12": ("0.22501", "0.00068", "0.00068"),
        "s23": ("0.04183", "0.00069", "0.00079"),
        "s13": ("0.003732", "0.000085", "0.000090"),
        "delta_rad": ("1.147", "0.026", "0.026"),
        "J": ("3.12e-5", "0.12e-5", "0.13e-5"),
    },
}
SOURCES = {
    "action": "manuscrito/sections/05_accion.tex",
    "barbero": "fuentes/propietarios_II/B02/c43_funcional_barbero.tex",
    "ckm": "fuentes/propietarios_II/C02/74_mezcla_contenido_exclusivo_post_rev2.tex",
    "thermal": "fuentes/propietarios_integral/11_informacion_entropia_landauer.tex",
    "gravity": "fuentes/propietarios_II/G02/c42_gravedad_escalar.tex",
}
REFERENCES = {
    "BIPM": "https://www.bipm.org/en/measurement-units/si-defining-constants",
    "CODATA2022": "https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
    "PDG2025": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf",
    "GhoshMitra": "https://arxiv.org/pdf/gr-qc/0411035",
}


def atan_small(x: D) -> D:
    term = x
    total = x
    n = 1
    while True:
        term *= -x*x
        new = total + term / (2*n+1)
        if new == total:
            return new
        total = new
        n += 1


def sincos(x: D) -> tuple[D, D]:
    s = ts = x
    c = tc = D(1)
    n = 1
    while True:
        ts *= -x*x / ((2*n)*(2*n+1))
        tc *= -x*x / ((2*n-1)*(2*n))
        ns, nc = s+ts, c+tc
        if ns == s and nc == c:
            return ns, nc
        s, c = ns, nc
        n += 1


def gm_root(pi: D) -> tuple[D, D]:
    """Raíz EXTERNA de Ghosh--Mitra, ecuación (7), lambda=2*pi*gamma."""
    lo, hi = D("0.27"), D("0.28")
    cutoff = 128
    spectrum = [(D(n+1), (D(n)*D(n+2)).sqrt()) for n in range(1, cutoff+1)]
    def f(gamma: D) -> D:
        return sum((multiplicity*(-pi*gamma*root).exp()
                    for multiplicity, root in spectrum), D(0))-1
    assert f(lo) > 0 and f(hi) < 0
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    r = (-pi*D("0.27")).exp()
    tail_bound = r**(cutoff+1)*((cutoff+2)-(cutoff+1)*r)/(1-r)**2
    assert tail_bound < D("1e-43")
    # The n=1 term alone bounds |f'| > 2 throughout this bracket.
    derivative_floor = 2*pi*D(3).sqrt()*(-pi*D("0.28")*D(3).sqrt()).exp()
    assert derivative_floor > 2
    return (lo+hi)/2, (hi-lo)/2 + tail_bound/derivative_floor


def evaluate() -> dict:
    with localcontext() as ctx:
        ctx.prec = 75
        pi = 16*atan_small(D(1)/5)-4*atan_small(D(1)/239)
        pre, ret = D(INTERNAL["hbar_pre_coefficient"]), D(INTERNAL["hbar_ret_coefficient"])
        h_reference = D(EXTERNAL["h_SI"])*D("1e34")
        hbar_reference = h_reference/(2*pi)
        result = {"pi_control": str(pi), "hbar_SI_coefficient": str(hbar_reference)}
        for name, value in [("pre", pre), ("ret", ret)]:
            result["h_"+name+"_coefficient"] = str(2*pi*value)
            result["relative_"+name] = str(value/hbar_reference-1)
            assert abs((2*pi*value/h_reference-1)-(value/hbar_reference-1)) < D("1e-70")
        gamma = D(INTERNAL["gamma"])
        reconstructed = D(INTERNAL["gamma_angular"])+12*D(INTERNAL["delta_S90"])-D(INTERNAL["delta_S120"])
        assert abs(gamma-reconstructed) < D("1e-29")
        external_gamma, root_bound = gm_root(pi)
        result.update(gamma_GM=str(external_gamma), gamma_GM_error_bound=str(root_bound),
                      gamma_difference=str(gamma-external_gamma),
                      gamma_relative=str(gamma/external_gamma-1),
                      barbero_reconstruction_residual=str(gamma-reconstructed))
        s12,c12 = sincos(D(INTERNAL["theta12_deg"])*pi/180)
        s23,c23 = sincos(D(INTERNAL["theta23_deg"])*pi/180)
        s13,c13 = sincos(D(INTERNAL["theta13_deg"])*pi/180)
        delta = D(INTERNAL["delta_deg"])*pi/180
        sd,cd = sincos(delta)
        j = c12*c23*c13*c13*s12*s23*s13*sd
        assert abs(j-D(INTERNAL["J_published"])) < D("2e-16")
        values = {"s12": s12, "s23": s23, "s13": s13, "delta_rad": delta, "J": j}
        result["ckm"] = {}
        for key, value in values.items():
            center, lower, upper = map(D, EXTERNAL["PDG2025"][key])
            difference = value-center
            uncertainty = upper if difference >= 0 else lower
            result["ckm"][key] = {"value": str(value), "difference": str(difference),
                                   "marginal_residual": str(difference/uncertainty)}
        def modulus(real, imag=D(0)):
            return (real*real+imag*imag).sqrt()
        matrix = [
            [c12*c13,s12*c13,s13],
            [modulus(-s12*c23-c12*s23*s13*cd,-c12*s23*s13*sd),
             modulus(c12*c23-s12*s23*s13*cd,-s12*s23*s13*sd),s23*c13],
            [modulus(s12*s23-c12*c23*s13*cd,-c12*c23*s13*sd),
             modulus(-c12*s23-s12*c23*s13*cd,-s12*c23*s13*sd),c23*c13],
        ]
        published = [["0.974350259","0.225005836","0.003734601"],
                     ["0.224873110","0.973489279","0.041841465"],
                     ["0.008582400","0.041121745","0.999117283"]]
        for row, frozen in zip(matrix, published):
            for value, expected in zip(row, frozen):
                assert abs(value-D(expected)) < D("5.1e-10")
            assert abs(sum((v*v for v in row),D(0))-1) < D("1e-68")
        result["V_moduli"] = [[str(v) for v in row] for row in matrix]
        result["gravity_selector"] = str((54/pi)**2)
        result["G_relative_reference_uncertainty"] = str(D(EXTERNAL["G_standard_uncertainty"])/D(EXTERNAL["G_CODATA2022"]))
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--numbers-only", action="store_true", help="Evalúa antes de integrar el fragmento; no declara aprobación del LaTeX.")
    args = parser.parse_args()
    results = evaluate()
    source_receipts = {}
    for key, relative in SOURCES.items():
        path = ROOT / relative
        data = path.read_bytes()
        source_receipts[key] = {"path": relative, "sha256": hashlib.sha256(data).hexdigest()}
    for source, keys in [("action", ["hbar_pre_coefficient", "hbar_ret_coefficient"]),
                         ("barbero", ["gamma", "gamma_angular"]),
                         ("ckm", ["theta12_deg", "theta23_deg", "theta13_deg", "delta_deg"])]:
        original = (ROOT/SOURCES[source]).read_text(encoding="utf-8")
        for key in keys:
            assert INTERNAL[key] in original, ("Coordenada no localizada en propietario", source, key)
    if not args.numbers_only:
        text = TEX.read_text(encoding="utf-8")
        printed = re.sub(r"%[^\n]*", "", text)
        printed = re.sub(r"\\times\s*10\^\{([^}]+)\}", r"e\1", printed)
        checked = []
        for key, expected, tolerance in re.findall(r"% NUMCHECK ([A-Za-z0-9_.]+)=([+0-9.eE-]+) tol=([0-9.eE-]+)", text):
            node = results
            for part in key.split("."):
                node = node[part]
            assert abs(D(node)-D(expected)) <= D(tolerance), (key,node,expected)
            assert expected in printed, ("unprinted",key)
            checked.append(key)
        assert len(checked) >= 15, "Faltan controles ligados a cifras impresas."
        for value in [INTERNAL["hbar_pre_coefficient"], INTERNAL["hbar_ret_coefficient"], INTERNAL["gamma"]]:
            assert value in text
        source_receipts["section"] = {"path": str(TEX.relative_to(ROOT)), "sha256": hashlib.sha256(TEX.read_bytes()).hexdigest()}
        results["checked_printed_values"] = checked
    receipt = {"schema_version":"1.0", "kind":"CERTIFICADO_NUEVO_ARITMETICA_COMPARATIVA",
               "status":"NUMBERS_ONLY" if args.numbers_only else "PASS_COMPARACIONES_II",
               "scope":"Comparación posterior; no certificación del generador, inferencia conjunta ni validación metrológica global.",
               "internal_published_inputs":INTERNAL, "external_references":EXTERNAL,
               "reference_urls":REFERENCES, "sources":source_receipts, "results":results,
               "si_exact":["h","hbar=h/(2*pi)","kB"],
               "G_and_kB_independent_numeric_prediction_claimed":False,
               "PMNS_numeric_prediction_claimed":False, "covariance_fit_claimed":False}
    serialized = json.dumps(receipt, ensure_ascii=False, indent=2)+"\n"
    receipt_path = args.receipt or ROOT/'certificados/RECIBO_COMPARACIONES_II.json'
    receipt_path.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    print(receipt["status"])


if __name__ == "__main__":
    main()
