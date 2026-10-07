#!/usr/bin/env python3
"""Pruebas pequeñas del enlace carácter estructural -> evaluador.

La fixture procede del certificado sellado y se verifica por SHA-256. No se
reconstruye el catálogo completo, no se publican cifras y no se atribuye a esta
suite el alcance de la generación coinductiva general.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REVISION_ROOT = HERE.parent
SEALED_TESTS = (
    REVISION_ROOT
    / "00_BASE_SELLADA"
    / "01_FUENTE_SUCESORA"
    / "pruebas"
)
ORIGINAL = SEALED_TESTS / "verificar_generacion_infinita_nonadica.py"
SUCCESSOR = HERE / "verificar_generacion_infinita_nonadica.py"
SEALED_RECEIPT = SEALED_TESTS / "certificado_generacion_infinita_nonadica.json"

ORIGINAL_SHA256 = "6ec66d5b35d10edb658b4fa7c624c5d5206632f135fea5be9ec153c4027e6f73"
SEALED_RECEIPT_SHA256 = "2f538b991f7cdae6034be90a84e6621713eae97bc5172f369ecbff682be6408c"
TARGET_SCALE = 729**2


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"no se puede cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CharacterEvaluatorBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if sha256_file(ORIGINAL) != ORIGINAL_SHA256:
            raise RuntimeError("la fuente sellada original no coincide con su huella")
        if sha256_file(SEALED_RECEIPT) != SEALED_RECEIPT_SHA256:
            raise RuntimeError("el certificado sellado no coincide con su huella")

        cls.original = load_module("hmt_nonadic_original", ORIGINAL)
        cls.successor = load_module("hmt_nonadic_character_bound", SUCCESSOR)
        with SEALED_RECEIPT.open("r", encoding="utf-8") as handle:
            receipt = json.load(handle)
        if receipt.get("status") != (
            "PASS_HMT_GENERATED_CHARACTERS_AND_ARCHIMEDEAN_PROJECTIONS"
        ):
            raise RuntimeError("estado inesperado del certificado sellado")
        generated = receipt.get("generated_characters")
        if type(generated) is not dict:
            raise RuntimeError("el certificado no contiene caracteres tipados")
        cls.characters = {
            name: copy.deepcopy(generated[name]) for name in ("pi", "e", "phi")
        }

    def valid_characters(self) -> dict[str, dict[str, object]]:
        return copy.deepcopy(self.characters)

    def test_valid_fixture_preserves_original_bounds(self) -> None:
        characters = self.valid_characters()
        expected = self.original.evaluate_generated_characters(
            copy.deepcopy(characters), TARGET_SCALE
        )
        observed = self.successor.evaluate_generated_characters(
            characters, TARGET_SCALE
        )
        self.assertEqual(observed, expected)

    def test_portable_layout_resolves_only_inside_sealed_base(self) -> None:
        layout = self.successor.resolve_portable_layout()
        sealed_base = (REVISION_ROOT / "00_BASE_SELLADA").resolve(strict=True)
        project_root = layout["project_root"]
        source_root = layout["source_root"]
        self.assertEqual(
            layout["status"], "PASS_PORTABLE_RUNTIME_FROM_SEALED_RECEIPT"
        )
        self.assertEqual(layout["dependency_count"], 9)
        self.assertFalse(layout["external_paths_used"])
        self.assertFalse(layout["symlinks_used"])
        project_root.relative_to(sealed_base)
        source_root.relative_to(sealed_base)

    def test_e_recurrence_mutation_is_rejected(self) -> None:
        characters = self.valid_characters()
        characters["e"]["recurrence"] = "(n+2)*a_(n+1)=a_n"
        with self.assertRaisesRegex(RuntimeError, "recurrencia"):
            self.successor.evaluate_generated_characters(characters, TARGET_SCALE)

    def test_phi_incidence_polynomial_mismatch_is_rejected(self) -> None:
        characters = self.valid_characters()
        characters["phi"]["incidence"] = [[0, 1], [1, 2]]
        with self.assertRaisesRegex(RuntimeError, "incidencia"):
            self.successor.evaluate_generated_characters(characters, TARGET_SCALE)

    def test_required_character_fields_cannot_be_absent(self) -> None:
        required = {
            "e": ("kind", "normalization", "recurrence"),
            "phi": (
                "kind",
                "incidence",
                "characteristic_polynomial",
                "orientation",
            ),
        }
        for channel, fields in required.items():
            for field in fields:
                with self.subTest(channel=channel, field=field):
                    characters = self.valid_characters()
                    del characters[channel][field]
                    with self.assertRaises(RuntimeError):
                        self.successor.evaluate_generated_characters(
                            characters, TARGET_SCALE
                        )

    def test_incidence_and_polynomial_reject_coercible_nonintegers(self) -> None:
        mutations = (
            ("incidence", 0, 0, False),
            ("incidence", 0, 0, 0.0),
            ("incidence", 0, 0, "0"),
            ("characteristic_polynomial", None, 0, True),
            ("characteristic_polynomial", None, 0, 1.0),
            ("characteristic_polynomial", None, 0, "1"),
        )
        for field, row, column, bad_value in mutations:
            with self.subTest(field=field, value=repr(bad_value)):
                characters = self.valid_characters()
                if row is None:
                    characters["phi"][field][column] = bad_value
                else:
                    characters["phi"][field][row][column] = bad_value
                with self.assertRaises(RuntimeError):
                    self.successor.evaluate_generated_characters(
                        characters, TARGET_SCALE
                    )

    def test_target_scale_rejects_bool_and_float(self) -> None:
        e_character = self.valid_characters()["e"]
        phi_character = self.valid_characters()["phi"]
        for bad_scale in (True, 1.0):
            with self.subTest(e_scale=repr(bad_scale)):
                with self.assertRaisesRegex(RuntimeError, "escala objetivo"):
                    self.successor.propagation_bounds(e_character, bad_scale)
            with self.subTest(phi_scale=repr(bad_scale)):
                with self.assertRaisesRegex(RuntimeError, "escala objetivo"):
                    self.successor.autoscale_bounds(phi_character, bad_scale)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        CharacterEvaluatorBindingTests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("PASS_VALIDACION_CARACTERES_E_PHI_INTERFAZ")
