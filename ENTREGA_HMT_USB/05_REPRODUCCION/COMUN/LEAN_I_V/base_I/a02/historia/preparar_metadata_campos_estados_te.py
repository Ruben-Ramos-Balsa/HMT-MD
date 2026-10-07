#!/usr/bin/env python3
"""Prepare fresh TE-successor metadata; never compile, run gates or package.

The exact previous generator supplies receipt authentication, literal inherited
genealogy preservation and exclusive file creation. Only the documentary TE
delta is specialized before each new file is written. The old README, generator,
receipts and metadata remain untouched. A successful integrated terminal receipt
containing both concrete TE owners and both TT precursors is mandatory; no
pending run is promoted. Its path and digest are explicit CLI inputs.
"""
import argparse
import copy
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREVIOUS_SHA = 'fcba1d32d21e93f1dd34fe9c51fadbc3ad65f698a5363feba5b3d260031dc2dd'
README_PREVIOUS_SHA = '522dadf3bfdf97a0d0707bc8b1d3f4cc04885a272f0ddb933bb43cd7839cd7d7'
PREVIOUS_TERMINAL_SHA = '41b023531bd6e6de5b3bab2a6bc041d38304c48d683f6f46f8927398af62b70b'
PINNED_SUCCESSOR_SOURCES = {
    'SkewFieldTransform': 'ec662e9e99563683fdeeed840460ad8e3bea21ae2c9a98d4b34df1f91a2450b0',
    'LatticeTwistedEvenProduct': '5fb5a58e778baab29dcec1c96886eb8e9c4c07613ddc1c8605a9c967a018c8f0',
    'LatticeFiniteInvariantPairing': 'a4b8f88af853414bc614d413c83bdd7f8829754cc97dc1e0f24711411e218ed3',
}
REQUIRED_TERMINAL_SOURCES = set(PINNED_SUCCESSOR_SOURCES) | {
    'LatticeTwistedContragredientTruncation'}
TARGET = 'TWISTED_ALL_STATE_FIELDS_CONCRETE_EE_ET_TE_CONFORMAL_AND_TT_PRECURSORS'


