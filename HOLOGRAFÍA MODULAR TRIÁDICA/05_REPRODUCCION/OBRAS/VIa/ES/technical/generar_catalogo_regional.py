#!/usr/bin/env python3
"""Emisor finito APP--TRIT--TPK. No recibe constantes ni prefijos objetivo.

Propietario: Artículo I, sections/extension.tex y sections/generacion.tex.
Este programa comprueba el censo finito; no es por sí solo la prolongación
coinductiva ni el productor del libro dodecafásico E108.
"""
import collections
import hashlib
import itertools
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
DIRS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
LOG = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5, 3: 0, 6: 0, 9: 0}


def rho(n):
    return 1 + (n - 1) % 9


def signature(i, j, direction, sheet):
    di, dj = DIRS[direction]
    totals, total = [], 0
    for t in range(1, 55):
        phase = (t - 1) % 3
        if phase == (0 if sheet == "+" else 1):
            value = rho(i + j + 2) if sheet == "+" else rho((i + 1) * (j + 1))
            total += value if sheet == "+" else LOG[value]
            i, j = (i + di) % 9, (j + dj) % 9
        if t % 9 == 0:
            totals.append(total % 10)
            total = 0
        if t % 27 == 0:
            di, dj = -di, -dj
    return tuple(totals)


def signature_closed(i, j, direction, sheet):
    """Fórmula cerrada impresa: control independiente del bucle temporal."""
    di, dj = DIRS[direction]
    values = []
    for k in range(18):
        f = k if k < 9 else 18-k
        a, b = (i + f*di) % 9, (j + f*dj) % 9
        values.append(rho(a+b+2) if sheet == "+" else LOG[rho((a+1)*(b+1))])
    return tuple(sum(values[3*m:3*m+3]) % 10 for m in range(6))


def r(w):
    return tuple(w[k] for k in (2, 0, 1, 4, 5, 3))


def s(w):
    return w[3:] + w[:3]


def orbit(w):
    return {w, r(w), r(r(w)), s(w), r(s(w)), r(r(s(w)))}


