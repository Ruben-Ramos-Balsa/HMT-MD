import LatticeEvenVertexFields
import LatticeStateFieldTranslation
import LatticeConformalState

/-!
Restriction of the existing translation and full state-field identities to
the existing parity-fixed carrier. Translation commutes with parity by the
coefficient-one creation theorem, not by a new infinite mode calculation.
The existing quadratic conformal state is fixed because it has two creators.
No Virasoro relation, twisted sector or orbifold is assumed or asserted.
-/

noncomputable section
namespace HMT.IV.LatticeEvenTranslation

open LatticeOscillatorFock LatticeParityCarrier LatticeStateFieldMap
open LatticeStateFieldParity LatticeEvenVertexFields LatticeStateFieldTranslation
open LatticeTranslationOperator LatticeFieldDerivative LatticeConformalState

theorem theta_translation (o : Fin 12) (u : LatticeCarrier o) :
    carrierTheta o (translation o u) = translation o (carrierTheta o u) := by
  rw [← stateField_translation_vacuum_coefficient,
    theta_stateField_apply, carrierTheta_vacuum,
    stateField_translation_vacuum_coefficient]

theorem theta_translation_commutes (o : Fin 12) :
    carrierTheta o * translation o = translation o * carrierTheta o := by
  apply LinearMap.ext
  exact theta_translation o

theorem translation_mem_parity (o : Fin 12) (s : ℂ) (u : LatticeCarrier o)
    (hu : u ∈ paritySpace o s) : translation o u ∈ paritySpace o s := by
  apply (mem_paritySpace o _ _).2
  rw [theta_translation, (mem_paritySpace o _ _).1 hu, map_smul]

theorem translation_mem_even (o : Fin 12) (u : LatticeCarrier o)
    (hu : u ∈ evenSpace o) : translation o u ∈ evenSpace o :=
  translation_mem_parity o 1 u hu

def evenTranslation (o : Fin 12) : Module.End ℂ (evenSpace o) where
  toFun u := ⟨translation o u.val, translation_mem_even o u.val u.property⟩
  map_add' u v := by apply Subtype.ext; exact map_add _ _ _
  map_smul' c u := by apply Subtype.ext; exact map_smul _ _ _

theorem evenTranslation_coe (o : Fin 12) (u : evenSpace o) :
    (evenTranslation o u).val = translation o u.val := rfl

theorem evenTranslation_vacuum (o : Fin 12) :
    evenTranslation o (evenVacuum o) = 0 := by
  apply Subtype.ext
  exact translation_vacuum o

theorem evenCoefficient_translation (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    evenTranslation o * evenCoefficient o u k -
      evenCoefficient o u k * evenTranslation o =
      ((k : ℂ)+1) • evenCoefficient o u (k+1) := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  exact LinearMap.congr_fun (stateField_translation o u.val k) v.val

theorem evenCoefficient_translation_vacuum (o : Fin 12) (u : evenSpace o) :
    evenCoefficient o u 1 (evenVacuum o) = evenTranslation o u := by
  apply Subtype.ext
  exact stateField_translation_vacuum_coefficient o u.val

theorem evenCoefficient_translated_state (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    evenCoefficient o (evenTranslation o u) k =
      ((k : ℂ)+1) • evenCoefficient o u (k+1) := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  have h := congrArg (fun B => HVertexOperator.coeff B k v.val)
    (stateField_translated_state o u.val)
  simpa only [derivativeField_coefficient, LinearMap.smul_apply] using h

/-- A genuine Laurent field on the fixed carrier, with the inherited
pointwise lower bound. -/
def evenField (o : Fin 12) (u : evenSpace o) : VertexOperator ℂ (evenSpace o) :=
  VertexOperator.of_coeff (evenCoefficient o u) (evenCoefficient_laurent_bound o u)

theorem evenField_coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (evenField o u) k = evenCoefficient o u k := by
  apply LinearMap.ext
  intro v
  rfl

theorem evenField_translation_covariant (o : Fin 12) (u : evenSpace o) :
    LatticeTranslationLinear.TranslationCovariant (evenTranslation o) (evenField o u) := by
  intro k
  simpa only [evenField_coefficient] using evenCoefficient_translation o u k

theorem evenField_translated_state (o : Fin 12) (u : evenSpace o) :
    evenField o (evenTranslation o u) = derivativeField (evenField o u) := by
  apply LinearMap.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  change HVertexOperator.coeff (evenField o (evenTranslation o u)) k v =
    HVertexOperator.coeff (derivativeField (evenField o u)) k v
  rw [evenField_coefficient, derivativeField_coefficient, evenField_coefficient]
  exact LinearMap.congr_fun (evenCoefficient_translated_state o u k) v

theorem conformalState_fixed (o : Fin 12) :
    carrierTheta o (conformalState o) = conformalState o := by
  simp only [conformalState, map_smul, map_sum, theta_create,
    map_neg, neg_neg, carrierTheta_vacuum]

theorem conformalState_mem_even (o : Fin 12) :
    conformalState o ∈ evenSpace o := (mem_evenSpace o _).2 (conformalState_fixed o)

theorem conformalMode_mem_even (o : Fin 12) (m : ℤ) (u : LatticeCarrier o)
    (hu : u ∈ evenSpace o) : conformalMode o m u ∈ evenSpace o :=
  stateField_coefficient_even o _ u (conformalState_mem_even o) hu (-m-2)

end HMT.IV.LatticeEvenTranslation
end
