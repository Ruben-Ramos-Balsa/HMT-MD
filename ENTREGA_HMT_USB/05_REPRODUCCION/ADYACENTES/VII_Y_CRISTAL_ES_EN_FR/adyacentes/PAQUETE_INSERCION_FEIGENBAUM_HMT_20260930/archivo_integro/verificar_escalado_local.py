#!/usr/bin/env python3
"""Exact checks and provenance for the written local scaling theorem.

This checks rational controls and the finite covers used by the written global
first-root theorem. It does not replace its analytic proofs or the imported
renormalization theorems, which remain explicit dependencies.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

BASE = Path(__file__).resolve().parent
DOC = BASE/'TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md'
EXCLUDED = ['FINITE_DELTA8_LIMIT_ERROR_CERTIFIED',
            'NUMERIC_PARAMETER_TAIL_CONSTANTS_CERTIFIED', 'ETA_NONZERO_TRANSVERSALITY_CERTIFIED']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first_exit_controls():
    """Check the exact first-exit bounds, tiling and stored cap witnesses.

    Full trajectory regeneration is performed by certificar_caps_kneading.py;
    here its audited implementation and completed output are pinned by hash.
    """
    script = BASE/'certificar_caps_kneading.py'
    path = BASE/'CERTIFICADO_CAP_NEGATIVA_PRIMERA_SALIDA.json'
    assert digest(script) == '1799cbce76516509ece9d614f1d4f54a6748a0d645fac5b3fd15d1113a5f0ccb'
    assert digest(path) == '39922813f8010b215869d7a7c80db41b3cb0f88c20f0448ac8d744068cd103b5'
    data = json.loads(path.read_text())
    assert data['status'] == 'PASS_NEGATIVE_FIRST_EXIT_CAP_EXCLUSION'
    assert data['failed_intervals'] == 0 and not data['failures']
    cap = data['cap']
    lo, hi = map(Q, cap['du_band'])
    k, L, h = Q('.21'), Q('.16'), Q('.006')
    lower = Q('4.521')-Q('.560')*k
    upper_u = 1+Q('1.9')*Q('3.669')
    upper = upper_u+Q('.560')*k
    assert lower == Q('4.4034') > 1
    assert upper_u == Q('7.9711') and upper == Q('8.0887')
    assert Q('.756')+Q('.719')*k < k*lower
    assert Q('551.757') < k*Q('3821.289115')
    initial = Q('.004993128')+Q('.00004')+L*(Q('.001396077')+Q('.00004'))
    assert initial == Q('.00526290032') < h
    inside = (1+k)*h+Q('.001666')+Q('.00004')
    assert inside == Q('.008966') < Q('.01')
    assert lo == h and hi == upper*h == Q('.0485322')
    assert Q(cap['cone_slope']) == k and Q(cap['stable_graph_slope']) == L
    assert Q(cap['stable_norm_radius']) == Q('.001666')
    assert Q(cap['fixed_point_error']) == Q('.00004')
    assert cap['restricted_to_self_maps']
    cursor, signs, contractions = lo, 0, 0
    largest_lip, max_horizon = Q(0), 0
    for leaf in data['certificates']:
        a, b = map(Q, leaf['du_band'])
        assert a == cursor and a < b
        cursor = b
        assert leaf['status'] == 'PASS_FINITE_KNEADING_CAP_EXCLUSION'
        assert leaf['sign'] == -1 and leaf['restricted_to_self_maps']
        assert Q(leaf['extra_norm_radius']) == Q('.001666')
        assert Q(leaf['cone_slope']) == k
        assert Q(leaf['stable_residual_slope']) == L
        assert leaf['order'] == 40
        if 'contradiction_at' in leaf:
            j = leaf['contradiction_at']
            witness = next(v for v in leaf['observations'] if v['iterate'] == j)
            tau = 1 if ((j & -j).bit_length()-1) % 2 == 0 else -1
            assert witness['tau'] == tau
            l, r = map(Q, (witness['enclosure']['lower'], witness['enclosure']['upper']))
            assert l <= r
            assert r < 0 if tau > 0 else l > 0
            signs += 1
            max_horizon = max(max_horizon, j)
        else:
            witness = leaf['contraction_exclusion']
            p = witness['return_period']
            assert p >= 8 and p & (p-1) == 0
            radius = Q(witness['critical_radius'])
            lip = Q(witness['return_lipschitz_bound'])
            assert 0 <= radius < 1 and 0 <= lip < 1
            largest_lip = max(largest_lip, lip)
            max_horizon = max(max_horizon, 2*p)
            contractions += 1
    assert cursor == hi == Q(data['cover_endpoint'])
    assert len(data['certificates']) == data['covered_intervals'] == 64
    assert signs == 54 and contractions == 10 and max_horizon == 64
    return {'status':data['status'], 'bands':64, 'failed_bands':0,
            'exact_tiling':True, 'opposite_sign_bands':signs,
            'contractive_return_bands':contractions,
            'largest_return_lipschitz_bound':str(largest_lip),
            'largest_exclusion_horizon':max_horizon,
            'secant_cone_slope':str(k), 'minimum_expansion':str(lower),
            'maximum_expansion':str(upper), 'first_exit_interval':[str(lo),str(hi)],
            'initial_separation_upper':str(initial), 'pre_exit_ball_bound':str(inside),
            'global_limit_equals_local_crossing_by_written_first_exit_proof':True,
            'script_sha256':digest(script), 'certificate_sha256':digest(path)}


def itinerary_bridge_controls():
    """Validate the exact cover and each stored exclusion inequality."""
    path = BASE/'CERTIFICADO_PUENTE_ITINERARIO.json'
    data = json.loads(path.read_text())
    assert data['status'] == 'PASS_EXCLUSION_LAMBDA_TAU_ON_FULL_BRIDGE'
    assert data['full_exclusion'] and not data['pending_intervals']
    for name, sha in data['sha256'].items():
        assert digest(BASE/name) == sha
    leaves = data['certified_leaves']
    pairs = sorted((Q(v['interval']['lower']), Q(v['interval']['upper']))
                   for v in leaves)
    assert pairs[0][0] == Q(data['interval']['lower'])
    assert pairs[-1][1] == Q(data['interval']['upper']) == Q('1.874038')
    assert all(a[1] == b[0] for a, b in zip(pairs, pairs[1:]))
    counts = {}
    for leaf in leaves:
        lo, hi = Q(leaf['return_interval']['lower']), Q(leaf['return_interval']['upper'])
        assert lo <= hi
        method = leaf['method']
        counts[method] = counts.get(method, 0)+1
        if method == 'opposite_itinerary_sign':
            j = leaf['iteration']
            v2 = (j & -j).bit_length()-1
            assert hi < 0 if v2 % 2 == 0 else lo > 0
        else:
            assert method == 'equal_sign_double_return'
            p = leaf['period']
            assert p >= 256 and p & (p-1) == 0
            bound = Q(leaf['second_derivative_upper'])
            assert bound >= 0 and max(abs(lo), abs(hi))*bound < 2
    assert counts == data['counts']
    return {'status':'PASS_EXCLUSION_LAMBDA_TAU_ON_FULL_BRIDGE',
            'interval':data['interval'], 'leaves':len(leaves),
            'counts':counts, 'exact_endpoint_tiling':True,
            'all_stored_sign_and_taylor_inequalities_checked':True,
            'certificate_sha256':digest(path),
            'scope':'Exclusion on the covered interval; local stable-sheet identity is not asserted.'}


def jacobi_and_oriented_sensitivity():
    """Exact spectral intertwiner and a finite test of the proposed moment lift.

    The Jacobi matrix represents the twelve frequency nodes, not parameter roots.
    The second test rejects one proposed positive-moment proof; it is not a
    counterexample to positive transversality or to the global cascade.
    """
    nodes = [Q(4*(3*m-1)**2, 899) for m in range(1, 13)]

    def value(poly, x):
        result = Q(0)
        for coefficient in reversed(poly):
            result = result*x+coefficient
        return result

    def inner(a, b):
        return sum((value(a, s)*value(b, s) for s in nodes), Q(0))/12

    polynomials, norms = [], []
    for degree in range(13):
        p = [Q(0)]*degree+[Q(1)]
        for previous, norm in zip(polynomials, norms):
            coefficient = inner(p, previous)/norm
            for j, v in enumerate(previous):
                p[j] -= coefficient*v
        norm = inner(p, p)
        if degree == 12:
            assert norm == 0 and all(value(p, s) == 0 for s in nodes)
        else:
            assert norm > 0
            polynomials.append(p)
            norms.append(norm)
    assert all(inner(a, b) == 0 for j, a in enumerate(polynomials)
               for b in polynomials[:j])
    diagonal = [inner([Q(0)]+p, p)/h for p, h in zip(polynomials, norms)]
    beta = [norms[j]/norms[j-1] for j in range(1, 12)]
    matrix = [[Q(0) for _ in range(12)] for _ in range(12)]
    for j in range(12):
        matrix[j][j] = diagonal[j]
        if j < 11:
            matrix[j+1][j] = 1
            matrix[j][j+1] = beta[j]
    evaluations = [[value(p, s) for p in polynomials] for s in nodes]
    # V T = D V, exactly, in the monic basis. Positive diagonal metric H
    # converts T to the symmetric Jacobi matrix with off-diagonal sqrt(beta).
    for i, s in enumerate(nodes):
        for j in range(12):
            assert sum(evaluations[i][k]*matrix[k][j] for k in range(12)) == s*evaluations[i][j]
            assert norms[i]*matrix[i][j] == norms[j]*matrix[j][i]
    assert diagonal[0] == 2 and sum(diagonal) == sum(nodes)
    vector = [Q(1)]+[Q(0)]*11
    for degree in range(31):
        assert vector[0] == sum(s**degree for s in nodes)/12
        vector = [sum(matrix[i][j]*vector[j] for j in range(12)) for i in range(12)]

    spec = importlib.util.spec_from_file_location('roots_spectral_check', BASE/'certificar_raices.py')
    roots = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = roots
    spec.loader.exec_module(roots)
    certificate = json.loads((BASE/'CERTIFICADO_RAICES_INTERVALOS.json').read_text())
    box = next(v['root_interval'] for v in certificate['root_certificates'] if v['level'] == 2)
    lo, hi = roots.Interval.rational(box['lower']), roots.Interval.rational(box['upper'])
    parameter = roots.Interval(lo.lo, hi.hi)
    family = roots.Family()
    x, derivative, product = roots.Interval.rational(1), roots.Interval.rational(0), roots.Interval.rational(1)
    oriented, weights = roots.Interval.rational(0), []
    for j in range(1, 4):
        potential, slope = family.potential(x)
        product = product*(-parameter*slope)
        assert not product.contains_zero()
        assert product.sign() == (-1)**bin(j).count('1')
        positive_product = product if product.sign() > 0 else -product
        weights.append(potential/positive_product)
        oriented = oriented-potential/product
        derivative = -potential-parameter*slope*derivative
        x = 1-parameter*potential
    quotient = derivative/product
    assert max(quotient.lo, oriented.lo) <= min(quotient.hi, oriented.hi)
    assert oriented.lo > 0
    assert weights[2].lo > weights[1].hi  # Reject moments of a positive measure on [0,1].
    return {'jacobi_dimension':12, 'positive_gram_norms':12, 'next_gram_rank':12,
            'exact_VT_equals_DV':True, 'exact_weighted_self_adjointness':True,
            'moments_checked':31, 'a0':str(diagonal[0]), 'beta1':str(beta[0]),
            'period4_oriented_transversality':oriented.record(),
            'period4_weights_t1_t2_t3':[w.record() for w in weights],
            'positive_measure_on_unit_interval_candidate_rejected':True,
            'scope':'Exact finite spectral representation and oriented sensitivity; global identification is proved separately in sections15-17.'}


def controls():
    a,b,c,d = map(Q, ('4.521','.560','.756','.719'))
    L,r,eps = Q('.16'),Q('.004'),Q('.00004')
    A,q = a-L*c,d+c*L
    assert (1+L)*r+eps < Q('.01')
    assert A*L-b-L*d == Q('.0289664') > 0
    assert (b+L*d)/A<L and 1/A<Q('.228') and q==Q('.83996')<1
    assert (c+d/4)/(a-b/4)<Q(1,4)
    # Negative controls: both an excessively narrow graph and a wide graph fail.
    assert (a-Q('.1')*c)*Q('.1')-b-Q('.1')*d<0
    assert d+c*Q('.5')>1
    entry=json.loads((BASE/'CERTIFICADO_ENTRADA_RENORMALIZACION.json').read_text())
    pieces=entry['pieces']
    assert len(pieces)==16 and entry['order']==32
    intervals=[tuple(map(Q,p['parameter_interval'])) for p in pieces]
    assert intervals[0][0]==Q('1.874038') and intervals[-1][1]==Q('1.874039')
    assert all(x[1]==y[0] for x,y in zip(intervals,intervals[1:]))
    lower_tangent=None
    for piece in pieces:
        levels=piece['levels']
        assert [v['level'] for v in levels]==list(range(5))
        for state in levels[1:]:
            assert state['real_return_domain_certified']
            ai,bi,ci=state['scale_a'],state['b_equals_fa'],state['f_of_b']
            assert 0<Q(ai['lower'])<=Q(ai['upper'])<1
            assert Q(bi['lower'])>Q(ai['upper']) and Q(ci['upper'])<Q(ai['lower'])
            assert Q(state['inner_argument_l1'])<1 and Q(state['outer_argument_l1'])<1
        st=levels[-1]
        assert Q(st['distance_to_Lanford_centre_upper'])<Q('.004993128')
        assert Q(st['nu_distance_centre_upper'])<Q('.001396077')
        assert Q(st['value_error_l1'])<Q('8.482e-19')
        assert Q(st['tangent_error_l1'])<Q('4.569e-15')
        du,dy=Q(st['du_interval']['lower']),Q(st['nu_tangent_l1_upper'])
        assert du>Q('3821.289115') and dy<Q('551.757000') and 4*dy<du
        transverse=du-L*dy
        lower_tangent=transverse if lower_tangent is None else min(lower_tangent,transverse)
    assert lower_tangent>Q('3733.007995')
    crossing=entry['stable_graph_crossing']
    assert Q(crossing['left_signed_margin_upper'])<Q('-.0011856110945')
    assert Q(crossing['right_signed_margin_lower'])>Q('.0021866053399')
    assert crossing['opposite_sides'] and crossing['whole_curve_in_graph_domain']
    assert crossing['whole_curve_positive_transverse']
    assert (1+L)*(Q('.001396077')+eps)<Q('.001666')
    # Independent low-degree test of the exact return and its parameter tangent.
    spec=importlib.util.spec_from_file_location('entry_local',BASE/'certificar_entrada_renormalizacion.py')
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    p=Q(7,5);scale=p-1
    v=mod.Dual(mod.Series.const(mod.I.rational(p)),mod.Series.const(1))
    w,_=mod.renormalize(v)
    expected=[2*p*p*scale-p**3*scale**3,-Q(5,2)*p**3*scale**3]
    derivative=[4*p*scale+2*p*p-3*p*p*scale**3-3*p**3*scale**2,
                -Q(5,2)*(3*p*p*scale**3+3*p**3*scale**2)]
    for series,values in ((w.v,expected),(w.d,derivative)):
        for i,box in enumerate(series.c):
            value=values[i] if i<len(values) else Q(0)
            assert Q(box.lo-series.err,mod.S)<=value<=Q(box.hi+series.err,mod.S)
    centre=list(map(Q,mod.CENTRE))
    verror=Q('.004')
    spread=sum(abs(x)*Q(2,5)**j for j,x in enumerate(centre) if j)
    slope=sum(j*abs(x)*Q(2,5)**(j-1) for j,x in enumerate(centre) if j)
    assert centre[0]-spread-verror>Q(6,5)
    assert centre[0]+spread+verror<Q(8,5)
    assert slope+Q('.01')<Q(1,2)
    assert Q('0.39')<centre[0]-1-Q('.001')
    assert centre[0]-1+Q('.001')<Q('.41')
    assert 1-Q('.41')**2*Q(8,5)==Q(4569,6250)>Q('.41')
    assert 1-Q(4569,6250)**2*Q(6,5)==Q(35028967,97656250)<Q('.39')
    finite=json.loads((BASE/'CERTIFICADO_CONTINUACION_FINITA.json').read_text())
    assert finite['status']=='PASS_FINITE_ROOT_CONTINUATION'
    assert finite['source_certificate_sha256']==digest(BASE/'CERTIFICADO_RAICES_INTERVALOS.json')
    assert finite['script_sha256']==digest(BASE/'certificar_continuacion_finita.py')
    assert [x['level'] for x in finite['reports']]==list(range(2,9))
    for report in finite['reports']:
        assert report['status']=='PASS_EXACTLY_TWO_ROOTS_ON_COVERED_INTERVAL'
        boxes=report['known_roots']+[x['interval'] for x in report['certified_leaves']]
        pairs=sorted((Q(v['lower']),Q(v['upper'])) for v in boxes)
        assert pairs[0][0]==Q(report['interval']['lower'])
        assert pairs[-1][1]==Q(report['interval']['upper'])
        assert all(x[1]==y[0] for x,y in zip(pairs,pairs[1:]))
    files=['certificar_entrada_renormalizacion.py','CERTIFICADO_ENTRADA_RENORMALIZACION.json',
           'certificar_continuacion_finita.py','CERTIFICADO_CONTINUACION_FINITA.json',
           'certificar_puente_itinerario.py','CERTIFICADO_PUENTE_ITINERARIO.json',
           'certificar_caps_kneading.py','CERTIFICADO_CAP_NEGATIVA_PRIMERA_SALIDA.json',
           'CLASIFICACION_ITINERARIOS_FEIGENBAUM.md']
    return {'status':'PASS_CONTROLES_ESCALADO_LOCAL_FEIGENBAUM',
            'artifact':str(DOC),'artifact_sha256':digest(DOC),
            'stable_graph':{'radius':str(r),'slope':str(L),'expansion':str(A),'contraction':str(q)},
            'uniform_transverse_lower_bound_conservative':'3733.007995',
            'operator_tail':'0.001666*(0.83996)^n; n>=0',
            'parameter_tail':'O(theta^j), existential 0<theta<1; numeric constants unevaluated',
            'finite_roots':8,'coverage_leaves':sum(len(x['certified_leaves']) for x in finite['reports']),
            'quadratic_return_and_tangent_exact_test':True,
            'spectral_and_oriented_controls':jacobi_and_oriented_sensitivity(),
            'itinerary_bridge':itinerary_bridge_controls(),
            'first_exit':first_exit_controls(),
            'negative_graph_controls_detected':2,
            'dependencies':{f:digest(BASE/f) for f in files},
            'imported_theorems':['Lanford hyperbolicity bounds','Eckmann-Wittwer unstable crossing',
                                 'Collet-Eckmann-Lanford section6 local scaling',
                                 'de Faria-de Melo-Pinto Theorem2.1 and Lemma3.2 quadratic-like realization',
                                 'Lyubich Theorem7.4 unique hybrid-class intersections; Lemma7.3 holonomy'],
            'excluded_claims':EXCLUDED}


def receipts():
    sha=digest(DOC);lines=DOC.read_text().splitlines()
    def locator(anchor):
        start=next(i for i,line in enumerate(lines) if line.startswith(anchor))
        depth=len(lines[start])-len(lines[start].lstrip('#'))
        end=next((i for i in range(start+1,len(lines)) if lines[i].startswith('#') and
                  len(lines[i])-len(lines[i].lstrip('#'))<=depth),len(lines))
        return {'path':str(DOC),'sha256':sha,'anchor':anchor,'lines':f'{start+1}-{end}'}
    rid='HMT_FEIGENBAUM_TRANSVERSE_LOCAL_SCALING_20260929'
    statement='Uniform HMT reader: all successive first exact-period roots exist, have the canonical doubling itinerary and converge to the certified stable crossing. Negative first-exit exclusion identifies the limit; fixed-neighbourhood hybrid-class uniqueness identifies the eventual centres. The original global gap ratios converge to delta with an existential power remainder. Ordered root-set transport and the twelve-node Jacobi realization preserve the HMT antecedent.'
    const=json.loads((BASE/'RECIBO_CONSTANTES_PROLONGACION.json').read_text())
    const.update(artifact=str(DOC),artifact_sha256=sha,result_id=rid,excluded_claims=EXCLUDED)
    const['result'].update(id=rid,file=str(DOC),statement=statement,
        domain='Uniform eta=0 HMT family and its global first-root selector; local stable crossing in J=[1.874038,1.874039].',
        operation='Analytic first-root existence, inductive classification, sign-margin convergence and bridge exclusion; exact tangent, stable graph and negative first-exit exclusion; quadratic-like realization and unique hybrid-class intersections; global metric scaling and ordered-field transport.',
        coefficients='HMT twelve phases and exact second moment; published Lanford centre and bounds only as posterior analytic certificate.',
        proof_locator=locator('## 17. Identificación'),
        falsifier='Omit the first-exit overshoot, the stable-residual slope or fixed-neighbourhood uniqueness; assign the operator rate or finite-root precision to the parameter error.')
    const['receipt_purpose']='Causal provenance control; the analytic proofs and their imported theorems are separate mathematical dependencies.'
    const['external_proof_dependencies']=['Lanford','Hertling-Spandl','Eckmann-Wittwer','Collet-Eckmann-Lanford','de Faria-de Melo-Pinto Theorem2.1 and Lemma3.2','Lyubich Theorem7.4 and Lemma7.3']
    (BASE/'RECIBO_CONSTANTES_ESCALADO_LOCAL.json').write_text(json.dumps(const,ensure_ascii=False,indent=2)+'\n')
    rec=json.loads((BASE/'RECIBO_GENEALOGIA_PROLONGACION.json').read_text())
    rec.update(receipt_id=rid,excluded_claims=EXCLUDED,conclusion_status='CLOSED_IN_HMT_DOMAIN',
        residual_if_any=None,
        focal_scope_note='Closure concerns the uniform eta=0 global first-root limit and universal gap scaling, with explicit imported analytic dependencies. Numerical remainder constants and the effective onset level are not claimed; antecedents retain their own owners.')
    rec['artifact'].update(path=str(DOC),sha256=sha)
    for anchor in rec['artifact']['anchors']:
        if anchor['stage']=='HMT_OUTPUT':anchor['text']='El lector resultante es'
        if anchor['stage']=='CONVENTIONAL':anchor['text']='## 3. Cotas externas utilizadas como reconocimiento posterior'
    rec['target'].update(statement=statement,domain='F_HMT',codomain='HMT_Local_Doubling_Cascade',
        result_id=rid,closure_criterion='Every first root exists, preserves W_n0, converges to the local stable crossing and eventually equals the local centre of the same period; its successive gap ratio tends to delta.')
    rec['proof_layers']['limit']={'required':True,
        'proof_locator':locator('## 17. Identificación'),
        'finite_levels':'Original successive first exact-period roots lambda_n, their normalized real returns and eventual identification with local target preimages of the same period.',
        'bonding_maps':'R maps one normalized return to the next; restrictive-return induction preserves W_n0, the stable graph preserves its sheet, and hybrid-class uniqueness identifies the eventual centres.',
        'compatibility_identity':'R^(m+n)=R^m composed with R^n on the certified real domains; y_next=V(sigma(y),y) and U(sigma(y),y)=sigma(y_next). The normal target coordinate satisfies z_j=delta^(-j).',
        'limit_object':'The fixed analytic map g; min Lambda_tau equals lambda_star; all original first roots increase to that limit and their gap ratios converge to delta.',
        'proof':'Sections15-16: all-root induction, nonzero sign margins, full bridge cover and first-exit cap prove min Lambda_tau=lambda_star. Section17: fixed-neighbourhood hybrid-class uniqueness yields eventual centre identity; C1beta holonomy and unstable linearization yield global scaling with power remainder.',
        'operation':'Ordered minimum transport, restrictive returns, uniform first-exit isolation, unique hybrid-class intersection and C1beta holonomy.',
        'typing_falsifier':'Conflate local cascade, global first-root selection, numerical root precision and asymptotic error.'}
    results=[
      ('HMT_REAL_RETURN_ENTRY','R^4 f_lambda is inside the analytic hyperbolic neighbourhood; its tangent lies in the expanding cone.', 'Exact moment series and dual return composition with arbitrary analytic l1 error.', '## 4. Certificado'),
      ('HMT_STABLE_GRAPH_TRANSVERSALITY','Exactly one stable crossing exists in J and is positively transverse.', 'Inverse graph contraction A^-1, endpoint margins and u_prime-L*norm(nu_prime)>3733.007995.', '## 6. Existencia'),
      ('HMT_OPERATOR_ASYMPTOTIC_BOUND','The stable trajectory has norm error below .001666*.83996^n.', 'Graph invariance, ||y_n||<=q^n||y_0||, preserved real return domains.', '## 5. Construcción'),
      ('HMT_LOCAL_METRIC_SCALING','The local superstable parameter gaps converge with ratio delta and an existential power remainder.', 'HMT family crossing plus EW target crossing and CEL local scaling, strengthened by C1beta interpolation.', '## 8. Escalado'),
      ('HMT_FIRST_EIGHT_ROOTS','The eight certified roots are successive first new roots on the declared ranges.', 'Exact endpoint tiling, sign exclusion, derivative exclusion and inherited root anchors.', '## 9. Continuación'),
      ('HMT_UPSTREAM_PARAMETER_INDEPENDENCE','For the declared free-parameter family, an antecedent-constant predicate is constant on the parameter fibre.', 'C_tilde(B,lambda)=C(B); substitution proves the predicate selects either all lambda or none.', '### 13.2. Independencia'),
      ('HMT_MINIMUM_TRANSPORT_CRITERION','A monotone reader sends a genealogical minimum to the original global root minimum exactly when its image is coinitial.', 'For every root z choose p with L(p)<=z; monotonicity gives L(p_min)<=L(p)<=z. Full-reader coverage is recovered in section14.1; sections15-17 identify the subsequent dynamic branch.', '### 13.3. Lema'),
      ('HMT_MINIMUM_SURVIVING_ITINERARY','Finite compact sign-margin constraints have increasing minima converging to the least parameter realizing the infinite doubling itinerary.', 'Use nonempty compact Lambda_tau from the antecedent section6, margins 1/B_j and nested closed A_N. Their minima converge to min Lambda_tau. No identity with finite first roots or the local stable crossing is asserted.', '### 13.6. Selección'),
      ('HMT_CRITICAL_HISTORY_INVERSE','The complete critical history determines the parameter through its second value.', 'c2=1-lambda*u0(1) and u0(1)>0 imply lambda=(1-c2)/u0(1). A sign itinerary retains less information than the complete critical history.', '### 13.7. Recuperación'),
      ('HMT_ORDERED_GLOBAL_ROOT_TRANSPORT','The ordered field isomorphism of Article XI transports the full return-zero sets, exact periods and root minima whenever those minima exist, in its declared internal universe.', 'Construct the cosine series and the twelve-phase return in the HMT ordered completion first. Preservation of rational coefficients, positive square root, limits and iteration proves return intertwining; surjectivity and order prove root coverage and minimum preservation.', '### 14.1. Cobertura'),
      ('HMT_DODECAPHASIC_JACOBI_REALIZATION','The twelve-node Jacobi matrix preserves the complete uniform critical profile and every moment.', 'Positive Gram forms up to degree11 produce orthogonal Q and DQ=QJ; finite spectral calculus gives u0(x)=e0^T[I-cos(x sqrt(J))]e0. Exact rational VT=DV, weighted self-adjointness and moments0..30 are checked.', '### 14.2. Representación'),
      ('HMT_ORIENTED_RETURN_SENSITIVITY','The normalized critical derivative equals the oriented orbital sum; a proposed positive-measure lift on the unit interval fails at period4 although oriented sensitivity there is positive.', 'Differentiate and telescope q_(j+1)=-u(cj)+f_prime(cj)qj. The canonical itinerary gives sign Dj=(-1)^s2(j). Certified period4 intervals give T2>0 and t3>t2, excluding that moment representation only.', '### 14.3. Sensibilidad'),
      ('HMT_GLOBAL_FIRST_ROOT_CONTINUATION','Every successive first exact-period root exists, has word W_n0 and converges increasingly to min Lambda_tau.', 'Before min Lambda_tau all kneading words are below tau. Restrictive-return induction classifies exact2^n centres. The last inherited zero provides existence of a new exact-period centre, while the selector remains the first. Fixed-horizon Taylor margins preserve every sign at the limit.', '### 15.2. Límite'),
      ('HMT_COMPLETE_ITINERARY_BRIDGE_EXCLUSION','There is no realization of tau between the certified lower endpoint of root8 and 1.874038.', 'Exact tiling by374 rational intervals:331 contrary-sign exclusions and43 equal-sign double-return exclusions with M times |return|<2.', '### 15.3. Certificado'),
      ('HMT_GLOBAL_LIMIT_IN_LOCAL_PARAMETER_INTERVAL','The global first-root limit satisfies 1.874038<min Lambda_tau<=lambda_star<1.874039.', 'Use the infinite selector theorem, the complete bridge exclusion and the tau realization provided by the stable crossing. Section16 supplies the additional isolation argument.', '### 15.4. Localización'),
      ('HMT_FIRST_EXIT_ISOLATION','The least realization of tau is exactly the certified local stable crossing.', 'A negative cone secant expands by at least4.4034 and at most8.0887. Its first exit lies in the full cap [.006,.0485322]. All64 rational cap bands exclude tau using shared-coefficient Taylor bounds with stable slope .16, so an earlier realization is impossible.', '## 16. Aislamiento'),
      ('HMT_EVENTUAL_ORIGINAL_CENTRE_IDENTITY','The original first roots coincide eventually with local centres indexed by physical period.', 'Analytic convergence gives a fixed quadratic-like realization. W_n0 identifies the canonical superstable hybrid class. Lyubich7.4 gives a unique intersection in a fixed parameter neighbourhood; lambda_n convergence puts the original roots there.', '### 17.2. Unicidad'),
      ('HMT_GLOBAL_FEIGENBAUM_SCALING','The original first-root gaps have limit ratio delta, with an existential power remainder.', 'Use eventual centre identity and C1beta hybrid holonomy with nonzero derivative on the unstable linearizing coordinate; take successive parameter differences with denominator bounded away from zero.', '### 17.3. Teorema')]
    for key,assertion,operation,anchor in results:
        rec['result_maps'].append({'id':key,'statement':assertion,'input_object':'family_HMT',
            'domain':'F_HMT','codomain':'HMT_Local_Doubling_Cascade','output_object':key.lower(),
            'map':operation,'generator_inputs':['family_HMT'],'source_family':'HMT',
            'structure_of_departure':'Fixed HMT reader; posterior analytic certificates and renormalization theorems explicitly cited in the document, with domains checked before application.',
            'proof_locator':locator(anchor),
            'falsifier':'Violate the domain, analytic error bounds, branch selection or separation of operator and parameter errors.'})
    rec['result_maps'].append({'id':rid,'statement':statement,'input_object':'family_HMT',
        'domain':'F_HMT','codomain':'HMT_Local_Doubling_Cascade','output_object':'local_scaling_dossier',
        'map':const['result']['operation'],'generator_inputs':['family_HMT'],'source_family':'HMT',
        'requires':[x[0] for x in results],'proof_locator':locator('## 17. Identificación'),
        'falsifier':const['result']['falsifier']})
    rec['conventional_uses'].append({'name':'Lanford and Hertling-Spandl bounds; EW target; CEL local scaling; de Faria-de Melo-Pinto realization; Lyubich hybrid uniqueness and holonomy.',
        'role':'PROOF_LANGUAGE','locator':locator('## 17. Identificación'),'occurs_after_hmt_output':True,
        'selects_hmt_state':False,'selects_route':False,'sets_generators':False,'sets_coefficients':False,
        'target_value_used_as_input':False,
        'scope_note':'The family and original first-root selector are constructed first. Imported theorems then identify the eventual local and global centres and the universal scaling; no target value is inserted into the generator.'})
    rec['additional_proof_owners'] = [{
        'path':str(BASE/'CLASIFICACION_ITINERARIOS_FEIGENBAUM.md'),
        'sha256':digest(BASE/'CLASIFICACION_ITINERARIOS_FEIGENBAUM.md'),
        'scope':'Complete proof of classification, all first-root existence and convergence to the least infinite itinerary; detailed metric transfer with stated analytic dependencies.'}]
    (BASE/'RECIBO_GENEALOGIA_ESCALADO_LOCAL.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    report=controls()
    receipts()
    (BASE/'CONTROLES_ESCALADO_LOCAL.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(report['status'])
    print(json.dumps(report,ensure_ascii=False,indent=2))
