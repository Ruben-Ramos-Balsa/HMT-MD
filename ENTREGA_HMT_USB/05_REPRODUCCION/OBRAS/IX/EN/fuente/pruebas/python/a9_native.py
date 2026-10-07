#!/usr/bin/env python3
"""Producto entero construido desde la extensión aritmética local A9#.

Los digitos son los representantes D9={1,...,9}.  Las palabras usan la
numeracion biyectiva de base nueve: el cero es la palabra vacia y, para una
palabra little-endian ``w``,

    value(w) = sum(w[k] * 9**k).

Esta eleccion es esencial: el representante 9 no se rebautiza como un cero
sin memoria.  Las unicas operaciones locales usadas por el transductor son
las dos hojas de A9#,

    a+b = 9 Q_plus(a,b)  + R_plus(a,b),
    a*b = 9 Q_times(a,b) + R_times(a,b),

con restos en D9.  El producto de palabras se implementa por Horner y no
evalua las palabras antes de multiplicarlas.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence


DIGITS = tuple(range(1, 10))
DigitWord = tuple[int, ...]
Operation = Literal["plus", "times"]


@dataclass(frozen=True)
class LiftedCell:
    """Una evaluacion local de una de las dos hojas de A9#."""

    operation: Operation
    left: int
    right: int
    residue: int
    quotient: int

    @property
    def reconstructed(self) -> int:
        return 9 * self.quotient + self.residue


def _require_digit(digit: int) -> None:
    if digit not in DIGITS:
        raise ValueError(f"digito fuera de D9: {digit!r}")


def require_word(word: Sequence[int]) -> None:
    for digit in word:
        _require_digit(digit)


def dr9(value: int) -> int:
    """Representante en D9, con 9 como representante del resto cero."""

    residue = value % 9
    return 9 if residue == 0 else residue


def lifted_cell(operation: Operation, left: int, right: int) -> LiftedCell:
    """Evalua exactamente una celda de A9#."""

    _require_digit(left)
    _require_digit(right)
    if operation == "plus":
        total = left + right
    elif operation == "times":
        total = left * right
    else:  # pragma: no cover - protegido por el tipo y por el auditor
        raise ValueError(f"hoja desconocida: {operation!r}")
    residue = dr9(total)
    quotient = (total - residue) // 9
    return LiftedCell(operation, left, right, residue, quotient)


def a9_add(left: int, right: int) -> tuple[int, int]:
    cell = lifted_cell("plus", left, right)
    return cell.residue, cell.quotient


def a9_multiply(left: int, right: int) -> tuple[int, int]:
    cell = lifted_cell("times", left, right)
    return cell.residue, cell.quotient


def encode_bijective9(value: int) -> DigitWord:
    """Codifica N_0 en palabras biyectivas de base nueve."""

    if value < 0:
        raise ValueError("la codificación nativa usa N_0")
    digits: list[int] = []
    while value:
        value -= 1
        digits.append(value % 9 + 1)
        value //= 9
    return tuple(digits)


def word_value(word: Sequence[int]) -> int:
    """Evaluacion arquimediana; se usa para el entrelazador y la auditoria."""

    require_word(word)
    value = 0
    place = 1
    for digit in word:
        value += digit * place
        place *= 9
    return value


def add_words(
    left: Sequence[int],
    right: Sequence[int],
    trace: list[LiftedCell] | None = None,
) -> DigitWord:
    """Suma nativa de palabras mediante la hoja aditiva de A9#."""

    require_word(left)
    require_word(right)
    output: list[int] = []
    carry = 0
    width = max(len(left), len(right))

    for index in range(width):
        have_left = index < len(left)
        have_right = index < len(right)
        if have_left and have_right:
            cell = lifted_cell("plus", left[index], right[index])
            if trace is not None:
                trace.append(cell)
            residue, next_carry = cell.residue, cell.quotient
        elif have_left:
            residue, next_carry = left[index], 0
        else:
            residue, next_carry = right[index], 0

        if carry:
            cell = lifted_cell("plus", residue, carry)
            if trace is not None:
                trace.append(cell)
            residue = cell.residue
            next_carry += cell.quotient

        output.append(residue)
        carry = next_carry
        if not 0 <= carry <= 2:
            raise ArithmeticError("acarreo aditivo fuera de la cota nativa")

    if carry:
        _require_digit(carry)
        output.append(carry)
    return tuple(output)


