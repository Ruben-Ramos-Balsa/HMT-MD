#!/usr/bin/env python3
"""Actualiza sólo la vinculación documental focal tras el delta editorial.

Reutiliza el preparador conservado sin alterar sus criterios ni validadores.
Desplaza los localizadores anteriores de 33 por el párrafo añadido, cuya
conservación exacta se comprueba antes. No produce una prueba científica nueva.
"""
import json
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    subprocess.run([sys.executable, '-I', '-S', '-B',
        str(ROOT / 'gestion/verificar_editorial_rev07.py')], check=True)
    delta = json.loads((ROOT / 'gestion/revision07/DELTA_EDITORIAL.json').read_text())
    row = next(r for r in delta['changes'] if r['path'] == '33_corriente_espinorial_y_densidad.tex')
    inserted = row['exact_delta']['inserted_text']
    after = (ROOT / 'manuscrito' / row['path']).read_text()
    before = (ROOT / row['preserved_before']).read_text()
    if after.count(inserted) != 1 or after.replace(inserted, '') != before:
        raise RuntimeError('El delta editorial dejó de ser una inserción exacta.')
    displacement = inserted.count('\n')
    insertion_line = after[:after.index(inserted)].count('\n') + 1
    namespace = runpy.run_path(str(ROOT / 'gestion/preparar_genealogia_s0.py'), run_name='editorial_binding')
    runtime = namespace['main'].__globals__
    original_locator, original_writer = runtime['loc'], runtime['write']
    def locator(path, lines=None):
        if path.name == row['path'] and lines:
            start, end = map(int, lines.split('-'))
            if start < insertion_line:
                raise RuntimeError('Revisar un localizador que cruce la inserción editorial.')
            lines = '%d-%d' % (start + displacement, end + displacement)
        return original_locator(path, lines)
    def writer(path, value):
        if path.name == 'RECIBO_GENEALOGIA_S0.json':
            value['provenance'] = 'RESULTADO_RECUPERADO'
            value['editorial_revision']['revision'] = '07'
            value['editorial_revision']['new_scientific_proof'] = False
            value['editorial_revision']['source_delta'] = original_locator(ROOT / 'gestion/revision07/DELTA_EDITORIAL.json')
            value['editorial_revision']['locator_shift_after_inserted_line'] = {'line': insertion_line, 'offset': displacement}
        return original_writer(path, value)
    runtime['loc'], runtime['write'] = locator, writer
    sys.argv = [str(ROOT / 'gestion/preparar_genealogia_s0.py'), '--out-name', 'genealogia_s0_rev07', '--validate']
    return namespace['main']()

if __name__ == '__main__':
    sys.exit(main())
