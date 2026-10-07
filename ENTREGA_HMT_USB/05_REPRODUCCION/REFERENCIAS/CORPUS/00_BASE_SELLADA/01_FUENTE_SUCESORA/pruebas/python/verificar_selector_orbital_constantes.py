#!/usr/bin/env python3
"""Certifica el selector orbital finito de las palabras de pi, e y phi.

La prueba usa exclusivamente el catalogo TPK publicado.  No consulta la
carta arquimediana L0/L1, cifras de pi/e/phi, alpha, CODATA ni el ledger
dodecafasico.  Separa dos operaciones:

1. seleccion intrinseca de tres orbitas del catalogo bajo una accion D3;
2. eleccion de un representante orientado mediante el gauge declarado
   ``diag_c = 6`` y ``hplus_type = ES``.

El segundo paso no selecciona una region concreta de la microfibra de pi:
selecciona solamente la palabra orientada.  El certificado tampoco demuestra
que la posterior carta arquimediana sea independiente ni que exista un emisor
infinito target-free de las expansiones reales.

El programa usa comprobaciones no optimizables y se ejecuta de la misma forma
con ``-O``.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
CATALOG_JSON = ROOT / "datos/TPK_U_catalog_468.json"
CATALOG_CSV = ROOT / "datos/catalogo_lector_arquimediano.csv"
OUTPUT = ROOT / "certificados/selector_orbital_constantes.json"

# r(abc|def)=cab|efd y s(abc|def)=def|abc.
R_PERMUTATION = (2, 0, 1, 4, 5, 3)
S_PERMUTATION = (3, 4, 5, 0, 1, 2)

EXPECTED_PI_ORBIT = (
    "001112",
    "010211",
    "100121",
    "112001",
    "121100",
    "211010",
)
EXPECTED_E_ORBIT = (
    "011120",
    "012110",
    "101201",
    "110012",
    "120011",
    "201101",
)
EXPECTED_PHI_ORBIT = (
    "002112",
    "020211",
    "112002",
    "121200",
    "200121",
    "211020",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_u6(value: str) -> tuple[int, ...]:
    parts = tuple(int(item) for item in value.split("|"))
    require(len(parts) == 6, f"U6 no tiene seis coordenadas: {value}")
    require(all(0 <= item < 1000 for item in parts), f"U6 fuera de base mil: {value}")
    return parts


def serialize_u6(u6: Sequence[int]) -> str:
    return "|".join(str(item) for item in u6)


def psi(u6: Sequence[int]) -> str:
    return "".join(str((-item) % 3) for item in u6)


def permute(values: Sequence[object], permutation: Sequence[int]) -> tuple[object, ...]:
    return tuple(values[index] for index in permutation)


def permute_word(word: str, permutation: Sequence[int]) -> str:
    require(len(word) == 6 and set(word) <= {"0", "1", "2"}, f"palabra invalida: {word}")
    return "".join(word[index] for index in permutation)


def rotate_word(word: str) -> str:
    return permute_word(word, R_PERMUTATION)


def swap_word(word: str) -> str:
    return permute_word(word, S_PERMUTATION)


def word_orbit(word: str) -> tuple[str, ...]:
    orbit: set[str] = set()
    current = word
    for _ in range(3):
        orbit.add(current)
        orbit.add(swap_word(current))
        current = rotate_word(current)
    return tuple(sorted(orbit))


def trit_census(word: str) -> tuple[int, int, int]:
    return tuple(word.count(str(digit)) for digit in range(3))  # type: ignore[return-value]


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "fraction": f"{value.numerator}/{value.denominator}",
    }


def same_census_on_orbit(orbit: Iterable[str]) -> tuple[int, int, int]:
    censuses = {trit_census(word) for word in orbit}
    require(len(censuses) == 1, f"el censo tritico cambia en la orbita: {sorted(censuses)}")
    return next(iter(censuses))


def main() -> None:
    for path in (CATALOG_JSON, CATALOG_CSV):
        require(path.is_file(), f"falta el dato local {path}")

    raw = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    require(isinstance(raw, list), "el catalogo JSON no es una lista")
    require(len(raw) == 468, "el catalogo JSON no contiene 468 emisiones")

    required_fields = {
        "U6",
        "count",
        "diag_c",
        "hplus_type",
        "px_size",
        "px_res_type",
        "Esig",
    }
    rows: list[dict[str, object]] = []
    by_u6: dict[tuple[int, ...], dict[str, object]] = {}
    fibers: dict[str, list[dict[str, object]]] = defaultdict(list)
    for position, item in enumerate(raw):
        require(isinstance(item, dict), f"fila JSON {position} no es un objeto")
        require(required_fields <= set(item), f"faltan campos en la fila JSON {position}")
        u6 = parse_u6(str(item["U6"]))
        require(u6 not in by_u6, f"U6 duplicado: {serialize_u6(u6)}")
        count = int(item["count"])
        require(count > 0, f"multiplicidad no positiva: {serialize_u6(u6)}")
        row = {
            **item,
            "u6_tuple": u6,
            "count_int": count,
            "diag_c_int": int(item["diag_c"]),
            "word": psi(u6),
        }
        rows.append(row)
        by_u6[u6] = row
        fibers[str(row["word"])].append(row)

    require(len(by_u6) == 468, "los U6 no son distintos")
    require(len(fibers) == 243, "la proyeccion Psi no tiene 243 palabras")
    require(sum(int(row["count_int"]) for row in rows) == 104_976, "censo de semillas")
    multiplicity_histogram = Counter(int(row["count_int"]) for row in rows)
    require(
        multiplicity_histogram == Counter({144: 432, 432: 18, 1944: 18}),
        "histograma de multiplicidades",
    )

    with CATALOG_CSV.open(encoding="utf-8", newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    require(len(csv_rows) == 468, "el catalogo CSV no contiene 468 emisiones")
    csv_map: dict[tuple[int, ...], tuple[int, str]] = {}
    for item in csv_rows:
        u6 = parse_u6(item["U6"])
        require(u6 not in csv_map, f"U6 duplicado en CSV: {serialize_u6(u6)}")
        csv_map[u6] = (int(item["count"]), item["w6"])
    json_map = {
        u6: (int(row["count_int"]), str(row["word"]))
        for u6, row in by_u6.items()
    }
    require(csv_map == json_map, "los catalogos JSON y CSV no coinciden")

    # La accion definida por r y s debe cerrar tanto en U6 como en W6 y
    # preservar la multiplicidad de semillas.
    for row in rows:
        u6 = row["u6_tuple"]
        require(isinstance(u6, tuple), "U6 interno mal tipado")
        r_u6 = permute(u6, R_PERMUTATION)
        s_u6 = permute(u6, S_PERMUTATION)
        require(r_u6 in by_u6 and s_u6 in by_u6, "la accion D3 no cierra en U6")
        require(
            int(by_u6[r_u6]["count_int"]) == int(row["count_int"])
            and int(by_u6[s_u6]["count_int"]) == int(row["count_int"]),
            "la accion D3 no preserva multiplicidades",
        )
        require(permute(permute(permute(u6, R_PERMUTATION), R_PERMUTATION), R_PERMUTATION) == u6,
                "r^3 no es la identidad en U6")
        require(permute(permute(u6, S_PERMUTATION), S_PERMUTATION) == u6,
                "s^2 no es la identidad en U6")
        srs_u6 = permute(permute(permute(u6, S_PERMUTATION), R_PERMUTATION), S_PERMUTATION)
        rr_u6 = permute(permute(u6, R_PERMUTATION), R_PERMUTATION)
        require(srs_u6 == rr_u6, "srs no coincide con r^{-1} en U6")
        require(psi(r_u6) == rotate_word(str(row["word"])), "Psi no es r-equivariante")
        require(psi(s_u6) == swap_word(str(row["word"])), "Psi no es s-equivariante")

    for word in fibers:
        require(rotate_word(rotate_word(rotate_word(word))) == word, "r^3 en W6")
        require(swap_word(swap_word(word)) == word, "s^2 en W6")
        require(
            swap_word(rotate_word(swap_word(word))) == rotate_word(rotate_word(word)),
            "srs=r^{-1} en W6",
        )

    orbits = sorted({word_orbit(word) for word in fibers})
    orbit_size_histogram = Counter(len(orbit) for orbit in orbits)
    require(len(orbits) == 43, "el cociente W6/D3 no tiene 43 orbitas")
    require(orbit_size_histogram == Counter({6: 38, 3: 5}), "tamano de orbitas D3")

    def fiber_size(word: str) -> int:
        return len(fibers[word])

    def seed_mass(word: str) -> int:
        return sum(int(row["count_int"]) for row in fibers[word])

    def simple_minimal_orbit(orbit: Sequence[str]) -> bool:
        return len(orbit) == 6 and all(
            fiber_size(word) == 1 and int(fibers[word][0]["count_int"]) == 144
            for word in orbit
        )

    def diagonal_support(orbit: Sequence[str]) -> set[int]:
        return {
            int(row["diag_c_int"])
            for word in orbit
            for row in fibers[word]
        }

    # Seleccion de pi: propiedad de orbita, no de una etiqueta nombrada.
    pi_candidates = [
        orbit
        for orbit in orbits
        if len(orbit) == 6
        and all(
            fiber_size(word) == 5
            and seed_mass(word) == 1008
            and sorted(int(row["count_int"]) for row in fibers[word])
            == [144, 144, 144, 144, 432]
            for word in orbit
        )
    ]
    require(len(pi_candidates) == 1, "la condicion orbital de pi no es unica")
    pi_orbit = pi_candidates[0]
    pi_census = same_census_on_orbit(pi_orbit)

    # Sector singleton radical: fibras minimas y soporte diagonal 0-3-6.
    radical_singleton_orbits = [
        orbit
        for orbit in orbits
        if simple_minimal_orbit(orbit) and diagonal_support(orbit) == {0, 3, 6}
    ]
    require(len(radical_singleton_orbits) == 6, "censo del sector singleton radical")

    # e conserva el censo tritico orientado de la orbita de pi.
    e_candidates = [
        orbit
        for orbit in radical_singleton_orbits
        if same_census_on_orbit(orbit) == pi_census
    ]
    require(len(e_candidates) == 1, "la condicion orbital de e no es unica")
    e_orbit = e_candidates[0]

    # phi es la unica orbita equilibrada del mismo sector: dos 0, dos 1 y dos 2.
    phi_candidates = [
        orbit
        for orbit in radical_singleton_orbits
        if same_census_on_orbit(orbit) == (2, 2, 2)
    ]
    require(len(phi_candidates) == 1, "la condicion orbital de phi no es unica")
    phi_orbit = phi_candidates[0]

    # Control: sin la condicion diagonal radical quedan cuatro candidatos
    # singleton equilibrados; la condicion 0-3-6 es realmente selectiva.
    phi_candidates_without_radical = [
        orbit
        for orbit in orbits
        if simple_minimal_orbit(orbit) and same_census_on_orbit(orbit) == (2, 2, 2)
    ]
    require(len(phi_candidates_without_radical) == 4, "control negativo de phi")

    # El gauge rompe la simetria de orbita y escoge una palabra. No escoge
    # una de las cinco regiones U6 de pi.
    def gauge_matches(orbit: Sequence[str]) -> list[str]:
        return [
            word
            for word in orbit
            if any(
                int(row["diag_c_int"]) == 6 and str(row["hplus_type"]) == "ES"
                for row in fibers[word]
            )
        ]

    pi_gauge_matches = gauge_matches(pi_orbit)
    e_gauge_matches = gauge_matches(e_orbit)
    phi_gauge_matches = gauge_matches(phi_orbit)
    require(len(pi_gauge_matches) == 1, "el gauge no orienta unicamente pi")
    require(len(e_gauge_matches) == 1, "el gauge no orienta unicamente e")
    require(len(phi_gauge_matches) == 1, "el gauge no orienta unicamente phi")
    pi_word = pi_gauge_matches[0]
    e_word = e_gauge_matches[0]
    phi_word = phi_gauge_matches[0]

    pi_gauge_emissions = [
        row
        for row in fibers[pi_word]
        if int(row["diag_c_int"]) == 6 and str(row["hplus_type"]) == "ES"
    ]
    require(len(pi_gauge_emissions) == 3, "el gauge deberia conservar tres regiones positivas de pi")

    # Testigos de regresion: las propiedades deben recuperar las palabras
    # publicadas, pero esas cadenas no intervienen en los predicados selectores.
    require(pi_orbit == EXPECTED_PI_ORBIT, "regresion en la orbita de pi")
    require(e_orbit == EXPECTED_E_ORBIT, "regresion en la orbita de e")
    require(phi_orbit == EXPECTED_PHI_ORBIT, "regresion en la orbita de phi")
    require(pi_word == "010211", "regresion en el gauge de pi")
    require(e_word == "201101", "regresion en el gauge de e")
    require(phi_word == "121200", "regresion en el gauge de phi")

    def orbit_emission_mass(orbit: Sequence[str]) -> Fraction:
        return Fraction(sum(fiber_size(word) for word in orbit), 468)

    def orbit_seed_mass(orbit: Sequence[str]) -> Fraction:
        return Fraction(sum(seed_mass(word) for word in orbit), 104_976)

    result = {
        "schema": "HMT.selector-orbital-constantes.v1",
        "status": "PASS_FINITE_INTERNAL_ORBIT_SELECTION_RELATIVE_TO_GAUGE",
        "source_hashes": {
            CATALOG_JSON.relative_to(ROOT).as_posix(): sha256(CATALOG_JSON),
            CATALOG_CSV.relative_to(ROOT).as_posix(): sha256(CATALOG_CSV),
        },
        "catalogue": {
            "emissions": len(rows),
            "visible_words": len(fibers),
            "weighted_seeds": sum(int(row["count_int"]) for row in rows),
            "emission_multiplicity_histogram": {
                str(key): value for key, value in sorted(multiplicity_histogram.items())
            },
            "json_csv_agree": True,
        },
        "D3_catalogue_action": {
            "r_on_words": "abc|def -> cab|efd",
            "s_on_words": "abc|def -> def|abc",
            "relations": ["r^3=1", "s^2=1", "srs=r^-1"],
            "preserves": ["U6 catalogue", "Psi projection", "seed multiplicity"],
            "word_orbits": len(orbits),
            "orbit_size_histogram": {
                str(key): value for key, value in sorted(orbit_size_histogram.items())
            },
            "logical_scope": (
                "The explicit action is verified on the complete finite catalogue; "
                "uniqueness among all possible catalogue automorphism actions is not claimed."
            ),
        },
        "orbit_selection": {
            "pi": {
                "predicate": (
                    "unique D3 orbit whose six words each have five U6 lifts, "
                    "seed mass 1008 and multiplicities 432+4*144"
                ),
                "orbit": list(pi_orbit),
                "trit_census_n0_n1_n2": list(pi_census),
            },
            "radical_singleton_sector": {
                "predicate": (
                    "D3 orbit of length six; one U6 lift of multiplicity 144 per word; "
                    "additive diagonal support exactly {0,3,6}"
                ),
                "orbit_count": len(radical_singleton_orbits),
                "representatives": [orbit[0] for orbit in radical_singleton_orbits],
            },
            "e": {
                "predicate": (
                    "unique radical singleton orbit with the same ordered trit census "
                    "as the pi orbit"
                ),
                "orbit": list(e_orbit),
                "trit_census_n0_n1_n2": list(same_census_on_orbit(e_orbit)),
            },
            "phi": {
                "predicate": "unique balanced radical singleton orbit with census (2,2,2)",
                "orbit": list(phi_orbit),
                "trit_census_n0_n1_n2": list(same_census_on_orbit(phi_orbit)),
            },
        },
        "orientation_gauge": {
            "clause": "a word has at least one U6 lift with diag_c=6 and hplus_type=ES",
            "role": "selects one oriented word inside each already selected D3 orbit",
            "pi_word": pi_word,
            "e_word": e_word,
            "phi_word": phi_word,
            "pi_U6_lifts_surviving_gauge": [
                serialize_u6(row["u6_tuple"])  # type: ignore[arg-type]
                for row in pi_gauge_emissions
            ],
            "pi_lifts_surviving_gauge_count": len(pi_gauge_emissions),
            "warning": (
                "The gauge orients the word but does not choose one of the five pi regions; "
                "three positive pi lifts remain."
            ),
        },
        "finite_priority_measures": {
            "interpretation": (
                "These are masses of catalogue words/orbits, not probabilities assigned "
                "to real numbers in R."
            ),
            "oriented_words_uniform_on_468_emissions": {
                "pi": fraction_record(Fraction(fiber_size(pi_word), 468)),
                "e": fraction_record(Fraction(fiber_size(e_word), 468)),
                "phi": fraction_record(Fraction(fiber_size(phi_word), 468)),
            },
            "oriented_words_pushforward_of_uniform_seeds": {
                "pi": fraction_record(Fraction(seed_mass(pi_word), 104_976)),
                "e": fraction_record(Fraction(seed_mass(e_word), 104_976)),
                "phi": fraction_record(Fraction(seed_mass(phi_word), 104_976)),
            },
            "D3_orbits_uniform_on_468_emissions": {
                "pi": fraction_record(orbit_emission_mass(pi_orbit)),
                "e": fraction_record(orbit_emission_mass(e_orbit)),
                "phi": fraction_record(orbit_emission_mass(phi_orbit)),
            },
            "D3_orbits_pushforward_of_uniform_seeds": {
                "pi": fraction_record(orbit_seed_mass(pi_orbit)),
                "e": fraction_record(orbit_seed_mass(e_orbit)),
                "phi": fraction_record(orbit_seed_mass(phi_orbit)),
            },
        },
        "negative_controls": {
            "pi_word_candidates_before_D3_quotient": len(pi_orbit),
            "phi_balanced_singleton_candidates_without_radical_support": len(
                phi_candidates_without_radical
            ),
            "orientations_before_gauge_per_selected_orbit": {
                "pi": len(pi_orbit),
                "e": len(e_orbit),
                "phi": len(phi_orbit),
            },
            "pi_regions_after_word_gauge": len(fibers[pi_word]),
            "pi_positive_regions_after_word_gauge": len(pi_gauge_emissions),
        },
        "dependency_statement": {
            "proved": (
                "The finite catalogue intrinsically selects three D3 orbits; the declared "
                "diag_c=6, ES gauge then selects the published oriented words."
            ),
            "declared_premises": [
                "the active 468-row target-free APP/TPK finite catalogue and its typed metadata",
                "the fixed TRIT labelling Psi(U)=(-U mod 3) and the published 3+3 coordinate split",
                "the explicit coordinate action r,s used to form D3_catalogue",
                "the orientation gauge diag_c=6 and hplus_type=ES",
            ],
            "not_used": [
                "L0 or L1",
                "decimal digits or analytic definitions of pi, e or phi",
                "alpha or CODATA",
                "signed U12 or the seal K",
            ],
            "still_not_proved": [
                "an APP-min derivation of the calibrated Archimedean reader L0/L1",
                "a target-free coinductive emitter of the complete infinite expansions",
                "that the gauge is forced uniquely rather than declared as an orientation convention",
                "a target-free realization of the signed U12/K state",
            ],
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS_SELECTOR_ORBITAL_CONSTANTES")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
