#!/usr/bin/env python3
"""Control racional del diferencial de una extensión de norma mínima.

Sólo biblioteca estándar; sin red, rutas externas ni escritura de archivos.
--json emite un recibo en stdout. Las comparaciones son explícitas y se
conservan bajo python -O. No se usan aproximaciones decimales ni diferencias
finitas: la energía se evalúa en Q[epsilon]/(epsilon**2) por eliminación
de Gauss--Jordan y se compara con el diferencial impreso.

Alcance: 26 identidades en 12 direcciones de una incidencia real 2x3 de
rango fila completo, y tres mutaciones rechazadas. Las matrices son testigos
algebraicos posteriores; no son parámetros del generador HMT. Este control
no selecciona una acción material, las rutas físicas, el campo de frontera
ni una amplitud s0. Las pruebas generales, también para espacios hermíticos,
residen en manuscrito/30e_corriente_extension_minima.tex.
"""

import argparse
import json
import sys
from fractions import Fraction as Q


PASS = "PASS_DIFERENCIAL_EXTENSION_MINIMA"
FAIL = "FAIL_DIFERENCIAL_EXTENSION_MINIMA"


class Dual:
    """Número dual racional a + epsilon*d, con epsilon**2 = 0."""

    def __init__(self, value=0, derivative=0):
        self.value = Q(value)
        self.derivative = Q(derivative)

    @staticmethod
    def lift(other):
        return other if isinstance(other, Dual) else Dual(other)

    def __add__(self, other):
        other = self.lift(other)
        return Dual(self.value + other.value,
                    self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        other = self.lift(other)
        return Dual(self.value * other.value,
                    self.value * other.derivative
                    + self.derivative * other.value)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        if not other.value:
            raise ZeroDivisionError("Divisor dual no invertible")
        return Dual(self.value / other.value,
                    (self.derivative * other.value
                     - self.value * other.derivative) / other.value**2)


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def multiply(left, right):
    return [[sum(x * y for x, y in zip(row, column))
             for column in zip(*right)] for row in left]


def add(left, right):
    return [[x + y for x, y in zip(row, other)]
            for row, other in zip(left, right)]


def scale(coefficient, matrix):
    return [[coefficient * value for value in row] for row in matrix]


def zero(rows, columns):
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def dual_matrix(matrix, variation):
    return [[Dual(x, dx) for x, dx in zip(row, drow)]
            for row, drow in zip(matrix, variation)]


def inverse_dual(matrix):
    """Gauss--Jordan en el anillo dual; pivotes con parte racional no nula."""
    size = len(matrix)
    augmented = [list(row) + [Dual(int(i == j)) for j in range(size)]
                 for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((i for i in range(column, size)
                      if augmented[i][column].value), None)
        if pivot is None:
            raise ValueError("Gramiano no invertible en el punto de prueba")
        augmented[column], augmented[pivot] = (
            augmented[pivot], augmented[column])
        divisor = augmented[column][column]
        augmented[column] = [value / divisor
                             for value in augmented[column]]
        for row in range(size):
            if row != column:
                coefficient = augmented[row][column]
                augmented[row] = [x - coefficient * y for x, y in
                                  zip(augmented[row], augmented[column])]
    return [row[size:] for row in augmented]


def run():
    # Incidencia rectangular auxiliar, no realización física de una pantalla.
    incidence = [[Q(1), Q(2), Q(0)], [Q(0), Q(1), Q(3)]]
    boundary = [[Q(2)], [Q(-1)]]
    normalization = Q(7, 5)
    constant_incidence = dual_matrix(incidence, zero(2, 3))
    gram = multiply(constant_incidence, transpose(constant_incidence))
    green = [[value.value for value in row] for row in inverse_dual(gram)]
    potential = multiply(green, boundary)
    minimum_field = multiply(transpose(incidence), potential)
    minimum_norm = multiply(transpose(boundary), potential)[0][0]
    energy = normalization * minimum_norm

    directions = []
    for row in range(2):
        for column in range(3):
            variation = zero(2, 3)
            variation[row][column] = Q(1)
            directions.append((f"incidencia_{row}_{column}", variation,
                               zero(2, 1), Q(0)))
    for row in range(2):
        variation = zero(2, 1)
        variation[row][0] = Q(1)
        directions.append((f"frontera_{row}", zero(2, 3), variation, Q(0)))
    directions.append(("normalizacion", zero(2, 3), zero(2, 1), Q(1)))
    directions.append(("variacion_conjunta",
                       [[Q(1), Q(-2), Q(3)], [Q(4), Q(0), Q(-1)]],
                       [[Q(3)], [Q(2)]], Q(-4)))

    generator_q = [[Q(0), Q(1)], [Q(-1), Q(0)]]
    generator_h = [[Q(0), Q(2), Q(0)],
                   [Q(-2), Q(0), Q(3)], [Q(0), Q(-3), Q(0)]]
    directions.append(("marco_puro",
                       add(multiply(generator_q, incidence),
                           scale(-1, multiply(incidence, generator_h))),
                       multiply(generator_q, boundary), Q(0)))
    length, dlength = Q(3), Q(2)
    directions.append(("escala_compensada", zero(2, 3),
                       scale(dlength / length, boundary),
                       -2 * normalization * dlength / length))

    identities = []
    failures = []
    mutation_witnesses = {"signo_de_delta_incidencia_invertido": None,
                          "omision_de_delta_frontera": None,
                          "omision_de_delta_normalizacion": None}

    def check(name, actual, expected):
        identities.append({"name": name, "actual": str(actual),
                           "expected": str(expected), "pass": actual == expected})
        if actual != expected:
            failures.append(name)

    for name, dincidence, dboundary, dnormalization in directions:
        dc = dual_matrix(incidence, dincidence)
        db = dual_matrix(boundary, dboundary)
        dgram = multiply(dc, transpose(dc))
        # Camino independiente: evaluar la energía completa en números duales.
        direct = (Dual(normalization, dnormalization)
                  * multiply(transpose(db),
                             multiply(inverse_dual(dgram), db))[0][0]).derivative
        boundary_term = multiply(transpose(potential), dboundary)[0][0]
        incidence_term = multiply(transpose(potential),
                                  multiply(dincidence, minimum_field))[0][0]
        expected = (dnormalization * minimum_norm
                    + 2 * normalization * (boundary_term - incidence_term))
        check(name + ": diferencial", direct, expected)

        action_scale, daction_scale = Q(11, 7), Q(-2, 9)
        direct_action = (Dual(action_scale, daction_scale)
                         * Dual(energy, direct)).derivative
        component = (4 * action_scale * normalization
                     * (incidence_term - boundary_term)
                     - 2 * action_scale * dnormalization * minimum_norm
                     - 2 * daction_scale * energy)
        check(name + ": componente_convencion_menos_un_medio",
              component, -2 * direct_action)
        if name in ("marco_puro", "escala_compensada"):
            check(name + ": invariancia", direct, Q(0))

        mutants = {
            "signo_de_delta_incidencia_invertido": (
                dnormalization * minimum_norm
                + 2 * normalization * (boundary_term + incidence_term)),
            "omision_de_delta_frontera": (
                dnormalization * minimum_norm - 2 * normalization * incidence_term),
            "omision_de_delta_normalizacion": (
                2 * normalization * (boundary_term - incidence_term)),
        }
        for mutant, value in mutants.items():
            if direct != value and mutation_witnesses[mutant] is None:
                mutation_witnesses[mutant] = {
                    "direction": name, "correct": str(direct),
                    "mutated": str(value), "rejected": True}

    if len(identities) != 26:
        failures.append("El control debe ejecutar exactamente 26 identidades")
    for name, witness in mutation_witnesses.items():
        if witness is None:
            failures.append("Mutacion no discriminada: " + name)

    return {
        "result": FAIL if failures else PASS,
        "scope": {
            "method": "Aritmetica racional exacta y numeros duales con epsilon^2=0",
            "domain": "Incidencia real 2x3 de rango fila completo; productos euclideos fijos",
            "identities": "Diferencial de energia, componentes de accion y dos invariancias",
            "source_labels": ["vii:eq:diferencial-minimo-completo",
                              "vii:eq:diferencial-minimo-escala",
                              "vii:prop:covariancia-minimo",
                              "vii:eq:componentes-minimo-conexion"],
            "not_certified": [
                "Seleccion fisica de rutas, dato de frontera o accion material",
                "Evaluacion de corriente material de espin o amplitud s0",
                "Derivacion del generador HMT o de constantes fisicas",
                "Prueba universal por enumeracion finita",
                "Autonomia o compilacion del articulo VII",
                "Verificacion exhaustiva de casos hermiticos complejos",
            ],
        },
        "execution": {"python_optimization": sys.flags.optimize,
                      "stdlib_only": True, "writes_files": False,
                      "network_access": False, "reads_external_inputs": False},
        "directions": len(directions),
        "identities_checked": len(identities),
        "negative_controls_rejected": sum(value is not None
                                          for value in mutation_witnesses.values()),
        "identities": identities,
        "negative_controls": mutation_witnesses,
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emitir recibo JSON en stdout")
    args = parser.parse_args()
    try:
        result = run()
    except Exception as error:
        result = {"result": FAIL, "failures": [type(error).__name__ + ": " + str(error)]}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["result"])
        if "identities_checked" in result:
            print(f"Identidades: {result['identities_checked']}; "
                  f"direcciones: {result['directions']}; "
                  f"mutaciones rechazadas: {result['negative_controls_rejected']}")
        for failure in result["failures"]:
            print(failure)
    return 0 if result["result"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
