#!/usr/bin/env python3
"""Controles exactos focales de la nota; no prueba CH ni certifica una edición.

Sin argumentos imprime JSON. --receipt escribe sólo el recibo solicitado.
Las fuentes y los PDF no se modifican. Sólo biblioteca estándar.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PROJECT = Path("/Users/ruben/Documents/New project")
F = HERE.parents[1] / "CORPUS/FUENTE"
ARTICLE = HERE.parents[1] / "ELECTRON/ARTICULO_HELICIDAD_ELECTRON_20260910"
NOTE = HERE / "ACOPLAMIENTO_PRESENTE_Y_RECONSTRUCCION_20260910.md"
SOURCES = {
    "observer": F / "manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/12a_observador_instrumentos.tex",
    "frames": F / "manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/14_autoinercia_mach.tex",
    "euler": F / "manuscrito/sections/hmt/09b_algebras_cuadraticas.tex",
    "hensel": F / "manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex",
    "full_update": F / "manuscrito/sections/hmt/20_arquitectura_operatoria_tpk_actualizada.tex",
    "present": F / "manuscrito/sucesor_102/radion_52/c52_12_conservacion_evolutiva.tex",
    "measurement": F / "manuscrito/integracion_83/parte_iv/body/B012_ch54_medicion_cuantica_genealogica_38d76bc63ccd_01a_medicion_cuantica_genealogica_rev2.tex",
    "center": ARTICLE / "sections/centro_electronico_registros.tex",
    "signature_code": ARTICLE / "technical/verificar_memoria_555555.py",
    "global_capacity": F / "manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex",
}

def need(p, message):
    if not p:
        raise AssertionError(message)

def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def mul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def inv_det(a):
    n = len(a)
    m = [[Q(x) for x in a[i] + eye(n)[i]] for i in range(n)]
    det = Q(1)
    for j in range(n):
        pivot = next(i for i in range(j,n) if m[i][j])
        if pivot != j:
            m[j],m[pivot] = m[pivot],m[j]
            det = -det
        scale = m[j][j]
        det *= scale
        m[j] = [x/scale for x in m[j]]
        for i in range(n):
            if i != j:
                scale = m[i][j]
                m[i] = [x-scale*y for x,y in zip(m[i],m[j])]
    return [row[n:] for row in m], det

def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def smul(t,a):
    return [[t*x for x in row] for row in a]

def mv(v,a):
    return mul([list(v)], a)[0]

def ints(v):
    need(all(Q(x).denominator == 1 for x in v), "integridad")
    return [int(x) for x in v]

def shear(t):
    return [[1,t],[0,1]]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    htext = SOURCES["hensel"].read_text()
    match = re.search(r"\nA=\s*\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", htext, re.S)
    need(match is not None, "matriz A_H no localizada en fuente")
    ah = [[int(x.strip()) for x in row.split("&")]
          for row in match[1].strip().split(r"\\") if row.strip()]
    need(len(ah)==6 and all(len(r)==6 for r in ah), "dimensión A_H")
    ahi, det = inv_det(ah)
    need(det==1 and all(x.denominator==1 for r in ahi for x in r), "unimodularidad")
    ahi = [ints(r) for r in ahi]
    need(mul(ah,ahi)==eye(6)==mul(ahi,ah), "inversa bilateral")

    residue_cases = 0
    v = [1,-2,0,3,-1,2]
    for u in product(range(3), repeat=6):
        x = mv([u[i]+3*v[i] for i in range(6)], ahi)
        y = mv(x, ah)
        got_u = [int(t % 3) for t in y]
        got_v = [(t-r)//3 for t,r in zip(y,got_u)]
        need(got_u==list(u) and got_v==v, "par residuo-cociente")
        residue_cases += 1
    witness = mv([3*t for t in v], ahi)
    need(witness != [0]*6 and all(t%3==0 for t in mv(witness,ah)),
         "residuo nulo con memoria no nula")

    history_cases = 0
    for start in ([0]*6, [1,2,3,4,5,6], [-7,3,-2,9,0,1]):
        for length in (1,2,9,27):
            x = list(start)
            residues = []
            states = [x]
            for _ in range(length):
                y = mv(x,ah)
                u = [t%3 for t in y]
                x = [(t-r)//3 for t,r in zip(y,u)]
                residues.append(u)
                states.append(x)
            back = list(x)
            for j in reversed(range(length)):
                back = mv([residues[j][i]+3*back[i] for i in range(6)],ahi)
                need(back==states[j], "reconstrucción de tramo")
            inverse_power = eye(6)
            polynomial = [0]*6
            for j,u in enumerate(residues):
                inverse_power = mul(inverse_power,ahi)
                term = mv(u,inverse_power)
                polynomial = [a+3**j*b for a,b in zip(polynomial,term)]
            tail = mv(x,inverse_power)
            need([a+3**length*b for a,b in zip(polynomial,tail)]==list(start),
                 "fórmula de frontera (5)")
            history_cases += 1

    n = [[0,1],[0,0]]
    need(mul(n,n)==[[0,0],[0,0]], "N nilpotente")
    frames = [eye(2), [[1,1],[0,1]], [[1,1],[1,2]]]
    relative_cases = 0
    for a,b in product((Q(-2),Q(0),Q(1,3),Q(5)), repeat=2):
        ts,tm = shear(a),shear(b)
        need(mul(shear(-b),ts)==shear(a-b), "régimen de umbral")
        need(mul(ts,shear(-a))==eye(2), "ida y retorno")
        for fs,fm in product(frames,repeat=2):
            fmi,_ = inv_det(fm)
            joint_m_inv,_ = inv_det(mul(tm,fm))
            direct = mul(joint_m_inv,mul(ts,fs))
            rhs = mul(mul(mul(fmi,shear(-b)),ts),fs)
            need(direct==rhs, "marco relativo (2)")
            if a==b:
                need(direct==mul(fmi,fs), "transporte común")
            relative_cases += 1

    ternary = []
    for length in range(1,5):
        rows = list(product(range(3),repeat=length))
        exhaustive = 0
        for s,m in product(rows,repeat=2):
            out = tuple((a+b)%3 for a,b in zip(s,m))
            recovered = tuple((a-b)%3 for a,b in zip(out,s))
            need(recovered==m, "acoplamiento reversible ternario")
            need(out[:-1]==tuple((a+b)%3 for a,b in zip(s[:-1],m[:-1])),
                 "naturalidad por truncamiento")
            exhaustive += 1
        allowed_free = len(rows)
        allowed_zero = sum(all(t==0 for t in s) for s in rows)
        need(allowed_zero==1, "fibra de resultado nulo")
        ternary.append({"depth":length,"full_couplings":exhaustive,
                        "free_records":allowed_free,"zero_record":allowed_zero})

    # Este script existente, leído antes de ejecutar, sólo escribe stdout sin --receipt.
    result = subprocess.run([sys.executable,"-I","-S","-B",str(SOURCES["signature_code"])],
                            check=True,capture_output=True,text=True,timeout=30)
    sig = json.loads(result.stdout)
    need(sig["status"]=="PASS_MEMORIA_555555_324_RUTAS","certificado de firma")
    need(sig["refinement_class_counts"]==[26,28,28],"refinamiento conservado")
    paths = {**SOURCES, "note":NOTE, "control":Path(__file__).resolve()}
    report = {
        "status":"PASS_CONTROLES_FOCALES_ACOPLAMIENTO",
        "scope":"Identidades finitas exactas y controles declarados en la nota",
        "is_ch_proof":False,
        "is_full_physical_observer_certificate":False,
        "arbitrary_depth_proof":"Proposición y prueba escrita en sección 6; no inferida de muestras",
        "hensel_matrix_det":int(det),
        "all_canonical_residues_checked":residue_cases,
        "exact_boundary_histories":history_cases,
        "relative_frame_cases":relative_cases,
        "ternary_model_control_not_physical_identification":ternary,
        "reused_signature_certificate":{
            k:sig[k] for k in ("status","state_count","refinement_class_counts",
                              "class_size_histogram","successor_histogram")},
        "source_bindings":{k:{"path":str(p),"sha256":sha256(p.read_bytes()).hexdigest()}
                           for k,p in paths.items()},
        "pdfs_or_sources_modified":False,
    }
    out = json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.receipt:
        target=args.receipt.resolve()
        need(target.parent==HERE,"el recibo debe quedar junto al control")
        target.write_text(out)
    print(out,end="")

if __name__=="__main__":
    main()

