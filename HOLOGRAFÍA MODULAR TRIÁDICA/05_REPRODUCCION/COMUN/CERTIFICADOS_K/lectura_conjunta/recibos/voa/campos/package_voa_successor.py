#!/usr/bin/env python3
"""Prepare the immutable-source Article I algebraic continuation package.

This is a packaging program, not a proof or compilation certificate. It is
deliberately separate from reproducir_voa.py, which compiles the declared
source closure and reports the actual theorem dependencies.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent
PROJECT = OUTPUT.parent
BASE = OUTPUT / "PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA"
DEFAULT_DESTINATION = OUTPUT / "PAQUETE_ARTICULO_I_CONTINUACION_VOA_20260918"
FORMAL = OUTPUT / "AMPLIACION_FORMAL_LEAN_SERIE_20260916"
FOUNDATION = Path("/Users/ruben/Documents/ChatGPT/jueces y controles/"
                  "CIERRE_ARTICULO_I_20260917/FoundationContract")

RECOVERED = {
    "WittPairingParity": "iv_lattice_cocycle",
    "IntegralBasisParity": "iv_lattice_cocycle",
    "TriangularSignCocycle": "iv_lattice_cocycle",
    "WittLatticeCocycle": "iv_lattice_cocycle",
    "WittCentralExtension": "iv_twisted_group_algebra",
    "WittTwistedAlgebra": "iv_twisted_group_algebra",
    "WittComplexAlgebra": "iv_twisted_group_algebra",
}
NEW_REQUIRED = (
    "APPFockRigidity", "SelectedLatticeAlgebra", "WittNegationLift",
    "LatticeOscillatorFock", "WittLatticeZeroModes", "LatticeParityCarrier",
    "SelectedVOAInput", "APPFockIndex",
    "LatticeFieldTruncation", "LatticeHeisenbergModes", "LatticeHeisenbergField",
    "SelectedHeisenbergInput",
)
NEW_OPTIONAL = ("APPFockOrientedTrace",)
BASE_ROOTS = ("deltas/witt", "deltas/accion_electron", "deltas/base_compartida")
BASE_FOCAL = (
    "WittReaderCompatibility", "SelectedActionDomain", "ElectronOrientationBridge",
    "SelectedElectronPublication", "SelectedArticleIComposition", "SharedArticleIBase",
)
BASE_PROBES = (
    "HMT.I.WittReaderCompatibility.charge_eq",
    "HMT.I.SelectedArticleI.principal_action_electron_composition",
    "HMT.Shared.ArticleI.shared_action_electron_incidence",
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise RuntimeError("Unsafe package path: " + value)
    return path


def load_verifier():
    spec = importlib.util.spec_from_file_location("voa_package_verifier", BASE / "verificar_lean.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load preserved source verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def qualified_probes(source: Path, verifier) -> list[str]:
    code = verifier.mask_comments_strings(source.read_text())
    namespace = re.search(r'^namespace\s+(HMT[\w.]*)\s*$', code, re.M)
    result = []
    for name in re.findall(r"#print\s+axioms\s+([\w.']+)", code):
        if '.' not in name:
            if namespace is None:
                raise RuntimeError('Unqualified theorem without an HMT namespace: ' + name)
            name = namespace.group(1) + '.' + name
        result.append(name)
    return result


def source_inventory() -> tuple[dict[str, Path], dict[str, Path]]:
    lean = {
        name: FORMAL / "stage14_contributions" / directory / (name + ".lean")
        for name, directory in RECOVERED.items()
    }
    lean["SymmetricTransport"] = (FORMAL / "contributions/reviewer/V_FockTransport/"
                                   "SymmetricTransport.lean")
    lean.update({name: HERE / (name + ".lean") for name in NEW_REQUIRED})
    lean.update({name: HERE / (name + ".lean") for name in NEW_OPTIONAL
                 if (HERE / (name + ".lean")).is_file()})
    lean["FoundationRegression"] = FOUNDATION / "FoundationRegression.lean"
    latex_root = (FORMAL / "stage18_article_I/delivery/"
                  "HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/documentation/payload")
    latex = {
        "integral/U030_capitulo_21_c20_lineas_1_2612.tex": OUTPUT /
            "REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/"
            "output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/"
            "partes_i_ii/source/base_residencias/capitulo_21_c20_lineas_1_2612.tex",
    }
    for language in ("es", "en"):
        for name in ("excepcional.tex", "moonshine_comparacion.tex"):
            latex[f"articulo_i_{language}/{name}"] = (
                latex_root / f"manuscript_{language}" / "sections" / name)
    for name, source in [*lean.items(), *latex.items()]:
        if not source.is_file():
            raise RuntimeError(f"Required source not available: {name}: {source}")
    return lean, latex


def wrapper_source(modules: list[str], probes: list[str]) -> str:
    return '''#!/usr/bin/env python3
"""Compile the shared base and its selected lattice/Fock/parity continuation."""
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hmt_voa_runner', root / 'verificar_lean.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
verifier.SOURCE_ROOTS += %r
verifier.MANDATORY_MODULES += %r
verifier.PROBE_DECLARATIONS += %r
sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
raise SystemExit(verifier.main())
''' % (BASE_ROOTS + ("deltas/voa",), BASE_FOCAL + tuple(modules),
       tuple(dict.fromkeys(BASE_PROBES + tuple(probes))))


def causal_receipt(destination: Path, lean: dict[str, Path]) -> dict:
    predecessor = BASE / "deltas/base_compartida/SHARED_BASE_CAUSAL_RECEIPT.json"
    receipt = json.loads(predecessor.read_text())
    artifact = destination / "README_VOA.md"
    receipt.update(
        artifact=str(artifact), artifact_sha256=sha(artifact),
        result_id="SELECTED_ARTICLE_I_ALGEBRAIC_VERTEX_CONTINUATION_20260918",
        artifact_role="PRESERVED_BASE_AND_ALGEBRAIC_CONTINUATION",
        scope="Packaging of preserved shared sources and explicit algebraic continuation "
              "on the selected lattice. New compilation is a separate action. No full "
              "VOA, FLM, twisted module, orbifold or Monster theorem is claimed.",
        mathematical_result="The named Lean sources construct the cocycle algebra, "
              "Fock carrier, oscillator and zero-mode relations, lattice-negation lift "
              "and untwisted parity splitting on the same selected lattice; exact "
              "statements and their hypotheses are in those sources.",
        predecessor_receipt=dict(path=str(predecessor), sha256=sha(predecessor)),
    )
    receipt["genealogy"]["tpk"].update(
        codomain="Selected register and incidence lattice, followed by its constructed "
                 "twisted complex group algebra, oscillator carrier and parity operators.",
        action="Reuse SharedArticleIBase and SelectedRegionalIncidence. Apply the "
               "constructed sign cocycle to that same selectedOrigin; specialize the "
               "Fock, zero-mode and negation constructions without supplying a second register.",
    )
    receipt["genealogy"]["source_locators"] += [
        str(destination / "deltas/voa" / (name + ".lean")) for name in lean
    ]
    receipt["semantic_scope_notes"] = [
        "The inherited declared corpus scope is documentary metadata, not a new theorem of this gate.",
        "The unordered S8 interface remains explicit and is not newly generated by this continuation.",
        "The inherited finite selector retains Lean.ofReduceBool; no new axiom is added for FLM.",
        "The selected lattice is the same carrier as the common incidence publication.",
        "The twisted associative group algebra is not the full vertex operator algebra.",
        "Untwisted parity splitting is proved; no twisted sector or orbifold product is asserted.",
        "The package conserves all predecessor manifested sources. A successful causal metadata "
        "audit must be distinguished from successful Lean compilation and from a full Moonshine proof.",
    ]
    receipt["genealogical_result_record"] = {
        "1_app_object_domain_sheets_operation": receipt["genealogy"]["app"],
        "2_trit_state_regime_orientation": receipt["genealogy"]["trit"],
        "3_tpk_operator_domain_codomain_action": receipt["genealogy"]["tpk"],
        "4_coefficient_origin": "APPFockRigidity supplies generatedAggregate and its oriented "
            "coefficient; APPFockIndex computes the operator trace. The selected radial norm is "
            "inherited from selected_incidence_lattice_properties. epsilon is constructed from "
            "the integral pairing modulo two. No target value selects the register.",
        "5_conservation": "The unchanged base retains word prefixes, orientation, route, "
            "carry and phase-memory distinction. The selectedOrigin and underlying lattice "
            "are preserved by definitional specialization; theta is proved involutive.",
        "6_enriched_state_and_continuum_residence": "Inherited common construction and its "
            "selected incidence publication. This addition is a continuation of that publication, "
            "not an independent redefinition or proof of the full continuum.",
        "7_hmt_output_before_recognition": "The same selected lattice and its explicitly "
            "constructed cocycle algebra, oscillator carrier, zero modes and parity splitting.",
        "8_posterior_recognition_and_falsifier": "FLM/Moonshine are later recognitions in "
            "the LaTeX provenance, not Lean assumptions. The compiler checks named equalities; "
            "source/hash mismatch, a failed axiom probe or a failed theorem prevents a PASS.",
        "9_material_owners": [dict(module=name,
            path="deltas/voa/" + name + ".lean", sha256=sha(source))
            for name, source in lean.items()],
    }
    receipt["genealogy_gate_status"] = "NINE_FIELDS_RECORDED_NOT_A_V4_GENEALOGY_CERTIFICATE"
    return receipt


README = """# Continuación algebraica del retículo seleccionado — Artículo I

