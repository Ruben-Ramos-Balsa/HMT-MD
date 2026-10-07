"""Comprueba exclusivamente el prefijo archivístico autorizado; no escribe."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
RESOLVER = Path('/Users/ruben/Documents/HMT2/CONTINUIDAD_EDITORIAL/resolver_ultima_autoridad_hmt_md.py')
SNAPSHOT = RESOLVER.with_name('ULTIMA_AUTORIDAD_HMT_MD.json')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

before = (HERE / 'resolver_antes.py').read_bytes()
after = (HERE / 'resolver_despues.py').read_bytes()
needle = b'    "EDITION_FR_HMT_",\n'
require(before.count(needle) == 1, 'Antecedente ambiguo')
require(after == before.replace(needle, needle + b'    "EDITION_FR_MANUSCRITS_",\n'), 'Cambio distinto del prefijo autorizado')
require(RESOLVER.read_bytes() == after, 'El resolver activo difiere del sucesor comprobado')
snapshot = (HERE / 'snapshot_antes.json').read_bytes()
require(SNAPSHOT.read_bytes() == snapshot, 'Snapshot modificado')
command = [sys.executable, '-I', '-S', '-B', str(RESOLVER), '--check']
process = subprocess.run(command, capture_output=True, text=True)
require(process.returncode == 0 and process.stdout.startswith('PASS_ULTIMA_AUTORIDAD_HMT_MD\n'), process.stdout + process.stderr)
require(SNAPSHOT.read_bytes() == snapshot, 'La comprobación modificó el snapshot')
print(json.dumps({'status': 'PASS_RECONCILIACION_PREFIJO_ARCHIVISTICO',
    'before_sha256': digest(before), 'after_sha256': digest(after),
    'snapshot_before_sha256': digest(snapshot), 'snapshot_after_sha256': digest(SNAPSHOT.read_bytes()),
    'snapshot_byte_identical': True, 'command': command, 'returncode': process.returncode,
    'stdout': process.stdout, 'stderr': process.stderr,
    'scope': 'Sólo exclusión de copias archivísticas francesas en el recuento de autoridad; ninguna modificación de corpus, índice, sello o selección editorial2249.',
    'scientific_validation': False}, ensure_ascii=False, indent=2))
