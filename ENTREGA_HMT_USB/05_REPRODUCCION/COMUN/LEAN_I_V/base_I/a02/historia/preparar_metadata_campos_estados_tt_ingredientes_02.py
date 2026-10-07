#!/usr/bin/env python3
"""Prepare successor metadata for actual TT ingredients without running gates.

Reuse the pinned TE metadata generator and all its receipt/source authentication.
Require the additional owners in the explicit successful terminal receipt; never
promote a focal compile or an in-progress integration to an integrated PASS.
The earlier generators, receipts and metadata remain byte-identical.
"""
import argparse
import copy
import hashlib
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TE_GENERATOR_SHA = '387b696edab18878032049d5d68e186ff8c9b9a11b5b99c2806222ebd47cbc0d'
TARGET = 'TWISTED_FIELDS_EE_ET_TE_AND_CONTRAGREDIENT_PAIRING_INGREDIENTS'
EXTRA_SOURCES = {
    'LatticeTwistedCoordinateExponential':
        'f634e0467e257052c215ecb42b5f82979d74e68269934d65857a0b0c8a994aa9',
    'CoordinateWeightSign':
        'b14bf06d9dab486597bacf73d21540e2db0c5f817c00bdde5bc2904503f2c851',
    'LatticeTwistedWeightSignLaws':
        '93fad9f405721c5ec4af686bde64393ec0105fc4614043193862dd6dc5fb064a',
    'LatticeTwistedCoordinateSign':
        'd0466ca6d80bd0de5e6034ad53532e79171d39aedb277b1107355672f47415ba',
    'LatticeTwistedCoordinateConjugation':
        '0edeb63943d1c59ef0d755dec578d13ff3bf0b9fd21c47f82ba38b2ce3e259e3',
    'WeightedBasisPairing':
        'f1f0cf162e1d88ddd9a0b121153d8bac90d48e9172898eefb90db971e66fd3a0',
    'LatticeFactorialPairing':
        '7fe98a4d9dfec0144ab044727703645ac0c2c17f490d9678c248d84b2c973a49',
    'LatticeHalfGramTransport':
        '14c892ca757fcf25ed20b68b340ae62b45803b49b23cded32013d41603da1e18',
    'LatticeHalfFockPairing':
        'ec1b3648635d79f35eb7d8fb435f5a9ea946c055690aa8e422080f1b45d3fae2',
    'LatticeTwistedTensorPairing':
        'acfdc0a61ec09f4afddd7bcacdf4593db546249994c9b9a2bf0cf9fd7dca4915',
    'LatticeHalfGramWeight':
        '07b58b4b05c01c9dd59408212f08c090534c95b790ad291faa04a9d226f40058',
    'LatticeTwistedPairingGrading':
        '84aa2f1a08fa7a8e7b64386aa7d72964684c1d5e2edc701936e4e92c7cc5cbab',
    'LatticeIntegerFockPairing':
        '8edcd7156446723731f444904d5c3edd670f6eb175bf5c54370cd1d3de66f2c6',
    'LatticeTwistedContragredientCoefficients':
        'b94dd1cc2015f05031db17966504000a9b87322100b3923d64f53914a109ee0f',
}
SUMMARY_SUFFIX = (
    ' Se construyen ambas exponenciales formales del L1 efectivo sobre el '
    'sector positivo, inversas por ambos lados y puntualmente polinomiales; '
    'el signo de peso efectivo las conjuga y su producto con la exponencial '
    'es involutivo. Se construyen formas bilineales complejas no degeneradas '
    'en los Fock semientero y entero, en el tensor torcido y en el sector '
    'positivo, con las adjunciones y dualidades homogéneas expresamente '
    'probadas. Desde TE, la forma positiva y la exponencial de L1 se '
    'construyen coeficientes contragredientes en el dual algebraico del sector '
    'par, estables bajo ampliación del corte y extendidos linealmente por '
    'pesos; no se afirma representabilidad vectorial ni campo TT completo.')