Este paquete conserva íntegramente, por huella, los archivos manifestados de
BASE_COMPARTIDA y añade la continuación algebraica sobre **el mismo punto
marcado y el mismo retículo**. No introduce nuevamente el registro publicado.

## Orden operativo

1. El núcleo compartido conserva su orden APP → TRIT → TPK → estado enriquecido
   → publicaciones regionales correlacionadas → registro seleccionado → incidencia.
   Sus lecturas, condiciones y pruebas están en las fuentes heredadas; no se
   sustituyen por los valores numéricos de salida.
2. `SharedArticleIBase` reúne acción, electrón e incidencia. `SelectedLatticeAlgebra`
   prolonga el mismo retículo por el cociclo de signo, la extensión central y
   el álgebra compleja torcida, reutilizando siete módulos previos sin cambios.
3. `SymmetricTransport` y `LatticeOscillatorFock` construyen el portador simétrico
   de modos, sus operadores y las relaciones de conmutación. Los modos abarcan
   todos los índices naturales; no son un corte de dimensión finita. Los modos
   y los grados no tienen cota, pero cada elemento es una combinación algebraica
   finita. No se afirma una completación de Hilbert.
4. `WittLatticeZeroModes`, `WittNegationLift` y `LatticeParityCarrier` añaden modos
   cero, desplazamientos del retículo, involución y proyectores par/impar.
