#!/usr/bin/env python3
"""Exact finite controls for the written arbitrary-depth proofs.

No Feigenbaum target value is an input. These tests do not replace the
existence, induction and completion proofs in the accompanying document.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math

BASE = Path(__file__).resolve().parent
DOC = BASE / 'PROLONGACION_NONADICA_Y_LIMITE_FEIGENBAUM.md'


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def tau(n):
    return -1 if v2(n) % 2 else 1


def word(n):
    return ''.join('+' if tau(j) > 0 else '-' for j in range(1, 2**n))


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def add(a, b):
    return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]


def tr(a):
    return [list(x) for x in zip(*a)]


def checks():
    results = {}
    for n in range(1, 15):
        w = word(n)
        assert word(n+1) == w + ('+' if n % 2 == 0 else '-') + w
        p = 2**n
        inv = pow(9, -1, p)
        for j in range(1, p):
            assert v2((9*j) % p) == v2(j)
            assert inv*((9*j) % p) % p == j
    results['word_and_nonadic_permutation_levels'] = 14
    # Direct independent finite check of the parity order used in the proof.
    for shift in range(1, 1025):
        orientation = 1
        for k in range(1, 2049):
            a, b = tau(k), tau(k+shift)
            if a != b:
                assert k & (k-1) == 0
                assert orientation*(a-b) > 0
                break
            orientation *= -a
        else:
            raise AssertionError('First mismatch not found')
    results['strict_maximality_shifts_checked'] = 1024
    certificate = json.loads((BASE/'CERTIFICADO_RAICES_INTERVALOS.json').read_text())
    found = []

    def walk(obj):
        if isinstance(obj, dict):
            if 'sign_word' in obj:
                found.append(obj['sign_word'])
            for val in obj.values():
                walk(val)
        elif isinstance(obj, list):
            for val in obj:
                walk(val)
    walk(certificate)
    assert len(found) == 8, len(found)
    for n, w in enumerate(sorted(found, key=len), 1):
        assert w == word(n)
    results['inherited_interval_certificate_words_matched'] = len(found)
    # Chronological register: nonadic phases alone fail, lifts succeed.
    for n in range(1, 11):
        for k in range(1, 1001):
            rho, carry = ((k-1) % 9)+1, (k-1)//9
            assert rho+9*carry == k
            assert (rho+9*carry) % (2**n) == k % (2**n)
    assert 1 % 9 == 10 % 9 and tau(1) != tau(10)
    results['phase_only_falsifier_detected'] = True
    # Associate blocks without changing their ordered digits.
    for length in (18, 36, 72, 144):
        digits = [(j*j+3*j+1) % 9 for j in range(length)]
        target = 0
        for c in digits:
            target = 9*target+c
        for block in (2, 9):
            accum = 0
            for start in range(0, length, block):
                part = digits[start:start+block]
                d = 0
                for c in part:
                    d = 9*d+c
                accum = 9**len(part)*accum+d
            assert accum == target
        recovered = [(target//9**(length-j-1)) % 9 for j in range(length)]
        assert recovered == digits
    results['block_regrouping_lengths_checked'] = [18, 36, 72, 144]
    for m in range(1, 301):
        a, capacity = 0, 1
        while capacity < 9**m:
            a, capacity = a+1, capacity*1000
        k, binary_capacity = 0, 729
        while binary_capacity < capacity:
            k, binary_capacity = k+1, binary_capacity*729
        assert 9**m <= 1000**a <= 729**(k+1)
        assert 1000**(a-1) < 9**m
        assert 729**k < 1000**a
    results['capacity_unit_conversion_lengths_checked'] = 300
    # Rational upper bound for cos(3), alternating after its quadratic term.
    cos_upper = sum(Q((-1)**j * 3**(2*j), math.factorial(2*j))
                    for j in range(5))
    assert cos_upper < Q(-1, 2)
    assert 72 < 81  # (6 sqrt(2))^2 < 9^2.
    results['cos3_rational_upper'] = str(cos_upper)
    results['lipschitz_less_than_nine_exact_squared_test'] = True
    # Bilateral projectors in a rational basis, with metric diag(1,8).
    # S=diag(1,sqrt(8)); A_i=S^-1 P_i S; G=S^*S.
    a0 = [[Q(8, 9), Q(-8, 9)], [Q(-1, 9), Q(1, 9)]]
    a1 = [[Q(1, 9), Q(8, 9)], [Q(1, 9), Q(8, 9)]]
    identity, zero, metric = [[1, 0], [0, 1]], [[0, 0], [0, 0]], [[1, 0], [0, 8]]
    assert add(a0, a1) == identity
    assert mm(a0, a0) == a0 and mm(a1, a1) == a1
    assert mm(a0, a1) == zero and mm(a1, a0) == zero
    assert mm(tr(a0), metric) == mm(metric, a0)
    assert mm(tr(a1), metric) == mm(metric, a1)
    for n in range(1, 13):
        p = 2**n
        for j in range(p):
            # Equal coefficients 1/sqrt(2) on each side, compare supports.
            assert {(j+1) % (2*p), (j+p+1) % (2*p)} == {
                (j+1) % p, ((j+1) % p)+p}
            assert {(9*j) % (2*p), (9*(j+p)) % (2*p)} == {
                (9*j) % p, ((9*j) % p)+p}
            assert (9*(j+1)) % p == (9*j+9) % p
    results['bilateral_projector_identities_exact'] = True
    results['compatible_embedding_levels_checked'] = 12
    bp = 0
    for p in range(1, 30):
        bp = 16*bp+16**(2*p-1)
        assert bp == 16**p*(16**p-1)//15
    results['second_derivative_majorant_levels_checked'] = 29
    results['scope'] = 'Finite exact controls; arbitrary-depth scope is proved in the document.'
    return results


def generate_receipts(digest):
    """Transport the verified antecedent genealogy and register the new maps."""
    const = json.loads((BASE/'RECIBO_CONSTANTES_FEIGENBAUM.json').read_text())
    const['artifact'] = str(DOC)
    const['artifact_sha256'] = digest
    const['result_id'] = 'FEIGENBAUM_NONADIC_INFINITE_ITINERARY_20260929'
    const['result'] = {
        'id': const['result_id'], 'file': str(DOC),
        'statement': 'Conservative refinement, arbitrary-horizon reading, an infinite period-doubling itinerary and nested return intervals for every eta in the declared strip.',
        'domain': 'Fixed HMT critical reader; |eta|<=1/40; prescribed lambda interval.',
        'operation': 'Block composition, parameter cylinders, itinerary continuity, repeated normalized returns and compatible bilateral memory.',
        'coefficients': 'Inherited twelve phases and second moment; base nine from the memory chart; no Feigenbaum target as generator input.',
        'preserves': ['native genealogy', 'carry', 'ordered history', 'boundary multiplicity', 'separation of metric and symbolic conclusions'],
        'proof_locator': {'path': str(DOC), 'sha256': digest, 'anchor': '## 2. Crecimiento exterior y resolución interior'},
        'falsifier': 'Promote symbolic existence or memory conservation to a metric delta certificate.'
    }
    const['excluded_claims'] = ['UNIVERSAL_DELTA_LIMIT_CERTIFIED', 'UNIQUE_PARAMETER_PROVED', 'ASYMPTOTIC_TRANSVERSALITY_PROVED', 'EIGHT_ROOTS_GLOBAL_CASCADE_PROVED']
    (BASE/'RECIBO_CONSTANTES_PROLONGACION.json').write_text(json.dumps(const, ensure_ascii=False, indent=2)+'\n')
    rec = json.loads((BASE/'RECIBO_GENEALOGIA_FEIGENBAUM.json').read_text())
    rec['receipt_id'] = 'HMT-FEIGENBAUM-NONADIC-PROLONGATION-20260929'
    rec['artifact'] = {
        'path': str(DOC), 'sha256': digest, 'kind': 'DERIVATION',
        'anchors': [
            {'stage': 'APP', 'text': 'APP evalúa suma y producto'},
            {'stage': 'TRIT', 'text': 'TRIT determina régimen y orientación'},
            {'stage': 'TPK', 'text': 'El transporte TPK selecciona, transporta'},
            {'stage': 'ESTADO_ENRIQUECIDO', 'text': 'actualiza el estado con sus registros de acarreo, frontera y memoria'},
            {'stage': 'ESTRUCTURA_DISCRETA_CONTINUO', 'text': 'Sus lectores actúan sobre la misma estructura discreta del continuo.'},
            {'stage': 'HMT_OUTPUT', 'text': '## 2. Crecimiento exterior y resolución interior'},
            {'stage': 'CONVENTIONAL', 'text': 'La teoría de universalidad paramétrica de Lyubich'}
        ]
    }
    rec['target'].update({
        'statement': const['result']['statement'],
        'domain': 'F_HMT_eta',
        'codomain': 'HMT_Arbitrary_Depth_Return_Reader',
        'result_id': const['result_id'],
        'closure_criterion': 'Written existence, induction and completion proofs; metric delta, uniqueness and asymptotic transversality remain separate.'
    })
    new_results = [
        ('NONADIC_PARAMETER_READER', 'Parameter-cylinder return diameter < 9^(q-m), uniformly in the strip; m=2^N+r suffices.', 't=C_m/9^m; E_(q,m)=F_t^q(1/2); Lip(F)<9; carry and interval refinement retained.', '## 3. Presupuesto explícito'),
        ('NONADIC_BILATERAL_LIMIT', 'Compatible bilateral memory extends unitarily to the dyadic refinement limit and is conjugate to its ninth power.', 'C_(n+1)J_n=J_nC_n; U=P0 tensor I+P1 tensor C; S C S^-1=C^9.', '## 5. Memoria bilateral'),
        ('INFINITE_ITINERARY_EXISTENCE', 'For every |eta|<=1/40 an HMT family parameter realizes tau_j=(-1)^v2(j) for all j.', 'Continuous itinerary comparison, trapping of superstable returns and strict shift maximality prohibit jumping over tau.', '### 6.1. Realización'),
        ('NESTED_RETURNS_ALL_LEVELS', 'Every such realization has disjoint invariant return cycles of periods 2^n at every level.', 'J_n=conv(c_(2^n),c_(2^(n+1))); normalized two-step return preserves tau; disjointness by induction.', '### 6.3. Intervalos invariantes')
    ]
    for rid, statement, operation, anchor in new_results:
        doc_lines = DOC.read_text().splitlines()
        start = next(i for i, line in enumerate(doc_lines) if line.startswith(anchor))
        heading_depth = len(doc_lines[start])-len(doc_lines[start].lstrip('#'))
        end = next((i for i in range(start+1, len(doc_lines))
                    if doc_lines[i].startswith('#') and
                    len(doc_lines[i])-len(doc_lines[i].lstrip('#')) <= heading_depth), len(doc_lines))
        rec['result_maps'].append({
            'id': rid, 'statement': statement,
            'input_object': 'family_HMT_eta', 'domain': 'F_HMT_eta',
            'codomain': 'HMT_Arbitrary_Depth_Return_Reader', 'output_object': rid.lower(),
            'map': operation, 'generator_inputs': ['family_HMT_eta'], 'source_family': 'HMT',
            'structure_of_departure': 'Fixed Pcrit and declared deformation; native ledger, nonadic chronology and bilateral projections with explicit owners in section7.',
            'proof_locator': {'path': str(DOC), 'sha256': digest, 'anchor': anchor, 'lines': f'{start+1}-{end}'},
            'falsifier': 'Conflate phase, memory, parameter precision and metric renormalization; claim a universal delta error bound from finite ratios.'
        })
    rec['result_maps'].append({
        'id': const['result_id'], 'statement': const['result']['statement'],
        'input_object': 'family_HMT_eta', 'domain': 'F_HMT_eta',
        'codomain': 'HMT_Arbitrary_Depth_Return_Reader', 'output_object': 'feigenbaum_prolongation_dossier',
        'map': const['result']['operation'], 'generator_inputs': ['family_HMT_eta'], 'source_family': 'HMT',
        'proof_locator': {'path': str(DOC), 'sha256': digest, 'anchor': '### 6.4. Alcance', 'lines': f'1-{len(DOC.read_text().splitlines())}'},
        'requires': [x[0] for x in new_results], 'falsifier': const['result']['falsifier']
    })
    rec['excluded_claims'] = const['excluded_claims']
    rec['residual_if_any'] = 'Universal parametric scaling, certified tail bounds, transversal unstable projection, uniqueness and identification of the previously calculated roots with the infinite branch.'
    rec['conclusion_status'] = 'CONSTRUCTIVE_RESIDUAL_IDENTIFIED'
    rec['focal_scope_note'] = 'Ancestors remain finite claims with their original owners. Infinite claims are only the new written results; no original paper was edited.'
    (BASE/'RECIBO_GENEALOGIA_PROLONGACION.json').write_text(json.dumps(rec, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    result = checks()
    digest = hashlib.sha256(DOC.read_bytes()).hexdigest()
    result.update({'artifact': str(DOC), 'artifact_sha256': digest,
                   'status': 'PASS_CONTROLES_EXACTOS_PROLONGACION_FEIGENBAUM'})
    (BASE/'CONTROLES_PROLONGACION.json').write_text(json.dumps(result, indent=2)+'\n')
    generate_receipts(digest)
    print(result['status'])
    print(json.dumps(result, indent=2))