EXTRA_EXCLUSIONS = [
    'Simetría de las formas transportadas Fock, tensorial, finita o positiva, '
        'salvo la simetría expresamente probada de la forma factorial auxiliar',
    'Positividad hermítica, dualidad con el dual algebraico entero del Fock infinito '
        'o adjunción de la familia completa de modos conformes',
    'Representabilidad de los coeficientes contragredientes por vectores de '
        'evenSpace, truncación Laurent y Jacobi de un campo TT',
]
EXTRA_GROUPS = [
    ('COORDINATE_EXPONENTIAL', ('LatticeTwistedCoordinateExponential',),
     'Series formales con coeficientes en End complejo de positiveSector o',
     'Unidad formal exp(z L1), inversa exp(-z L1), ambas puntualmente polinomiales',
     'Identificar coeficientes con (1/n!)(+/-L1)^n, reutilizar el producto de '
     'exponenciales finitas para demostrar las dos composiciones identidad '
     'y aplicar la nilpotencia local efectiva de L1 para la finitud sobre '
     'cada vector; no suponer nilpotencia de L(-1).',
     ('CONTRAGREDIENT_TRUNCATION',)),
    ('COORDINATE_WEIGHT_SIGN', ('CoordinateWeightSign',
       'LatticeTwistedWeightSignLaws', 'LatticeTwistedCoordinateSign'),
     'positiveSector o con su descomposición interna por pesos conformes enteros',
     'Signo efectivo (-1)^L0, involutivo, conmutante con L0 y anticomutante con L1',
     'Construir el signo por la suma directa interna de autoespacios que ya '
     'generan el portador, determinarlo por (-1)^d en cada peso y demostrar '
     'sus leyes con el L1 que baja peso. No recibir el signo final como '
     'hipótesis ni identificarlo con la involución que define el sector fijo.',
     ('CONTRAGREDIENT_TRUNCATION',)),
    ('COORDINATE_CONJUGATION', ('LatticeTwistedCoordinateConjugation',),
     'Series formales de endomorfismos de positiveSector o, exponencial y signo efectivos',
     'Conjugación de las dos exponenciales entre sí y cuadrado identidad de exp(zL1) C(signo)',
     'Conjugar cada coeficiente factorial usando el signo probado de L1^n, '
     'identificarlo con la exponencial inversa y componer con la identidad '
     'formal bilateral ya demostrada; no afirmar convergencia analítica.',
     ('COORDINATE_EXPONENTIAL', 'COORDINATE_WEIGHT_SIGN')),
    ('HALF_FOCK_PAIRING', ('WeightedBasisPairing', 'LatticeFactorialPairing',
       'LatticeHalfGramTransport', 'LatticeHalfFockPairing'),
     'Fock semientero heredado, base monomial y matriz de Gram marcada existentes',
     'Forma bilineal compleja no degenerada, separante a derecha, creador adjunto igual a menos aniquilador',
     'Construir la forma factorial simétrica auxiliar y transportarla por el '
     'bloque -(n+1/2) Gram con inverso explícito. Deducir no degeneración '
     'bilateral y adjunción semientera. No cambiar a base ortonormal ni '
     'atribuir a la forma transportada una simetría no enunciada.', ()),
    ('TWISTED_TENSOR_PAIRING', ('LatticeTwistedTensorPairing',),
     'Carrier o = HalfFock o tensor complejo FiniteSpace o, ambos efectivos',
     'Forma tensorial no degenerada, adjunción semientera e invariancia simultánea bajo carga',
     'Tensorizar las dos formas construidas, utilizar las bases duales '
     'izquierda y derecha del factor finito para separar vectores y '
     'transportar adjunción e invariancia de carga. No suponer simetría '
     'de la forma finita ni invariancia completa de campos de vértice.',
     ('HALF_FOCK_PAIRING', 'FINITE_INVARIANT_DUALITY')),
    ('POSITIVE_GRADED_PAIRING', ('LatticeHalfGramWeight', 'LatticeTwistedPairingGrading'),
     'Pesos del Carrier efectivo, positiveSector o y sus autoespacios conformes enteros',
     'Restricciones no degeneradas al sector fijo y a cada peso, con dualidades finitas homogéneas',
     'Probar que el transporte Gram preserva el modo cuadrático cero, que '
     'pesos diferentes son ortogonales y que el proyector par es autoadjunto '
     'para la forma; deducir restricciones no degeneradas y equivalencias '
     'con los duales de los espacios homogéneos finitos. positiveSector '
     'denota un sector fijo, no positividad hermítica de la forma.',
     ('TWISTED_TENSOR_PAIRING',)),
    ('INTEGER_FOCK_PAIRING', ('LatticeIntegerFockPairing',),
     'Fock ordinario sobre los mismos osciladores y retículo marcado',
     'Forma bilineal no degenerada de frecuencia n+1 y creador adjunto igual a menos aniquilador',
     'Reutilizar la forma factorial y el transporte por bloques con '
     'factor -(n+1), construir su inverso y demostrar separación bilateral '
     'y adjunción con el aniquilador ordinario. No seleccionar otro retículo.',
     ('HALF_FOCK_PAIRING',)),
    ('CONTRAGREDIENT_DUAL_COEFFICIENTS', ('LatticeTwistedContragredientCoefficients',),
     'Dos vectores de positiveSector o y un estado de evenSpace o',
     'Coeficientes bilineales en los vectores torcidos con valores en Module.Dual complejo de evenSpace o',
     'Sobre un vector de peso d sumar (-1)^d por los términos '
     'B+(w, TE(L1^j v/j!)_(j-2d-k) a) con j<d, demostrar invariancia al '
     'ampliar el corte a cualquier N>=d y extender linealmente mediante '
     'la descomposición interna por pesos. El resultado vive en el dual '
     'algebraico: no supone representabilidad en evenSpace, cota Laurent '
     'para TT ni sus identidades de Jacobi.',
     ('TWISTED_EVEN_PRODUCT', 'POSITIVE_GRADED_PAIRING',
      'COORDINATE_EXPONENTIAL', 'COORDINATE_WEIGHT_SIGN')),
]


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--te-generator', type=Path,
        default=HERE/'preparar_metadata_campos_estados_te.py')
    args, forwarded = parser.parse_known_args()
    path = args.te_generator.expanduser().resolve()
    if hashlib.sha256(path.read_bytes()).hexdigest() != TE_GENERATOR_SHA:
        raise RuntimeError('El generador TE antecedente no coincide con su huella fijada')
    spec = importlib.util.spec_from_file_location('tt_ingredients_te_generator', path)
    te = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(te)
    te.__doc__ = __doc__
    te.TARGET = TARGET
    te.PINNED_SUCCESSOR_SOURCES.update(EXTRA_SOURCES)
    te.REQUIRED_TERMINAL_SOURCES.update(EXTRA_SOURCES)
    original_load = te.load_previous

    def load_extended_base(base_path):
        base = original_load(base_path)
        original_maps, original_write = base.make_maps, base.write_new

        def make_maps(antecedent, inventory):
            # TE has already installed its groups when the base calls this.
            base.GROUPS += copy.deepcopy(EXTRA_GROUPS)
            base.SUMMARY += SUMMARY_SUFFIX
            base.EXCLUSIONS += copy.deepcopy(EXTRA_EXCLUSIONS)
            return original_maps(antecedent, inventory)

        def write_new(output, value):
            # Called after the pinned TE wrapper has applied its documentary
            # delta, before the inherited exclusive-create filesystem write.
            value = copy.deepcopy(value)
            name = Path(output).name
            if name in ('RECIBO_GENEALOGICO.json', 'CAUSAL.json',
                        'CAUSAL_AUDITORIA_FUENTE.json'):
                value['successor_documentation'].update(
                    te_metadata_generator=base.locator(path),
                    ingredients_metadata_generator=base.locator(__file__),
                    additional_owners=sorted(EXTRA_SOURCES),
                    delta='EE/ET/TE concretos, formas y signo efectivos, coeficientes contragredientes en el dual; TT sigue como argumento')
                focal = value['focal_genealogical_receipt']
                focal['4_coefficient_origins'] += (
                    ' El signo opuesto de L1 produce la exponencial inversa; '
                    'ambos coeficientes se deducen de la misma serie formal '
                    'y de los factoriales, sin nuevos coeficientes objetivo. '
                    'El signo (-1)^d procede del peso entero heredado; los '
                    'factores de las formas son los factoriales de ocupación '
                    'y las frecuencias -(n+1/2) o -(n+1) contra la misma Gram. '
                    'El índice j-2d-k corresponde al cambio formal de '
                    'coordenada registrado en los coeficientes duales.')
                focal['5_conserved_information'] += (
                    ' Las dos composiciones exponenciales son identidad en '
                    'series de operadores; su finitud es por vector, no un '
                    'grado de corte global. Se conservan base monomial, Gram, '
                    'cociclo, representación finita y graduaciones. Las formas '
                    'no se hacen hermíticas por llamar positivo al sector fijo. '
                    'Los coeficientes contragredientes conservan su codominio '
                    'dual y no se convierten nominalmente en vectores pares.')
                focal['8_posterior_recognition_and_falsifier'] += (
                    ' Las dualidades homogéneas son finitas, no una '
                    'identificación global del Fock con su dual algebraico. '
                    'Los coeficientes en el dual no se anuncian como un '
                    'campo TT vectorial o Laurent.')
            if name == 'RECIBO_GENEALOGICO.json':
                value['receipt_id'] = 'CAMPOS_ESTADOS_TE_INGREDIENTES_TT_CONTINUIDAD_20260922'
                value['target']['actual_lean_domain'] += (
                    ' La unidad exponencial actúa en las series de '
                    'endomorfismos complejos del mismo positiveSector o. '
                    'Las formas actúan en Fock, Carrier y sus subespacios '
                    'efectivos. Los coeficientes finales son mapas '
                    'positiveSector -> positiveSector -> Module.Dual de evenSpace, '
                    'no mapas con valores probados en evenSpace.')
                value['global_falsifier'] += (
                    ' Promover una forma bilineal a hermítica/simétrica '
                    'sin el enunciado correspondiente, o los coeficientes '
                    'duales a un campo TT representable y Laurent.')
            if name in ('CAUSAL.json', 'CAUSAL_AUDITORIA_FUENTE.json'):
                value['formalization_scope'].update(
                    actual_coordinate_exponential_unit=True,
                    both_coordinate_exponentials_pointwise_finite=True,
                    actual_coordinate_weight_sign=True,
                    sign_conjugates_exponential_to_inverse=True,
                    signed_exponential_square_identity=True,
                    actual_half_and_integer_fock_pairings=True,
                    actual_tensor_and_positive_pairings=True,
                    graded_finite_dualities=True,
                    transported_pairing_symmetry_claimed=False,
                    hermitian_positivity_claimed=False,
                    entire_fock_algebraic_duality_claimed=False,
                    actual_contragredient_dual_coefficients=True,
                    homogeneous_coefficient_cutoff_independent=True,
                    dual_coefficients_linearly_extended=True,
                    even_vector_representability_claimed=False,
                    TT_laurent_truncation_claimed=False,
                    whole_contragredient_coordinate_transform_claimed=False,
                    actual_TT_product_claimed=False)
                value['posterior_realization']['operator'] += (
                    ' Signo por peso, formas contravariantes y coeficientes '
                    'contragredientes concretos con valores en el dual par.')
            if name == 'MANIFIESTO_METADATA.json':
                value['te_metadata_generator'] = value['script']
                value['script'] = base.locator(__file__)
                value['additional_owner_source_hashes'] = copy.deepcopy(EXTRA_SOURCES)
                value['scope_delta'] += (
                    '; exponenciales y signo efectivos, formas Fock/tensor/'
                    'positiva y coeficientes contragredientes en el dual')
            original_write(output, value)

        base.make_maps, base.write_new = make_maps, write_new
        return base

    te.load_previous = load_extended_base
    if not any(v == '--output-dir' or v.startswith('--output-dir=') for v in forwarded):
        forwarded += ['--output-dir', str(HERE/'metadata_campos_estados_tt_ingredientes_20260922')]
    if not any(v == '--destination' or v.startswith('--destination=') for v in forwarded):
        project = next(p for p in HERE.parents if (p/'tools/verificar_genealogia_unica_hmt.py').is_file())
        forwarded += ['--destination', str(project/'output/PAQUETE_ARTICULO_I_DUALIDAD_DE_ESTADOS_20260922')]
    before = sys.argv
    try:
        sys.argv = [str(path), *forwarded]
        return te.main()
    finally:
        sys.argv = before


if __name__ == '__main__':
    raise SystemExit(main())
