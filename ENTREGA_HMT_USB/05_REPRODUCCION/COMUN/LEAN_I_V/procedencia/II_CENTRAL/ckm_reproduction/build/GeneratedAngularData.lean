import GeneratedActionDomain
import ActionProducedAngles
import ElectronComposition

/-! Article II: the angular inputs of CKM are publications of the generated
regional/action chain. The global torsion below is `regionalFull`, not the
different vacancy logarithm used in the alpha analytic chart. No CKM value or
experimental angle is an input. -/
noncomputable section
namespace HMT.II.CKM.Generated
open HMT.IncidenceRegister AlphaIncidencePublications
open HMT.II.ActionReturn

def direct (l : Ledger) : ℝ := directDegrees (HMT.II.GeneratedAction.alpha l)
def conjugate (l : Ledger) : ℝ :=
  conjugateDegrees (HMT.II.GeneratedAction.alpha l)
    HMT.II.GeneratedAction.phi HMT.II.GeneratedAction.pi
def torsion : ℝ := ElectronComposition.regionalFull
def torsionDegrees : ℝ := (180 / HMT.II.GeneratedAction.pi) * torsion
def coordinates (l : Ledger) : Fin 3 → ℝ :=
  ![direct l, conjugate l / 6, torsionDegrees]
def phaseDegrees (l : Ledger) : ℝ := 9 * direct l

theorem sqrt_character_tight {α φ p : ℝ} (h : PrintedDomain α φ p) :
    (212 : ℝ) / 100 < Real.sqrt (1000 * α / φ) ∧
      Real.sqrt (1000 * α / φ) < (213 : ℝ) / 100 := by
  constructor
  · apply Real.lt_sqrt_of_sq_lt
    apply (lt_div_iff₀ h.phi_pos).mpr
    nlinarith [h.alpha_lower, h.phi_upper]
  · apply (Real.sqrt_lt' (by norm_num : (0 : ℝ) < 213 / 100)).mpr
    apply (div_lt_iff₀ h.phi_pos).mpr
    nlinarith [h.alpha_upper, h.phi_lower]

theorem H5_tight {α φ p : ℝ} (h : PrintedDomain α φ p) :
    (105 : ℝ) / 100 < H5 α φ ∧ H5 α φ < (106 : ℝ) / 100 := by
  have hs := sqrt_character_tight h
  have hn := h.negative_terms_bound
  have h2 : α ^ 2 ≤ ((1 : ℝ) / 125) ^ 2 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 2
  have h4 : α ^ 4 ≤ ((1 : ℝ) / 125) ^ 4 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 4
  have h2p := sq_nonneg α
  have h3p := pow_nonneg h.alpha_pos.le 3
  have h4p := pow_nonneg h.alpha_pos.le 4
  have h5p := pow_nonneg h.alpha_pos.le 5
  unfold H5
  constructor <;> linarith [h.alpha_lower]

theorem return_tight {α φ p : ℝ} (h : PrintedDomain α φ p) :
    (104 : ℝ) / 100 < etaRet α φ p ∧ etaRet α φ p < (106 : ℝ) / 100 := by
  have hb := H5_tight h
  constructor
  · unfold etaRet
    linarith [h.returnCorrection_upper]
  · exact h.etaRet_lt_H5.trans hb.2

theorem torsion_positive : 0 < torsion := ElectronComposition.regional_full_pos

theorem torsion_upper : torsion < (1 : ℝ) / 500 := by
  have hp := AlphaSourceBounds.closure_enclosure
  have he := AlphaSourceBounds.propagation_enclosure
  have hp0 : 0 < ClosureAnalytic.value := by linarith
  have he0 : 0 < PropagationLimit.value := by linarith
  have hpe : PropagationLimit.value < ClosureAnalytic.value := by linarith
  have hl := Real.log_lt_log he0 hpe
  rw [PropagationLimit.value_eq_exp_one, Real.log_exp] at hl
  have hnum : ClosureAnalytic.value -
      PropagationLimit.value * Real.log ClosureAnalytic.value < (1 : ℝ) / 2 := by
    nlinarith [mul_pos he0 (sub_pos.mpr hl)]
  have hred : ElectronComposition.reducedTorsion ClosureAnalytic.value
      PropagationLimit.value < (1 : ℝ) / 540 := by
    unfold ElectronComposition.reducedTorsion
    linarith
  have hfactor : 1 + ClosureAnalytic.value / 729 < (101 : ℝ) / 100 := by
    linarith
  have hrpos := ElectronComposition.regional_reduced_pos
  change 0 < ElectronComposition.reducedTorsion ClosureAnalytic.value
    PropagationLimit.value at hrpos
  unfold torsion ElectronComposition.regionalFull ElectronComposition.fullTorsion
  calc
    _ < ((1 : ℝ) / 540) * (101 / 100) :=
      mul_lt_mul hred hfactor.le (by linarith) (by norm_num)
    _ < (1 : ℝ) / 500 := by norm_num

theorem angular_input_bounds (l : Ledger) (hl : PublishedRegister l) :
    (7297 : ℝ) / 1000 < direct l ∧ direct l < (7298 : ℝ) / 1000 ∧
    (34 : ℝ) / 100 < conjugate l / 6 ∧ conjugate l / 6 < (36 : ℝ) / 100 ∧
    0 < torsionDegrees ∧ torsionDegrees < (12 : ℝ) / 100 := by
  have h := HMT.II.GeneratedAction.generated_action_domain l hl
  have hr := return_tight h
  have hp : 0 < 180 / HMT.II.GeneratedAction.pi :=
    div_pos (by norm_num) h.pi_pos
  have hfac : 180 / HMT.II.GeneratedAction.pi < (60 : ℝ) := by
    apply (div_lt_iff₀ h.pi_pos).mpr
    linarith [h.pi_lower]
  have htd : torsionDegrees < (12 : ℝ) / 100 := by
    unfold torsionDegrees
    have := mul_lt_mul hfac torsion_upper.le torsion_positive (by norm_num : (0 : ℝ) ≤ 60)
    norm_num at this ⊢
    exact this
  refine ⟨?_, ?_, ?_, ?_, mul_pos hp torsion_positive, htd⟩
  · dsimp [direct, directDegrees]; linarith [h.alpha_lower]
  · dsimp [direct, directDegrees]; linarith [h.alpha_upper]
  · dsimp [conjugate, conjugateDegrees]; linarith [h.alpha_pos]
  · dsimp [conjugate, conjugateDegrees]; linarith [h.alpha_upper]

theorem generated_phase_interval (l : Ledger) (hl : PublishedRegister l) :
    0 < phaseDegrees l ∧ phaseDegrees l < 90 := by
  have h := angular_input_bounds l hl
  unfold phaseDegrees
  constructor <;> linarith

#print axioms sqrt_character_tight
#print axioms H5_tight
#print axioms return_tight
#print axioms torsion_positive
#print axioms torsion_upper
#print axioms angular_input_bounds
#print axioms generated_phase_interval
end HMT.II.CKM.Generated
