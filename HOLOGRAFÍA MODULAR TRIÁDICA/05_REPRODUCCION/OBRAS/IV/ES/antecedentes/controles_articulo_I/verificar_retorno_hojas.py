#!/usr/bin/env python3
"""Control exacto focal del retorno entre hojas y su evaluación de frontera.

Procedencia: sections/generacion.tex (calendario e incidencia),
sections/retorno_areal_volumetrico.tex (normalización y retorno marcado),
sections/electron.tex (intercambio de las dos orientaciones).

El calendario produce F antes de toda realización en Q(phi). La relación
phi^2=phi+1 se usa aquí como reconocimiento algebraico posterior del vector
propio de esa incidencia. PI es una indeterminada que representa la salida
regional previamente construida: este programa no genera ni aproxima pi.

Los controles son exactos y finitos. No sustituyen las pruebas generales de
convergencia, maximalidad entrópica, unicidad de Parry o generación coinductiva.
El control de preservación es editorial, no una certificación matemática.
No se consultan valores objetivo, CODATA ni constantes decimales externas.

Uso: python3 -I -S technical/verificar_retorno_hojas.py
     python3 -I -S technical/verificar_retorno_hojas.py --check-preservation
     python3 -I -S technical/verificar_retorno_hojas.py --receipt RUTA.json
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError("FAIL_RETORNO_HOJAS: " + message)


@dataclass(frozen=True)
class QPhi:
    """a+b*phi, con phi^2=phi+1, aritmética racional exacta."""
    a: Q = Q(0)
    b: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, "a", Q(self.a))
        object.__setattr__(self, "b", Q(self.b))

    @staticmethod
    def lift(x):
        return x if isinstance(x, QPhi) else QPhi(x)

    def __add__(self, other):
        y = self.lift(other)
        return QPhi(self.a + y.a, self.b + y.b)

    __radd__ = __add__

    def __neg__(self):
        return QPhi(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.lift(other)

    def __mul__(self, other):
        y = self.lift(other)
        return QPhi(self.a*y.a + self.b*y.b,
                    self.a*y.b + self.b*y.a + self.b*y.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a + self.a*self.b - self.b*self.b
        require(norm != 0, "inversión de un elemento nulo")
        return QPhi((self.a + self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self * self.lift(other).inverse()

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result, base = QPhi(1), self
        while exponent:
            if exponent & 1:
                result = result * base
            base, exponent = base * base, exponent // 2
        return result

    def json(self):
        return {"rational": str(self.a), "phi_coefficient": str(self.b)}


def matmul(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def matpow(a, exponent):
    result = ((1, 0), (0, 1))
    for _ in range(exponent):
        result = matmul(result, a)
    return result


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a


def modal_cycle(length):
    require(length > 0 and length % 3 == 0, "calendario de ciclos completos")
    mode = 1  # Pi: el cierre del ciclo (+,-,0) termina en esta hoja.
    modes = []
    for k in range(length):
        phase = (1, -1, 0)[k % 3]
        if phase == 1:
            mode = 0  # Sigma
        elif phase == -1:
            mode = 1  # Pi
        modes.append(mode)  # fase 0 conserva el modo precedente
    incidence = [[0, 0], [0, 0]]
    for i, j in zip(modes, modes[1:] + modes[:1]):
        incidence[i][j] += 1
    return tuple(modes), tuple(tuple(row) for row in incidence)


def p_add(a, b):
    result = dict(a)
    for degree, coefficient in b.items():
        result[degree] = result.get(degree, Q(0)) + coefficient
    return {d: c for d, c in result.items() if c}


def p_mul(a, b):
    result = {}
    for d, c in a.items():
        for e, f in b.items():
            result[d+e] = result.get(d+e, Q(0)) + c*f
    return {d: c for d, c in result.items() if c}


def p_matrix_mul(a, b):
    return tuple(tuple(p_add(p_mul(a[i][0], b[0][j]),
                             p_mul(a[i][1], b[1][j]))
                       for j in range(2)) for i in range(2))


def source_preservation(root, previous):
    require(previous.is_dir(), "directorio precedente inexistente")
    originals = [previous / "main.tex"] + sorted((previous / "sections").rglob("*.tex"))
    mutable = {"sections/generacion.tex", "sections/electron.tex"}
    identical, insertions = [], {}
    for source in originals:
        relative = source.relative_to(previous).as_posix()
        target = root / relative
        require(target.is_file(), "fuente desaparecida: " + relative)
        before, after = source.read_bytes(), target.read_bytes()
        if before == after:
            identical.append(relative)
            continue
        require(relative in mutable, "fuente modificada fuera del delta: " + relative)
        left, right = before.decode("utf-8").splitlines(keepends=True), after.decode("utf-8").splitlines(keepends=True)
        operations = SequenceMatcher(a=left, b=right, autojunk=False).get_opcodes()
        require(all(tag in ("equal", "insert") for tag, *_ in operations),
                "supresión o sustitución de texto: " + relative)
        added = [line for tag, _, _, j, k in operations if tag == "insert" for line in right[j:k]]
        if relative.endswith("generacion.tex"):
            require([x.strip() for x in added if x.strip()] == [r"\input{sections/retorno_areal_volumetrico.tex}"],
                    "inserción de generación distinta de la inclusión prevista")
        else:
            expected = """El espacio de trayectorias, su medida y el operador de clausura están
