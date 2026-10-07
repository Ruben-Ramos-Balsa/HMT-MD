#!/usr/bin/env python3
"""Reproducción focal portable. No compila el PDF ni certifica autonomía global."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def safe_path(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), 'Ruta fuera del paquete: ' + str(relative))
    return path

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def check_originals(check_sources=False):
    path = ROOT / 'MANIFIESTO_ORIGINALES.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    checked = []
    for item in manifest['files']:
        p = safe_path(ROOT, item['destination'])
        require(p.is_file() and digest(p) == item['sha256'], 'Integridad original: ' + str(p))
        if check_sources:
            require(digest(Path(item['source'])) == item['sha256'], 'Fuente local alterada: ' + item['source'])
        checked.append({'path': item['destination'], 'sha256': digest(p)})
    for rel in ('D07/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md', 'B06/c51_barbero_area_informacion.tex'):
        require(digest(ROOT / 'originales/BORRADOR_02/01_FUENTES' / rel)
                == digest(ROOT / 'originales/ARTICULO_II_REV05' / rel),
                'Propietario B02/II diferente: ' + rel)
    return {'status': 'PASS_24_ORIGINALES_INTEGROS', 'count': len(checked), 'files': checked,
            'source_comparison': check_sources, 'manifest_sha256': digest(path),
            'D07_B06_identity_B02_vs_II': True}

def check_article_copies(check_sources=False):
    article = ROOT.parent.parent
    entries = []
    for subdir, name in (
        ('base_articulo_I', 'MANIFIESTO_COPIA_NUCLEO.json'),
        ('base_articulo_I', 'MANIFIESTO_ADICION_EXCEPCIONAL.json'),
        ('base_articulo_II', 'MANIFIESTO_DEPENDENCIAS_II.json'),
    ):
        manifest_path = article / subdir / name
        require(manifest_path.is_file(), 'Manifesto de la entrega III ausente: ' + str(manifest_path))
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        for item in manifest['files']:
            relative = item.get('relative_path', item['destination'])
            require(not Path(relative).is_absolute(), 'Se requiere una ruta relativa de copia')
            p = safe_path(article / subdir, relative)
            require(digest(p) == item['sha256_destination'] == item['sha256_source'], 'Copia modificada: ' + str(p))
            if check_sources:
                require(digest(Path(item['source'])) == item['sha256_source'], 'Fuente de copia modificada: ' + item['source'])
            entries.append({'path': subdir + '/' + relative, 'sha256': digest(p)})
    return {'status': 'PASS_COPIAS_I_II_BYTE_IDENTICAS', 'count': len(entries),
            'source_comparison': check_sources, 'files': entries}

def seal():
    files = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        relative = p.relative_to(ROOT)
        if relative.parts[0] == 'ejecuciones' or '__pycache__' in relative.parts or p.name == 'SELLADO.json':
            continue
        files.append({'path': relative.as_posix(), 'sha256': digest(p), 'bytes': p.stat().st_size})
    data = {'scope': 'INTEGRIDAD_DE_ARCHIVOS_NO_FIRMA_INSTITUCIONAL_NI_PRUEBA_GLOBAL', 'files': files}
    path = ROOT / 'SELLADO.json'
    if path.exists():
        require(json.loads(path.read_text()) == data, 'Sellado existente distinto; crear una revisión, no reemplazar.')
    else:
        write_json(path, data)
    return {'status': 'PASS_SELLADO_TECNICO', 'count': len(files), 'sha256': digest(path)}

def check_seal():
    path = ROOT / 'SELLADO.json'
    require(path.is_file(), 'Falta SELLADO.json; etapa de preparación aún no sellada')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    for item in manifest['files']:
        p = safe_path(ROOT, item['path'])
        require(p.is_file() and digest(p) == item['sha256'], 'Fallo de integridad: ' + item['path'])
    return {'status': 'PASS_INTEGRIDAD_PAQUETE', 'count': len(manifest['files']), 'sha256': digest(path)}

def execute(script, arguments, stdout_path):
    command = [sys.executable, '-I', '-S', str(script), *map(str, arguments)]
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=60)
    stdout_path.write_text(process.stdout, encoding='utf-8')
    stdout_path.with_suffix('.stderr.txt').write_text(process.stderr, encoding='utf-8')
    require(process.returncode == 0, 'Ejecución fallida: ' + str(script) + '\n' + process.stderr)
    return json.loads(process.stdout), {'program': script.relative_to(ROOT).as_posix(),
            'program_sha256': digest(script), 'return_code': process.returncode,
            'stdout_sha256': digest(stdout_path)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seal', action='store_true', help='Preparación local: sellar archivos existentes, sin ejecutar pruebas')
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--check-article-copies', action='store_true', help='Requiere el árbol III completo junto al paquete')
    parser.add_argument('--check-sources', action='store_true', help='Sólo local: compara también rutas fuente originales de procedencia')
    parser.add_argument('--receipt', type=Path, default=ROOT / 'ejecuciones/REPRODUCCION.json')
    args = parser.parse_args()
    if args.seal:
        print(json.dumps(seal(), ensure_ascii=False))
        return
    stages = [check_seal(), check_originals(args.check_sources)]
    if args.check_article_copies:
        stages.append(check_article_copies(args.check_sources))
    receipt_path = args.receipt.resolve()
    require(receipt_path.is_relative_to(ROOT / 'ejecuciones'), 'Los recibos se escriben sólo en ejecuciones/')
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    if not args.integrity_only:
        nucleus_path = receipt_path.parent / 'NUCLEO_FINITO.json'
        info, execution = execute(ROOT / 'verificar_nucleo_finito.py', ['--receipt', nucleus_path],
                                  receipt_path.parent / 'nucleo.stdout.txt')
        require(info['status'] == 'PASS_NUCLEO_FINITO_REGLA_Y_REGISTRO_DECLARADOS', 'Estado inesperado del censo')
        stages.append({**execution, 'status': info['status'], 'result_sha256': digest(nucleus_path)})
        original = ROOT / 'originales/BORRADOR_02/04_DESARROLLO/verificar_confluencia_espectral.py'
        data, execution = execute(original, [], receipt_path.parent / 'confluencia.stdout.txt')
        require(data['status'] == 'PASS_LOCAL_IDENTIDADES_CONFLUENCIA_ESPECTRAL' and data['count'] == 44,
                'Resultado inesperado de confluencia')
        for relative, expected in data['sha256'].items():
            require(digest(safe_path(ROOT / 'originales/BORRADOR_02', relative)) == expected,
                    'Inconsistencia de los hashes emitidos por el programa original')
        write_json(receipt_path.parent / 'CONFLUENCIA.json', data)
        stages.append({**execution, 'status': data['status'], 'count': data['count'], 'scope': data['scope']})
    result = {'status': 'PASS_REPRODUCCION_FOCAL_ARTICULO_III',
              'utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
              'scope': 'Integridad documental, censo finito, reconstrucción relativa a transiciones y confluencia algebraica local. No generación primaria global ni equivalencia física.',
              'stages': stages}
    write_json(receipt_path, result)
    print(json.dumps({'status': result['status'], 'stages': len(stages), 'receipt': str(receipt_path),
                      'receipt_sha256': digest(receipt_path)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
