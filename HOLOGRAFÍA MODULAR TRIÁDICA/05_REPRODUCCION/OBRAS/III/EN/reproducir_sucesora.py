#!/usr/bin/env python3
"""Entrada portable: integridad, continuidad exacta y controles focales.

No declara reejecutados todos los productores del corpus ni una prueba física
global. Los generadores conservados se consultan en su orden documentado.
"""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');args=p.parse_args()
manifest=json.loads((ROOT/'MANIFIESTO_SUCESORA.json').read_text())
for row in manifest['files']:
    path=ROOT/row['path']
    assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],row['path']
print('PASS_INTEGRIDAD_SUCESORA',len(manifest['files']),flush=True)
commands=manifest['portable_checks']
for command in commands:
    cmd=[sys.executable,*command]
    r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    print('PASS_CONTROL_FOCAL',command[-1],flush=True)
if args.build:
    tex=shutil.which('lualatex')
    if not tex:raise RuntimeError('Se requiere LuaLaTeX con STIX Two.')
    out=ROOT/'reproduccion';out.mkdir(exist_ok=True)
    env=dict(os.environ);env.update(TEXMFVAR=str(out/'tex-cache'),TEXMFCACHE=str(out/'tex-cache'))
    for n in range(3):
        r=subprocess.run([tex,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory=reproduccion','main.tex'],cwd=ROOT,env=env,text=True,capture_output=True)
        (out/f'compilacion_{n+1}.txt').write_text(r.stdout+'\n'+r.stderr)
        if r.returncode:raise RuntimeError(r.stdout[-4000:]+r.stderr[-2000:])
    log=(out/'main.log').read_text(errors='replace')
    bad=[line for line in log.splitlines() if any(x in line for x in ('Overfull \\hbox','Overfull \\vbox','Missing character:','undefined references','undefined on input','multiply defined'))]
    assert not bad,bad
    print('PDF_REPRODUCIDO',out/'main.pdf')
print('PASS_REPRODUCCION_SUCESORA_FOCAL')
