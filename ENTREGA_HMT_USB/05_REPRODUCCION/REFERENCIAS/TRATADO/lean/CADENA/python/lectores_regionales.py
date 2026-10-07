#!/usr/bin/env python3
"""Selector coinductivo global de las tres ramas arquimedianas de HMT.

La fuente no contiene prefijos decimales ni ternarios de pi, e o phi. Recibe
las tres palabras raíz que produjo el selector orbital finito, que no usa
L0/L1 ni expansiones objetivo, y prolonga cada rol por su funcional intrínseco:

* cierre: monodromía circular, evaluada por la identidad de Machin;
* propagación: flujo exponencial unitario, evaluado por su serie factorial;
* autoescala: razón positiva fija de x -> 1 + 1/x.

Cada funcional se encierra entre racionales exactos.  Una palabra de longitud
n queda emitida únicamente cuando ambos extremos pertenecen al mismo cilindro
de base b y profundidad n.  El procedimiento sirve para todo n y no consulta
una expansión objetivo.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import inspect
import json
import math
from pathlib import Path
from typing import Callable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROOT_CERTIFICATE = ROOT / (
    "../verificaciones/R15/"
    "EL_CIERRE_HOLOGRAFICO_DEL_INFINITO_HMT_MD_2026-07-22/"
    "01_HOLOGRAFIA_MODULAR_TRIADICA/certificados/"
    "selector_orbital_constantes.json"
)
FINITE_R36_CONTROL = HERE / "CERTIFICADO_SELECTOR_INTERNO.json"
OUTPUT = HERE / "CERTIFICADO_SELECTOR_GLOBAL.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"selector global HMT: {message}")


@dataclass(frozen=True)
class Intervalo:
    inferior: Fraction
    superior: Fraction
    iteraciones: int

    def __post_init__(self) -> None:
        require(self.inferior < self.superior, "intervalo vacío o degenerado")

    @property
    def anchura(self) -> Fraction:
        return self.superior - self.inferior


def intervalo_arctan_inverso(q: int, terminos: int) -> tuple[Fraction, Fraction]:
    """Cotas alternantes exactas para arctan(1/q), q>1."""
    require(q > 1 and terminos >= 1, "parámetros inválidos en arctan")
    x = Fraction(1, q)
    parcial = Fraction(0)
    for k in range(terminos):
        termino = x ** (2 * k + 1) / (2 * k + 1)
        parcial += termino if k % 2 == 0 else -termino
    siguiente = x ** (2 * terminos + 1) / (2 * terminos + 1)
    vecino = parcial + (siguiente if terminos % 2 == 0 else -siguiente)
    return min(parcial, vecino), max(parcial, vecino)


def intervalo_cierre(iteraciones: int) -> Intervalo:
    """Cotas de 16 arctan(1/5)-4 arctan(1/239)."""
    l5, u5 = intervalo_arctan_inverso(5, iteraciones)
    l239, u239 = intervalo_arctan_inverso(239, iteraciones)
    return Intervalo(16 * l5 - 4 * u239, 16 * u5 - 4 * l239, iteraciones)


def intervalo_propagacion(iteraciones: int) -> Intervalo:
    """Cotas exactas de sum(1/k!), con una cota geométrica de la cola."""
    n = iteraciones
    require(n >= 2, "se requieren al menos dos términos factoriales")
    factorial = 1
    parcial = Fraction(1)
    for k in range(1, n + 1):
        factorial *= k
        parcial += Fraction(1, factorial)
    factorial_siguiente = factorial * (n + 1)
    # Para j>=0, 1/((n+1)...(n+1+j)) <= (1/(n+2))^j/(n+1)!.
    cola_superior = Fraction(n + 2, factorial_siguiente * (n + 1))
    return Intervalo(parcial, parcial + cola_superior, iteraciones)


def intervalo_autoescala(iteraciones: int) -> Intervalo:
    """Bisección racional de la raíz positiva de x^2-x-1."""
    require(iteraciones >= 1, "se requiere al menos una bisección")
    inferior, superior = Fraction(1), Fraction(2)
    for _ in range(iteraciones):
        medio = (inferior + superior) / 2
        if medio * medio - medio - 1 < 0:
            inferior = medio
        else:
            superior = medio
    return Intervalo(inferior, superior, iteraciones)


FUNCIONALES: dict[str, Callable[[int], Intervalo]] = {
    "cierre": intervalo_cierre,
    "propagacion": intervalo_propagacion,
    "autoescala": intervalo_autoescala,
}


def parte_entera_comun(intervalo: Intervalo) -> int | None:
    a = intervalo.inferior.numerator // intervalo.inferior.denominator
    b = intervalo.superior.numerator // intervalo.superior.denominator
    return a if a == b else None


def prefijo_unico(intervalo: Intervalo, base: int, longitud: int) -> int | None:
    require(base >= 2 and longitud >= 1, "base o longitud inválida")
    entero = parte_entera_comun(intervalo)
    if entero is None:
        return None
    escala = base ** longitud
    inferior = (intervalo.inferior - entero) * escala
    superior = (intervalo.superior - entero) * escala
    a = inferior.numerator // inferior.denominator
    b = superior.numerator // superior.denominator
    return a if a == b else None


def digitos(valor: int, base: int, longitud: int) -> tuple[int, ...]:
    require(0 <= valor < base ** longitud, "prefijo fuera de rango")
    salida = [0] * longitud
    for indice in range(longitud - 1, -1, -1):
        valor, salida[indice] = divmod(valor, base)
    return tuple(salida)


def emitir(
    funcional: Callable[[int], Intervalo],
    base: int,
    longitud: int,
) -> tuple[tuple[int, ...], Intervalo]:
    """Refina cotas hasta aislar un único cilindro de profundidad dada."""
    paso = 8
    iteraciones = 8
    while True:
        intervalo = funcional(iteraciones)
        prefijo = prefijo_unico(intervalo, base, longitud)
        if prefijo is not None:
            return digitos(prefijo, base, longitud), intervalo
        iteraciones += paso
        require(iteraciones <= 10000, "la refinación no aisló el cilindro")


def palabra(digitos_emitidos: tuple[int, ...]) -> str:
    return "".join(str(x) for x in digitos_emitidos)


def fraccion_json(x: Fraction) -> dict[str, str]:
    return {"numerador": str(x.numerator), "denominador": str(x.denominator)}


def codigo_sin_prefijos_literales(prefijos: list[str]) -> bool:
    fuente = inspect.getsource(inspect.getmodule(codigo_sin_prefijos_literales))
    return all(prefijo not in fuente for prefijo in prefijos)


def main() -> None:
    raiz = json.loads(ROOT_CERTIFICATE.read_text(encoding="utf-8"))
    require(
        raiz["status"] == "PASS_FINITE_INTERNAL_ORBIT_SELECTION_RELATIVE_TO_GAUGE",
        "el selector orbital finito no está certificado",
    )
    calibre = raiz["orientation_gauge"]
    roles = {
        "cierre": calibre["pi_word"],
        "propagacion": calibre["e_word"],
        "autoescala": calibre["phi_word"],
    }
    require(set(roles) == set(FUNCIONALES), "roles internos incompletos")

    # Se certifican simultáneamente el prefijo ternario y 120 tríadas
    # decimales. La elección 120 es una prueba finita exigente; el algoritmo no
    # contiene un máximo matemático y acepta cualquier profundidad finita.
    longitudes_ternarias = (6, 18, 36, 72, 180, 360)
    numero_tríadas = 120
    resultado: dict[str, object] = {}
    for rol, funcional in FUNCIONALES.items():
        cilindros = []
        anterior = ""
        for longitud in longitudes_ternarias:
            ds, intervalo = emitir(funcional, 3, longitud)
            actual = palabra(ds)
            require(actual.startswith(anterior), "los cilindros no están anidados")
            anterior = actual
            cilindros.append(
                {
                    "longitud": longitud,
                    "palabra": actual,
                    "iteraciones": intervalo.iteraciones,
                    "anchura": fraccion_json(intervalo.anchura),
                }
            )
        require(cilindros[0]["palabra"] == roles[rol], f"la raíz interna de {rol} no coincide")
        triadas, intervalo_decimal = emitir(funcional, 1000, numero_tríadas)
        resultado[rol] = {
            "raiz_interna": roles[rol],
            "cilindros_ternarios": cilindros,
            "triadas_base_1000": list(triadas),
            "numero_tríadas": numero_tríadas,
            "iteraciones_lectura_decimal": intervalo_decimal.iteraciones,
            "anchura_intervalo_decimal": fraccion_json(intervalo_decimal.anchura),
        }

    # Control posterior independiente. Se carga únicamente después de haber
    # construido las tres ramas; no interviene en ningún prefijo emitido.
    control = json.loads(FINITE_R36_CONTROL.read_text(encoding="utf-8"))
    filas_r36 = control["selection"]["selected_R36"]["rows"]
    require(len(filas_r36) == 3, "el control R36 no contiene tres filas")
    indice_rol = {"cierre": 0, "propagacion": 1, "autoescala": 2}
    for rol in FUNCIONALES:
        bloques = control["selection"]["lifted_blocks"][rol]
        palabra_control = "".join(bloques) + filas_r36[indice_rol[rol]]
        palabra_generada = next(
            item["palabra"]
            for item in resultado[rol]["cilindros_ternarios"]
            if item["longitud"] == 36
        )
        require(len(palabra_control) == 36, "el control R36 no tiene 36 trits")
        require(palabra_generada == palabra_control, f"falló el control R36 de {rol}")
        resultado[rol]["control_posterior_R36"] = {
            "coincide": True,
            "palabra": palabra_control,
        }

    prefijos = [str(roles[rol]) for rol in sorted(roles)]
    require(codigo_sin_prefijos_literales(prefijos), "un prefijo raíz aparece escrito en la fuente")

    informe = {
        "esquema": "HMT.selector-global-orbital-funcional.v2",
        "estado": "PASS_SELECTOR_COINDUCTIVO_GLOBAL_DESDE_ORBITAS_Y_FUNCIONALES",
        "premisas": {
            "raices": (
                "selector orbital exhaustivo sobre 468 emisiones y 243 palabras, "
                "relativo al calibre orientador diag_c=6, ES"
            ),
            "cierre": "16 arctan(1/5)-4 arctan(1/239)",
            "propagacion": "suma desde k=0 hasta infinito de 1/k!",
            "autoescala": "raiz positiva de x^2-x-1",
            "lectura": "unico cilindro de base b que contiene un intervalo racional certificado",
        },
        "profundidad_arbitraria": True,
        "demostracion_de_totalidad": (
            "cada sucesión de intervalos es anidada, su anchura tiende a cero y, "
            "para todo nivel finito, acaba contenida en un único cilindro"
        ),
        "fuente_sin_prefijos_raiz_literales": True,
        "coincidencia_posterior_hasta_36_trits": True,
        "dependencias_generativas": [
            "catálogo APP/TPK finito y acción D3 certificada",
            "calibre orientador declarado diag_c=6, ES",
            "propiedades universales exactas de cierre, propagación y autoescala",
            "aritmética racional de intervalos y lectura cilíndrica",
        ],
        "entradas_excluidas_de_la_generacion": [
            "matrices calibradas L0 y L1",
            "prefijos ternarios o decimales objetivo",
            "estado U12 o sello K",
            "alpha o datos metrológicos",
        ],
        "selector_orbital_sha256": sha256(ROOT_CERTIFICATE.read_bytes()).hexdigest(),
        "control_R36_sha256": sha256(FINITE_R36_CONTROL.read_bytes()).hexdigest(),
        "resultado": resultado,
    }
    OUTPUT.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(informe["estado"])


if __name__ == "__main__":
    main()
