import ElectronReturn
import ElectronSpin
import AlphaPositionalBridge
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# Composition of the central electronic readers

This is the posterior scalar composition with the regional injection fixed
by the source. Deficit, memory and return coefficients are evaluated from
the finite objects/readers below, not supplied as target constants.
-/

noncomputable section
namespace ElectronComposition

abbrev ReturnSpace := Fin 9 × Fin 3
abbrev Regions := Fin 5

/-- The source's fixed regional gauge; it is not inferred from a mass. -/
def regionalInjection : Regions → ReturnSpace := ![(4,0), (5,0), (6,0), (6,1), (6,2)]
def regionalImage : Finset ReturnSpace := Finset.univ.image regionalInjection
def complement : Finset ReturnSpace := Finset.univ \ regionalImage
def deficitCount : Nat := complement.card
def memoryCount : Nat := Fintype.card (Regions × Fin 3)
def orientedDeficit : Int := -(deficitCount : Int)

theorem regional_injection_injective : Function.Injective regionalInjection := by decide
theorem return_space_card : Fintype.card ReturnSpace = 27 := by decide
theorem regional_image_card : regionalImage.card = 5 := by decide
theorem deficit_count : deficitCount = 22 := by decide
theorem memory_count : memoryCount = 15 := by decide
theorem oriented_deficit : orientedDeficit = -22 := by simp [orientedDeficit, deficit_count]

/-- The functional acts after each finite reader has been generated. -/
def evaluateTriple (triple : Int × Int × Int) (alpha delta : ℝ) : ℝ :=
  (triple.1 : ℝ) - alpha * (triple.2.1 : ℝ) + delta * (triple.2.2 : ℝ)
def exponentD (alpha delta : ℝ) : ℝ :=
  evaluateTriple (ElectronReturn.discrepancyReader ElectronReturn.gamma) alpha delta
def exponentOmega (alpha delta : ℝ) : ℝ :=
  evaluateTriple (ElectronReturn.windowReader ElectronReturn.tau) alpha delta

theorem exponent_readers_agree (alpha delta : ℝ) : exponentD alpha delta = exponentOmega alpha delta := by
  unfold exponentD exponentOmega
  rw [ElectronReturn.readers_agree]

theorem generated_exponent (alpha delta : ℝ) :
    exponentD alpha delta = 80 - 54 * alpha + 6 * delta := by
  unfold exponentD
  rw [ElectronReturn.discrepancy_reader_central]
  norm_num [evaluateTriple]
  ring

def reducedTorsion (p e : ℝ) : ℝ := (p - e * Real.log p) / 270
def fullTorsion (p e : ℝ) : ℝ := reducedTorsion p e * (1 + p / 729)

theorem torsion_difference (p e : ℝ) :
    fullTorsion p e - reducedTorsion p e = p / 729 * reducedTorsion p e := by
  unfold fullTorsion
  ring

theorem reduced_torsion_nonneg_exp (p : ℝ) (hp : 0 < p) :
    0 ≤ reducedTorsion p (Real.exp 1) := by
  have he : 0 < Real.exp 1 := Real.exp_pos _
  have hl := Real.log_le_sub_one_of_pos (div_pos hp he)
  rw [Real.log_div hp.ne' he.ne', Real.log_exp] at hl
  have hle : Real.log p ≤ p / Real.exp 1 := by linarith
  have hm := (le_div_iff₀ he).mp hle
  unfold reducedTorsion
  apply div_nonneg _ (by norm_num)
  nlinarith

