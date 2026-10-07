"""Ejecuta la cadena de controles existente y conserva su salida completa.

Las pruebas analíticas están en las notas. Este informe no certifica una
formalización Lean ni el cierre global de las cuatro interacciones.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
scripts = [
    'verificar_composicion.py',
    'quantum/verificar_memoria_dominio_algebra.py',
    'quantum/anomalias_quirales.py',
    'quantum/verificar_acoplamiento_gravitatorio_memoria.py',
    'quantum/verificar_acoplamiento_finito.py',
    'quantum/verificar_torsion_fock.py',
    'quantum/verificar_refinamiento_dinamico.py',
    'quantum/verificar_accion_memoria.py',
    'quantum/verificar_dimension_densidad.py',
    'quantum/verificar_trit_curvaturas_deformaciones.py',
    'quantum/verificar_limite_materia_memoria.py',
]
for optional in ('verificar_suspension_reloj.py', 'verificar_legendre_reloj.py',
                 'verificar_conmutador_espacial.py', 'verificar_deformaciones_espaciales.py',
                 'verificar_limite_espacial_quiral.py', 'verificar_supercargas_doble_proyeccion.py',
                 'verificar_curvatura_memoria.py', 'verificar_cociclo_accion_curvatura.py',
                 'verificar_curvatura_tpk_refinamiento.py', 'verificar_curvatura_deformaciones_pch.py',
                 'verificar_gravedad_conjunta.py', 'verificar_autoinercia_acoplamiento.py',
                 'verificar_retroaccion_restricciones.py'):
    if (ROOT/'quantum'/optional).is_file():
        scripts.append('quantum/'+optional)

results = []
for name in scripts:
    path = ROOT/name
    run = subprocess.run([sys.executable, '-I', '-S', str(path)], cwd=ROOT,
                         capture_output=True, text=True, timeout=120)
    result = {
        'script': name,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'command': [sys.executable, '-I', '-S', str(path)],
        'returncode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr,
    }
    results.append(result)
    print(('PASS' if run.returncode == 0 else 'FAIL') + ': ' + name, flush=True)

report = {
    'scope': 'Controles focales reproducidos; las demostraciones analíticas están en los Markdown',
    'quantum_four_interaction_closure_certified': False,
    'lean_formalization_claimed': False,
    'passed': sum(r['returncode'] == 0 for r in results),
    'total': len(results), 'results': results,
    'notes': [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in sorted((ROOT/'quantum').glob('*.md'))],
}
(ROOT/'RESULTADOS_REPRODUCIDOS.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
if report['passed'] != report['total']:
    raise SystemExit(1)
print(f"CONTROLES_FOCALES_REPRODUCIDOS: {report['passed']}/{report['total']}")
