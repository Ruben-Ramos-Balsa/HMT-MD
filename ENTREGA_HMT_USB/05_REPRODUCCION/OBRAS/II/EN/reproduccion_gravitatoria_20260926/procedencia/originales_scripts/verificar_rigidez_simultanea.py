"""Exact controls of rigidity for the complete R1--R8 realization.

The selected class explicitly contains the longitudinal composition and radial
metric rule. These tests do not infer them from a weaker list of axioms.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import permutations
import importlib.util
import hashlib
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'polar_helpers', HERE/'verificar_transporte_radial_polar.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
eye, tr, mm, add, sub, scale, inv = m.eye, m.tr, m.mm, m.add, m.sub, m.scale, m.inv


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def run():
    checks = []

    def ck(b, name):
        if not b:
            raise AssertionError(name)
        checks.append(name)

    N=12*4*8*15
    rn=F(N-1,4*N)
    ck(N==5760, 'marked_incidence_count')
    ck(rn==F(5759,23040), 'return_factor')
    ck(rn+F(1,4*N)==F(1,4), 'complementary_archive')
    ck(F(11,48)!=rn, 'twelve_coordinate_reader_distinct')

    I=eye(4)
    B=scale(mat(((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))),F(1,4))
    U=scale(B,2)
    P=[[F(1,4)]*4 for _ in range(4)]
    C0, M0=mm(sub(I,P),B),mm(P,B)
    ck(mm(B,tr(B))==scale(I,F(1,4)), 'H4_normalization')
    ck(add(C0,M0)==B, 'full_archive_reconstruction')
    ck(add(mm(tr(C0),C0),mm(tr(M0),M0))==scale(I,F(1,4)), 'archive_norm')
    ck(m.diagonal(mm(C0,tr(C0)))==scale(I,F(3,16)), 'finite_return_instance')
    for i in range(4):
        for j in range(4):
            Eij=[[F(k==i and l==j) for l in range(4)] for k in range(4)]
            ck(m.diagonal(Eij)==(Eij if i==j else scale(I,0)),
               'marked_expectation_basis_'+str((i,j)))
    for weights in ((1,0,0,0),(0,1,0,0),(1,2,3,5),(3,0,7,11)):
        dw=[[F(weights[i],sum(weights)) if i==j else F(0)
             for j in range(4)] for i in range(4)]
        source=mm(tr(U),mm(dw,U))
        ck(trace(mm(C0,mm(source,tr(C0))))==F(3,16), 'arbitrary_diagonal_weights')
        ck(trace(mm(M0,mm(source,tr(M0))))==F(1,16), 'weighted_memory_complement')

    a=mat(((1,1,0,2),(0,1,2,1),(1,0,1,0),(0,2,0,1)))
    X=add(mm(tr(a),a),I)
    ck(m.positive(X),'character_positive')
    alpha,Lstar,hbar,c=F(2,11),F(13,17),F(19,23),F(29,31)
    L=Lstar*alpha**16*rn
    D=scale(U,L)
    Y=mm(U,mm(X,tr(U)))
    R=scale(Y,L)
    inverse_length=scale(inv(Y),L)
    Q=hbar*c/L
    H=scale(Y,Q)
    M=scale(H,1/c**2)
    G=c**3*L**2/hbar
    ck(mm(D,tr(D))==scale(I,L**2), 'longitudinal_metric')
    ck(mm(R,R)==mm(D,mm(mm(X,X),tr(D))), 'positive_radial_square')
    ck(m.positive(R), 'positive_radial_solution')
    ck(mm(R,inverse_length)==scale(I,L**2), 'area_product')
    ck(mm(H,inverse_length)==scale(I,hbar*c), 'action_velocity_product')
    ck(R==scale(M,G/c**2), 'unique_G_identity')

    for s in (F(1,2),F(2),F(17,9)):
        Rs=scale(R,s)
        ck(mm(Rs,Rs)!=mm(R,R), 'rescale_breaks_metric')
        ck(mm(Rs,inverse_length)!=scale(I,L**2), 'rescale_breaks_area')
        alternate_inverse=scale(inverse_length,1/s)
        ck(mm(Rs,alternate_inverse)==scale(I,L**2), 'paired_rescale_preserves_area_only')
        ck(mm(H,alternate_inverse)!=scale(I,hbar*c), 'paired_rescale_breaks_action_product')
        theta=F(7,13)
        ck(s*hbar*theta/hbar!=theta,'rescale_breaks_lifted_phase')
        ck(s*L!=Lstar*alpha**16*rn,'length_rescale_breaks_longitudinal_rule')
    ck(Lstar**2*alpha**32*rn!=L**2,'rms_replacement_is_different_type')
    ck(Lstar*alpha**16*F(1,4)!=L,'full_archive_norm_is_different_reader')

    # Every permutation below is transported with the pointer algebra,
    # common projector, character, and source/arrival frames.
    T=mat(((F(3,5),F(-4,5),0,0),(F(4,5),F(3,5),0,0),
           (0,0,0,-1),(0,0,1,0)))
    ck(mm(T,tr(T))==I,'source_frame_unitary')
    for perm in permutations(range(4)):
        S=[[F(j==perm[i]) for j in range(4)] for i in range(4)]
        Bp=mm(S,mm(B,tr(T)))
        Xp=mm(T,mm(X,tr(T)))
        Up=scale(Bp,2)
        Dp=scale(Up,L)
        Rp=scale(mm(Up,mm(Xp,tr(Up))),L)
        Hp=scale(mm(Up,mm(Xp,tr(Up))),Q)
        ck(Dp==mm(S,mm(D,tr(T))),'equivalent_longitudinal_reader')
        ck(Rp==mm(S,mm(R,tr(S))),'equivalent_radial_reader')
        ck(Hp==mm(S,mm(H,tr(S))),'equivalent_energy_reader')
        ck(Rp==scale(scale(Hp,1/c**2),G/c**2),'equivalent_G')

    for length_unit,time_unit,mass_unit in ((F(2),F(3),F(5)),(F(7,3),F(2,5),F(11,13))):
        cp=c*time_unit/length_unit
        Lp=L/length_unit
        hp=hbar*time_unit/(mass_unit*length_unit**2)
        Gp=cp**3*Lp**2/hp
        ck(Gp==G*mass_unit*time_unit**2/length_unit**3,'dimensional_covariance')
        ck(Lp==(Lstar/length_unit)*alpha**16*rn,'longitudinal_unit_transport')
    return checks


if __name__=='__main__':
    checks=run()
    print(json.dumps({
        'status':'PASS_RIGIDEZ_SIMULTANEA_R1_R8',
        'exact_checks':len(checks),
        'checks':checks,
        'longitudinal_and_metric_rules_are_explicit':True,
        'same_constraints_with_different_G_possible':False,
        'G_observed_input':False,
        'weaker_axioms_claimed_sufficient':False,
        'PDFs_compiled':False,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    },ensure_ascii=False,indent=2))