construidos en los apartados~\\ref{sec:medida-retorno-hojas}
y~\\ref{sec:operador-retorno-marcado}. La fórmula
\\eqref{eq:retorno-marcado-finito} conserva su procedencia como cociente
de retornos; la aplicación electrónica compone después esta lectura
con la involución siguiente. La firma regional \\(555555\\) acompaña
a la región de clausura, cuyo transporte conserva el estado con memoria;
el centro \\((5,5)\\) fija la celda de origen de la sección electrónica
orientada. Ambas informaciones convergen en la composición y mantienen
sus dominios respectivos.
"""
            require("".join(added).strip() == expected.strip(),
                    "el enlace electrónico difiere del bloque definitivo autorizado")
        insertions[relative] = {"line_count": len(added), "inserted_text": "".join(added)}
    figures = sorted(p for p in (previous / "figures").rglob("*") if p.is_file())
    figure_records = []
    for source in figures:
        relative = source.relative_to(previous).as_posix()
        target = root / relative
        require(target.is_file() and source.read_bytes() == target.read_bytes(),
                "figura ausente o modificada: " + relative)
        figure_records.append({"path": relative, "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    return {"status": "PASS_PRESERVACION_FOCAL", "previous": str(previous),
            "current": str(root), "original_tex_count": len(originals),
            "identical_original_tex_count": len(identical), "identical_original_tex": identical,
            "insertions": insertions, "identical_figure_count": len(figures),
            "figures": figure_records,
            "scope": "Sólo main.tex, sections/*.tex y figuras de la versión precedente; no autonomía matemática."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--check-preservation", action="store_true")
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    modes, F = modal_cycle(3)
    require(modes == (0, 1, 1), "modos Sigma,Pi,Pi")
    require(F == ((0, 1), (1, 1)), "incidencia extraída del calendario")
    frequencies = [Q(Counter(modes)[i], len(modes)) for i in range(2)]
    counts = {}
    for length in (9, 27, 108):
        _, count = modal_cycle(length)
        require(count == tuple(tuple(length//3*x for x in row) for row in F), "conteo del calendario")
        require(count != matpow(F, length), "confusión entre conteo temporal y potencia")
        counts[str(length)] = count
    for n in range(1, 109):
        require(matpow(F, n) == ((fibonacci(n-1), fibonacci(n)),
                                 (fibonacci(n), fibonacci(n+1))), "fórmula de potencias en n=" + str(n))

    one, zero, phi = QPhi(1), QPhi(), QPhi(0, 1)
    require(phi**2 == phi + one, "relación cuadrática")
    r = (one, phi)
    require(all(sum(F[i][j]*r[j] for j in range(2)) == phi*r[i] for i in range(2)), "vector propio")
    P = tuple(tuple(F[i][j]*r[j]/(phi*r[i]) for j in range(2)) for i in range(2))
    require(P == ((zero, one), (phi**-2, phi**-1)), "normalización de transición")
    require(all(sum(row) == one for row in P), "suma de filas")
    mu = (one/(one+phi**2), phi**2/(one+phi**2))
    require(sum(mu) == one, "normalización de mu")
    require(all(mu[i]*P[i][j] == mu[j]*P[j][i] for i in range(2) for j in range(2)), "balance detallado")
    require(all(sum(mu[i]*P[i][j] for i in range(2)) == mu[j] for j in range(2)), "estacionariedad")
    require(mu[0]/mu[1] == phi**-2, "razón de pesos")
    require(mu != tuple(QPhi(f) for f in frequencies), "frecuencia cronológica distinta de la distribución estacionaria")

    PI = {1: Q(1)}  # símbolo, nunca evaluación numérica ni entrada metrológica
    D = ((PI, {}), ({}, {0: Q(1)}))
    marked = {}
    for n in (1, 2, 108):
        Fn = matpow(F, n)
        Fn_symbolic = tuple(tuple({0: Q(x)} if x else {} for x in row) for row in Fn)
        numerator = p_matrix_mul(D, Fn_symbolic)[0][0]
        expected = {1: Q(fibonacci(n-1))} if n > 1 else {}
        require(numerator == expected, "marca terminal aplicada una vez")
        denominator = Fn[1][1]
        require(denominator == fibonacci(n+1) and denominator > 0, "denominador de retorno")
        marked[str(n)] = {"areal_count": Fn[0][0], "volumetric_count": denominator,
                          "PI_coefficient": str(Q(Fn[0][0], denominator)),
                          "PI_degree": 1 if numerator else None}
    # Falsador exacto: marcar en cada paso altera el lector (n=4).
    Fp = tuple(tuple({0: Q(x)} if x else {} for x in row) for row in F)
    DF = p_matrix_mul(D, Fp)
    repeated = (({0: Q(1)}, {}), ({}, {0: Q(1)}))
    for _ in range(4):
        repeated = p_matrix_mul(repeated, DF)
    require(repeated[0][0] == {1: Q(1), 2: Q(1)}, "control de marca repetida")
    require(repeated[0][0] != {1: Q(matpow(F, 4)[0][0])}, "el falsador no discrimina la multiplicidad de marca")

    mirror_cases = []
    for x, y in ((Q(2), Q(3)), (Q(7,11), Q(13,17)), (Q(5), Q(1)), (Q(1), Q(2)), (Q(3,4), Q(5,6))):
        forward, reverse = x/y**2, y/x**2
        require(reverse == 1/(y**3*forward**2), "identidad de intercambio")
        require(tuple(reversed(tuple(reversed((x,y))))) == (x,y), "involución")
        mirror_cases.append({"x": str(x), "y": str(y), "forward": str(forward), "reverse": str(reverse)})

    report = {"status": "PASS_RETORNO_HOJAS_EXACTO_FOCAL", "calendar": [1,-1,0],
              "modes": ["Sigma","Pi","Pi"], "incidence": F, "calendar_counts": counts,
              "fibonacci_power_tests": {"first": 1, "last": 108, "count": 108},
              "Q_phi_transition": [[v.json() for v in row] for row in P],
              "Q_phi_stationary_distribution": [v.json() for v in mu],
              "calendar_frequency": [str(f) for f in frequencies], "marked_returns": marked,
              "repeated_mark_negative_control": "(D_PI F)^4[0,0]=PI+PI^2, distinto de (D_PI F^4)[0,0]=2PI",
              "mirror_rational_tests": mirror_cases,
              "causal_scope": "Calendario -> incidencia; realización algebraica posterior. PI sólo representa la salida regional previa y se aplica una vez.",
              "limits": ["Los 108 exponentes probados no sustituyen la demostración inductiva universal.",
                         "No se demuestra el límite universal mediante aproximaciones finitas.",
                         "Balance y estacionariedad no sustituyen la prueba de maximalidad entrópica y unicidad de Parry.",
                         "No se comprueba aquí la generación primaria de pi ni una identificación física."]}
    if args.check_preservation:
        root = Path(__file__).resolve().parent.parent
        previous = args.previous or root.parent / "ARTICULO_REVISION_FIGURAS_CENTRO_20260909"
        report["editorial_preservation"] = source_preservation(root, previous)
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