5. `APPFockRigidity` conserva el origen aritmético del índice 54 y la rigidez del
   parámetro positivo 12. `APPFockIndex` construye el operador finito de grado dos
   sobre 24 + 300 coordenadas: su dimensión es 324 y su traza es 54. Comprueba
   también el acoplamiento orientado del agregado suma–producto y el falsador
   de la fuente. La comparación con la norma radial es una igualdad de valores
   construidos; no se usa como un entrelazador operatorio ni como selección del
   registro. `SelectedVOAInput` reúne la continuación sobre el origen seleccionado.
6. `FoundationRegression` repite los controles del contrato común dentro de la
   misma compilación; el suplemento original se conserva íntegro en
   `suplementos/FoundationContract`.

## Reproducción

Se requieren Python 3 (biblioteca estándar), Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, con sus dependencias compiladas.
Desde esta carpeta:

```sh
python3 -I -S reproducir_voa.py --plan
python3 -I -S reproducir_voa.py --mathlib /ruta/a/mathlib --lean /ruta/a/lean
```

`--plan` verifica rutas, huellas y clausura de imports; no compila ni demuestra
por sí mismo. La segunda orden compila la clausura declarada, interroga los
axiomas de los teoremas y escribe su resultado en
`resultados/lean_unificado/VERIFICATION.json`. Un ZIP íntegro no equivale a ese
resultado. `PACKAGE_ASSEMBLY.json` acredita sólo la conservación y el montaje.
El recibo causal conserva los nueve campos genealógicos y el alcance heredado.
Su control de metadatos está separado de Lean y no se presenta como un teorema.

El comprobador original `verificar_lean.py` permanece idéntico. La nueva entrada
`reproducir_voa.py` amplía sus raíces y controles. Los ejecutables históricos se
conservan como procedencia; algunos retienen sus rutas locales originales. La
entrada portátil de esta ampliación es `reproducir_voa.py`.

