import LatticeLocalFieldUniqueness
import LatticeTranslationLinear
import LatticeTranslationOperator

/-!
Differential covariance propagates a zero initial vacuum coefficient through
all nonnegative coefficients. Combined with regularity and actual locality,
this proves uniqueness of creative fields on the constructed carrier.
-/

noncomputable section
namespace HMT.IV.LatticeCovariantFieldUniqueness

open LatticeTranslationLinear LatticeLocalFieldUniqueness LatticeFieldLocality
open LatticeStateFieldMap LatticeDescendantFields LatticeOscillatorFock

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem covariant_nonnegative_zero (T : Module.End ℂ V)
    (F : VertexOperator ℂ V) (v : V) (hTv : T v = 0)
    (hF : TranslationCovariant T F) (hzero : HVertexOperator.coeff F 0 v = 0)
    (n : ℕ) : HVertexOperator.coeff F (n : ℤ) v = 0 := by
  induction n with
  | zero => exact hzero
  | succ n ih =>
    have h := LinearMap.congr_fun (hF (n : ℤ)) v
    simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
      hTv, ih, map_zero, sub_zero] at h
    have hs : (n+1 : ℂ) • HVertexOperator.coeff F ((n+1 : ℕ) : ℤ) v = 0 := by
      simpa only [Int.cast_natCast, Nat.cast_add, Nat.cast_one] using h.symm
    exact (smul_eq_zero.mp hs).resolve_left (by exact_mod_cast Nat.succ_ne_zero n)

theorem covariant_vacuum_zero (T : Module.End ℂ V)
    (F : VertexOperator ℂ V) (v : V) (hTv : T v = 0)
    (hF : TranslationCovariant T F)
    (hregular : ∀ k : ℤ, k < 0 → HVertexOperator.coeff F k v = 0)
    (hzero : HVertexOperator.coeff F 0 v = 0) (k : ℤ) :
    HVertexOperator.coeff F k v = 0 := by
  by_cases hk : k < 0
  · exact hregular k hk
  · have he : (k.toNat : ℤ) = k := Int.toNat_of_nonneg (by omega)
    simpa only [he] using covariant_nonnegative_zero T F v hTv hF hzero k.toNat

theorem creative_covariant_fields_unique (o : Fin 12)
    (A B : VertexOperator ℂ (LatticeCarrier o)) (u : LatticeCarrier o)
    (hA_local : ∀ v : LatticeCarrier o, Local A (stateField o v))
    (hB_local : ∀ v : LatticeCarrier o, Local B (stateField o v))
    (hA_covariant : TranslationCovariant (LatticeTranslationOperator.translation o) A)
    (hB_covariant : TranslationCovariant (LatticeTranslationOperator.translation o) B)
    (hA_creates : Creates o A u) (hB_creates : Creates o B u) : A = B := by
  let F := A + (-1 : ℂ) • B
  have hlocal : ∀ v : LatticeCarrier o, Local F (stateField o v) := by
    intro v
    exact local_add_left (hA_local v) (local_smul_left (-1) (hB_local v))
  have hcov : TranslationCovariant (LatticeTranslationOperator.translation o) F :=
    covariant_add hA_covariant (covariant_smul hB_covariant (-1))
  have hregular : ∀ k : ℤ, k < 0 → HVertexOperator.coeff F k (vacuum o) = 0 := by
    intro k hk
    simp only [F, HVertexOperator.coeff_add, HVertexOperator.coeff_smul,
      Pi.add_apply, Pi.smul_apply, LinearMap.add_apply, LinearMap.smul_apply,
      hA_creates.1 k hk, hB_creates.1 k hk, smul_zero, add_zero]
  have hzero : HVertexOperator.coeff F 0 (vacuum o) = 0 := by
    simp only [F, HVertexOperator.coeff_add, HVertexOperator.coeff_smul,
      Pi.add_apply, Pi.smul_apply, LinearMap.add_apply, LinearMap.smul_apply,
      hA_creates.2, hB_creates.2, neg_one_smul, add_neg_cancel]
  have hF := local_field_zero o F hlocal
    (covariant_vacuum_zero (LatticeTranslationOperator.translation o) F (vacuum o)
      (LatticeTranslationOperator.translation_vacuum o) hcov hregular hzero)
  apply LinearMap.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  change HVertexOperator.coeff A k v = HVertexOperator.coeff B k v
  have h : HVertexOperator.coeff F k v = 0 := by rw [hF]; rfl
  apply sub_eq_zero.mp
  simpa only [F, HVertexOperator.coeff_add, HVertexOperator.coeff_smul,
    Pi.add_apply, Pi.smul_apply, LinearMap.add_apply, LinearMap.smul_apply,
    neg_one_smul, sub_eq_add_neg] using h

end HMT.IV.LatticeCovariantFieldUniqueness
end

#print axioms HMT.IV.LatticeCovariantFieldUniqueness.covariant_nonnegative_zero
#print axioms HMT.IV.LatticeCovariantFieldUniqueness.covariant_vacuum_zero
#print axioms HMT.IV.LatticeCovariantFieldUniqueness.creative_covariant_fields_unique
