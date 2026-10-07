#!/usr/bin/env python3
"""Portable local checks and optional LuaLaTeX compilation for Article III REV04."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build',action='store_true');ap.add_argument('--receipt',type=Path)
    args=ap.parse_args()
    require(not sys.flags.optimize,'Use normal Python: one inherited regression script contains assert')
    manifest=json.loads((ROOT/'MANIFIESTO_REV04.json').read_text())
    for row in manifest['files']:
        p=(ROOT/row['path']).resolve();require(p.is_relative_to(ROOT),'Unsafe manifest path')
        require(p.is_file() and sha(p)==row['sha256'],'Missing/changed file: '+row['path'])
    results=[]
    with tempfile.TemporaryDirectory(prefix='hmt-iii-rev04-check-') as temp:
        commands=[
          ['technical/rev04/verificar_revision.py'],
          ['technical/rev04/verificar_enlace_velocidad.py'],
          ['technical/verificar_delta_rev02.py','--receipt',str(Path(temp)/'delta.json')],
          ['technical/cantera_radion/verificar_radion_iii.py'],
          ['technical/propuestas/verificar_vacancias_prefactor.py']]
        for command in commands:
            full=[sys.executable,'-I','-S',str(ROOT/command[0]),*command[1:]]
            p=subprocess.run(full,cwd=temp,text=True,capture_output=True)
            require(p.returncode==0,p.stdout+p.stderr)
            results.append({'script':command[0],'returncode':p.returncode,'stdout':p.stdout.strip()})
    built=None
    if args.build:
        build=ROOT/'reproduccion_rev04';cache=build/'tex-cache';cache.mkdir(parents=True,exist_ok=True)
        env=dict(os.environ,TEXMFVAR=str(cache),TEXMFCACHE=str(cache))
        tex=shutil.which('lualatex')
        if not tex and Path('/Library/TeX/texbin/lualatex').exists():tex='/Library/TeX/texbin/lualatex'
        require(bool(tex),'LuaLaTeX required, together with STIX Two Text and STIX Two Math')
        for i in range(3):
            p=subprocess.run([tex,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+str(build),'main.tex'],cwd=ROOT,env=env,text=True,capture_output=True)
            (build/f'pass-{i+1}.log').write_text(p.stdout+'\n'+p.stderr)
            require(p.returncode==0,p.stdout[-5000:]+p.stderr)
        log=(build/'main.log').read_text(errors='replace')
        bad=[line for line in log.splitlines() if any(s in line for s in ('Overfull \\hbox','Overfull \\vbox','Missing character:','undefined references','undefined on input','multiply defined'))]
        require(not bad,'\n'.join(bad));built={'path':str(build/'main.pdf'),'sha256':sha(build/'main.pdf')}
    receipt={'status':'PASS_REPRODUCTION_PORTABLE_III_REV04_FOCAL','files_verified':len(manifest['files']),'checks':results,'build':built,
      'scope':'Hashes, preserved local sources and finite regression tests. Historical canonical receipts are conserved as provenance and not rerun from external paths. No primary E108 generator or global scientific autonomy is certified.'}
    if args.receipt:args.receipt.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
