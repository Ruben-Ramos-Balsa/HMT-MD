#!/usr/bin/env python3
"""Extrae el ZIP final, comprueba huellas y recompila VII desde otra carpeta.

Python stdlib; LuaLaTeX y pdftotext son herramientas de ejecución externas.
La recepción se escribe fuera del ZIP para evitar un manifiesto circular.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def execute(command, cwd, timeout=300):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    require(result.returncode == 0, result.stdout + result.stderr)
    return json.loads(result.stdout)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    parser.add_argument('--lualatex', default='lualatex')
    parser.add_argument('--pdftotext', default='pdftotext')
    args = parser.parse_args()
    archive_path = args.zip.resolve()
    require(archive_path.is_file(), 'ZIP inexistente.')
    engine = shutil.which(args.lualatex)
    extractor = shutil.which(args.pdftotext)
    require(engine and extractor, 'Se requieren LuaLaTeX y pdftotext.')
    with tempfile.TemporaryDirectory(prefix='vii_rev07_zip_') as temp:
        temporary = Path(temp)
        with zipfile.ZipFile(archive_path) as archive:
            require(archive.testzip() is None, 'CRC inválido.')
            members = archive.namelist()
            require(len(members) == len(set(members)), 'Miembros ZIP duplicados.')
            for item in archive.infolist():
                path = Path(item.filename)
                require(not path.is_absolute() and '..' not in path.parts and path.parts[0] == 'ARTICULO_VII', 'Ruta ZIP no permitida.')
                require((item.external_attr >> 16) & 0o170000 != 0o120000, 'Enlace simbólico en ZIP.')
            archive.extractall(temporary)
        root = temporary / 'ARTICULO_VII'
        manifest = json.loads((root / 'gestion/MANIFIESTO_ENTREGA_VII.json').read_text())
        for row in manifest['files']:
            require(sha(root / row['path']) == row['sha256'], 'Huella ZIP incorrecta: ' + row['path'])
        require(len(members) == len(manifest['files'])+1, 'Inventario ZIP incompleto.')
        empty_cwd = temporary / 'empty_cwd'
        empty_cwd.mkdir()
        runs = []
        for optimized in (False, True):
            command = [sys.executable, '-I', '-S', '-B']
            if optimized:
                command.append('-O')
            payload = execute(command + [str(root / 'gestion/verificar_editorial_rev07.py')], empty_cwd)
            require(payload['status'] == 'PASS_CONSERVACION_EDITORIAL_VII_REV07', 'Conservación fallida.')
            runs.append(payload)
        require(runs[0] == runs[1], 'Conservación normal/-O diferente.')
        checks = execute([sys.executable, '-I', '-S', '-B', str(root / 'pruebas/verificar_paquete_local.py')], empty_cwd)
        require(checks == {'status':'PASS_CONTROLES_LOCALES_VII', 'scripts':13, 'runs':26, 'failures':[]}, 'Controles focales fallidos.')
        pdf = root / manifest['pdf']['path']
        original_text = subprocess.run([extractor, '-layout', str(pdf), '-'], capture_output=True, check=True).stdout
        original_pdf_sha = sha(pdf)
        preflight = root / 'gestion/preflight_s0/runs/editorial_rev07/RECIBO_PRECOMPILACION.json'
        build = execute([sys.executable, '-I', '-S', '-B', str(root / 'gestion/compilar_portable_VII.py'),
            '--preflight', str(preflight), '--lualatex', engine], empty_cwd, timeout=1000)
        require(not build['errors'] and build['pdf'], 'Compilación reproducida fallida.')
        new_text = subprocess.run([extractor, '-layout', str(pdf), '-'], capture_output=True, check=True).stdout
        require(original_text == new_text, 'Texto/paginación extraídos difieren tras recompilar.')
        require(build['pdf']['pages_from_log'] == manifest['pdf']['pages'], 'Paginación reproducida diferente.')
        receipt = json.loads((root / build['receipt']).read_text())
        fls = json.loads((root / build['manifest']).read_text())
        require(not fls['changed_authored_sources'] and not fls['authored_sources_missing_from_fls'], 'Fuentes no conservadas/incluidas.')
        result = {'schema':'hmt.vii.zip_reproduction.rev07.v1', 'status':'PASS_REPRODUCCION_ZIP_VII_REV07',
            'zip':str(archive_path), 'zip_sha256':sha(archive_path), 'members':len(members),
            'inventory_files_verified':len(manifest['files']), 'local_scripts':13, 'local_runs':26,
            'editorial_check_normal_optimized_identical':True, 'empty_cwd_used':True,
            'tex_executed_from_zip_extraction':True, 'successful_lualatex_passes':len(receipt['passes']),
            'pages':manifest['pdf']['pages'], 'original_pdf_sha256':original_pdf_sha,
            'reproduced_pdf_sha256':sha(pdf), 'extracted_layout_text_identical':True,
            'extracted_layout_text_sha256':hashlib.sha256(new_text).hexdigest(),
            'preflight_payload_sha256':json.loads(preflight.read_text())['receipt_payload_sha256'],
            'preflight_bound_to_current_sources':True, 'final_warnings':build['warnings'],
            'source_graph':{'files':len(fls['active_sources_before']['tex'])+len(fls['active_sources_before']['images']),
                'active_graph_sha256':fls['active_sources_before']['active_graph_sha256'],
                'all_in_fls':True, 'changed':[]},
            'whole_article_mathematical_certification':False,
            'external_canonical_scientific_gates_rerun_from_zip':False,
            'scope':'Huellas, controles focales y tres pasadas TeX desde ZIP extraído. El driver consume el preflight real ya emitido; no produce una prueba matemática global.'}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    require(not args.receipt.exists(), 'El recibo de destino ya existe.')
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