def load_previous(path):
    import hashlib
    if hashlib.sha256(path.read_bytes()).hexdigest() != PREVIOUS_SHA:
        raise RuntimeError('El generador anterior no coincide con su huella fijada')
    spec = importlib.util.spec_from_file_location('state_fields_te_previous', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for role in ('normalization', 'continuation', 'descendants', 'terminal'):
        p.add_argument('--'+role+'-verification', type=Path, required=True)
        p.add_argument('--'+role+'-sha256', required=True)
    p.add_argument('--readme', type=Path, default=HERE/'README_CAMPOS_ESTADOS_TE.md')
    p.add_argument('--readme-sha256', required=True)
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--previous-generator', type=Path, default=HERE/'preparar_metadata_campos_estados.py')
    p.add_argument('--previous-readme', type=Path, default=HERE/'README_CAMPOS_ESTADOS.md')
    p.add_argument('--previous-terminal-verification', type=Path,
        default=HERE/'terminal_results_20260922/VERIFICATION.json')
    p.add_argument('--destination', type=Path)
    p.add_argument('--output-dir', type=Path, default=HERE/'metadata_campos_estados_te_20260922')
    args = p.parse_args()
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    old = load_previous(args.previous_generator)
    old.check_hash(args.previous_readme, README_PREVIOUS_SHA)
    if args.destination is None:
        args.destination = old.PROJECT/'output/PAQUETE_ARTICULO_I_CAMPOS_ESTADOS_TE_20260922'
    # Require both TE owners, both TT precursors and the exact parent link.
    # No terminal-successor digest is fixed here: it is an explicit CLI input.
    terminal = old.pinned(args.terminal_verification, args.terminal_sha256)
    if (terminal['status'] != 'PASS_TWISTED_TERMINAL_DELTA'
            or terminal.get('parent_receipt_sha256') != args.descendants_sha256
            or not REQUIRED_TERMINAL_SOURCES <= set(terminal['sources'])):
        raise RuntimeError('Se exige el recibo terminal integrado con TE, los dos precursores TT y su padre exacto')
    for name, digest in PINNED_SUCCESSOR_SOURCES.items():
        if terminal['sources'][name]['sha256'] != digest:
            raise RuntimeError('Propietario sucesor divergente: '+name)
        old.check_hash(args.source_dir/(name+'.lean'), digest)
    previous_terminal = old.pinned(args.previous_terminal_verification, PREVIOUS_TERMINAL_SHA)
    previous_names = set(previous_terminal['sources'])
    if (previous_terminal['status'] != 'PASS_TWISTED_TERMINAL_DELTA'
            or previous_terminal['parent_receipt_sha256'] != args.descendants_sha256
            or previous_terminal['inherited_module_count'] + len(previous_names) != 443
            or not previous_names <= set(terminal['sources'])
            or any(previous_terminal['sources'][n]['sha256'] != terminal['sources'][n]['sha256']
                   for n in previous_names)):
        raise RuntimeError('El terminal TE no conserva las fuentes exactas del corte histórico 443')
    old.TARGET = TARGET
    old.SUMMARY = old.SUMMARY.rstrip('.') + (
        '; construcción efectiva del bloque TE por exp(zD) ET(u,-z)v sobre el '
        'sector positivo, con EE y ET ya concretos y únicamente TT como argumento '
        'del ensamblaje; dualidad bilineal invariante del factor finito sin fijar '
        'su escala ni afirmar simetría, y nilpotencia local del L1 efectivo con '
        'finitud puntual de los coeficientes de su exponencial contragrediente.')
    old.EXCLUSIONS = [
        'Identidad de Jacobi torcida completa y sus identidades de módulo',
        'Producto TT concreto y compatibilidades mixtas completas del orbifold',
        *old.EXCLUSIONS[2:],
    ]
    old.GROUPS = copy.deepcopy(old.GROUPS) + [
        ('TWISTED_EVEN_PRODUCT', ('SkewFieldTransform', 'LatticeTwistedEvenProduct'),
         'positiveSector o -> campos heterogéneos de evenSpace o a positiveSector o',
         'TE concreto y stateFieldWithTT con EE/ET/TE fijados; sólo TT es argumento explícito',
         'Aplicar exp(zD) ET(u,-z)v con D=positiveConformalMode(-1); demostrar finitud '
         'coeficiente a coeficiente desde la truncación Laurent de ET, sin nilpotencia '
         'de D; probar Taylor sobre vacío, creación, inyectividad y compatibilidad '
         'conforme del ensamblaje para cada argumento TT.',
         ('POSITIVE_ET', 'DIAGONAL_EVEN_ACTION')),
        ('FINITE_INVARIANT_DUALITY', ('LatticeFiniteInvariantPairing',),
         'FiniteSpace o y su representación heredada de FiniteExtension o',
         'Dualidad bilineal no degenerada e invariante, con escala libre; no se afirma simetría',
         'Calcular dimensión uno del espacio de morfismos equivariantes hacia el '
         'dual mediante el carácter heredado, elegir un morfismo no nulo y usar '
         'irreducibilidad y dimensión finita para obtener una equivalencia lineal '
         'con el dual; demostrar invariancia para el grupo y operadores reticulares.', ()),
        ('CONTRAGREDIENT_TRUNCATION', ('LatticeTwistedContragredientTruncation',),
         'positiveSector o con sus modos conformes y graduación positiva efectivos',
         'L1 localmente nilpotente y coeficientes (1/n!) L1^n puntualmente finitos',
         'Derivar [L0,L1]=-L1 de Virasoro, bajar el peso y usar la anulación '
         'del peso cero junto con la generación por espacios de peso para '
         'probar nilpotencia local. No se afirma nilpotencia de L(-1), simetría '
         'de la forma finita, ni se construye TT con este resultado.', ()),
    ]
    original_write = old.write_new

    def write_te(path, value):
        value = copy.deepcopy(value)
        name = Path(path).name
        if name == 'RECIBO_GENEALOGICO.json':
            value['receipt_id'] = 'CAMPOS_ESTADOS_TE_CONTINUIDAD_20260922'
            value['target']['actual_lean_domain'] = (
                'LatticeCarrier o -> campos en Carrier o; evenSpace o -> campos en '
                'positiveSector o; positiveSector o -> campos de evenSpace o a '
                'positiveSector o. EE, ET y TE son concretos; TT es argumento '
                'explícito. Los precursores añadidos actúan sobre FiniteSpace o '
                'y el L1 efectivo de positiveSector o. No se afirma el sistema '
                'completo de identidades mixtas.')
            value['target']['forbidden_generator_inputs'] = [
                'NUEVA_SELECCION_K', 'JACOBI_COMO_HIPOTESIS',
                'TT_PRESENTADO_COMO_PRODUCTO_CONSTRUIDO', 'MONSTER_COMO_ENTRADA']
            value['global_falsifier'] = (
                'Tratar corrección, descendientes, ET o TE como argumentos no construidos; '
                'afirmar TT concreto o Jacobi mixto completo; confundir conservación '
                'documental con formalización íntegra de HMT o Moonshine.')
            value['proof_layers']['compatibility'] += (
                ' El TE concreto conserva el mismo sector positivo y sus coeficientes '
                'de Taylor sobre vacío; el ensamblaje mantiene sólo TT parametrizado.')
            value['source_review_testimony']['scope'] = (
                'Testimonio de lectura heredado para los campos de estados previos; '
                'no se amplía su objeto a TE ni a los precursores TT. Su evidencia '
                'Lean está en el recibo terminal y sus propietarios explícitos.')
        if name in ('RECIBO_GENEALOGICO.json', 'CAUSAL.json', 'CAUSAL_AUDITORIA_FUENTE.json'):
            focal = value['focal_genealogical_receipt']
            focal['4_coefficient_origins'] += (
                ' En TE, (-1)^(k-n) procede del cambio z a -z, 1/n! de la '
                'exponencial formal y D del modo conforme -1 ya construido. '
                'Para la exponencial contragrediente se usan 1/n! y el L1 '
                'efectivo; la dualidad finita se elige no nula sin fijar escala.')
            focal['5_conserved_information'] += (
                ' TE usa los mismos evenSpace y positiveSector; el soporte finito '
                'depende del vector y del coeficiente, no de truncar globalmente D. '
                'La nilpotencia local demostrada corresponde a L1, no a D=L(-1); '
                'la dualidad conserva la representación finita heredada.')
            focal['8_posterior_recognition_and_falsifier'] = (
                'La realización usa lenguaje de Fock y campos de vértice después '
                'del origen HMT. EE, ET y TE son asignaciones concretas. TT conserva '
                'su tipo como argumento. Dualidad finita y truncación contragrediente '
                'son precursores, no ese producto. Estos metadatos no demuestran '
                'simetría de la forma, Jacobi mixto completo, TT concreto ni Aut(Vnatural)=Monster.')
            value['successor_documentation'] = dict(
                previous_readme=old.locator(args.previous_readme),
                previous_generator=old.locator(args.previous_generator),
                sealed_443_terminal_receipt=old.locator(args.previous_terminal_verification),
                construction_reuse_cut=406,
                same_normalization_continuation_descendants=True,
                previous_terminal_source_hashes_preserved=True,
                delta='TE concreto y dos precursores TT; EE/ET/TE fijados y sólo TT parametrizado',
                previous_assets_modified=False)
        if name in ('CAUSAL.json', 'CAUSAL_AUDITORIA_FUENTE.json'):
            scope = value['formalization_scope']
            scope.update(actual_TE_assignment=True, TE_mixed_Jacobi_claimed=False,
                explicit_mixed_block_arguments=['TT'],
                actual_finite_invariant_duality=True, finite_pairing_scale_normalized=False,
                finite_pairing_symmetry_claimed=False, actual_L1_locally_nilpotent=True,
                translation_locally_nilpotent_claimed=False,
                contragredient_exponential_pointwise_finite=True)
            value['posterior_realization']['operator'] += (
                ' Transformación formal exp(zD) ET(u,-z)v que construye TE; '
                'dualidad finita invariante y exponencial puntual del L1 efectivo '
                'como precursores separados de TT.')
        if name == 'MANIFIESTO_METADATA.json':
            value['inherited_generator'] = value['script']
            value['script'] = old.locator(__file__)
            value['previous_readme'] = old.locator(args.previous_readme)
            value['sealed_443_terminal_receipt'] = old.locator(args.previous_terminal_verification)
            value['scope_delta'] = ('EE/ET/TE concretos; dualidad finita y truncación '
                'contragrediente; TT argumento; sin Jacobi mixto completo ni FLM')
        original_write(path, value)

    old.write_new = write_te
    forwarded = []
    for role in ('normalization', 'continuation', 'descendants', 'terminal'):
        forwarded += ['--'+role+'-verification', str(getattr(args, role+'_verification')),
                      '--'+role+'-sha256', getattr(args, role+'_sha256')]
    for flag in ('readme', 'readme_sha256', 'source_dir', 'destination', 'output_dir'):
        forwarded += ['--'+flag.replace('_', '-'), str(getattr(args, flag))]
    before = sys.argv
    try:
        sys.argv = [str(args.previous_generator), *forwarded]
        return old.main()
    finally:
        sys.argv = before


if __name__ == '__main__':
    raise SystemExit(main())
