import SelectedActionDomain
import GeneratedAngularData
import RationalCKMChart
import CKMCycle

/-!
Concrete CKM publication of the already selected HMT action domain.
The APP--TRIT--TPK genealogy, selected register and its explicit inherited
interfaces are unchanged. No incidence ledger is manufactured and no
PublishedRegister premise is received. The full declared sector reader is
reused downstream, not selected anew from its six cardinalities.
The physical names of arbitrary later mass spectra are not selected here.
-/

noncomputable section
open Matrix Complex
open scoped ComplexConjugate

namespace HMT.II.CKM.Selected
open HMT.I.SelectedAction HMT.II.ActionReturn
open HMT.CKM.ComplexRealization HMT.CKM.Spectral

def direct : ℝ := directDegrees alpha
def conjugate : ℝ := conjugateDegrees alpha phi pi
def torsion : ℝ := ElectronComposition.regionalFull
def torsionDegrees : ℝ := (180 / pi) * torsion
def coordinates : Vec3 := ![direct, conjugate / 6, torsionDegrees]
def mixingDegrees : Vec3 := chart coordinates
def phaseDegrees : ℝ := 9 * direct
def radians (d : ℝ) : ℝ := (pi / 180) * d
def mixingRadians : Vec3 := fun i => radians (mixingDegrees i)
def phaseRadians : ℝ := radians phaseDegrees
def matrix : HMT.CKM.ComplexRealization.M3 :=
  CKM (mixingRadians 0) (mixingRadians 1) (mixingRadians 2) phaseRadians

theorem same_selected_action_coordinates :
    coordinates = ![1000 * alpha, 2 * (etaRet alpha phi pi + alpha) / 6,
      (180 / pi) * ElectronComposition.regionalFull] := rfl

theorem torsion_positive : 0 < torsion := Generated.torsion_positive
theorem torsion_upper : torsion < (1 : ℝ) / 500 := Generated.torsion_upper

theorem angular_input_bounds :
    (7297 : ℝ) / 1000 < direct ∧ direct < (7298 : ℝ) / 1000 ∧
    (34 : ℝ) / 100 < conjugate / 6 ∧ conjugate / 6 < (36 : ℝ) / 100 ∧
    0 < torsionDegrees ∧ torsionDegrees < (12 : ℝ) / 100 := by
  have h := action_domain
  have hr := Generated.return_tight h
  have hp : 0 < 180 / pi := div_pos (by norm_num) h.pi_pos
  have hfac : 180 / pi < (60 : ℝ) := by
    apply (div_lt_iff₀ h.pi_pos).mpr
    linarith [h.pi_lower]
  have htd : torsionDegrees < (12 : ℝ) / 100 := by
    unfold torsionDegrees
    have := mul_lt_mul hfac torsion_upper.le torsion_positive
      (by norm_num : (0 : ℝ) ≤ 60)
    norm_num at this ⊢
    exact this
  refine ⟨?_, ?_, ?_, ?_, mul_pos hp torsion_positive, htd⟩
  · dsimp [direct, directDegrees]; linarith [h.alpha_lower]
  · dsimp [direct, directDegrees]; linarith [h.alpha_upper]
  · dsimp [conjugate, conjugateDegrees]; linarith [h.alpha_pos]
  · dsimp [conjugate, conjugateDegrees]; linarith [h.alpha_upper]

theorem sector_evaluation : sectorRules 4 5 7 6 8 3 coordinates = mixingDegrees :=
  sector_rules_evaluate coordinates

theorem mixing_degrees_formula : mixingDegrees =
    ![2 * direct - 5 * (conjugate / 6) + 28 * torsionDegrees,
      7 * (conjugate / 6) - (25 / 2) * torsionDegrees,
      direct - 20 * (conjugate / 6) - (2 / 3) * torsionDegrees] := by
  ext i
  fin_cases i <;>
    simp [mixingDegrees, chart, chartMatrix, coordinates, Matrix.mulVec,
      dotProduct, Fin.sum_univ_succ] <;> ring

theorem coordinate_recovery : recover mixingDegrees = coordinates := recover_chart _

theorem phase_check : 3857 * phaseDegrees =
    9 * (1528 * mixingDegrees 0 + 3380 * mixingDegrees 1 + 801 * mixingDegrees 2) := by
  simpa [HMT.II.CKM.phase, phaseDegrees, coordinates, mixingDegrees] using
    phase_linear_check coordinates

theorem mixing_intervals : ∀ i, 0 < mixingDegrees i ∧ mixingDegrees i < 90 := by
  rcases angular_input_bounds with ⟨ha0, ha1, hu0, hu1, hd0, hd1⟩
  intro i
  rw [mixing_degrees_formula]
  fin_cases i <;> dsimp <;> constructor <;> linarith

theorem phase_interval : 0 < phaseDegrees ∧ phaseDegrees < 90 := by
  have h := angular_input_bounds
  unfold phaseDegrees
  constructor <;> linarith