def multiply_word_by_digit(
    word: Sequence[int],
    digit: int,
    trace: list[LiftedCell] | None = None,
) -> DigitWord:
    """Multiplica una palabra por un digito usando producto y suma de A9#."""

    require_word(word)
    _require_digit(digit)
    if not word:
        return ()

    output: list[int] = []
    carry = 0
    for source_digit in word:
        product_cell = lifted_cell("times", source_digit, digit)
        if trace is not None:
            trace.append(product_cell)
        residue = product_cell.residue
        next_carry = product_cell.quotient

        if carry:
            add_cell = lifted_cell("plus", residue, carry)
            if trace is not None:
                trace.append(add_cell)
            residue = add_cell.residue
            next_carry += add_cell.quotient

        output.append(residue)
        carry = next_carry
        if not 0 <= carry <= 9:
            raise ArithmeticError("memoria multiplicativa fuera de D9")

    if carry:
        _require_digit(carry)
        output.append(carry)
    return tuple(output)


def native_product_words(
    left: Sequence[int],
    right: Sequence[int],
    trace: list[LiftedCell] | None = None,
) -> DigitWord:
    """Producto nativo A9# por Horner sobre la palabra derecha.

    En cada paso se realiza ``acc <- 9*acc + digit*left``.  Tanto la
    multiplicacion por 9 y por ``digit`` como la suma son transductores de
    celdas A9#.  No se llama a ``word_value`` ni se multiplica la evaluacion
    de las palabras.
    """

    require_word(left)
    require_word(right)
    if not left or not right:
        return ()

    accumulator: DigitWord = ()
    for digit in reversed(right):
        shifted = multiply_word_by_digit(accumulator, 9, trace)
        partial = multiply_word_by_digit(left, digit, trace)
        accumulator = add_words(shifted, partial, trace)
    return accumulator


def native_product(left: int, right: int) -> int:
    """Interfaz numerica; la operacion interna sigue siendo el transductor."""

    if left < 0 or right < 0:
        raise ValueError("el producto nativo trabaja sobre N_0")
    word = native_product_words(
        encode_bijective9(left), encode_bijective9(right)
    )
    return word_value(word)


def all_factor_pairs_native(limit: int) -> dict[int, tuple[tuple[int, int], ...]]:
    """Coproducto finito obtenido con el producto nativo, no con divisibilidad."""

    if limit < 1:
        return {}
    factors: dict[int, list[tuple[int, int]]] = {
        value: [] for value in range(1, limit + 1)
    }
    encoded = [encode_bijective9(value) for value in range(limit + 1)]
    for left in range(1, limit + 1):
        for right in range(1, limit + 1):
            product_word = native_product_words(encoded[left], encoded[right])
            product = word_value(product_word)
            if product > limit:
                break
            factors[product].append((left, right))
    return {value: tuple(pairs) for value, pairs in factors.items()}


def irreducibles_native(limit: int) -> tuple[int, ...]:
    """Selecciona atomos por ausencia de apertura nativa no trivial."""

    factors = all_factor_pairs_native(limit)
    return tuple(
        value
        for value in range(2, limit + 1)
        if not any(left >= 2 and right >= 2 for left, right in factors[value])
    )


def cell_table(operation: Operation) -> tuple[tuple[LiftedCell, ...], ...]:
    return tuple(
        tuple(lifted_cell(operation, left, right) for right in DIGITS)
        for left in DIGITS
    )


def flatten(cells: Iterable[Iterable[LiftedCell]]) -> tuple[LiftedCell, ...]:
    return tuple(cell for row in cells for cell in row)
