#!/usr/bin/env python3
"""Verificador documental del expediente editorial v2 de zeta; sólo lectura.
No prueba RH, no autentica por sí mismo la identidad del autor, no escribe registros.
"""
from pathlib import Path
import argparse, hashlib, json, runpy, sys

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def ensure(ok, message):
    if not ok:
        raise ValueError(message)

def reference(row):
    path=Path(row["path"])
    ensure(path.is_file() and not path.is_symlink() and sha(path)==row["sha256"], "Referencia alterada: "+str(path))
    return path

def verify(certificate, canvas=None):
    data=read(certificate)
    ensure(data["scope"]=="EDITORIAL_DOCUMENT_IDENTITY_AND_STATUS_PRESERVATION", "Alcance incorrecto")
    local=reference(data["local_preflight"])
    checker=reference(data["local_checker"])
    module=runpy.run_path(str(checker), run_name="zeta_editorial_check")
    module["verify_receipt"](local)
    ensure(data["source_files"]==read(local)["snapshot"]["graph"]["files"], "Inventario difiere del preflight local")
    root=Path(data["source_root"])
    for row in data["source_files"]:
        ensure(sha(root/row["path"])==row["sha256"], "Fuente alterada: "+row["path"])
    for row in data["predecessor_sources"]:
        reference(row)
    approval=read(reference(data["approval_event"]))
    mandate=reference(approval["mandate"])
    text=mandate.read_text()
    ensure(approval["approved"] and approval["approved_by"]=="Rubén", "Encargo no registrado")
    ensure(approval["author_review_of_exact_matrix_or_hashes"] is False, "Aprobación de hashes no atribuible")
    ensure(approval["scope"]=="AUTHORIAL_EDITORIAL_APPROVAL_ONLY", "Alcance del encargo incorrecto")
    for quote in approval["quotes"]:
        ensure(quote in text, "Cita no conservada en encargo")
    status=read(reference(data["scientific_status_snapshot"]))
    current={r["id"]:r for r in read(data["claims_registry"])["claims"]}
    for row in status["claims"]:
        ensure(row["id"] in current, "Claim previo retirado")
        ensure(all(current[row["id"]].get(k)==row.get(k) for k in ("assertion_status","scope_type")), "Estatuto científico previo cambiado")
    for row in data["results"]:
        for block in row["source_blocks"]:
            text=(root/block["path"]).read_text()
            a,b=block["begin_marker"],block["end_marker"]
            ensure(text.count(a)==text.count(b)==1, "Bloque no único")
            payload=text.split(a,1)[1].split(b,1)[0].strip().replace("\r\n","\n").replace("\r","\n")
            ensure(hashlib.sha256(payload.encode()).hexdigest()==block["sha256"], "Bloque alterado")
    if canvas:
        cv=read(canvas)
        reference(cv["approval_event_ref"]); reference(cv["matrix_ref"]); reference(cv["revision_delta"])
        ensure(cv["approved"] and cv["approved_by"]=="Rubén", "Canvas sin alcance autorizado")
        ensure(cv["approval_scope"]=="AUTHORIAL_EDITORIAL_APPROVAL_ONLY", "Alcance canvas incorrecto")
        ensure(cv["author_review_of_exact_matrix_or_hashes"] is False and cv["scientific_validation_by_author"] is False, "Promoción indebida del encargo")
        ensure(cv["approved_matrix_sha256"]==cv["matrix_ref"]["sha256"]==cv["matrix_sha256"], "Matriz divergente")
        ensure(cv["results"]==data["results"], "Residencias del canvas divergentes")
    return data

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--certificate",required=True,type=Path);p.add_argument("--canvas",type=Path)
    a=p.parse_args()
    try:
        d=verify(a.certificate,a.canvas)
        print(("PASS_EDITORIAL_CANVAS " if a.canvas else "PASS_EDITORIAL_CONTINUITY ")+json.dumps({"scope":d["scope"],"source_files":len(d["source_files"]),"global_weil_certified":False,"rh_certified":False},ensure_ascii=False))
        return 0
    except (ValueError,KeyError,OSError) as e:
        print("FAIL_EDITORIAL_CONTINUITY "+str(e),file=sys.stderr);return 1
if __name__=="__main__":
    raise SystemExit(main())