theorem radians_chamber {d : ℝ} (hd : 0 < d ∧ d < 90) :
    0 < radians d ∧ radians d < Real.pi / 2 := by
  have hp : pi = Real.pi := ClosureAnalytic.value_eq_pi
  have hf : 0 < Real.pi / 180 := div_pos Real.pi_pos (by norm_num)
  unfold radians
  rw [hp]
  refine ⟨mul_pos hf hd.1, ?_⟩
  calc
    _ < (Real.pi / 180) * 90 := mul_lt_mul_of_pos_left hd.2 hf
    _ = Real.pi / 2 := by ring

theorem radian_intervals :
    (∀ i, 0 < mixingRadians i ∧ mixingRadians i < Real.pi / 2) ∧
    (0 < phaseRadians ∧ phaseRadians < Real.pi / 2) :=
  ⟨fun i => radians_chamber (mixing_intervals i), radians_chamber phase_interval⟩

theorem matrix_unitary : matrixᴴ * matrix = 1 ∧ matrix * matrixᴴ = 1 :=
  ⟨CKM_left_unitary _ _ _ _, CKM_right_unitary _ _ _ _⟩

theorem jarlskog_formula : jarlskog matrix =
    Real.cos (mixingRadians 0) * Real.cos (mixingRadians 1) *
      Real.cos (mixingRadians 2) ^ 2 * Real.sin (mixingRadians 0) *
      Real.sin (mixingRadians 1) * Real.sin (mixingRadians 2) * Real.sin phaseRadians :=
  CKM_jarlskog _ _ _ _

theorem jarlskog_positive : 0 < jarlskog matrix := by
  have h := radian_intervals
  have hs : ∀ i, 0 < Real.sin (mixingRadians i) := by
    intro i
    apply Real.sin_pos_of_pos_of_lt_pi (h.1 i).1
    linarith [(h.1 i).2, Real.pi_pos]
  have hc : ∀ i, 0 < Real.cos (mixingRadians i) := by
    intro i
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · linarith [(h.1 i).1, Real.pi_pos]
    · exact (h.1 i).2
  have hd : 0 < Real.sin phaseRadians := by
    apply Real.sin_pos_of_pos_of_lt_pi h.2.1
    linarith [h.2.2, Real.pi_pos]
  rw [jarlskog_formula]
  exact mul_pos (mul_pos (mul_pos (mul_pos (mul_pos
    (mul_pos (hc 0) (hc 1)) (sq_pos_of_pos (hc 2))) (hs 0)) (hs 1)) (hs 2)) hd

theorem no_real_rephasing (u d : Fin 3 → ℂ)
    (hu : ∀ i, u i * conj (u i) = 1) (hd : ∀ i, d i * conj (d i) = 1) :
    ¬ (∀ i j, (rephase u d matrix i j).im = 0) :=
  nonzero_jarlskog_obstructs_real_rephasing matrix (ne_of_gt jarlskog_positive) u d hu hd

def transportedMass (m : Fin 3 → ℝ) : HMT.CKM.Spectral.Mat3 :=
  massTransport (mixingRadians 0) (mixingRadians 1) (mixingRadians 2) phaseRadians m

def spectralSeparation (m : Fin 3 → ℝ) : ℝ :=
  (m 0 - m 1) * (m 1 - m 2) * (m 2 - m 0)

theorem mass_spectral_transport (m : Fin 3 → ℝ) :
    (transportedMass m).IsHermitian ∧
    (transportedMass m).charpoly = (diagonal (fun i => (m i : ℂ))).charpoly ∧
    spectrum ℂ (transportedMass m) = spectrum ℂ (diagonal (fun i => (m i : ℂ))) :=
  ⟨massTransport_hermitian _ _ _ _ m, massTransport_charpoly _ _ _ _ m,
    massTransport_spectrum _ _ _ _ m⟩

theorem commutator_determinant (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det =
      2 * I * (jarlskog matrix * spectralSeparation u * spectralSeparation d : ℝ) :=
  massTransport_jarlskog_determinant _ _ _ _ u d

/-- Closed selected instance, with no ledger, target-value or angular premise. -/
theorem selected_ckm_principal_chain :
    recover mixingDegrees = coordinates ∧
    (matrixᴴ * matrix = 1 ∧ matrix * matrixᴴ = 1) ∧
    0 < jarlskog matrix ∧
    (∀ m : Fin 3 → ℝ,
      spectrum ℂ (transportedMass m) = spectrum ℂ (diagonal (fun i => (m i : ℂ)))) ∧
    (∀ u d : Fin 3 → ℝ,
      (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det =
        2 * I * (jarlskog matrix * spectralSeparation u * spectralSeparation d : ℝ)) :=
  ⟨coordinate_recovery, matrix_unitary, jarlskog_positive,
    fun m => (mass_spectral_transport m).2.2, commutator_determinant⟩

#print axioms same_selected_action_coordinates
#print axioms angular_input_bounds
#print axioms sector_evaluation
#print axioms coordinate_recovery
#print axioms matrix_unitary
#print axioms jarlskog_positive
#print axioms no_real_rephasing
#print axioms mass_spectral_transport
#print axioms commutator_determinant
#print axioms selected_ckm_principal_chain
end HMT.II.CKM.Selected
