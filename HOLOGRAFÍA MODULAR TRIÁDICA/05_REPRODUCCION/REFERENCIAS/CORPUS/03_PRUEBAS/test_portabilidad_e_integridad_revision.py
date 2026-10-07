#!/usr/bin/env python3
"""Pruebas pequeñas: remapeo FLS y detección de alteración/ausencia."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REVISION_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se puede cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


source_audit = load_module("source_audit", REVISION_ROOT / "comprobar_lectura_fuentes.py")
integrity = load_module("integrity", REVISION_ROOT / "03_PRUEBAS" / "verificar_integridad_revision.py")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class SourceReadPortabilityTests(unittest.TestCase):
    def build_fixture(self, root: Path) -> Path:
        cwd_rel = Path("01_FUENTES/B/tree/manuscrito")
        output_rel = Path("02_PDF/B")
        base_rel = Path("00_BASE_SELLADA/original")
        for directory in (root / cwd_rel, root / output_rel, root / base_rel):
            directory.mkdir(parents=True, exist_ok=True)
        tex = b"\\documentclass{article}\n\\begin{document}x\\end{document}\n"
        bbl = b"\\begin{thebibliography}{1}\\end{thebibliography}\n"
        (root / base_rel / "main.tex").write_bytes(tex)
        (root / base_rel / "references.bbl").write_bytes(bbl)
        (root / cwd_rel / "main.tex").write_bytes(tex)
        (root / cwd_rel / "references.bbl").write_bytes(bbl)
        (root / output_rel / "references.bbl").write_bytes(bbl)
        old_root = Path("/old/compilation/location/REVISION_EDITORIAL_HMT_MD")
        (root / output_rel / "main.fls").write_text(
            "\n".join(
                [
                    f"PWD {old_root / cwd_rel}",
                    "INPUT main.tex",
                    f"INPUT {old_root / output_rel / 'references.bbl'}",
                    "INPUT /usr/local/texlive/2026/texmf-dist/tex/latex/base/article.cls",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        plan = [
            {
                "bundle": "B",
                "entrypoint": (cwd_rel / "main.tex").as_posix(),
                "cwd": cwd_rel.as_posix(),
                "output": output_rel.as_posix(),
            }
        ]
        provenance = [
            {
                "bundle": "B",
                "source": "original/main.tex",
                "source_sha256": digest(tex),
                "destination": (cwd_rel / "main.tex").as_posix(),
                "prepared_sha256": digest(tex),
            },
            {
                "bundle": "B",
                "source": "original/references.bbl",
                "source_sha256": digest(bbl),
                "destination": (cwd_rel / "references.bbl").as_posix(),
                "prepared_sha256": digest(bbl),
            },
        ]
        (root / "PLAN_COMPILACION.json").write_text(json.dumps(plan), encoding="utf-8")
        (root / "PROCEDENCIA_FUENTES.json").write_text(json.dumps(provenance), encoding="utf-8")
        (root / "04_CONTROL").mkdir()
        (root / "04_CONTROL" / "RECIBO_CONSERVACION.json").write_text(
            json.dumps(
                {
                    "scope": "fixture",
                    "checked_dependencies": len(provenance),
                    "substantively_modified_sources": [],
                    "protected_sources": [],
                    "errors": [],
                    "status": "PASS_CONSERVACION_DOCUMENTAL",
                }
            ),
            encoding="utf-8",
        )
        (root / "RECIBO_RUTAS_RELATIVAS.json").write_text("[]\n", encoding="utf-8")
        return root / cwd_rel / "main.tex"

    def test_remaps_recorded_root_without_basename_search(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "moved_revision"
            self.build_fixture(root)
            result = source_audit.audit_revision(root)
            self.assertEqual(result["status"], "PASS")
            bundle = result["bundles"][0]
            self.assertEqual(bundle["relocation"], "REMAPPED")
            self.assertEqual((bundle["read"], bundle["expected"]), (2, 2))
            self.assertEqual(bundle["bibliography_errors"], [])

    def test_detects_prepared_source_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "moved_revision"
            target = self.build_fixture(root)
            target.write_text("altered\n", encoding="utf-8")
            result = source_audit.audit_revision(root)
            self.assertEqual(result["status"], "FAIL")
            errors = {item["error"] for item in result["bundles"][0]["source_integrity_errors"]}
            self.assertIn("current_hash_mismatch_after_declared_changes", errors)

    def test_accepts_only_an_explicit_hash_chained_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "moved_revision"
            target = self.build_fixture(root)
            changed = b"declared editorial change\n"
            target.write_bytes(changed)
            provenance = json.loads((root / "PROCEDENCIA_FUENTES.json").read_text(encoding="utf-8"))
            receipt_path = root / "04_CONTROL" / "RECIBO_CONSERVACION.json"
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["substantively_modified_sources"] = [
                {
                    "path": provenance[0]["destination"],
                    "base_source": provenance[0]["source"],
                    "base_sha256": provenance[0]["prepared_sha256"],
                    "current_sha256": digest(changed),
                }
            ]
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            result = source_audit.audit_revision(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["declared_change_evidence"]["substantive_changes"], 1)

    def test_accepts_only_an_explicit_relative_path_hash_transition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "moved_revision"
            target = self.build_fixture(root)
            provenance = json.loads((root / "PROCEDENCIA_FUENTES.json").read_text(encoding="utf-8"))
            before = b"include /old/root/file.tex\n"
            changed = b"include ../../file.tex\n"
            source = root / "00_BASE_SELLADA" / provenance[0]["source"]
            source.write_bytes(before)
            target.write_bytes(changed)
            provenance[0]["source_sha256"] = digest(before)
            provenance[0]["prepared_sha256"] = digest(before)
            (root / "PROCEDENCIA_FUENTES.json").write_text(json.dumps(provenance), encoding="utf-8")
            (root / "RECIBO_RUTAS_RELATIVAS.json").write_text(
                json.dumps(
                    [
                        {
                            "path": provenance[0]["destination"],
                            "before_sha256": digest(before),
                            "after_sha256": digest(changed),
                            "old_prefix": "/old/root/",
                            "new_prefix": "../../",
                            "replacement_count": 1,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            result = source_audit.audit_revision(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["declared_change_evidence"]["relative_path_changes"], 1)


class IntegrityManifestTests(unittest.TestCase):
    def make_manifest(self, base: Path, data: bytes = b"stable\n") -> tuple[Path, Path]:
        payload = base / "payload"
        payload.mkdir(parents=True)
        tracked = payload / "tracked.txt"
        tracked.write_bytes(data)
        manifest = base / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema": integrity.SCHEMA,
                    "scope": integrity.SCOPE,
                    "artifact_class": integrity.ARTIFACT_CLASS,
                    "publication_status": integrity.PUBLICATION_STATUS,
                    "mathematical_universal_claims": integrity.MATHEMATICAL_CLAIMS_STATUS,
                    "computational_regression": integrity.COMPUTATIONAL_REGRESSION_SCOPE,
                    "seal_state": integrity.SEALED_STATE,
                    "compilation_complete": True,
                    "root": "payload",
                    "hash_algorithm": "sha256",
                    "entries": [
                        {
                            "path": "tracked.txt",
                            "size": len(data),
                            "sha256": digest(data),
                            "role": "fixture",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest, tracked

    def test_detects_altered_and_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, tracked = self.make_manifest(Path(directory))
            self.assertEqual(integrity.verify_manifest(manifest)["status"], "PASS_FILE_INTEGRITY")
            tracked.write_bytes(b"changed\n")
            changed = integrity.verify_manifest(manifest)
            self.assertEqual(changed["status"], "FAIL_FILE_INTEGRITY")
            self.assertEqual(changed["altered"][0]["path"], "tracked.txt")
            tracked.unlink()
            missing = integrity.verify_manifest(manifest)
            self.assertEqual(missing["status"], "FAIL_FILE_INTEGRITY")
            self.assertEqual(missing["missing"], ["tracked.txt"])

    def test_rejects_unconfined_path_and_bool_size(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, _ = self.make_manifest(Path(directory))
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["entries"][0]["path"] = "../escape"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(integrity.ManifestError):
                integrity.verify_manifest(manifest)
            data["entries"][0]["path"] = "tracked.txt"
            data["entries"][0]["size"] = True
            manifest.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(integrity.ManifestError):
                integrity.verify_manifest(manifest)

    def test_draft_template_cannot_pass(self) -> None:
        result = integrity.verify_manifest(REVISION_ROOT / "MANIFIESTO_INTEGRIDAD_REVISION_PLANTILLA.json")
        self.assertEqual(result["status"], "HOLD_NOT_SEALED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