theorem reduced_torsion_pos_exp (p : ℝ) (hp : 0 < p) (hne : p ≠ Real.exp 1) :
    0 < reducedTorsion p (Real.exp 1) := by
  have he : 0 < Real.exp 1 := Real.exp_pos _
  have hdiv : p / Real.exp 1 ≠ 1 := by
    intro h
    apply hne
    exact (div_eq_one_iff_eq he.ne').mp h
  have hl := Real.log_lt_sub_one_of_pos (div_pos hp he) hdiv
  rw [Real.log_div hp.ne' he.ne', Real.log_exp] at hl
  have hlt : Real.log p < p / Real.exp 1 := by linarith
  have hm := (lt_div_iff₀ he).mp hlt
  unfold reducedTorsion
  apply div_pos _ (by norm_num)
  nlinarith

theorem full_torsion_nonneg (p e : ℝ) (hp : 0 ≤ p) (hd : 0 ≤ reducedTorsion p e) :
    0 ≤ fullTorsion p e := by
  unfold fullTorsion
  exact mul_nonneg hd (by positivity)

theorem full_torsion_strict (p e : ℝ) (hp : 0 < p) (hd : 0 < reducedTorsion p e) :
    reducedTorsion p e < fullTorsion p e := by
  have hdiff := torsion_difference p e
  have hpos : 0 < p / 729 * reducedTorsion p e := by positivity
  linarith

def regionalReduced : ℝ := reducedTorsion ClosureAnalytic.value PropagationLimit.value
def regionalFull : ℝ := fullTorsion ClosureAnalytic.value PropagationLimit.value

theorem regional_reduced_pos : 0 < regionalReduced := by
  have hp := AlphaPositionalBridge.closure_integer_part
  have he := AlphaPositionalBridge.propagation_integer_part
  unfold regionalReduced
  rw [PropagationLimit.value_eq_exp_one]
  apply reduced_torsion_pos_exp _ (by linarith)
  rw [← PropagationLimit.value_eq_exp_one]
  linarith

theorem regional_full_strict : regionalReduced < regionalFull := by
  apply full_torsion_strict
  · have hp := AlphaPositionalBridge.closure_integer_part
    linarith
  · exact regional_reduced_pos

theorem regional_full_pos : 0 < regionalFull := lt_trans regional_reduced_pos regional_full_strict

/-- Positive off-diagonal entry in the already selected principal plane.
This definition does not assert the norm of the global 729-point operator. -/
def localPrefactor : ℝ := (ElectronSpin.commutator ElectronSpin.P ElectronSpin.Q) 0 1

theorem local_prefactor_value : localPrefactor = Real.sqrt 3 / 4 := by
  unfold localPrefactor
  rw [ElectronSpin.commutator_explicit]
  rfl

def basal (p phi alpha delta : ℝ) : ℝ :=
  localPrefactor * (Real.exp (phi / p ^ 2) - (deficitCount : ℝ) * alpha ^ 3) *
    (1 + (memoryCount : ℝ) * delta)

theorem basal_formula (p phi alpha delta : ℝ) :
    basal p phi alpha delta = Real.sqrt 3 / 4 *
      (Real.exp (phi / p ^ 2) - 22 * alpha ^ 3) * (1 + 15 * delta) := by
  simp [basal, local_prefactor_value, deficit_count, memory_count]

theorem cubic_correction_lt_one (alpha : ℝ) (ha : 0 < alpha) (ha1 : alpha < 1 / 100) :
    (deficitCount : ℝ) * alpha ^ 3 < 1 := by
  rw [deficit_count]
  have hpow : alpha ^ 3 < (1 / 100 : ℝ) ^ 3 :=
    pow_lt_pow_left₀ ha1 ha.le (by decide : (3 : Nat) ≠ 0)
  norm_num at hpow ⊢
  linarith

theorem basal_positive (p phi alpha delta : ℝ) (hp : 0 < p) (hphi : 0 < phi)
    (ha : 0 < alpha) (ha1 : alpha < 1 / 100) (hd : 0 ≤ delta) :
    0 < basal p phi alpha delta := by
  have hexp : 1 < Real.exp (phi / p ^ 2) := Real.one_lt_exp_iff.mpr (by positivity)
  have hcube := cubic_correction_lt_one alpha ha ha1
  unfold basal
  rw [local_prefactor_value]
  apply mul_pos
  · exact mul_pos (by positivity) (by linarith)
  · rw [memory_count]
    norm_num
    linarith

def returnMultiplier (alpha delta R : ℝ) : ℝ := Real.exp (exponentD alpha delta * Real.log R)
def composition (p phi alpha delta R : ℝ) : ℝ := basal p phi alpha delta * returnMultiplier alpha delta R

theorem return_multiplier_positive (alpha delta R : ℝ) : 0 < returnMultiplier alpha delta R :=
  Real.exp_pos _

theorem composition_formula (p phi alpha delta R : ℝ) :
    composition p phi alpha delta R = Real.sqrt 3 / 4 *
      (Real.exp (phi / p ^ 2) - 22 * alpha ^ 3) * (1 + 15 * delta) *
      Real.exp ((80 - 54 * alpha + 6 * delta) * Real.log R) := by
  rw [composition, basal_formula, returnMultiplier, generated_exponent]

theorem composition_positive (p phi alpha delta R : ℝ) (hp : 0 < p) (hphi : 0 < phi)
    (ha : 0 < alpha) (ha1 : alpha < 1 / 100) (hd : 0 ≤ delta) :
    0 < composition p phi alpha delta R :=
  mul_pos (basal_positive p phi alpha delta hp hphi ha ha1 hd)
    (return_multiplier_positive alpha delta R)

theorem common_unit_cancellation (p phi alpha delta R U : ℝ)
    (hb : basal p phi alpha delta ≠ 0) (hU : U ≠ 0) :
    (composition p phi alpha delta R * U) / (basal p phi alpha delta * U) =
      returnMultiplier alpha delta R := by
  unfold composition
  field_simp
  ring

theorem action_unit_cancellation (pre post U : ℝ) (hpost : post ≠ 0) (hU : U ≠ 0) :
    (pre * U) / (post * U) = pre / post := by field_simp; ring

theorem return_multiplier_strict (alpha R d₁ d₂ : ℝ) (hR : 1 < R) (hd : d₁ < d₂) :
    returnMultiplier alpha d₁ R < returnMultiplier alpha d₂ R := by
  unfold returnMultiplier
  rw [generated_exponent, generated_exponent]
  apply Real.exp_lt_exp.mpr
  exact mul_lt_mul_of_pos_right (by linarith) (Real.log_pos hR)

theorem composition_normalization_strict (p phi alpha R d₁ d₂ : ℝ)
    (hp : 0 < p) (hphi : 0 < phi) (ha : 0 < alpha) (ha1 : alpha < 1 / 100)
    (hd₁ : 0 ≤ d₁) (hd : d₁ < d₂) (hR : 1 < R) :
    composition p phi alpha d₁ R < composition p phi alpha d₂ R := by
  have hB : 0 < Real.sqrt 3 / 4 *
      (Real.exp (phi / p ^ 2) - (deficitCount : ℝ) * alpha ^ 3) := by
    have he : 1 < Real.exp (phi / p ^ 2) := Real.one_lt_exp_iff.mpr (by positivity)
    have hc := cubic_correction_lt_one alpha ha ha1
    exact mul_pos (by positivity) (by linarith)
  have hb : basal p phi alpha d₁ < basal p phi alpha d₂ := by
    unfold basal
    rw [local_prefactor_value]
    apply mul_lt_mul_of_pos_left _ hB
    rw [memory_count]
    norm_num
    linarith
  exact mul_lt_mul hb (return_multiplier_strict alpha R d₁ d₂ hR hd).le
    (return_multiplier_positive alpha d₁ R) (basal_positive p phi alpha d₂ hp hphi ha ha1 (by linarith)).le

theorem regional_normalization_strict (alpha R : ℝ)
    (ha : 0 < alpha) (ha1 : alpha < 1 / 100) (hR : 1 < R) :
    composition ClosureAnalytic.value AlphaCarryLimit.autoscaleValue alpha regionalReduced R <
      composition ClosureAnalytic.value AlphaCarryLimit.autoscaleValue alpha regionalFull R := by
  apply composition_normalization_strict
  · have hp := AlphaPositionalBridge.closure_integer_part
    linarith
  · have hf := AlphaPositionalBridge.autoscale_integer_part
    linarith
  · exact ha
  · exact ha1
  · exact regional_reduced_pos.le
  · exact regional_full_strict
  · exact hR

theorem return_multiplier_ratio (alpha R d₁ d₂ : ℝ) :
    returnMultiplier alpha d₂ R / returnMultiplier alpha d₁ R =
      Real.exp (6 * (d₂ - d₁) * Real.log R) := by
  unfold returnMultiplier
  rw [← Real.exp_sub, generated_exponent, generated_exponent]
  congr 1
  ring

theorem normalization_ratio (p phi alpha R d₁ d₂ : ℝ)
    (hB : Real.sqrt 3 / 4 * (Real.exp (phi / p ^ 2) - 22 * alpha ^ 3) ≠ 0) :
    composition p phi alpha d₂ R / composition p phi alpha d₁ R =
      ((1 + 15 * d₂) / (1 + 15 * d₁)) * Real.exp (6 * (d₂ - d₁) * Real.log R) := by
  simp only [composition, mul_div_mul_comm]
  rw [return_multiplier_ratio, basal_formula, basal_formula]
  congr 1
  exact mul_div_mul_left _ _ hB

theorem action_ratio_gt_one (pre post : ℝ) (hpost : 0 < post) (h : post < pre) :
    1 < pre / post := (one_lt_div hpost).mpr h

/-- The regional readers and alpha closure are used downstream, not supplied
as conventional numerical targets. -/
def regionalComposition (register : RadixRecovery.K12) (R : ℝ) : ℝ :=
  composition ClosureAnalytic.value AlphaCarryLimit.autoscaleValue
    (AlphaCarryLimit.value register) regionalFull R

theorem regional_composition_positive (register : RadixRecovery.K12) (R : ℝ)
    (ha : 0 < AlphaCarryLimit.value register) (ha1 : AlphaCarryLimit.value register < 1 / 100) :
    0 < regionalComposition register R := by
  apply composition_positive
  · have hp := AlphaPositionalBridge.closure_integer_part
    linarith
  · have hf := AlphaPositionalBridge.autoscale_integer_part
    linarith
  · exact ha
  · exact ha1
  · exact regional_full_pos.le

end ElectronComposition
end

#print axioms ElectronComposition.regional_injection_injective
#print axioms ElectronComposition.return_space_card
#print axioms ElectronComposition.regional_image_card
#print axioms ElectronComposition.deficit_count
#print axioms ElectronComposition.memory_count
#print axioms ElectronComposition.oriented_deficit
#print axioms ElectronComposition.exponent_readers_agree
#print axioms ElectronComposition.generated_exponent
#print axioms ElectronComposition.torsion_difference
#print axioms ElectronComposition.reduced_torsion_nonneg_exp
#print axioms ElectronComposition.reduced_torsion_pos_exp
#print axioms ElectronComposition.full_torsion_nonneg
#print axioms ElectronComposition.full_torsion_strict
#print axioms ElectronComposition.regional_reduced_pos
#print axioms ElectronComposition.regional_full_strict
#print axioms ElectronComposition.regional_full_pos
#print axioms ElectronComposition.local_prefactor_value
#print axioms ElectronComposition.basal_formula
#print axioms ElectronComposition.cubic_correction_lt_one
#print axioms ElectronComposition.basal_positive
#print axioms ElectronComposition.return_multiplier_positive
#print axioms ElectronComposition.composition_formula
#print axioms ElectronComposition.composition_positive
#print axioms ElectronComposition.common_unit_cancellation
#print axioms ElectronComposition.action_unit_cancellation
#print axioms ElectronComposition.return_multiplier_strict
#print axioms ElectronComposition.composition_normalization_strict
#print axioms ElectronComposition.regional_normalization_strict
#print axioms ElectronComposition.return_multiplier_ratio
#print axioms ElectronComposition.normalization_ratio
#print axioms ElectronComposition.action_ratio_gt_one
#print axioms ElectronComposition.regional_composition_positive
