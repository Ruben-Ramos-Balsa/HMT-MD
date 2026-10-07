#!/usr/bin/env python3
"""Lectura OOXML y auditoría del registro direccional TPK de 108 pasos.

El libro se trata como fuente histórica de sólo lectura. El análisis construye
primero invariantes que no dependen del sello dodecafásico y relega cualquier
comparación con K a una sección de contraste posterior.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
BOOK = ROOT / (
    "02_LECTURA/ingesta_usuario_2026-07-19_enero_stale/EXTRACTED/"
    "2026-01-14/14-enero-26/rutas_TPK_108_APP9x9.xlsx"
)
BOOK_ALIAS = BOOK.with_name("rutas_TPK_108_APP9x9-1.xlsx")
CURRENT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"
CERTIFICATE = Path(__file__).resolve().parent / "RESULTADO_REGISTRO_DIRECCIONAL_108.json"

NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
SHEET_NAMES = ("Summary", "N", "E", "S", "O")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    import hashlib

    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def column_index(cell_reference: str) -> int:
    letters = re.match(r"[A-Z]+", cell_reference)
    require(letters is not None, "referencia de celda inválida")
    value = 0
    for letter in letters.group(0):
        value = 26 * value + ord(letter) - 64
    return value - 1


def parse_sheet(archive: zipfile.ZipFile, number: int) -> list[list[object]]:
    root = ET.fromstring(archive.read(f"xl/worksheets/sheet{number}.xml"))
    rows: list[list[object]] = []
    for row in root.findall("x:sheetData/x:row", NS):
        cells = row.findall("x:c", NS)
        if not cells:
            rows.append([])
            continue
        width = max(column_index(str(cell.attrib["r"])) for cell in cells) + 1
        values: list[object] = [None] * width
        for cell in cells:
            index = column_index(str(cell.attrib["r"]))
            cell_type = cell.attrib.get("t", "n")
            if cell_type == "inlineStr":
                texts = cell.findall(".//x:t", NS)
                values[index] = "".join(text.text or "" for text in texts)
            else:
                node = cell.find("x:v", NS)
                raw = "" if node is None else node.text or ""
                if cell_type == "b":
                    values[index] = raw == "1"
                else:
                    number_value = float(raw)
                    values[index] = int(number_value) if number_value.is_integer() else number_value
        rows.append(values)
    return rows


def load_book() -> dict[str, list[dict[str, object]]]:
    with zipfile.ZipFile(BOOK) as archive:
        output: dict[str, list[dict[str, object]]] = {}
        for number, name in enumerate(SHEET_NAMES, start=1):
            rows = parse_sheet(archive, number)
            require(rows, f"hoja vacía: {name}")
            headers = [str(value) for value in rows[0]]
            output[name] = [dict(zip(headers, row)) for row in rows[1:]]
    return output


def window_sums(rows: list[dict[str, object]], size: int) -> list[dict[str, object]]:
    require(len(rows) % size == 0, "la longitud no es divisible por la ventana")
    numeric_fields = ("delta(t)", "moved?", "i", "j", "APP_plus", "APP_times", "d_lex", "tau(i+j mod3)", "tau_digit")
    result: list[dict[str, object]] = []
    for index in range(0, len(rows), size):
        block = rows[index:index + size]
        record: dict[str, object] = {
            "window": index // size + 1,
            "t_range": [int(block[0]["t"]), int(block[-1]["t"])],
            "heading_start": block[0]["heading"],
            "heading_end": block[-1]["heading"],
        }
        for field in numeric_fields:
            record[f"sum_{field}"] = sum(int(row[field]) for row in block)
        record["APP_plus_word_mod3"] = "".join(str(int(row["APP_plus"]) % 3) for row in block)
        record["APP_times_word_mod3"] = "".join(str(int(row["APP_times"]) % 3) for row in block)
        record["d_lex_word_mod3"] = "".join(str(int(row["d_lex"]) % 3) for row in block)
        record["tau_digit_word"] = "".join(str(int(row["tau_digit"])) for row in block)
        result.append(record)
    return result


def hadamard4(values: list[int]) -> list[int]:
    require(len(values) == 4, "H4 requiere cuatro direcciones")
    matrix = (
        (1, 1, 1, 1),
        (1, 1, -1, -1),
        (1, -1, 1, -1),
        (1, -1, -1, 1),
    )
    return [sum(coefficient * value for coefficient, value in zip(row, values)) for row in matrix]


def period_certificate(data: dict[str, list[dict[str, object]]]) -> dict[str, object]:
    """Prueba la repetición de 54 pasos sin usar K ni ninguna constante."""
    comparisons = 0
    fields_by_direction: dict[str, list[str]] = {}
    for direction in "NESO":
        rows = data[direction]
        fields = [field for field in rows[0] if field != "t"]
        fields_by_direction[direction] = fields
        for index in range(54):
            for field in fields:
                require(
                    rows[index][field] == rows[index + 54][field],
                    f"se rompió la periodicidad 54 en {direction}, t={index + 1}, campo={field}",
                )
                comparisons += 1
    return {
        "period_in_steps": 54,
        "period_in_nine_step_windows": 6,
        "directions": list("NESO"),
        "fields_compared_excluding_absolute_time": fields_by_direction,
        "exact_field_comparisons": comparisons,
        "statement": (
            "Para cada dirección y cada campo distinto del tiempo absoluto, "
            "R_d(t+54)=R_d(t), t=1,...,54."
        ),
    }


def h4_windows(windows9: dict[str, list[dict[str, object]]]) -> dict[str, object]:
    fields = ("sum_APP_plus", "sum_APP_times", "sum_i", "sum_j", "sum_d_lex")
    output: dict[str, object] = {}
    for field in fields:
        rows: list[dict[str, object]] = []
        for phase in range(12):
            values = [int(windows9[direction][phase][field]) for direction in "NESO"]
            rows.append({
                "phase_one_based": phase + 1,
                "NESO": values,
                "H4": hadamard4(values),
            })
        require(
            all(rows[index]["H4"] == rows[index + 6]["H4"] for index in range(6)),
            f"la carta H4 dejó de tener período seis para {field}",
        )
        output[field] = rows
    return output


def posterior_contrast(current: dict[str, object]) -> dict[str, object]:
    """Contraste posterior: no interviene en la prueba de periodicidad."""
    state_types = current["state_types"]
    seal = [int(value) for value in state_types["CanonicalSealK"]["coordinates"]]
    signed = [int(value) for value in state_types["SignedDodecaphaseState"]["coordinates"]]
    require(len(seal) == len(signed) == 12, "objetos dodecafásicos mal tipados")
    seal_pairs = [[seal[index], seal[index + 6]] for index in range(6)]
    signed_pairs = [[signed[index], signed[index + 6]] for index in range(6)]
    require(all(a != b for a, b in seal_pairs), "K se volvió periódico de período seis")
    require(all(a != b for a, b in signed_pairs), "U12 firmado se volvió periódico de período seis")
    return {
        "performed_after_the_rule_is_fixed": True,
        "K_pairs_phase_m_and_m_plus_6": seal_pairs,
        "U12_signed_pairs_phase_m_and_m_plus_6": signed_pairs,
        "K_is_not_periodic_with_period_6": True,
        "U12_signed_is_not_periodic_with_period_6": True,
    }


def build() -> dict[str, object]:
    require(digest(BOOK) == digest(BOOK_ALIAS), "los dos libros dejaron de ser duplicados exactos")
    data = load_book()
    require(len(data["Summary"]) == 4, "resumen direccional alterado")
    for direction in "NESO":
        require(len(data[direction]) == 108, f"{direction} no tiene 108 pasos")
        require(sum(bool(row["moved?"]) for row in data[direction]) == 36,
                f"{direction} no tiene 36 movimientos")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current["revision"] == "2026-07-22.2", "revisión canónica inesperada")
    windows9 = {direction: window_sums(data[direction], 9) for direction in "NESO"}
    windows27 = {direction: window_sums(data[direction], 27) for direction in "NESO"}
    return {
        "schema": "HMT.directional-108-period-obstruction.v1",
        "status": "PASS_LECTURA_OOXML_DIRECCIONAL",
        "source_status": "STALE_PRECANONICO_NO_NORMATIVO; cantera de rutas",
        "current_revision": current["revision"],
        "authors": ["Oumar Haidara Fall", "Rubén Ramos Balsa"],
        "book_sha256": digest(BOOK),
        "duplicate_is_byte_identical": True,
        "source_sha256": {
            relative(CURRENT): digest(CURRENT),
            relative(BOOK): digest(BOOK),
            relative(BOOK_ALIAS): digest(BOOK_ALIAS),
        },
        "summary": data["Summary"],
        "exact_periodicity": period_certificate(data),
        "windows_9": windows9,
        "windows_27": windows27,
        "directional_H4_by_nine_step_window": h4_windows(windows9),
        "no_go_theorem": {
            "domain": (
                "lectores deterministas, locales por ventana y equivariantes por traslación, "
                "que sólo reciben los campos publicados del registro N/E/S/O"
            ),
            "proof": (
                "Las ventanas m y m+6 son idénticas en todos los campos disponibles. "
                "Todo lector de ese dominio satisface F(W_m)=F(W_{m+6}); su salida tiene período seis."
            ),
            "conclusion": (
                "El registro direccional publicado no basta para producir un estado dodecafásico "
                "no periódico. Hace falta memoria de rama, orientación enriquecida, supervivencia "
                "o un dato equivalente que no sobreviva en esta proyección."
            ),
            "does_not_forbid": (
                "un lector del estado TPK completo; tampoco un lector que reciba memoria adicional "
                "o el índice absoluto, aunque este último requiere justificar su naturalidad"
            ),
        },
        "posterior_contrast_not_used_for_selection": posterior_contrast(current),
        "provenance": {
            "architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE: cuatro rutas N/E/S/O y 108 pasos",
            "certificate": "CERTIFICADO_NUEVO: repetición exacta de 54 pasos y obstrucción de período seis",
            "status": "EXACTO_INTERNO relativo al libro histórico publicado; no promueve el libro al canon",
        },
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--check-certificate", action="store_true")
    args = parser.parse_args(argv)
    text = render(build())
    if args.write_certificate:
        CERTIFICATE.write_text(text, encoding="utf-8")
    if args.check_certificate:
        require(CERTIFICATE.exists(), "falta el certificado congelado")
        require(CERTIFICATE.read_text(encoding="utf-8") == text, "el certificado congelado no coincide")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
