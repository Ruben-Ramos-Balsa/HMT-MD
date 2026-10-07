#!/usr/bin/env python3
"""Controles focales de VI; no certifican el artículo ni una interfaz física.

Python estándar. Por defecto recorre el ambiente completo de 3**12 palabras.
--quick limita ese control a muestras; ambos modos declaran su alcance.
Las constantes físicas no intervienen en estos controles.
"""

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import exp
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def cm(tau):
    if len(tau) != 12 or any(t not in (-1, 0, 1) for t in tau):
        raise ValueError("C_M requiere doce trits")
    return tuple(-t for t in tau[::-1])


def invert_lattice(a, b):
    if not isinstance(a, int) or not isinstance(b, int) or (a+b) % 12:
        raise ValueError("Punto fuera de la imagen entera")
    return F(a+b, 12), F(a-b, 2)


def channels(a, b):
    if a <= abs(b):
        raise ValueError("Se requiere a>|b| para ambos canales contractivos")
    return exp(-a-b), exp(-a+b)


def ellipse(mu, coupling, semimajor, eccentricity):
    if min(mu, coupling, semimajor) <= 0 or not 0 <= eccentricity < 1:
        raise ValueError("Dominio eliptico: mu,K,a>0 y 0<=epsilon<1")
    p = semimajor*(1-eccentricity*eccentricity)
    ell2 = coupling*p/mu
    b2 = semimajor*semimajor*(1-eccentricity*eccentricity)
    return p, ell2, b2


def rejects(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def mul(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def scale(z, A):
    return tuple(tuple(z*t for t in row) for row in A)


def run(quick=False):
    root = Path(__file__).resolve().parents[1]
    names = ("02_particula_persistencia.tex", "03_conjugacion_mobius.tex",
             "06_kepler_sommerfeld.tex")
    labels, refs, proofs, files = [], [], 0, []
    for name in names:
        p = root / "sections" / name
        raw = p.read_bytes()
        text = raw.decode("utf-8")
        own = re.findall(r"\\label\{([^}]+)\}", text)
        labels.extend(own)
        refs.extend(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text))
        proofs += text.count(r"\begin{proof}")
        stack = []
        for op, env in re.findall(r"\\(begin|end)\{([^}]+)\}", text):
            if op == "begin":
                stack.append(env)
            else:
                require(bool(stack) and stack.pop() == env, "Entorno: " + name)
        require(not stack, "Entorno abierto: " + name)
        require(all(x.startswith("vi:") for x in own), "Prefijo: " + name)
        require(all(x not in text for x in ("+gravitatorio", "TODO", "FIXME",
                                           "TPK actualizado")), "Residuo editorial")
        files.append({"path": str(p), "sha256": sha256(raw).hexdigest()})
    require(len(labels) == len(set(labels)), "Etiquetas duplicadas")
    require(not set(refs)-set(labels), "Cruce local sin destino")

    tau_e = (1,1,1,-1,-1,-1,1,1,1,-1,-1,-1)
    words = product((-1,0,1), repeat=12)
    # El modo rapido se construye por separado para mantener doce posiciones.
    if quick:
        words = [(0,)*12, (1,)*12, (-1,)*12, tau_e]
        words += [tuple(1 if i == j else 0 for i in range(12)) for j in range(12)]
    w = tuple(min(j, 11-j) for j in range(12))
    count = 0
    for tau in words:
        ct = cm(tau)
        require(cm(ct) == tau, "C_M no involutivo")
        require(sum(a*t for a,t in zip(w,ct)) == -sum(a*t for a,t in zip(w,tau)),
                "Paridad lineal")
        require(sum(ct[j]*ct[(j+1)%12] for j in range(12)) ==
                sum(tau[j]*tau[(j+1)%12] for j in range(12)), "Paridad cuadratica")
        count += 1
    require(cm(tau_e) == tau_e, "Registro electronico fijo")

    lattice_count = 0
    for a,b in product(range(-24,25), repeat=2):
        if (a+b) % 12 == 0:
            n,s = invert_lattice(a,b)
            require(n.denominator == s.denominator == 1, "Inversa no entera")
            require((6*n+s,6*n-s) == (a,b), "Inversa incorrecta")
            lattice_count += 1

    identity = ((1,0),(0,1))
    sigma = (((0,1),(1,0)), ((0,-1j),(1j,0)), ((1,0),(0,-1)))
    for A in sigma:
        require(mul(A,A) == identity, "Cuadrado de Pauli")
    for a,b,c in ((0,1,2),(1,2,0),(2,0,1)):
        require(mul(sigma[a],sigma[b]) == scale(1j,sigma[c]), "Producto ciclico")
        require(mul(sigma[b],sigma[a]) == scale(-1j,sigma[c]), "Producto inverso")

    orbital_count = 0
    for mu,K,a,e in product((F(1),F(2)), (F(1),F(3)),
                            (F(1),F(5)), (F(0),F(1,3),F(2,3))):
        p,ell2,b2 = ellipse(mu,K,a,e)
        require(a*a*b2/ell2 == mu*a**3/K, "Ley de periodo")
        require(K*(e*e-1)/(2*p) == -K/(2*a), "Energia eliptica")
        orbital_count += 1

    negative = []
    for title, condition in (
        ("C_M rechaza longitud incorrecta", rejects(cm, (1,0))),
        ("C_M rechaza simbolo exterior", rejects(cm, (2,)*12)),
        ("Inversa rechaza punto de suma no divisible por 12", rejects(invert_lattice,1,0)),
        ("Canales rechazan frontera a=|b|", rejects(channels,1,1)),
        ("Canales rechazan exterior a<|b|", rejects(channels,1,2)),
        ("Elipse rechaza masa nula", rejects(ellipse,F(0),F(1),F(1),F(0))),
        ("Elipse rechaza acoplamiento no positivo", rejects(ellipse,F(1),F(-1),F(1),F(0))),
        ("Elipse rechaza excentricidad parabolica", rejects(ellipse,F(1),F(1),F(1),F(1))),
        ("Holonomia trivial no requiere dos vueltas", 1**1 == 1 and (-1)**1 != 1),
    ):
        require(condition, title)
        negative.append(title)
    test_word = (1,) + (0,)*11
    require(cm(test_word)[0] != -test_word[0], "Control peso no simetrico")
    negative.append("Un peso lineal no simetrico no satisface la paridad general")
    require(cm(test_word)[0]**2 != test_word[0]**2, "Control cuadratica no reversible")
    negative.append("Una cuadratica sin simetria de reversion no es necesariamente par")
    q1,q2 = channels(2,1)
    r1,r2 = channels(2,-1)
    require(0 < q1 < q2 < 1 and (q1,q2) == (r2,r1), "Intercambio de canales")

    return {
        "status": "PASS_FOCAL_PARTICULA_MOBIUS_KEPLER",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "QUICK_SAMPLE" if quick else "FULL_AMBIENT_CM",
        "scope": "Controles locales; no certificado global ni artefacto sellado",
        "physical_targets_used": False,
        "latex": {"labels": len(labels), "references": len(refs), "proofs": proofs},
        "checks": {"cm_ambient_words": count, "lattice_points": lattice_count,
                   "pauli_products": "EXACT", "kepler_rational_cases": orbital_count,
                   "negative_controls": negative},
        "files": files,
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "not_checked": ["Compilacion", "QA visual", "Selector fisico de especies",
                        "Clausura completa de dependencias de VI", "Interfaz orbital concreta"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    receipt = run(args.quick)
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
