#!/usr/bin/env python3
"""Operadores enteros de lectura del registro dodecafásico TPK.

El módulo no intenta reconstruir el estado enriquecido desde una proyección
empobrecida. Formaliza la lectura que corresponde al tipo declarado
``TPKFullState``: el registro orientado de doce eventos es una coordenada del
estado y no un dato que deba adivinarse a partir de la palabra periódica U6.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence


Vector12 = tuple[int, ...]

H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def _v12(values: Iterable[int]) -> Vector12:
    out = tuple(int(x) for x in values)
    if len(out) != 12:
        raise ValueError("se requieren exactamente doce coordenadas")
    return out


@dataclass(frozen=True)
class EstadoTPKEnriquecido:
    """Carta mínima del estado completo necesaria para la lectura armónica.

    ``visible`` representa la proyección observable que puede ser periódica.
    ``registro`` conserva la cocadena dodecafásica orientada. Dos estados con
    la misma proyección visible pueden poseer registros distintos.
    """

    visible: tuple[int, ...]
    orientacion: int
    hoja: int
    registro: Vector12
    firma_frontera: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.orientacion not in (-1, 1):
            raise ValueError("la orientación debe ser +1 o -1")
        if self.hoja not in (-1, 1):
            raise ValueError("la hoja debe ser +1 o -1")
        object.__setattr__(self, "registro", _v12(self.registro))


@dataclass(frozen=True)
class ObservablesTransversales:
    """Datos agregados de los dos canales transversales y del modo total.

    Esta carta evita tomar ``K`` como una tabla aislada: el registro se
    reconstruye a partir de las diferencias orientadas de pasos tres y cuatro
    y de la carga dodecafasica.  Las 25 coordenadas pueden contener
    redundancias; la reconstruccion comprueba tambien su compatibilidad.
    """

    paso3: Vector12
    paso4: Vector12
    carga: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "paso3", _v12(self.paso3))
        object.__setattr__(self, "paso4", _v12(self.paso4))
        object.__setattr__(self, "carga", int(self.carga))


def desplazar(v: Sequence[int], paso: int) -> Vector12:
    """Acción cíclica positiva de Z/12Z."""

    w = _v12(v)
    k = paso % 12
    return tuple(w[(m + k) % 12] for m in range(12))


def reflejar(v: Sequence[int]) -> Vector12:
    """Reflexión que fija el origen y revierte la orientación."""

    w = _v12(v)
    return tuple(w[(-m) % 12] for m in range(12))


def diferencia(v: Sequence[int], paso: int) -> Vector12:
    """Cocadena transversal D_k=(I-S^k)."""

    w = _v12(v)
    sw = desplazar(w, paso)
    return tuple(a - b for a, b in zip(w, sw))


def _h4(v: Sequence[int]) -> tuple[int, int, int, int]:
    if len(v) != 4:
        raise ValueError("H4 actúa sobre bloques de cuatro coordenadas")
    return tuple(sum(row[j] * int(v[j]) for j in range(4)) for row in H4)  # type: ignore[return-value]


def leer_registro(estado: EstadoTPKEnriquecido) -> Vector12:
    """Proyección tipada del estado TPK completo sobre su registro orientado."""

    return estado.registro


def lectura_armonica(registro: Sequence[int]) -> Vector12:
    """Tres transformadas H4 sobre las órbitas de paso tres, reintercaladas."""

    k = _v12(registro)
    out = [0] * 12
    for r in range(3):
        bloque = (k[r], k[r + 3], k[r + 6], k[r + 9])
        modos = _h4(bloque)
        for j, value in enumerate(modos):
            out[r + 3 * j] = value
    return tuple(out)


def invertir_lectura_armonica(modos: Sequence[int]) -> Vector12:
    """Inversa exacta H4/4 sobre la imagen entera de la lectura."""

    u = _v12(modos)
    out = [0] * 12
    for r in range(3):
        bloque = (u[r], u[r + 3], u[r + 6], u[r + 9])
        numeradores = _h4(bloque)
        if any(x % 4 for x in numeradores):
            raise ValueError("el vector no pertenece a la imagen entera de la carta armónica")
        for j, value in enumerate(numeradores):
            out[r + 3 * j] = value // 4
    return tuple(out)


def lectura_transversal(registro: Sequence[int]) -> tuple[Vector12, Vector12, int]:
    """Lectura de los pasos 3 y 4 y del modo total."""

    k = _v12(registro)
    return diferencia(k, 3), diferencia(k, 4), sum(k)


def _resolver_sistema_racional(
    filas: Sequence[Sequence[int]], terminos: Sequence[int], numero_variables: int
) -> tuple[Fraction, ...]:
    """Resuelve un sistema compatible de rango completo por Gauss exacto.

    Se conservan todas las ecuaciones, incluidas las redundantes, para que una
    perturbacion de un observable sea detectada como incompatibilidad y no se
    silencie al escoger un menor conveniente.
    """

    if len(filas) != len(terminos):
        raise ValueError("numero desigual de filas y terminos")
    matriz = [
        [Fraction(int(x)) for x in fila] + [Fraction(int(b))]
        for fila, b in zip(filas, terminos)
    ]
    if any(len(fila) != numero_variables + 1 for fila in matriz):
        raise ValueError("dimension incorrecta del sistema")

    pivotes: list[int] = []
    fila_pivote = 0
    for columna in range(numero_variables):
        candidata = next(
            (r for r in range(fila_pivote, len(matriz)) if matriz[r][columna]),
            None,
        )
        if candidata is None:
            continue
        matriz[fila_pivote], matriz[candidata] = matriz[candidata], matriz[fila_pivote]
        pivote = matriz[fila_pivote][columna]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]
        for r in range(len(matriz)):
            if r == fila_pivote or not matriz[r][columna]:
                continue
            factor = matriz[r][columna]
            matriz[r] = [
                x - factor * y for x, y in zip(matriz[r], matriz[fila_pivote])
            ]
        pivotes.append(columna)
        fila_pivote += 1
        if fila_pivote == len(matriz):
            break

    for fila in matriz:
        if all(x == 0 for x in fila[:-1]) and fila[-1] != 0:
            raise ValueError("observables transversales incompatibles")
    if len(pivotes) != numero_variables:
        raise ValueError("los observables no determinan un registro unico")

    solucion = [Fraction(0)] * numero_variables
    for r, columna in enumerate(pivotes):
        solucion[columna] = matriz[r][-1]
    return tuple(solucion)


def reconstruir_registro_transversal(
    observables: ObservablesTransversales,
) -> Vector12:
    """Reconstruye el potencial dodecafasico desde ``(D3 K,D4 K,Q)``.

    La conectividad de los pasos tres y cuatro deja solamente el modo
    constante; la carga lo fija.  La funcion verifica esa afirmacion sin
    presuponer el vector buscado y exige que la solucion sea integral.
    """

    filas: list[list[int]] = []
    terminos: list[int] = []
    for paso, valores in ((3, observables.paso3), (4, observables.paso4)):
        for m, valor in enumerate(valores):
            fila = [0] * 12
            fila[m] = 1
            fila[(m + paso) % 12] -= 1
            filas.append(fila)
            terminos.append(valor)
    filas.append([1] * 12)
    terminos.append(observables.carga)

    racional = _resolver_sistema_racional(filas, terminos, 12)
    if any(x.denominator != 1 for x in racional):
        raise ValueError("los observables determinan un registro no integral")
    registro = tuple(int(x) for x in racional)
    if lectura_transversal(registro) != (
        observables.paso3,
        observables.paso4,
        observables.carga,
    ):
        raise ValueError("fallo interno al recomponer los observables")
    return registro


def agregar_observables_transversales(
    observables: ObservablesTransversales,
) -> tuple[Vector12, Vector12]:
    """Agregacion completa ``(D3,D4,Q) -> K -> U12``."""

    registro = reconstruir_registro_transversal(observables)
    return registro, lectura_armonica(registro)


def separar_signos(modos: Sequence[int]) -> tuple[Vector12, Vector12]:
    """Descomposición canónica y de soportes disjuntos u=u+−u−."""

    u = _v12(modos)
    positivo = tuple(max(x, 0) for x in u)
    negativo = tuple(max(-x, 0) for x in u)
    return positivo, negativo


def accion_inducida_en_modos(modos: Sequence[int], *, rotacion: int = 0,
                             reflexion: bool = False) -> Vector12:
    """Transporte de la acción diedral a la carta armónica.

    La fórmula H rho H^{-1} evita confundir covariancia con invariancia: una
    reflexión o rotación del registro cambia los contrastes de modo controlado.
    """

    k = invertir_lectura_armonica(modos)
    if reflexion:
        k = reflejar(k)
    k = desplazar(k, rotacion)
    return lectura_armonica(k)


def olvidar_hoja_por_suma(registro: Sequence[int]) -> tuple[int, ...]:
    """Ablación 12→6 que suma posiciones opuestas."""

    k = _v12(registro)
    return tuple(k[m] + k[m + 6] for m in range(6))