def build():
    signatures = {"+": collections.defaultdict(list), "x": collections.defaultdict(list)}
    for sheet in signatures:
        for i, j, d in itertools.product(range(9), range(9), DIRS):
            sig = signature(i, j, d, sheet)
            assert sig == signature_closed(i, j, d, sheet)
            signatures[sheet][sig].append((i, j, d))
    catalog = []
    fibers = collections.defaultdict(list)
    for a, a_states in sorted(signatures["+"].items()):
        for b, b_states in sorted(signatures["x"].items()):
            u = tuple(100 * x + 10 * ((x + y) % 10) + (3*x + 5*y + 1) % 10
                      for x, y in zip(a, b))
            w = tuple((-x) % 3 for x in u)
            row = {"U": u, "w": w, "additive_signature": a,
                   "multiplicative_signature": b,
                   "multiplicity": len(a_states) * len(b_states),
                   "additive_initial_states": a_states,
                   "multiplicative_initial_states": b_states}
            catalog.append(row)
            fibers[w].append(row)
    remaining = set(fibers)
    orbits = []
    while remaining:
        w = min(remaining)
        o = orbit(w)
        assert o <= set(fibers), "La acción regional debe conservar la imagen"
        remaining -= o
        orbits.append(sorted(o))
    closure, propagation, autoscale = [], [], []
    sector = []
    for o in orbits:
        def multiplicities(w):
            return sorted(row["multiplicity"] for row in fibers[w])
        assert all(multiplicities(w) == multiplicities(o[0]) for w in o)
        if len(o) == 6 and all(multiplicities(w) == [144]*4+[432] for w in o):
            closure.append(o)
        ds = {(i+j) % 9 for w in o for row in fibers[w]
              for i, j, d in row["additive_initial_states"]}
        if len(o) == 6 and ds == {0, 3, 6} and all(multiplicities(w) == [144] for w in o):
            sector.append(o)
            counts = tuple(o[0].count(k) for k in range(3))
            if counts == (2, 3, 1):
                propagation.append(o)
            if counts == (2, 2, 2):
                autoscale.append(o)
    assert len(signatures["+"]) == 18
    assert len(signatures["x"]) == 26
    assert len(catalog) == len({tuple(row["U"]) for row in catalog}) == 468
    assert len(fibers) == 243
    assert sum(row["multiplicity"] for row in catalog) == 104976
    assert collections.Counter(len(o) for o in orbits) == {6: 38, 3: 5}
    assert len(closure) == len(propagation) == len(autoscale) == 1
    assert len(sector) == 6
    representatives = {}
    for name, candidates in (("clausura", closure), ("propagacion", propagation), ("autoescala", autoscale)):
        o = candidates[0]
        marked = {w for w in o for row in fibers[w] for i, j, d in row["additive_initial_states"]
                  if (i+j) % 9 == 6 and d in {"E", "S"}}
        assert len(marked) == 1, (name, marked)
        representatives[name] = next(iter(marked))
    payload = {
        "scope": "censo_finito_de_emision_y_seleccion_regional",
        "generator_inputs": "Todas las parejas de cursores orientados sobre APP; reglas declaradas.",
        "not_claimed": ["productor_de_E108", "prolongacion_coinductiva_completa", "comparacion_metrologica"],
        "counts": {"initial_pairs": 104976, "decimal_emissions": 468,
                   "ternary_image": 243, "ambient_words": 729, "orbits": 43},
        "signature_preimage_histograms": {
            sheet: dict(sorted(collections.Counter(len(v) for v in sigs.values()).items()))
            for sheet, sigs in signatures.items()},
        "signatures": {
            sheet: [{"signature": sig, "multiplicity": len(states),
                     "initial_states": states} for sig, states in sorted(sigs.items())]
            for sheet, sigs in signatures.items()},
        "regional_representatives": representatives,
        "orbits": orbits,
        "orbit_data": [{"representative": o[0], "size": len(o),
                        "fiber_size": len(fibers[o[0]]),
                        "weight_per_word": sum(row["multiplicity"] for row in fibers[o[0]]),
                        "trit_census": [o[0].count(k) for k in range(3)],
                        "additive_diagonals": sorted({(i+j) % 9 for w in o for row in fibers[w]
                                                      for i, j, d in row["additive_initial_states"]})}
                       for o in orbits],
        "catalog": catalog,
    }
    return payload


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("CONTROL_NO_EJECUTADO: este programa requiere Python sin -O")
    result = build()
    out = BASE / "catalogo_regional_generado.json"
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")
    rows = [r"% Generado por technical/generar_catalogo_regional.py; censo completo de firmas.",
            r"\begin{longtable}{@{}llr@{}}", r"\toprule Hoja&Firma de seis ventanas&Preimágenes\\\midrule\endhead"]
    for sheet, name in (("+", "Aditiva"), ("x", "Multiplicativa")):
        for entry in result["signatures"][sheet]:
            digits = "".join(map(str, entry["signature"]))
            rows.append(name + r"&\(\mathtt{" + digits + r"}\)&" + str(entry["multiplicity"]) + r"\\")
    rows.extend([r"\bottomrule", r"\end{longtable}", ""])
    (BASE.parent / "sections" / "14_tablas_firmas_regionales.tex").write_text("\n".join(rows), encoding="utf-8")
    rows = [r"% Generado por technical/generar_catalogo_regional.py; 43 órbitas, sin omisiones.",
            r"\begin{longtable}{@{}lrrrrl@{}}", r"\toprule Representante&Órbita&Fibra&Peso&\(\nu\)&Diagonales\\\midrule\endhead"]
    for entry in result["orbit_data"]:
        rep = "".join(map(str, entry["representative"]))
        nu = "".join(map(str, entry["trit_census"]))
        ds = ",".join(map(str, entry["additive_diagonals"]))
        rows.append(r"\(\mathtt{" + rep + r"}\)&" + str(entry["size"]) + "&"
                    + str(entry["fiber_size"]) + "&" + str(entry["weight_per_word"]) + "&"
                    + r"\((" + ",".join(map(str, entry["trit_census"])) + r")\)&\(\{" + ds + r"\}\)\\")
    rows.extend([r"\bottomrule", r"\end{longtable}", ""])
    (BASE.parent / "sections" / "14_tabla_orbitas_regionales.tex").write_text("\n".join(rows), encoding="utf-8")
    print("PASS_CENSO_REGIONAL_FINITO_VI", result["counts"])
    print("representantes", result["regional_representatives"])
    print("sha256", hashlib.sha256(text.encode()).hexdigest())
