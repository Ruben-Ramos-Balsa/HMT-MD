import LatticeTwistedPairProduct

/-! A concrete state-field assignment on the existing two-sector carrier.
All four blocks are constructed. This file does not conflate that construction
with the further locality/Jacobi theorem or the Monster automorphism theorem. -/

noncomputable section
namespace HMT.IV.LatticeOrbifoldFullStateFields
open LatticeEvenVertexFields LatticeTwistedPositiveSector
open LatticeTwistedPositiveStateDescent LatticeOrbifoldCarrier
open LatticeOrbifoldEvenAction LatticeTwistedEvenProduct LatticeTwistedPairProduct

def stateField (o : Fin 12) : Space o →ₗ[ℂ] VertexOperator ℂ (Space o) :=
  stateFieldWithTT o (twistedPairField o)

theorem stateField_coefficient (o : Fin 12) (u v : Space o) (k : ℤ) :
    HVertexOperator.coeff (stateField o u) k v =
      (evenCoefficient o u.1 k v.1 + pairCoefficient o k u.2 v.2,
       HVertexOperator.coeff (positiveDescendedAssignment o u.1) k v.2 +
         HVertexOperator.coeff (twistedEvenField o u.2) k v.1) :=
  stateFieldWithTT_coefficient o (twistedPairField o) u v k

theorem stateField_vacuum (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (stateField o (vacuum o)) k =
      if k=0 then (1 : Module.End ℂ (Space o)) else 0 :=
  stateFieldWithTT_vacuum o (twistedPairField o) k

theorem stateField_creation (o : Fin 12) (u : Space o) :
    HVertexOperator.coeff (stateField o u) 0 (vacuum o) = u :=
  stateFieldWithTT_creation o (twistedPairField o) u

theorem stateField_negative_vacuum (o : Fin 12) (u : Space o)
    (k : ℤ) (hk : k<0) :
    HVertexOperator.coeff (stateField o u) k (vacuum o) = 0 :=
  stateFieldWithTT_negative_vacuum o (twistedPairField o) u k hk

theorem stateField_injective (o : Fin 12) : Function.Injective (stateField o) :=
  stateFieldWithTT_injective o (twistedPairField o)

theorem stateField_twisted_even (o : Fin 12) (u : positiveSector o)
    (v : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (stateField o (0,u)) k (v,0) =
      (0, HVertexOperator.coeff (twistedEvenField o u) k v) :=
  stateFieldWithTT_twisted_even o (twistedPairField o) u v k

theorem stateField_twisted_twisted (o : Fin 12)
    (u v : positiveSector o) (k : ℤ) :
    HVertexOperator.coeff (stateField o (0,u)) k (0,v) =
      (pairCoefficient o k u v, 0) :=
  stateFieldWithTT_twisted_twisted o (twistedPairField o) u v k

theorem stateField_conformal_coefficient (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff (stateField o (conformalState o)) (-m-2) = modes o m :=
  stateFieldWithTT_conformal_coefficient o (twistedPairField o) m

theorem stateField_conformal_virasoro (o : Fin 12) (m n : ℤ) :
    HVertexOperator.coeff (stateField o (conformalState o)) (-m-2) *
      HVertexOperator.coeff (stateField o (conformalState o)) (-n-2) -
    HVertexOperator.coeff (stateField o (conformalState o)) (-n-2) *
      HVertexOperator.coeff (stateField o (conformalState o)) (-m-2) =
    ((m-n:ℤ):ℂ) • HVertexOperator.coeff (stateField o (conformalState o)) (-(m+n)-2) +
      (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
        (LinearMap.id : Module.End ℂ (Space o)) else 0) := by
  simp only [stateField_conformal_coefficient]
  exact virasoro_central_charge_twentyFour o m n

end HMT.IV.LatticeOrbifoldFullStateFields
end

#print axioms HMT.IV.LatticeOrbifoldFullStateFields.stateField
#print axioms HMT.IV.LatticeOrbifoldFullStateFields.stateField_creation
#print axioms HMT.IV.LatticeOrbifoldFullStateFields.stateField_conformal_virasoro
