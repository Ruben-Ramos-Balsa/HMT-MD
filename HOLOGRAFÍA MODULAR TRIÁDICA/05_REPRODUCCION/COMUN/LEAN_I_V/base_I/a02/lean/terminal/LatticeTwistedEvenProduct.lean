import SkewFieldTransform
import LatticeOrbifoldEvenConformal

/-! The twisted-to-even-input field obtained from the actual descended even
action and the existing translation mode. The exponential acts coefficientwise
with pointwise finite sums; no nilpotence of translation is assumed. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedEvenProduct
open LatticeEvenVertexFields LatticeEvenLocality LatticeEvenTranslation
open LatticeTwistedPositiveSector LatticeTwistedPositiveStateDescent
open LatticeOrbifoldCarrier LatticeOrbifoldEvenAction SkewFieldTransform

def translation (o : Fin 12) : Module.End ℂ (positiveSector o) :=
  positiveConformalMode o (-1)

def twistedEvenField (o : Fin 12) :
    positiveSector o →ₗ[ℂ] HVertexOperator ℤ ℂ (evenSpace o) (positiveSector o) :=
  skewAssignment (positiveDescendedAssignment o) (translation o)

theorem twistedEvenField_coefficient (o : Fin 12) (v : positiveSector o)
    (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (twistedEvenField o v) k u =
      ∑ᶠ n : ℕ, (n.factorial : ℂ)⁻¹ •
        ((translation o)^n) (((-1:ℂ)^(k-(n:ℤ))) •
          HVertexOperator.coeff (positiveDescendedAssignment o u) (k-(n:ℤ)) v) := by
  exact skewAssignment_coefficient_apply (positiveDescendedAssignment o)
    (translation o) v u k

theorem vacuum_taylor (o : Fin 12) (v : positiveSector o) (n : ℕ) :
    HVertexOperator.coeff (twistedEvenField o v) (n:ℤ) (evenVacuum o) =
      (n.factorial : ℂ)⁻¹ • (((translation o)^n) v) := by
  rw [twistedEvenField_coefficient]
  rw [finsum_eq_single _ n]
  · simp only [sub_self, zpow_zero, positiveDescent_vacuum_coefficient,
      if_pos rfl, Module.End.one_apply, one_smul]
    rfl
  · intro m hm
    rw [positiveDescent_vacuum_coefficient, if_neg (by omega)]
    simp only [LinearMap.zero_apply, smul_zero, map_zero]

theorem vacuum_negative (o : Fin 12) (v : positiveSector o) (k : ℤ) (hk : k<0) :
    HVertexOperator.coeff (twistedEvenField o v) k (evenVacuum o) = 0 := by
  rw [twistedEvenField_coefficient]
  apply finsum_eq_zero_of_forall_eq_zero
  intro n
  rw [positiveDescent_vacuum_coefficient, if_neg (by omega)]
  simp only [LinearMap.zero_apply, smul_zero, map_zero]

theorem vacuum_creation (o : Fin 12) (v : positiveSector o) :
    HVertexOperator.coeff (twistedEvenField o v) 0 (evenVacuum o) = v := by
  simpa only [Nat.cast_zero, Nat.factorial_zero, Nat.cast_one, inv_one,
    pow_zero, Module.End.one_apply, one_smul] using vacuum_taylor o v 0

theorem twistedEvenField_injective (o : Fin 12) :
    Function.Injective (twistedEvenField o) := by
  intro u v h
  have hh := congrArg (fun F => HVertexOperator.coeff F 0 (evenVacuum o)) h
  simpa only [vacuum_creation] using hh

abbrev TwistedPairField (o : Fin 12) :=
  positiveSector o →ₗ[ℂ] HVertexOperator ℤ ℂ (positiveSector o) (evenSpace o)

def remainingWithTT (o : Fin 12) (tt : TwistedPairField o) : RemainingFields o where
  te := twistedEvenField o
  tt := tt

/-- Only the twisted--twisted product is still an explicit argument. -/
def stateFieldWithTT (o : Fin 12) (tt : TwistedPairField o) :
    Space o →ₗ[ℂ] VertexOperator ℂ (Space o) :=
  LatticeOrbifoldBlocks.stateField o (completeWith o (remainingWithTT o tt))

theorem stateFieldWithTT_coefficient (o : Fin 12) (tt : TwistedPairField o)
    (u v : Space o) (k : ℤ) :
    HVertexOperator.coeff (stateFieldWithTT o tt u) k v =
      (evenCoefficient o u.1 k v.1 + HVertexOperator.coeff (tt u.2) k v.2,
       HVertexOperator.coeff (positiveDescendedAssignment o u.1) k v.2 +
         HVertexOperator.coeff (twistedEvenField o u.2) k v.1) := by
  exact LatticeOrbifoldBlocks.coefficient_formula o
    (completeWith o (remainingWithTT o tt)) u v k

theorem stateFieldWithTT_vacuum (o : Fin 12) (tt : TwistedPairField o) (k : ℤ) :
    HVertexOperator.coeff (stateFieldWithTT o tt (vacuum o)) k =
      if k=0 then (1 : Module.End ℂ (Space o)) else 0 := by
  unfold stateFieldWithTT
  change HVertexOperator.coeff
    (LatticeOrbifoldBlocks.stateField o (completeWith o (remainingWithTT o tt))
      (evenVacuum o,0)) k = _
  rw [completeWith_even_source, vacuum_coefficient]

theorem stateFieldWithTT_creation (o : Fin 12) (tt : TwistedPairField o)
    (u : Space o) :
    HVertexOperator.coeff (stateFieldWithTT o tt u) 0 (vacuum o) = u := by
  rw [stateFieldWithTT_coefficient]
  change (evenCoefficient o u.1 0 (evenVacuum o) + HVertexOperator.coeff (tt u.2) 0 0,
    HVertexOperator.coeff (positiveDescendedAssignment o u.1) 0 0 +
      HVertexOperator.coeff (twistedEvenField o u.2) 0 (evenVacuum o)) = u
  rw [map_zero, map_zero, add_zero, zero_add, evenCoefficient_creates, vacuum_creation]

theorem stateFieldWithTT_negative_vacuum (o : Fin 12) (tt : TwistedPairField o)
    (u : Space o) (k : ℤ) (hk : k<0) :
    HVertexOperator.coeff (stateFieldWithTT o tt u) k (vacuum o) = 0 := by
  rw [stateFieldWithTT_coefficient]
  change (evenCoefficient o u.1 k (evenVacuum o) + HVertexOperator.coeff (tt u.2) k 0,
    HVertexOperator.coeff (positiveDescendedAssignment o u.1) k 0 +
      HVertexOperator.coeff (twistedEvenField o u.2) k (evenVacuum o)) = 0
  rw [map_zero, map_zero, add_zero, zero_add,
    evenCoefficient_negative_vacuum o u.1 k hk, vacuum_negative o u.2 k hk]
  rfl

theorem stateFieldWithTT_injective (o : Fin 12) (tt : TwistedPairField o) :
    Function.Injective (stateFieldWithTT o tt) := by
  intro u v h
  have hh := congrArg (fun F => HVertexOperator.coeff F 0 (vacuum o)) h
  simpa only [stateFieldWithTT_creation] using hh

theorem stateFieldWithTT_twisted_even (o : Fin 12) (tt : TwistedPairField o)
    (u : positiveSector o) (v : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (stateFieldWithTT o tt (0,u)) k (v,0) =
      (0, HVertexOperator.coeff (twistedEvenField o u) k v) := by
  exact LatticeOrbifoldBlocks.twisted_even o
    (completeWith o (remainingWithTT o tt)) u v k

theorem stateFieldWithTT_twisted_twisted (o : Fin 12) (tt : TwistedPairField o)
    (u v : positiveSector o) (k : ℤ) :
    HVertexOperator.coeff (stateFieldWithTT o tt (0,u)) k (0,v) =
      (HVertexOperator.coeff (tt u) k v, 0) := by
  exact LatticeOrbifoldBlocks.twisted_twisted o
    (completeWith o (remainingWithTT o tt)) u v k

theorem stateFieldWithTT_conformal_coefficient (o : Fin 12) (tt : TwistedPairField o)
    (m : ℤ) :
    HVertexOperator.coeff (stateFieldWithTT o tt (conformalState o)) (-m-2) =
      modes o m := by
  exact LatticeOrbifoldEvenConformal.completeWith_conformal_coefficient o
    (remainingWithTT o tt) m

end HMT.IV.LatticeTwistedEvenProduct
end
