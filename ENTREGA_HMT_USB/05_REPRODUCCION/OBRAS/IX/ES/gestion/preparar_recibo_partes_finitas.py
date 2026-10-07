#!/usr/bin/env python3
"""Recibo focal de una evaluación; no licencia para publicar VIII como cerrado.

Hereda explícitamente el contexto normativo del recibo existente de la serie.
Verifica sus propietarios sin convertir esa herencia en una nueva prueba.
El artefacto enlazado es una instantánea textual de las fuentes realmente leídas.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
INHERITED = PROJECT/"output/ARTICULO_VII_REV07_EDICION_INTEGRADA_20260910/gestion/genealogia_s0_rev07/RECIBO_GENEALOGIA_S0.json"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def loc(p):
    return {"path":str(p), "sha256":sha(p), "lines":"1-"+str(len(p.read_text().splitlines()))}


def main():
    old = json.loads(INHERITED.read_text())
    r = {k:copy.deepcopy(old[k]) for k in (
        "schema_version","formal_kernel","universal_genealogy","foundation",
        "stage_order","stages","trit_constraints","tpk_constraints","non_regression")}
    source = ROOT/"manuscrito/04_PARTES_FINITAS_Y_LECTORES_RESIDUALES.md"
    native = ROOT/"manuscrito/01_CONSTRUCCION_ARITMETICA.md"
    producer = ROOT/"fuente/pruebas/python/partes_finitas_exactas.py"
    ids = set(r["foundation"]["evidence_ids"])
    for stage in r["stages"]:
        ids.update(stage["inheritance"]["source_ids"])
        stage["inheritance"]["reproved_by_finite_parts_delta"] = False
    r["source_manifest"] = {k:copy.deepcopy(old["source_manifest"][k]) for k in sorted(ids)}
    for item in [r["formal_kernel"]["typed_operator_graph"]]+list(r["source_manifest"].values())+[s["owner"] for s in r["stages"]]:
        if sha(Path(item["path"])) != item["sha256"]:
            raise ValueError("Herencia modificada: "+item["path"])
    r["source_manifest"].update({"NATIVE_ARITHMETIC":loc(native), "FINITE_PARTS_PROOF":loc(source),
                                  "RATIONAL_PRODUCER":loc(producer)})
    purpose = ("Evaluación focal posterior al operador de modos enteros publicado. Las cinco etapas "
               "se heredan como contexto de la serie, no se vuelven a demostrar mediante Euler--Maclaurin. "
               "Este recibo no declara autonomía completa del VIII, ni positividad de Weil, ni RH, "
               "ni cierre del catálogo de constantes y masas. No autoriza compilar el PDF público.")
    r["universal_genealogy"]["scope_semantics"] = {"mode":"INHERITED_NORMATIVE_CONTEXT",
        "source_receipt":loc(INHERITED), "catalogue_or_terminal_proof_by_local_checks":False}
    r["foundation"]["inherited_receipt"] = loc(INHERITED)
    r["foundation"]["inheritance_is_new_global_reproof"] = False
    target = "VIII_FINITE_PARTS_INTERVALS_AFTER_NATIVE_INTEGER_MODES"
    statement = ("Desde los modos enteros publicados por las formas normales, Z(s)=sum n^-s admite "
                 "la continuación Euler--Maclaurin con resto explícito; las fórmulas de capítulo04 "
                 "producen intervalos racionales para FP_1 Z y Z(3), y Z(-1)=-1/12 exactamente.")
    falsifier = ("Cambiar la hoja aditiva o el residuo-cociente del sucesor; introducir cifras objetivo; "
                 "omitir el término 1/(2N), un término de Bernoulli o su resto; presentar la evaluación "
                 "regularizada como suma ordinaria; usar estos controles como prueba de positividad de Weil.")
    r.update({"receipt_id":target,"scope_kind":"MODULE","receipt_purpose":purpose,
        "normative_context_semantics":purpose,"provenance":"CERTIFICADO_NUEVO",
        "proof_strength":"DEMOSTRADO_CON_ESTRUCTURA_DE_PARTIDA_EXPLICITA",
        "conclusion_status":"CLOSED_IN_HMT_DOMAIN","residual_if_any":None,
        "global_falsifier":falsifier,
        "whole_article_closed":False,"pdf_compilation_authorized_by_this_receipt":False,
        "target":{"statement":statement,"result_id":target,
            "domain":"PublishedPositiveIntegerModes","codomain":"ExactRationalIntervalsAndRegularizedValue",
            "closure_criterion":"Pruebas de capítulos01 y04; cotas racionales y controles ejecutables posteriores.",
            "target_family":"POST_CONTINUUM_HMT","causal_cutoff":"ESTRUCTURA_DISCRETA_CONTINUO",
            "causal_cutoff_reason":"Se aplica un funcional a modos publicados; no se reconstruye el estado completo a partir de su escalar.",
            "forbidden_generator_inputs":["TARGET_EULER_MASCHERONI","TARGET_APERY","EXTERNAL_ZETA_VALUE"]}})
    r["result_maps"] = [{"id":"VIII_PUBLISHED_NATIVE_MODES","statement":"Publicación de formas normales y operatoria entera.",
        "input_object":"C_cont_generated","domain":"C_cont^disc","codomain":"PublishedPositiveIntegerModes",
        "output_object":"native_positive_modes","source_family":"HMT","generator_inputs":["C_cont_generated"],
        "map":"Leer prefijos TPK, normalizar por beta9 y conservar la aritmética de las formas normales; el sucesor nativo enumera las palabras positivas.",
        "proof_locator":loc(native),"falsifier":"Confundir la enumeración de formas normales con una biyección de todas las historias."},
        {"id":target,"statement":statement,"input_object":"native_positive_modes","domain":"PublishedPositiveIntegerModes",
        "codomain":"ExactRationalIntervalsAndRegularizedValue","output_object":"finite_parts_output",
        "source_family":"HMT","generator_inputs":["native_positive_modes"],
        "map":"Z=sum n^-s; EM con Bernoulli racional y resto; parte finita en1; evaluación3; continuación a-1. N,p,M sólo regulan precisión.",
        "proof_locator":loc(source),"falsifier":falsifier}]
    r["conventional_uses"] = [{"name":"Euler--Maclaurin, Fourier de Bernoulli y reconocimiento de Euler--Mascheroni/Apéry",
        "role":"PROOF_LANGUAGE","locator":loc(source),"occurs_after_hmt_output":True,
        "selects_hmt_state":False,"selects_route":False,"sets_generators":False,"sets_coefficients":False,
        "target_value_used_as_input":False,
        "scope_note":"La fórmula analítica define la lectura posterior sobre modos ya publicados; no decide la dinámica de las semillas."}]
    r["proof_layers"] = {"finite":"Recurrencia racional de Bernoulli, sucesor nativo y evaluación de sumas finitas.",
        "compatibility":"La unicidad de continuación identifica los distintos horizontes y órdenes sobre dominios comunes.",
        "limit":{"required":True,"statement":"El resto EM tiene cota explícita tendente a cero al aumentar N con p fijo; la serie del logaritmo lleva cola geométrica.",
                 "proof_locator":loc(source),"formula":"|R_Np(s)|<=|B2p| |(s)2p| N^(1-Re(s)-2p)/((2p)!(Re(s)+2p-1))",
                 "finite_levels":"Sumas EM de horizonte entero N y orden p, con intervalos racionales de logaritmo de longitud M; Re(s)>1-2p.",
                 "bonding_maps":"Prolongar N por el sucesor nativo y M por una suma racional adicional; comparar lecturas de órdenes p sobre sus dominios comunes. Los intervalos no se suponen anidados.",
                 "compatibility_identity":"EM(N,p;s)+R(N,p;s)=Z(s)=EM(N+1,p;s)+R(N+1,p;s), primero para Re(s)>1 y después por continuación única; la identidad de la cola de logaritmo conserva su suma al aumentar M.",
                 "limit_object":"FP en s=1 de Z, Z(3), y la continuación holomorfa en s=-1; las dos primeras lecturas son límites únicos de aproximaciones con error explícito, y la tercera es una evaluación exacta.",
                 "proof":"En capítulo 04 se integra por partes la fórmula EM con el Bernoulli periódico, se acota su integral por N^(1-Re(s)-2p)/(Re(s)+2p-1), se toma la parte finita en s=1 y se obtiene la cota |B2p|/(2p N^(2p)); para el logaritmo se domina la cola por una serie geométrica. Estas cotas tienden a cero con p fijo y N,M crecientes en los dominios indicados."},
        "recognition":"La parte finita coincide con lim(H_N-logN); Z(3) con la suma convergente de cubos inversos."}
    parts = []
    anchors = []
    for stage in r["stages"]:
        anchor = "RESIDENCIA HEREDADA "+stage["id"]
        anchors.append({"stage":stage["id"],"text":anchor})
        parts.extend([anchor,Path(stage["owner"]["path"]).read_text()])
    for stage,p in (("HMT_OUTPUT",native),("CONVENTIONAL",source)):
        anchor = "RESIDENCIA FOCAL "+stage
        anchors.append({"stage":stage,"text":anchor})
        parts.extend([anchor,p.read_text()])
    assembled = "\n\n".join(parts)
    out = ROOT/"gestion/recibo_partes_finitas"
    out.mkdir(exist_ok=True)
    composite = out/"FUENTE_COMPUESTA.txt"
    composite.write_text(assembled)
    r["artifact"] = {"path":str(composite),"sha256":sha(composite),"kind":"MODULE","anchors":anchors,
        "binding_note":"Instantánea focal e herencia explícita; no es el main de un PDF ni una acreditación de inclusión material en ese PDF."}
    r["genealogical_nine_fields"] = {
        "1_app_object_domain_sheets_operation":r["stages"][0],
        "2_trit_state_regime_orientation":r["stages"][1],
        "3_tpk_operator_domain_codomain_action":r["stages"][2],
        "4_coefficient_origins":"Bernoulli por recurrencia; N=81,p=8,M=120 son horizontes de precisión y no valores objetivo.",
        "5_information_preservation":"Las formas normales conservan residuo-cociente; la lectura escalar no afirma invertir toda historia.",
        "6_enriched_state_and_continuum":{"mode":"INHERITED_NOT_REPROVED","stages":r["stages"][3:]},
        "7_hmt_output_before_realization":r["result_maps"][0],
        "8_posterior_realization_and_falsifier":{"realization":r["result_maps"][1],"falsifier":falsifier},
        "9_material_owners":r["source_manifest"]}
    path = out/"RECIBO_GENEALOGIA_PARTES_FINITAS.json"
    path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n")
    result = subprocess.run([sys.executable,"-I","-S",str(PROJECT/"tools/verificar_genealogia_unica_hmt.py"),"--receipt",str(path)],capture_output=True,text=True)
    (out/"RESULTADO_VALIDACION.txt").write_text(result.stdout+result.stderr)
    print(result.stdout+result.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)
    inherited_constants = INHERITED.with_name("RECIBO_CONSTANTES_S0.json")
    old_constants = json.loads(inherited_constants.read_text())
    constants_gate = Path("/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py")
    for chapter in (source, ROOT/"manuscrito/05_CONSTRUCCION_CORRELATIVA_DEL_CONTINUO.md"):
        genealogy = copy.deepcopy(old_constants["genealogy"])
        genealogy["tpk"] = {
            "operator":"U_t y Gamma9 del contexto heredado; publicación normalizada de prefijos y transporte de historias",
            "domain":"Estados con hoja, orientación, residuo, cociente, ruta y memoria declarados en el núcleo",
            "codomain":"Estado enriquecido; historias y formas normales publicadas por sus lectores",
            "action":"La composición conserva las actualizaciones afines y la prolongación. El capítulo01 especifica la publicación normalizada; 04 evalúa después los modos enteros y 05 reúne identidades locales de sus historias."}
        genealogy["source_locators"] = [str(native), str(source), str(ROOT/"manuscrito/05_CONSTRUCCION_CORRELATIVA_DEL_CONTINUO.md"),
                                         r["formal_kernel"]["typed_operator_graph"]["path"]]
        c = {"schema_version":"1.1", "artifact":str(chapter),
             "local_artifact_sha256":sha(chapter), "result_id":target+"_"+chapter.stem[:2],
             "genealogy":genealogy,
             "inherited_receipt":loc(inherited_constants),
             "control_scope":"Control focal del rol causal de las entradas y publicaciones. El contrato general se conserva como contexto normativo heredado; este control no demuestra su catálogo ni los resultados terminales. No es licencia de compilación ni certificado de autonomía del VIII.",
             "inherited_normative_scope":{"mode":"INHERITED_NOT_REPROVED", "declared_scope_is_not_local_proof":True,
                                          "catalogue_and_terminals_certified_by_delta":False},
             "local_results":[{"causal_role":"POST_PUBLICATION_READER_OR_LOCAL_IDENTITY",
                               "proof_owner":loc(chapter), "whole_article_closed":False,
                               "global_weil_positivity_certified":False,
                               "target_values_used_as_inputs":False}],
             "focal_genealogical_receipt":loc(path),
             "pdf_compilation_authorized":False}
        cp = out/("RECIBO_CONSTANTES_"+chapter.stem[:2]+".json")
        cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
        check = subprocess.run([sys.executable,"-I","-S",str(constants_gate),"--audit",str(chapter),"--receipt",str(cp)],capture_output=True,text=True)
        (out/("RESULTADO_CONSTANTES_"+chapter.stem[:2]+".txt")).write_text(check.stdout+check.stderr)
        print(chapter.stem+": "+check.stdout+check.stderr)
        if check.returncode:
            raise SystemExit(check.returncode)


if __name__ == "__main__":
    main()