## Alcance formal exacto

Se conservan explícitos la interfaz S8 no ordenada del antecedente y el límite
de confianza `Lean.ofReduceBool` de su selector finito. Esta ampliación no los
elimina ni los convierte en un nuevo axioma. No incorpora una hipótesis de
igualdad con el registro para sustituir su selección anterior.

Las nuevas pruebas construyen cociclo, extensión central, álgebra torcida,
portador oscilatorio, conmutadores, modos cero e involución sobre el retículo
seleccionado. El álgebra asociativa torcida no se identifica con una VOA completa.
La descomposición par/impar es la del portador no torcido; no afirma haber
construido por ella sola el módulo torcido ni el producto del orbifold.
La involución corresponde al cociclo triangular construido; no presupone una
identificación con una normalización diagonal específica de FLM.

**FLM y Moonshine no se han añadido como axiomas.** La compilación de esta
continuación no se presenta como formalización íntegra de esos teoremas ni de
todo el PDF. Los desarrollos LaTeX copiados bajo `procedencia/latex` documentan
la composición y sus fuentes; copiarlos no transforma sus teoremas en pruebas Lean.

## Conservación y caché

`versiones_previas/MANIFIESTO_BASE_COMPARTIDA.json` conserva el manifiesto de
partida. Todos sus archivos mantienen su contenido y ruta relativa. El suplemento
FoundationContract también se copia byte a byte, incluidos sus testigos históricos.
Sus objetos compilados históricos son procedencia y no se adoptan como caché del
nuevo runner.

