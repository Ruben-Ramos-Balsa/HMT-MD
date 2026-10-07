#!/usr/bin/env python3
"""Copie mécanique de provenance. Ce script de collecte est local, non génératif."""
from pathlib import Path
from hashlib import sha256
import json
import shutil

HERE = Path(__file__).resolve().parent
PROJECT = Path('/Users/ruben/Documents/New project')
B02 = PROJECT / 'output/ARTICULO_ACCION_BARBERO_HMT_20260907_BORRADOR_02'
II = PROJECT / 'output/ARTICULO_II_AUTONOMIA_20260909_REVISION_05_TRABAJO'
I = PROJECT / 'output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909'
C = PROJECT / 'output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/fuentes/integral'
TRUNK = PROJECT / 'PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA'
S = PROJECT / 'output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente'

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def main():
    pairs = []
    def add(root, relative, destination, role):
        pairs.append((root / relative, Path(destination) / relative, role))
    for p in (
        '04_DESARROLLO/verificar_confluencia_espectral.py',
        '04_DESARROLLO/CONFLUENCIA_ESPECTRAL_Y_JERARQUIA_20260907.md',
        '01_FUENTES/A07/capitulo_14_apertura_causal_accion_parangular.tex',
        '01_FUENTES/D06/INTERRELACIONES_ESTRUCTURALES_VACIO.md',
        '01_FUENTES/D07/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md',
        '01_FUENTES/B06/c51_barbero_area_informacion.tex',
        '01_FUENTES/B03/c43_operador_area.tex',
        '01_FUENTES/B04/parte_iv_area_hamiltoniano_memoria.tex',
        '01_FUENTES/B01/c43_precedencia_dodecafasica_20260905.tex',
        'manuscrito/main.tex',
        'output/pdf/ACCION_GEOMETRIA_BARBERO_BORRADOR_02.pdf',
    ):
        add(B02, p, 'originales/BORRADOR_02', 'ANTECEDENTE_CONFLUENCIA_NO_ARTICULO_III')
    for p in ('D07/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md',
              'B06/c51_barbero_area_informacion.tex'):
        add(II / 'fuentes/propietarios_II', p, 'originales/ARTICULO_II_REV05', 'PROPIETARIO_II_REV05')
    for p in ('sections/extension.tex', 'sections/generacion.tex',
              'technical/AUTONOMIA_DEPENDENCIAS_LOCALIZADAS.md',
              'technical/APENDICE_REGLAS_PROCEDENCIA.md'):
        add(I, p, 'originales/ARTICULO_I_117', 'ANTECEDENTE_NUCLEO_Y_ALCANCE')
    add(C, 'manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex',
        'originales/PROPIETARIOS_NUCLEO', 'PRUEBA_RECONSTRUCCION_FINITA')
    for p in ('pruebas/python/verificar_censo_regiones.py',
              'pruebas/python/verificar_dinamica_cociente_468.py',
              'datos/TPK_U_catalog_468.json', 'datos/hmt_u_route_catalog_full.csv'):
        add(TRUNK, p, 'originales/CENSO_REGIONAL', 'TESTIGO_CENSO_Y_REGLA_FINITA')
    add(S, 'manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex',
        'originales/PROPIETARIOS_NUCLEO', 'EXTRACTOR_Y_RECONSTRUCCION_K')
    add(S, 'manuscrito/ampliaciones_sucesoras_20260824/parte_i_ii/owners/U008_orbitas_elevacion_r36.tex',
        'originales/PROPIETARIOS_NUCLEO', 'PROPIETARIO_TRANSPORTE_CON_MEMORIA')
    entries = []
    for source, relative, role in pairs:
        destination = HERE / relative
        if not source.is_file():
            raise SystemExit('Fuente ausente: ' + str(source))
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and digest(destination) != digest(source):
            raise SystemExit('Copia diferente: se conserva sin sobrescribir ' + str(destination))
        if not destination.exists():
            shutil.copy2(source, destination)
        entries.append({'source': str(source), 'destination': relative.as_posix(),
                        'sha256': digest(source), 'bytes': source.stat().st_size, 'role': role})
    result = {'scope': 'COPIAS_LITERALES_NO_CERTIFICACION_MATEMATICA_GLOBAL',
              'files': entries, 'file_count': len(entries),
              'source_paths': 'Sólo procedencia y regeneración local de las copias; la reproducción usa rutas relativas.'}
    out = HERE / 'MANIFIESTO_ORIGINALES.json'
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if out.exists() and out.read_text() != serialized:
        raise SystemExit('Manifiesto anterior distinto: crear revisión antes de reemplazar.')
    out.write_text(serialized, encoding='utf-8')
    print(json.dumps({'status': 'PASS_COPIAS_LITERALES', 'files': len(entries),
                      'manifest_sha256': digest(out)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
