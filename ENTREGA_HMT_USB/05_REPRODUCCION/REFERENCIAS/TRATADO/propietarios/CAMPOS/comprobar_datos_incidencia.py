#!/usr/bin/env python3
"""Run the preserved finite checks using this package's manifested locations."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    out=ROOT/'resultados/datos_incidencia';out.mkdir(parents=True,exist_ok=True)
    receipt=out/'VERIFICATION.json'
    receipt.write_text(json.dumps(dict(status='RUNNING'))+'\n')
    try:
        runner=module(ROOT/'reproducir_cadena.py','incidence_chain_runner')
        v=runner.configure(ROOT);plan=v.load_plan(ROOT)
        manifested={r['path']:r for r in json.loads((ROOT/'MANIFIESTO.json').read_text())['files']}
        for relative in ['python/union/check_golay.py','python/union/check_incidence_chart.py',
                'datos/union/incidence_chart_132.json','fuentes/union/excepcional.tex']:
            if v.sha_file(ROOT/relative)!=manifested[relative]['sha256']:
                raise RuntimeError('Changed input '+relative)
        checker=module(ROOT/'python/union/check_incidence_chart.py','preserved_incidence_checker')
        checker.SOURCES=[(plan['graph'][n]['source'],'manifested active Lean source') for n in
            ['CoxeterNeighbor','SectorIncidenceData','PaleyCharacterConstruction']]+[
            (ROOT/'fuentes/union/excepcional.tex','521-566: manuscript realization chart'),
            (ROOT/'python/union/check_golay.py','binary encoder and dodecad')]
        generated=checker.certificate()
        published=json.loads((ROOT/'datos/union/incidence_chart_132.json').read_text())
        keys=[k for k in generated if k not in ['sources','generator_script_sha256']]
        for key in keys:
            if json.loads(json.dumps(generated[key]))!=published[key]:
                raise RuntimeError('Certificate data differ: '+key)
        command=[sys.executable,'-I','-S',str(ROOT/'python/union/check_golay.py')]
        p=subprocess.run(command,text=True,capture_output=True,timeout=60)
        if p.returncode or 'PASS_CLASSICAL_BINARY_GOLAY_EXPLORATION' not in p.stdout:
            raise RuntimeError(p.stdout+p.stderr)
        result=dict(status='PASS_PACKAGE_INCIDENCE_DATA',full_support_equality=True,
            compared_fields=keys,script_stdout=p.stdout,source_files=generated['sources'],
            chart_sha256=v.sha_file(ROOT/'datos/union/incidence_chart_132.json'),
            scope='Finite reproduction; Lean proofs are checked separately by reproducir_productos.py')
        code=0
    except Exception as e:
        result=dict(status='FAIL',error=str(e));code=1
    receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(result['status'],flush=True)
    if code: print(result['error'],flush=True)
    return code

if __name__=='__main__':raise SystemExit(main())