Si se solicitó caché local, los 122 objetos de la base se copian sólo después de
verificar fuentes y huellas contra su recibo. Quedan en `resultados/`, fuera del
manifiesto y del ZIP. El runner vuelve a validar sus dependencias, compilador y
huellas; no acepta como acierto una caché sin recibo. Quien recibe únicamente el
ZIP recompila los módulos propios sobre el mismo Mathlib.
"""


def copy_verified_cache(destination: Path) -> dict:
    report_dir = BASE / "resultados/lean_unificado"
    receipt = json.loads((report_dir / "VERIFICATION.json").read_text())
    if receipt.get("status") != "PASS_PORTABLE_LEAN_SOURCE_CLOSURE":
        raise RuntimeError("The base does not have a successful Lean source-closure receipt")
    cache = json.loads((report_dir / "CACHE.json").read_text())
    if cache.get("format") != 1:
        raise RuntimeError("Unsupported base cache format")
    verified = []
    for record in receipt["modules"]:
        name = record["module"]
        source = BASE / safe_relative(record["source"])
        module_path = Path(*name.split("."))
        obj = (report_dir / "build" / module_path).with_suffix(".olean")
        cached = cache["modules"].get(name)
        if not cached or cached.get("exit_code") != 0:
            raise RuntimeError("Unreceipted cache entry: " + name)
        if sha(source) != record["source_sha256"] or sha(obj) != record["object_sha256"]:
            raise RuntimeError("Base source/object hash mismatch: " + name)
        for field in ("fingerprint", "source_sha256", "object_sha256"):
            if cached[field] != record[field]:
                raise RuntimeError("Base cache/receipt mismatch: " + name + ":" + field)
        target = destination / "resultados/lean_unificado/build" / module_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(obj, target.with_suffix(".olean"))
        shutil.copy2(source, target.with_suffix(".lean"))
        verified.append(name)
    target_dir = destination / "resultados/lean_unificado"
    shutil.copy2(report_dir / "CACHE.json", target_dir / "CACHE.json")
    result = dict(status="BASE_CACHE_COPIED_AFTER_SOURCE_AND_OBJECT_HASH_CHECK",
                  modules=verified, new_compilation_claimed=False,
                  source_receipt_sha256=sha(report_dir / "VERIFICATION.json"),
                  excluded_from_manifest_and_zip=True)
    write_json(target_dir / "COPIA_CACHE_BASE.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    parser.add_argument("--with-local-cache", action="store_true")
    parser.add_argument("--zip", action="store_true", dest="make_zip")
    args = parser.parse_args()
    destination = args.destination.expanduser().resolve()
    if destination.exists():
        raise RuntimeError("Refusing to overwrite an existing successor: " + str(destination))
    if destination == BASE.resolve() or destination.is_relative_to(BASE.resolve()):
        raise RuntimeError("The sealed base cannot be a destination")
    archive = destination.with_suffix(".zip")
    if args.make_zip and archive.exists():
        raise RuntimeError("Refusing to overwrite an existing ZIP: " + str(archive))

    sys.dont_write_bytecode = True
    manifest_path = BASE / "MANIFIESTO.json"
    manifest_hash = sha(manifest_path)
    base_manifest = json.loads(manifest_path.read_text())
    verifier = load_verifier()
    lean, latex = source_inventory()
    probes = []
    for name, source in lean.items():
        data = source.read_bytes()
        verifier.inspect_source(data, str(source))
        probes.extend(qualified_probes(source, verifier))
    base_paths = set()
    for record in base_manifest["files"]:
        relative = safe_relative(record["path"])
        if relative.as_posix() in base_paths:
            raise RuntimeError("Duplicate inherited path: " + str(relative))
        base_paths.add(relative.as_posix())
        if sha(BASE / relative) != record["sha256"]:
            raise RuntimeError("Inherited file differs from manifest: " + str(relative))

    destination.mkdir(parents=True)
    records = {}

    def copy_file(source: Path, relative: str, role: str, **metadata) -> None:
        path = safe_relative(relative)
        key = path.as_posix()
        if key in records:
            raise RuntimeError("Package-path collision: " + key)
        before = sha(source)
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if sha(target) != before or sha(source) != before:
            raise RuntimeError("Source changed during byte-preserving copy: " + str(source))
        records[key] = dict(source=str(source), path=key, sha256=before,
                            bytes=target.stat().st_size, role=role, **metadata)

    def generated_file(relative: str, content: str, role: str) -> None:
        path = safe_relative(relative)
        key = path.as_posix()
        if key in records:
            raise RuntimeError("Generated file would replace inherited content: " + key)
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        records[key] = dict(source="generated_by_package_voa_successor.py", path=key,
                            sha256=sha(target), bytes=target.stat().st_size, role=role)

    for record in base_manifest["files"]:
        copy_file(BASE / record["path"], record["path"],
                  record.get("role", "inherited_source"), inherited=True,
                  predecessor_source=record.get("source"))
    copy_file(manifest_path, "versiones_previas/MANIFIESTO_BASE_COMPARTIDA.json",
              "immutable_predecessor_manifest")
    for name, source in lean.items():
        copy_file(source, f"deltas/voa/{name}.lean", "lean_continuation_source",
                  disposition="RESULTADO_RECUPERADO" if name in RECOVERED or name in
                  ("SymmetricTransport", "FoundationRegression") else "FORMALIZACION_NUEVA")
    for relative, source in latex.items():
        copy_file(source, "procedencia/latex/" + relative, "latex_provenance_unchanged")
    for source in sorted(FOUNDATION.rglob("*")):
        if source.is_symlink():
            raise RuntimeError("Unexpected symlink in intact supplement: " + str(source))
        if source.is_file():
            relative = source.relative_to(FOUNDATION).as_posix()
            copy_file(source, "suplementos/FoundationContract/" + relative,
                      "foundation_supplement_unchanged_not_new_execution")
    # Keep the focal source receipts, including their exact scope and failures,
    # as documentary evidence; a package is not a replacement for a fresh run.
    for pattern in ("*.json", "verify_*.py"):
        for source in sorted(HERE.glob(pattern)):
            copy_file(source, "procedencia/implementacion/" + source.name,
                      "focal_receipt_or_runner_preserved")
    copy_file(Path(__file__).resolve(), "herramientas/package_voa_successor.py",
              "package_builder_provenance")
    generated_file("reproducir_voa.py", wrapper_source(list(lean), probes),
                   "portable_extended_source_verifier")
    generated_file("README_VOA.md", README, "continuation_scope_and_reproduction")
    causal = causal_receipt(destination, lean)
    generated_file("recibos/voa/CAUSAL_RECEIPT.json",
                   json.dumps(causal, ensure_ascii=False, indent=2) + "\n",
                   "causal_metadata_not_mathematical_proof")
    gate = Path("/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/"
                "verify_generated_constants.py")
    command = [sys.executable, "-I", "-S", str(gate), "--audit",
               str(destination / "README_VOA.md"), "--receipt",
               str(destination / "recibos/voa/CAUSAL_RECEIPT.json")]
    control = subprocess.run(command, capture_output=True, text=True, timeout=60)
    control_output = control.stdout + control.stderr
    generated_file("recibos/voa/CONTROL_CAUSAL.txt", control_output,
                   "actual_causal_metadata_gate_output")
    metadata_control = dict(command=command, exit_code=control.returncode,
                            checker_sha256=sha(gate), artifact_sha256=sha(destination / "README_VOA.md"),
                            receipt_sha256=sha(destination / "recibos/voa/CAUSAL_RECEIPT.json"),
                            lean_compilation=False, result_is_not_a_mathematical_proof=True)
    generated_file("recibos/voa/CONTROL_CAUSAL.json",
                   json.dumps(metadata_control, ensure_ascii=False, indent=2) + "\n",
                   "actual_causal_metadata_gate_execution")
    if control.returncode or "PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY" not in control_output:
        raise RuntimeError("Causal metadata gate did not pass; output retained in recibos/voa")
    assembly = dict(schema="hmt.voa.successor.assembly.v1", status="ASSEMBLED_NOT_COMPILED",
                    created_at_utc=datetime.now(timezone.utc).isoformat(),
                    source_manifest_sha256=manifest_hash, base=str(BASE),
                    inherited_files=len(base_manifest["files"]),
                    inherited_bytes_unchanged=True, original_pdfs_modified=False,
                    lean_modules_added=list(lean),
                    probes_added=list(dict.fromkeys(probes)),
                    compilation_entry="reproducir_voa.py", flm_axiomatized=False,
                    full_voa_or_moonshine_formalization_claimed=False,
                    local_cache_in_manifest=False)
    generated_file("PACKAGE_ASSEMBLY.json", json.dumps(assembly, ensure_ascii=False, indent=2)
                   + "\n", "assembly_receipt_not_proof_certificate")
    successor = {k: v for k, v in base_manifest.items() if k != "files"}
    successor.update(
        schema="hmt.voa.successor.snapshot.v1", status="DOCUMENTARY_SNAPSHOT_NOT_A_GLOBAL_PROOF",
        claim="Preserved shared base plus selected lattice algebra, Fock and parity continuation; "
              "no complete FLM/Moonshine formalization claimed.",
        predecessor=dict(path=str(BASE), manifest_sha256=manifest_hash,
                         preserved_file_count=len(base_manifest["files"])),
        continuation=assembly,
        files=[records[key] for key in sorted(records)],
    )
    write_json(destination / "MANIFIESTO.json", successor)
    # Final all-file hash check, including every inherited entry, before output.
    for key, record in records.items():
        if sha(destination / key) != record["sha256"]:
            raise RuntimeError("Final package verification failed: " + key)
    if sha(manifest_path) != manifest_hash:
        raise RuntimeError("The base manifest changed during packaging")
    cache_result = copy_verified_cache(destination) if args.with_local_cache else None
    zip_result = None
    if args.make_zip:
        members = sorted(records) + ["MANIFIESTO.json"]
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as handle:
            for relative in members:
                handle.write(destination / relative, destination.name + "/" + relative)
        with zipfile.ZipFile(archive) as handle:
            if handle.testzip() is not None:
                raise RuntimeError("ZIP CRC verification failed")
            expected = {destination.name + "/" + relative for relative in members}
            if set(handle.namelist()) != expected:
                raise RuntimeError("ZIP member mismatch")
            for key, record in records.items():
                digest = hashlib.sha256(handle.read(destination.name + "/" + key)).hexdigest()
                if digest != record["sha256"]:
                    raise RuntimeError("ZIP content hash mismatch: " + key)
        zip_result = dict(path=str(archive), sha256=sha(archive), files=len(members),
                          local_runtime_cache_included=False)
    print(json.dumps(dict(status="ASSEMBLED_NOT_COMPILED", package=str(destination),
                          manifested_files=len(records), added_modules=list(lean),
                          manifest_sha256=sha(destination / "MANIFIESTO.json"),
                          local_cache=cache_result, zip=zip_result),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
