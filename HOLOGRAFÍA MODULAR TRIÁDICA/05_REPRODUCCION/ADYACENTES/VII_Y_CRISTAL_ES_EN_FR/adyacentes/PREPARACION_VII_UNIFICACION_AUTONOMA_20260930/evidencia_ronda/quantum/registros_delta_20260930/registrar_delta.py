#!/usr/bin/env python3
"""Recibos documentales focales; no modifica ni sella la entrega precedente.

Los verificadores comprueban contratos documentales y causales, no demuestran
las identidades matemáticas ni amplían el dominio declarado en las notas.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
Q = OUT.parent
ROOT = Path(__file__).resolve().parents[4]
PACKAGE = ROOT / "output/ENTREGA_INTEGRACION_GRAVEDAD_CUATRO_INTERACCIONES_20260930"
BASE_G = PACKAGE / "registros/RECIBO_GENEALOGIA_ACCION_CANONICA_TOTAL.json"
BASE_C = PACKAGE / "registros/RECIBO_CONSTANTES_ACCION_CANONICA_TOTAL.json"
PIN_G = "23c67f7a768194a6dee4cc4e1a6a38b7b3d7fe417c0d7e4d88ee6d377afa24d8"
PIN_C = "e429eb549e69470f8e33c32792fba976bd7b7eeaa3dccf3f3c0ce119ae6d6332"
GATE_G = ROOT / "tools/verificar_genealogia_unica_hmt.py"
GATE_C = Path("/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py")
F10 = PACKAGE / "latex/10_gravedad_energia_autoinercia.tex"
F20 = PACKAGE / "latex/20_accion_retroaccion_restricciones.tex"
A28 = Path("/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes")
EXPECTED_NOTES = (
    "RECTIFICACION_OPERADOR_TOTAL_Y_ENCARGO_20260930.md",
    "ENUNCIADO_UNIFICACION_ACCION_TOTAL_20260930.md",
    "TRANSPORTE_CILINDRICO_EXPLICITO_20260930.md",
)

SPECS = {
    "RECTIFICACION": {
        "file": EXPECTED_NOTES[0],
        "codomain": "CONEXION_CARACTERISTICA_TOTAL_RECTIFICADA",
        "statement": "Calcular la curvatura de la conexión característica de la acción total y distinguirla del operador interactuante posterior h_x o H_loc.",
        "map": "Desde los transportes y la acción total recibidos: (Theta_tot,C_A) -> Omega_tot=-dTheta_tot; nabla_N=X_N-i*Theta_tot(X_N)/hbar; H_N=-Theta_tot(X_N); F_NM=Omega_tot(X_N,X_M)=u^A*v^B*f_AB^C*C_C, nula sobre Z={C_C=0}; Q(f)=-i*hbar*nabla_Xf+f conserva el corchete de Dirac en su dominio suave.",
        "domain": "Carta simpléctica regular de la misma acción total, tras reducción de segunda clase; secciones suaves de la línea precuántica; hbar fijo y no nulo; variaciones interiores o borde compatible; direcciones características X_N=u^A X_CA sobre Z.",
        "boundary": "La planitud característica no trivializa la holonomía global ni identifica historias por sus extremos. No identifica por nombre esta representación con h_x, H_loc o una regularización espacial arbitraria.",
        "falsifier": "La identidad falla si F_NM difiere de Omega_tot(X_N,X_M), si se elimina la derivada del coeficiente Theta_tot(X_N), o si se promueve el resultado a la igualdad no probada con h_x. Fuera de Z se retienen los términos proporcionales a restricciones de las extensiones elegidas.",
        "finite": "Cálculo diferencial contiguo de F=-dTheta_tot(X_N,X_M), primera clase y conmutador precuántico; no es un muestreo numérico de deformaciones.",
        "compatibility": "Mismo potencial, restricciones, acción y derivadas; [Q(f),Q(g)]=i*hbar*Q({f,g}_D) y Q(aC)=aQ(C)+C(Q(a)-a), antes de restringir a Z.",
        "limit": "La rectificación calcula una conexión en una carta regular; no añade un límite espacial-quiral ni sustituye el operador de una realización posterior.",
        "output_anchor": "Las constantes son salidas HMT recibidas",
        "recognition_anchor": "reconocimiento convencional posterior",
        "owners": [F20, A28 / "VIII_ES/manuscrito/30d_realizacion_geometrica.tex"],
    },
    "ENUNCIADO": {
        "file": EXPECTED_NOTES[1],
        "codomain": "UNIFICACION_VARIACIONAL_CANONICA_ACCION_TOTAL",
        "statement": "Reunir la unificación variacional y canónica de la gravitación y las interacciones internas fuerte y electrodébil, incluida su realización electromagnética, desde la misma acción covariante y sus restricciones.",
        "map": "Transportes de pantalla y materia -> S_tot[e,omega,A,H,Psi] -> sigma=sum_s sigma_s -> k_star[sigma] -> S_spin_eff=-1/4 integral k_star[sigma] wedge sigma, con cruces entre especies -> fuente métrica de S_m,red -> Legendre regular y restricciones totales de primera clase -> propagación por Noether-Bianchi -> F_can=Omega(X,Y)=0 en direcciones características.",
        "domain": "Coframe no degenerado, gamma real no nulo, materia afín en contorsión, inversas de Holst y torsión en su dominio, carta de Legendre regular, reducción de segunda clase y variaciones interiores o borde compatible. Los multipletes y pesos son los declarados; el contenido cuántico de Fock finita y Higgs sin corte conserva por separado el dominio del fragmento 10.",
        "boundary": "Acción común construida, no unicidad entre funcionales posibles; unificación variacional y canónica con planitud característica precuántica, no identidad automática con h_x ni afirmación universal sobre límites espaciales o representaciones operatorias.",
        "falsifier": "Ablación de los cruces torsionales, del valor absoluto del potencial Higgs o de la variación de la cotetrada; cambio de acción entre Legendre y restricciones; pérdida de la equivariancia Yukawa o promoción de la carta cuántica declarada a un límite espacial universal.",
        "finite": "La nota reúne y localiza las pruebas completas de los fragmentos 10 y 20: equivariancia material, reducción cuadrática, fuente métrica, Legendre, primera clase y propagación; las puertas no sustituyen esas pruebas.",
        "compatibility": "Geometría, color, débil, hipercarga y Yukawa actúan sobre la misma materia; Q=J_3+Y preserva H_0; la corriente total se forma antes de eliminar contorsión; la conexión característica usa el potencial de esa misma acción.",
        "limit": "Se conserva el retiro del corte escalar y funcional de enlace de la carta cuántica del fragmento 10, sin anunciar un nuevo límite espacial-quiral conjunto. Este recibo es una reunión documental de resultados con dominio declarado.",
        "output_anchor": "El retorno marcado produce",
        "recognition_anchor": "En la identificación radial declarada",
        "owners": [F10, F20, A28 / "VIII_ES/manuscrito/30d_realizacion_geometrica.tex"],
    },
    "TRANSPORTE_CILINDRICO": {
        "file": EXPECTED_NOTES[2],
        "codomain": "TRANSPORTE_CILINDRICO_CINEMATICO_COMPATIBLE",
        "statement": "Construir explícitamente el refinamiento isométrico de amplitudes, su derivada y una completación unitaria cinemática compatible en el límite cilíndrico, distinguiendo conexión transportada y proyectada.",
        "map": "J_mn(|s> tensor u)=sum_(t>s) sqrt(p_t/p_s)|t> tensor exp((theta_t-theta_s)J_E)u; J_lm J_mn=J_ln y J_mn Psi_n=Psi_m. Las rotaciones O_s de la carta positiva y la recursión U_(n+1)=R_n[J_n^0 U_n (J_n^0)*+I-J_n^0(J_n^0)*] producen U_(n+1)J_n^0=J_n(b)U_n. Su límite U_inf induce nabla_inf=U_inf d U_inf*, plana sobre secciones cilíndricas suaves. En contraste, J*R^P J=diag_s(J_E sum_t dq_(t|s) wedge dphi_ts), no nula en general.",
        "domain": "Particiones finitas por prefijos con antecesor único; preparación compatible con p_s>0 en soporte fijo y fases C2 sobre carta local B; J_E fijo, antiadjunto y de cuadrado -I. Límite por isometrías y núcleo de secciones cilíndricas suaves en la trivialización construida.",
        "boundary": "Refinamiento de prefijos, no refinamiento espacial ni tiempo físico. La conexión es cinemática y no se identifica con la conexión PCH, h_x o un generador físico autoadjunto. No se infiere equivalencia global de medidas ni cota uniforme de derivadas por nivel.",
        "falsifier": "Fracaso de J*J=I o del cuadrado de composición, descarte de ramas, cambio de soporte sin dominio adicional, confusión de P d con la conexión transportada compensada, o identificación del límite cinemático con la curvatura física total.",
        "finite": "Pruebas de isometría, adjunto, derivada y composición por cancelación de probabilidades y fases; rotación O_s construida y verificada algebraicamente. Controles racionales focales de nueve ramas y del cuadrado recursivo no sustituyen las pruebas.",
        "compatibility": "J_lm J_mn=J_ln; derivada por regla del producto; U_(n+1)J_n^0=J_n(b)U_n; nabla_(n+1)J_n=J_n nabla_n; iota_m J_mn=iota_n. La graduación de prefijos no se cambia por una geometría física no declarada.",
        "limit": "El límite se construye explícitamente sobre el núcleo cilíndrico y no amplía el resultado a dinámica física total.",
        "limit_detail": {"required": True, "finite_levels": "H_n=ell2(S_n) tensor E, con particiones finitas de soporte positivo.", "bonding_maps": "J_mn de la ecuación (3), isométricos y coherentes.", "compatibility_identity": "J_lm J_mn=J_ln; iota_m J_mn=iota_n; U_m J_mn^0=J_mn(b)U_n.", "limit_object": "L2 de la sigma-álgebra de prefijos, o clausura cilíndrica en una realización de medida mayor, con trivialización U_inf.", "proof": "Ecuaciones (21)-(23): iota_n es isométrico; la cancelación de probabilidad y fase prueba compatibilidad; densidad da el unitario límite. La conexión y sus dos derivadas se calculan en un nivel finito que contiene la sección, dando curvatura cero en el núcleo cilíndrico."},
        "output_anchor": "el estado propietario es",
        "recognition_anchor": "La conexión de proyección",
        "tpk_operator": "Transporte de amplitudes, fases y prefijos de la preparación genealógica recibida; completación cinemática explícita posterior.",
        "owners": [ROOT / "output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/04ab_postulados_cuanticos_genealogicos_rev2.tex"],
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locator(path: Path) -> dict:
    return {"path": str(path), "sha256": digest(path),
            "lines": f"1-{len(path.read_text(encoding='utf-8').splitlines())}"}


def write_json(path: Path, value: dict) -> None:
    if path.parent.resolve() != OUT:
        raise ValueError("La delta sólo escribe dentro de su propio directorio")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def anchors(spec: dict, text: str) -> list[dict]:
    values = list(zip(
        ["APP", "TRIT", "TPK", "ESTADO_ENRIQUECIDO", "ESTRUCTURA_DISCRETA_CONTINUO", "HMT_OUTPUT", "CONVENTIONAL"],
        ["APP →", "TRIT →", "TPK →", "estado enriquecido →", "estructura discreta conjunta del continuo", spec["output_anchor"], spec["recognition_anchor"]],
    ))
    pos = -1
    result = []
    for stage, token in values:
        pos = text.find(token, pos + 1)
        if pos < 0:
            raise ValueError(f"Ancla tipada ausente o fuera de orden: {stage}: {token}")
        result.append({"stage": stage, "text": token})
    return result


def produce(key: str, spec: dict, base_g: dict, base_c: dict) -> dict:
    source = Q / spec["file"]
    if not source.is_file():
        return {"note": str(source), "status": "NOT_AVAILABLE", "accepted": False}
    loc = locator(source)
    owners = [locator(p) for p in spec["owners"]]
    rid = f"DELTA-DOCUMENTAL-20260930-{key}"
    gpath = OUT / f"RECIBO_GENEALOGIA_{key}.json"
    cpath = OUT / f"RECIBO_CONSTANTES_{key}.json"
    g = copy.deepcopy(base_g)
    g.update({
        "receipt_id": rid,
        "artifact": dict(loc, kind="DERIVATION", anchors=anchors(spec, source.read_text(encoding="utf-8"))),
        "inherited_receipt": locator(BASE_G),
        "focal_owners": owners,
        "inheritance_note": "Procedencia heredada de ACCION_CANONICA_TOTAL; núcleo, grafo tipado y etapas conservados sin cambios. Mapa, dominio, falsadores y anclas son propios de esta nota. Los PASS son documentales, no nuevas pruebas matemáticas.",
        "scope_boundaries": [spec["domain"], spec["boundary"], "No edita ni sella el paquete precedente, los manuscritos o sus PDF."],
        "global_falsifier": spec["falsifier"],
        "documentary_checks_only": True,
        "global_corpus_claims_revalidated": False,
    })
    g["target"].update({
        "statement": spec["statement"], "codomain": spec["codomain"],
        "closure_criterion": spec["map"] + " " + spec["domain"] + " " + spec["boundary"],
        "result_id": rid,
        "causal_cutoff_reason": "Los transportes, lectores y constantes recibidos son salidas HMT posteriores al continuo conjunto; la nota compone sus realizaciones en el dominio focal declarado.",
    })
    g["result_maps"] = [{
        "id": rid, "statement": spec["statement"], "input_object": "c_cont_disc",
        "domain": "C_CONT_DISC", "codomain": spec["codomain"],
        "output_object": spec["codomain"].lower(), "map": spec["map"],
        "generator_inputs": ["c_cont_disc"], "source_family": "HMT",
        "proof_locator": loc, "falsifier": spec["falsifier"],
        "realization_domain": spec["domain"],
    }]
    g["conventional_uses"] = [{
        "name": "Cálculo variacional, simpléctico y precuántico como lenguaje posterior de realización y prueba.",
        "role": "PROOF_LANGUAGE", "locator": loc, "occurs_after_hmt_output": True,
        "selects_hmt_state": False, "selects_route": False, "sets_generators": False,
        "sets_coefficients": False, "target_value_used_as_input": False,
    }]
    g["proof_layers"] = {
        "finite": spec["finite"], "compatibility": spec["compatibility"],
        "limit": spec.get("limit_detail", {"required": False, "reason": spec["limit"], "typing_falsifier": spec["boundary"]}),
        "recognition": "Las realizaciones convencionales operan después de las salidas HMT, con los dominios y propietarios conservados. " + spec["boundary"],
    }
    for field in ("formal_kernel", "universal_genealogy", "foundation", "stage_order", "stages", "trit_constraints", "tpk_constraints", "non_regression"):
        assert g[field] == base_g[field], field
    write_json(gpath, g)
    c = copy.deepcopy(base_c)
    c.update({
        "artifact": str(source), "artifact_sha256": loc["sha256"], "result_id": rid,
        "scope_note": spec["statement"] + " " + spec["boundary"],
        "prior_receipt_provenance": locator(BASE_C), "focal_material_owners": owners,
        "declared_realization_assumptions": {"domain": spec["domain"]},
        "audited_text_scope": loc, "focal_claim_locator": loc,
        "focal_genealogy_receipts": [locator(gpath)],
        "documentary_checks_only": True, "global_corpus_claims_revalidated": False,
        "precompile_approval": False,
    })
    c["genealogy"]["tpk"] = {
        "operator": spec.get("tpk_operator", "Composición de transportes de pantalla, materia y memoria recibidos de APP-TRIT-TPK; realización focal de la acción canónica total."),
        "domain": spec["domain"], "codomain": spec["codomain"], "action": spec["map"],
    }
    c["genealogy"]["source_locators"] = [str(p) for p in spec["owners"]] + [str(source)]
    write_json(cpath, c)
    commands = [
        ("genealogy", [sys.executable, "-I", "-S", str(GATE_G), "--receipt", str(gpath)], "PASS_GENEALOGIA_UNICA_APP_TRIT_TPK"),
        ("constants", [sys.executable, "-I", "-S", str(GATE_C), "--audit", str(source), "--receipt", str(cpath)], "PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY"),
    ]
    checks = []
    for name, command, expected in commands:
        run = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        checks.append({"name": name, "command": command, "returncode": run.returncode,
                       "stdout": run.stdout, "stderr": run.stderr,
                       "passed": run.returncode == 0 and expected in run.stdout})
    unchanged = digest(source) == loc["sha256"]
    accepted = unchanged and all(check["passed"] for check in checks)
    return {"note": loc, "genealogy_receipt": locator(gpath), "constants_receipt": locator(cpath),
            "source_unchanged_during_checks": unchanged, "checks": checks,
            "accepted": accepted, "status": "PASS_DOCUMENTARY_FOCAL_DELTA" if accepted else "FAIL_DOCUMENTARY_FOCAL_DELTA"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=tuple(SPECS), action="append")
    args = parser.parse_args()
    if digest(BASE_G) != PIN_G or digest(BASE_C) != PIN_C:
        raise SystemExit("STOP: el recibo de procedencia no coincide con su huella fijada")
    base_g = json.loads(BASE_G.read_text(encoding="utf-8"))
    base_c = json.loads(BASE_C.read_text(encoding="utf-8"))
    keys = args.only or list(SPECS)
    results = [produce(key, SPECS[key], base_g, base_c) for key in keys]
    report = {
        "schema": "HMT_FOCAL_DOCUMENTARY_DELTA_V1", "script": locator(Path(__file__)),
        "inherited_genealogy": locator(BASE_G), "inherited_constants": locator(BASE_C),
        "meaning": "Los PASS verifican vinculación documental, tipado causal y roles de constantes; no prueban unificación cuántica global ni amplían los dominios matemáticos de las notas.",
        "sealed_package_modified": False, "results": results,
        "unprofiled_notes": [str(Q / name) for name in EXPECTED_NOTES if name not in {s["file"] for s in SPECS.values()}],
    }
    report_path = OUT / "CONTROL_DELTA_20260930.json"
    write_json(report_path, report)
    for result in results:
        print(result["status"], result["note"] if isinstance(result["note"], str) else result["note"]["path"])
        for check in result.get("checks", []):
            print(check["stdout"].strip())
            if check["stderr"]:
                print(check["stderr"].strip(), file=sys.stderr)
    print("Informe:", report_path)
    return 0 if all(r["accepted"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
