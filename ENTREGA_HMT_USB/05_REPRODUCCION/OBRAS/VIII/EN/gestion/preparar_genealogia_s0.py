#!/usr/bin/env python3
"""Prepara recibos focales de VII sin editar manuscritos ni otros artículos.

Reutiliza la estructura documental de V; comprueba las huellas de la herencia.
La instantánea corresponde exclusivamente al main real de VII. Cada ejecución
requiere un subdirectorio nuevo. Los validadores globales mantienen sus rutas
canónicas: este preparador no declara su portabilidad fuera de la instalación.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECT = next(p for p in ROOT.parents if (p / "tools/verificar_genealogia_unica_hmt.py").is_file())
V = PROJECT / "output/ARTICULO_V_REV02_EDICION_INTEGRADA_20260910/gestion/genealogia_final"
II = PROJECT / "output/ARTICULO_II_REV09_ENTREGA_20260910"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def loc(p, lines=None):
    return {"path": str(p), "sha256": sha(p),
            "lines": lines or "1-%d" % len(p.read_text(encoding="utf-8").splitlines())}


def write(p, value):
    with p.open("x", encoding="utf-8") as f:
        f.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def check_locator(item):
    p = Path(item["path"])
    if not p.is_file() or sha(p) != item["sha256"]:
        raise ValueError("Herencia con identidad distinta: " + str(p))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-name", default="genealogia_s0")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"genealogia_s0(?:_[A-Za-z0-9_-]+)?", args.out_name):
        raise ValueError("Nombre de salida no autorizado")
    out = ROOT / "gestion" / args.out_name
    if out.exists():
        raise ValueError("Se conserva el recibo previo; elija un subdirectorio nuevo")
    inherited_path = V / "RECIBO_GENEALOGIA_LIMITE_TERMODINAMICO.json"
    previous = load(inherited_path)
    helper = II / "herramientas_portables.py"
    spec = importlib.util.spec_from_file_location("vii_readonly_assembly", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assembled = module.assemble(ROOT / "manuscrito")
    owners = {
        "ACTION_VII": ROOT / "manuscrito/sections/v_accion_estructural.tex",
        "BARBERO_VII": ROOT / "manuscrito/sections/v_funcional_barbero.tex",
        "GRAVITY_VII": ROOT / "manuscrito/sections/v_unidad_areal.tex",
        "PENTADIC_VII": ROOT / "manuscrito/28_portador_tensorial.tex",
        "GEOMETRY_VII": ROOT / "manuscrito/30d_realizacion_geometrica.tex",
        "CARTAN_VII": ROOT / "manuscrito/31_corriente_y_respuesta_cartan.tex",
        "SPINORIAL_VII": ROOT / "manuscrito/33_corriente_espinorial_y_densidad.tex",
    }
    for name, p in owners.items():
        if p not in assembled["files"]:
            raise ValueError("Propietario no incluido materialmente en main: " + name)
    receipt = {key: copy.deepcopy(previous[key]) for key in (
        "schema_version", "formal_kernel", "universal_genealogy", "foundation",
        "stage_order", "stages", "trit_constraints", "tpk_constraints", "non_regression")}
    for stage in receipt["stages"]:
        check_locator(stage["owner"])
        stage["inheritance"].pop("reproved_by_thermal_delta", None)
        stage["inheritance"]["reproved_by_spinorial_delta"] = False
    check_locator(receipt["formal_kernel"]["typed_operator_graph"])
    inherited_ids = set(receipt["foundation"]["evidence_ids"])
    for stage in receipt["stages"]:
        inherited_ids.update(stage["inheritance"]["source_ids"])
    inherited_manifest = {key: copy.deepcopy(previous["source_manifest"][key])
                          for key in sorted(inherited_ids)}
    for item in inherited_manifest.values():
        check_locator(item)
    purpose = (
        "Corte focal de corriente espinorial, contracción Cartan--Holst y amplitud material s0. "
        "G, hbar, c y gamma se heredan como publicaciones internas anteriores; no son objetivos "
        "numéricos ni constantes reprobadas por el control local. La acción afín, el estado CAR, "
        "el modo homogéneo periódico, el orden normal, el observador y Vc son datos explícitos "
        "de esta realización posterior. Se certifica la composición en ese dominio; no el "
        "catálogo integral, los terminales ni la autonomía científica del artículo VII completo."
    )
    statement = (
        "Con Clifford(-+++), acción espinorial mínima afín, orden normal de ocupación y "
        "Fock Lambda(C^4), s0[rho,Vc]=(3*kappa*c^2*hbar^2/16)*gamma^2/(1+gamma^2)*Tr(rho*Q)/Vc^2. "
        "La variación de lapse y escala da rho_spin=p_spin=-s0*a^-6. La amplitud es constante "
        "si Tr(rho Q) se conserva; Q=4I sobre Lambda^3 proporciona un dominio positivo "
        "conservado por toda evolución unitaria que preserve ese sector."
    )
    falsifier = (
        "Cambiar el signo o el factor de la corriente; eliminar el orden normal; sustituir "
        "el segundo momento por el cuadrado de la media; omitir Vc^2; inferir conservación "
        "de Q sólo de la ocupación media; elegir rho o un coeficiente xi externo para obtener "
        "un valor objetivo; identificar sin prueba la acción afín con la extensión mínima."
    )
    hypothesis = [
        "Cotetrada no degenerada, firma(-+++), orientación de31 y estructura de espín",
        "G,c,hbar positivos y gamma real no nulo constantes durante variación",
        "Acción Dirac mínima afín; campos y estado canónicos fijos durante variación de conexión/métrica",
        "Fock finita Lambda(C^4), estado positivo de traza1, vacío de ocupación y orden normal declarados",
        "Celda periódica comóvil Vc>0, modo homogéneo, observador fijado, a>0 y lapse N>0",
        "Amplitud constante condicionada a conservación de Tr(rho Q); dominio positivo condicionado a esa esperanza positiva",
    ]
    result_id = "VII_S0_FUNCTIONAL_OF_DECLARED_SPINORIAL_STATE"
    receipt.update({
        "receipt_id": "VII_CORRIENTE_ESPINORIAL_S0_20260910", "scope_kind": "MANUSCRIPT",
        "receipt_purpose": purpose, "normative_context_semantics": purpose,
        "binding_status": "ACTUAL_VII_SOURCE_SNAPSHOT_FOCAL_NOT_GLOBAL_SEAL",
        "provenance": "FORMALIZACION_NUEVA",
        "proof_strength": "DEMOSTRADO_CON_ESTRUCTURA_DE_PARTIDA_EXPLICITA",
        "conclusion_status": "CLOSED_IN_HMT_DOMAIN", "residual_if_any": None,
        "global_falsifier": falsifier,
        "editorial_revision": {"scope": "FOCAL_SPINORIAL_REALIZATION_S0",
            "whole_VII_certified": False, "catalogue_or_terminals_reproved": False,
            "screen_action_equals_Dirac_action_certified": False,
            "observed_cosmological_state_selected": False},
        "target": {"statement": statement, "result_id": result_id,
            "domain": "DeclaredSpinorialStateFamily", "codomain": "SignedTorsionalDensityAmplitudes",
            "closure_criterion": "Proposiciones y pruebas contiguas de33; matrices completas de contracción y CAR; variación N,a y conservación sectorial.",
            "target_family": "POST_CONTINUUM_HMT", "causal_cutoff": "ESTRUCTURA_DISCRETA_CONTINUO",
            "causal_cutoff_reason": "La realización reutiliza constantes, incidencia, representación y transporte anteriores al estado material evaluado.",
            "forbidden_generator_inputs": ["CONVENTIONAL_PI_E_PHI", "CODATA", "TARGET_G", "TARGET_HBAR", "EXTERNAL_XI_GAMMA", "TARGET_S0"]},
    })
    receipt["foundation"]["inherited_receipt"] = loc(inherited_path)
    receipt["foundation"]["inheritance_is_new_global_reproof"] = False
    receipt["universal_genealogy"]["scope_semantics"] = {
        "mode": "INHERITED_NORMATIVE_CONTEXT", "source_receipt": loc(inherited_path),
        "catalogue_or_terminal_proof_by_local_checks": False}
    receipt["result_maps"] = [{
        "id": "VII_INHERITED_ACTION_GRAVITY_BARBERO",
        "statement": "Publicaciones internas de acción, gravedad y parámetro de incidencia, con su genealogía y cartas previas.",
        "input_object": "C_cont_generated", "domain": "C_cont^disc",
        "codomain": "PublishedActionGravityBarbero", "output_object": "published_gravity_action_data",
        "source_family": "HMT", "generator_inputs": ["C_cont_generated"],
        "map": "Lectores de acción y unidad areal, funcional hexada--octada y representación pentacomponente -> hbar,c,G,gamma; kappa=8*pi_HMT*G/c^4 en la carta.",
        "proof_locator": loc(owners["GRAVITY_VII"]), "falsifier": "Sustituir una publicación interna por un objetivo metrológico.",
        "inheritance": {"mode": "INHERITED_NOT_REPROVED_BY_237_CHECKS", "owners": [loc(owners[x]) for x in ("ACTION_VII", "BARBERO_VII", "PENTADIC_VII")]},
    }, {
        "id": "VII_DECLARED_AFFINE_SPINORIAL_REALIZATION",
        "statement": "Realización espinorial afín con corriente explícita y su observable cuártico sobre los datos materiales declarados.",
        "input_object": "published_gravity_action_data", "domain": "PublishedActionGravityBarbero",
        "codomain": "DeclaredSpinorialStateFamily", "output_object": "spinorial_state_family",
        "source_family": "HMT", "generator_inputs": ["published_gravity_action_data"],
        "map": "g=(J tensor I,R tensor I,Z tensor R,Z tensor Z); A_D=-i*g0; S_D afín -> sigma_JK=-(hbar/2)*B^I_JK*eta_I; Q=sum signs :dGamma(M)^2: sobre Lambda(C^4). Parametrizar por rho,Vc y campos, sin elegirlos para producir s0.",
        "proof_locator": loc(owners["SPINORIAL_VII"], "34-339"), "falsifier": falsifier,
        "representation_hypotheses": hypothesis,
        "realization_is_unique_choice_from_APP_certified_here": False,
        "state_and_volume_are_material_initial_data": True,
        "screen_current_identified_with_Dirac_current": False,
        "geometric_owner": loc(owners["GEOMETRY_VII"]),
    }, {
        "id": result_id, "statement": statement, "input_object": "spinorial_state_family",
        "domain": "DeclaredSpinorialStateFamily", "codomain": "SignedTorsionalDensityAmplitudes",
        "output_object": "s0_functional", "source_family": "HMT", "generator_inputs": ["spinorial_state_family"],
        "map": "Invertir Holst y torsión de31; C_gamma=(3*kappa*c*hbar^2/16)*gamma^2/(1+gamma^2); variar lapse y escala en S=N*c*C_gamma*q/(a^3*Vc); s0=c*C_gamma*Tr(rho Q)/Vc^2. Q|Lambda^3=4I acredita no vacuidad y conservación en ese sector.",
        "proof_locator": loc(owners["SPINORIAL_VII"], "142-468"), "falsifier": falsifier,
        "response_owner": loc(owners["CARTAN_VII"]),
    }]
    receipt["conventional_uses"] = [{
        "name": "Realización material espinorial afín, productos CAR y variación métrica en celda homogénea",
        "role": "PROOF_LANGUAGE", "locator": loc(owners["SPINORIAL_VII"]),
        "occurs_after_hmt_output": True, "selects_hmt_state": False, "selects_route": False,
        "sets_generators": False, "sets_coefficients": False, "target_value_used_as_input": False,
        "scope_note": "Estos indicadores conciernen al generador HMT. La acción, el orden normal y los datos materiales posteriores sí determinan el funcional de esta realización; son hipótesis explícitas, no una conclusión de unicidad de representación."}]
    receipt["proof_layers"] = {
        "finite": "Clifford4, diez coeficientes cuadráticos para cada parte de Holst, CAR16 y restricciones por ocupación; 237 identidades y6 mutaciones en el control focal.",
        "compatibility": "La misma corriente afín entra en ambas inversas y en la eliminación; normalización coherente de hbar,kappa,c y del volumen. Conservación probada para el sectorN3; no identificada con conservación de la ocupación media.",
        "limit": {"required": False, "reason": "El corte es una realización material finita con observables matriciales y variación homogénea. No afirma límite de muchos modos ni extrapolación a un estado cósmico único.",
                  "typing_falsifier": "Usar esta evaluación finita como demostración del límite de campos o de un estado cosmológico seleccionado."},
        "recognition": "Densidad de energía y presión obtenidas por variación métrica después de las publicaciones previas; uso en el dominio positivo de50 conserva sus demás condiciones."}
    receipt["source_manifest"] = inherited_manifest
    receipt["source_manifest"].update({key: loc(p) for key, p in owners.items()})
    receipt["source_manifest"]["INHERITED_RECEIPT_V"] = loc(inherited_path)
    receipt["genealogical_nine_fields"] = {
        "1_app_object_domain_sheets_operation": receipt["stages"][0],
        "2_trit_state_regime_orientation": receipt["stages"][1],
        "3_tpk_operator_domain_codomain_action": receipt["stages"][2],
        "4_coefficient_origins": {"inherited_constants": [loc(owners[x]) for x in ("ACTION_VII", "BARBERO_VII", "GRAVITY_VII")],
            "three_over_sixteen": loc(owners["SPINORIAL_VII"], "142-206"), "gamma_ratio": loc(owners["CARTAN_VII"]),
            "four_and_volume_square": loc(owners["SPINORIAL_VII"], "208-433"), "external_xi_received": False},
        "5_information_preservation": "Representación y conexión heredadas; se conservan firma, orientación, estado y segundos momentos. La densidad es una lectura, no una reconstrucción de todas las rutas.",
        "6_enriched_state_and_continuum": {"mode": "INHERITED", "stages": receipt["stages"][3:]},
        "7_hmt_output_before_realization": receipt["result_maps"][0],
        "8_posterior_realization_and_falsifier": {"realization": receipt["conventional_uses"][0], "falsifier": falsifier},
        "9_material_owners": {key: loc(p) for key, p in owners.items()},
    }
    anchors, cursor = [], -1
    for item in previous["artifact"]["anchors"]:
        needle = {"HMT_OUTPUT": "\\label{v:ant:sec:gravity}",
                  "CONVENTIONAL": "\\label{vii:eq:accion-dirac-material}"}.get(item["stage"], item["text"])
        index = assembled["text"].find(needle, cursor + 1)
        if index < 0:
            raise ValueError("Ancla literal ausente o fuera de orden: " + item["stage"])
        anchors.append({"stage": item["stage"], "text": needle, "line": assembled["text"][:index].count("\n") + 1})
        cursor = index
    out.mkdir()
    composite = out / "FUENTE_COMPUESTA_VII.tex.txt"
    write(composite, assembled["text"])
    receipt["artifact"] = {"path": str(composite), "sha256": sha(composite), "kind": "MANUSCRIPT", "anchors": anchors,
        "binding_note": "Fuente compuesta del main real. Las remisiones se registran aparte; este recibo no declara clausura editorial integral."}
    genealogy_path = out / "RECIBO_GENEALOGIA_S0.json"
    write(genealogy_path, receipt)
    old_constants = load(V / "RECIBO_CONSTANTES_LIMITE_TERMODINAMICO.json")
    constants = {"schema_version": "1.1", "artifact": str(owners["SPINORIAL_VII"]),
        "result_id": result_id, "local_artifact_sha256": sha(owners["SPINORIAL_VII"]),
        "control_scope": purpose, "genealogy": copy.deepcopy(old_constants["genealogy"]),
        "inherited_receipt": loc(V / "RECIBO_CONSTANTES_LIMITE_TERMODINAMICO.json"),
        "inherited_normative_scope": {"mode": "INHERITED_NOT_REPROVED", "declared_scope_is_not_local_proof": True,
            "catalogue_and_terminals_certified_by_delta": False},
        "candidate_selection": {"status": "NO_TARGET_SELECTION", "parameter_optimization": False},
        "local_results": [{"generated_by": receipt["result_maps"][-1]["map"],
            "causal_role": "DOWNSTREAM_EXPLICIT_REALIZATION", "joint_generation_id": "APP_TRIT_TPK_NONADIC_TYPED_IMAGE_V2",
            "publication_stage": "AFTER_HMT_ACTION_GRAVITY_BARBERO_AND_DECLARED_SPINORIAL_STATE",
            "proof_owner": loc(owners["SPINORIAL_VII"]), "representation_hypotheses": hypothesis,
            "parameter_roles": {"G_c_hbar_gamma_pi": "PRIOR_INTERNAL_PUBLICATIONS_REUSED_DOWNSTREAM",
                "rho_Vc_fields_observer_normal_order": "EXPLICIT_MATERIAL_STATE_AND_REALIZATION_DATA",
                "s0": "COMPUTED_STATE_FUNCTIONAL_NOT_UNIVERSAL_NUMBER",
                "external_xi_gamma_or_target_s0": "NOT_USED"}}],
        "material_owners": {key: loc(p) for key, p in owners.items()},
        "implementation": loc(ROOT / "pruebas/verificar_corriente_espinorial.py"),
        "independent_algebraic_runs": [loc(ROOT / "pruebas" / n) for n in
            ("RECIBO_corriente_espinorial.json", "RECIBO_corriente_espinorial_optimizado.json")],
    }
    constants["genealogy"]["source_locators"] = [str(p) for p in owners.values()] + [str(inherited_path)]
    constants["genealogy"]["tpk"].update({"codomain": "Estado enriquecido y estructura discreta conjunta con publicaciones de acción, incidencia y gravedad anteriores",
        "action": "La actualización previa conserva genealogía, ruta y memoria. Después,31 y33 componen la representación afín, su corriente, la inversión torsional y su lectura de segundo momento; el estado y la celda se declaran antes de evaluar s0."})
    constant_path = out / "RECIBO_CONSTANTES_S0.json"
    write(constant_path, constants)
    write(out / "VINCULACION_FOCAL_VII.json", {
        "scope": purpose, "main": loc(ROOT / "manuscrito/main.tex"), "helper": loc(helper),
        "source_count": len(assembled["files"]), "sources": [loc(p) for p in assembled["files"]],
        "edges": assembled["edges"], "undefined_references": assembled["undefined_references"],
        "duplicate_labels": assembled["duplicate_labels"], "pdf_compiled_here": False,
        "global_theorems_reproved": False, "canonical_gate_is_portable": False})
    write(out / "README.md", "# Recibos focales de la amplitud torsional\n\n" + purpose + "\n\n"
        "El PASS de cada puerta valida su contrato causal/documental sobre esta instantánea; no sustituye la prueba impresa ni amplía su dominio. "
        "El control algebraico portable conserva237 identidades y6 mutaciones. Las puertas canónicas usan rutas absolutas, incluido el grafo permanente; "
        "esta validación es local y no prueba portabilidad de esas puertas. Los resultados heredados conservan huellas y no reciben una nueva prueba por este delta.\n\n"
        "La instantánea se regenera después de cambios de fuentes con gestion/preparar_genealogia_s0.py --out-name genealogia_s0_REV --validate. "
        "Se exige un directorio nuevo para conservar cada resultado anterior. Ninguna fuente ni otro artículo se modifica. "
        "La puerta de no disgregación del continuo no se vuelve a demostrar mediante este resultado material: permanece antecedente de su propio dominio.\n")
    if args.validate:
        generated = Path("/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py")
        commands = [
            [sys.executable, "-I", "-S", str(PROJECT / "tools/verificar_genealogia_unica_hmt.py"), "--receipt", str(genealogy_path)],
            [sys.executable, "-I", "-S", str(generated), "--audit", str(owners["SPINORIAL_VII"]), "--receipt", str(constant_path)],
        ]
        results = []
        for command in commands:
            result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            results.append({"command": command, "returncode": result.returncode, "output": result.stdout})
        write(out / "VALIDACION_FOCAL_VII.json", {"scope": purpose, "results": results,
            "passed_contract_checks": all(r["returncode"] == 0 for r in results), "whole_article_mathematically_certified": False})
        for result in results:
            print(result["output"], end="")
        print("Recibos: " + str(out))
        return 0 if all(r["returncode"] == 0 for r in results) else 1
    print("Recibos preparados sin ejecutar validadores: " + str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
