import SelectedActionDomain
import GeneratedCKMClosure

/-!
The sectorial reader of Article II is evaluated on the already selected
regional/action coordinates of Article I. There is no input Ledger, no
PublishedRegister hypothesis, and no ledger manufactured from target digits.
The three declared sector rules remain the source's representation. Spectral
mass readers and unit-modulus rephasings are subsequent parameters.

The analytic bounds below instantiate the existing angular lemmas at the
proved SelectedAction.action_domain. Classical matrix and spectral results
are reused from GeneratedCKMClosure, not proved afresh.
-/
noncomputable section
namespace HMT.II.CKM.SelectedPublication

open HMT.I.SelectedAction HMT.II.ActionReturn
open HMT.CKM.Spectral HMT.CKM.ComplexRealization
open Matrix Complex
open scoped ComplexConjugate

def direct : ℝ := directDegrees alpha
def conjugate : ℝ := conjugateDegrees alpha phi pi
def torsionDegrees : ℝ := Generated.torsionDegrees
def coordinates : Vec3 := ![direct, conjugate / 6, torsionDegrees]
def mixingDegrees : Vec3 := chart coordinates
def phaseDegrees : ℝ := 9 * direct
def mixingRadians : Vec3 := fun i => Generated.radians (mixingDegrees i)
def phaseRadians : ℝ := Generated.radians phaseDegrees
def matrix : HMT.CKM.ComplexRealization.M3 :=
  CKM (mixingRadians 0) (mixingRadians 1) (mixingRadians 2) phaseRadians

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
    change (180 / pi) * Generated.torsion < (12 : ℝ) / 100
    have hx := mul_lt_mul hfac Generated.torsion_upper.le
      Generated.torsion_positive (by norm_num : (0 : ℝ) ≤ 60)
    norm_num at hx ⊢
    exact hx
  refine ⟨?_, ?_, ?_, ?_, mul_pos hp Generated.torsion_positive, htd⟩
  · dsimp [direct, directDegrees]; linarith [h.alpha_lower]
  · dsimp [direct, directDegrees]; linarith [h.alpha_upper]
  · dsimp [conjugate, conjugateDegrees]; linarith [h.alpha_pos]
  · dsimp [conjugate, conjugateDegrees]; linarith [h.alpha_upper]

theorem mixing_degrees_formula :
    mixingDegrees =
      ![2 * direct - 5 * (conjugate / 6) + 28 * torsionDegrees,
        7 * (conjugate / 6) - (25 / 2) * torsionDegrees,
        direct - 20 * (conjugate / 6) - (2 / 3) * torsionDegrees] := by
  ext i
  fin_cases i <;>
    simp [mixingDegrees, chart, chartMatrix, coordinates, Matrix.mulVec,
      dotProduct, Fin.sum_univ_succ] <;> ring

theorem mixing_intervals : ∀ i, 0 < mixingDegrees i ∧ mixingDegrees i < 90 := by
  rcases angular_input_bounds with ⟨ha0, ha1, hu0, hu1, hd0, hd1⟩
  intro i
  rw [mixing_degrees_formula]
  fin_cases i <;> dsimp <;> constructor <;> linarith

theorem phase_interval : 0 < phaseDegrees ∧ phaseDegrees < 90 := by
  have h := angular_input_bounds
  unfold phaseDegrees
  constructor <;> linarith

theorem radian_intervals :
    (∀ i, 0 < mixingRadians i ∧ mixingRadians i < Real.pi / 2) ∧
    (0 < phaseRadians ∧ phaseRadians < Real.pi / 2) :=
  ⟨fun i => Generated.radians_chamber (mixing_intervals i),
    Generated.radians_chamber phase_interval⟩

theorem selected_sector_incidence :
    Incidence.markedFace.card = 4 ∧ Incidence.hexadSupport.card = 6 ∧
    Incidence.tritAlphabet.card = 3 ∧
    (∀ s : Incidence.DeclaredSectorFrame,
      Incidence.incidenceReader s coordinates = mixingDegrees) :=
  ⟨Incidence.marked_face_card, Incidence.hexad_card, Incidence.trit_card,
    fun s => Incidence.incidence_reader_is_chart s coordinates⟩

theorem sector_rules : sectorRules 4 5 7 6 8 3 coordinates = mixingDegrees :=
  sector_rules_evaluate coordinates

theorem selected_recovery : recover mixingDegrees = coordinates := recover_chart _

theorem selected_phase_check :
    3857 * phaseDegrees =
      9 * (1528 * mixingDegrees 0 + 3380 * mixingDegrees 1 + 801 * mixingDegrees 2) := by
  simpa [phase, phaseDegrees, coordinates, mixingDegrees] using
    phase_linear_check coordinates

theorem selected_unitary : matrixᴴ * matrix = 1 ∧ matrix * matrixᴴ = 1 :=
  ⟨CKM_left_unitary _ _ _ _, CKM_right_unitary _ _ _ _⟩

theorem selected_jarlskog : jarlskog matrix =
    Real.cos (mixingRadians 0) * Real.cos (mixingRadians 1) *
    Real.cos (mixingRadians 2) ^ 2 * Real.sin (mixingRadians 0) *
    Real.sin (mixingRadians 1) * Real.sin (mixingRadians 2) * Real.sin phaseRadians :=
  CKM_jarlskog _ _ _ _

theorem selected_jarlskog_positive : 0 < jarlskog matrix := by
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
  rw [selected_jarlskog]
  exact mul_pos (mul_pos (mul_pos (mul_pos (mul_pos
    (mul_pos (hc 0) (hc 1)) (sq_pos_of_pos (hc 2))) (hs 0)) (hs 1)) (hs 2)) hd

theorem selected_no_real_rephasing (u d : Fin 3 → ℂ)
    (hu : ∀ i, u i * conj (u i) = 1) (hd : ∀ i, d i * conj (d i) = 1) :
    ¬ (∀ i j, (rephase u d matrix i j).im = 0) :=
  nonzero_jarlskog_obstructs_real_rephasing matrix
    (ne_of_gt selected_jarlskog_positive) u d hu hd

def transportedMass (m : Fin 3 → ℝ) : HMT.CKM.Spectral.Mat3 :=
  massTransport (mixingRadians 0) (mixingRadians 1) (mixingRadians 2) phaseRadians m

theorem selected_mass_transport (m : Fin 3 → ℝ) :
    (transportedMass m).IsHermitian ∧
    (transportedMass m).charpoly = (diagonal (fun i => (m i : ℂ))).charpoly ∧
    spectrum ℂ (transportedMass m) = spectrum ℂ (diagonal (fun i => (m i : ℂ))) :=
  ⟨massTransport_hermitian _ _ _ _ m, massTransport_charpoly _ _ _ _ m,
    massTransport_spectrum _ _ _ _ m⟩

theorem selected_commutator_determinant (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det =
      2 * I * (jarlskog matrix * Generated.spectralSeparation u *
        Generated.spectralSeparation d : ℝ) :=
  massTransport_jarlskog_determinant _ _ _ _ u d

theorem selected_commutator_nonzero (u d : Fin 3 → ℝ)
    (hu : Generated.spectralSeparation u ≠ 0) (hd : Generated.spectralSeparation d ≠ 0) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det ≠ 0 := by
  rw [selected_commutator_determinant]
  apply mul_ne_zero
  · exact mul_ne_zero (by norm_num) Complex.I_ne_zero
  · exact Complex.ofReal_ne_zero.mpr
      (mul_ne_zero (mul_ne_zero (ne_of_gt selected_jarlskog_positive) hu) hd)

/-- One selected endpoint, with no new register premise. The action and
angular publications share exactly the regional coordinates of Article I. -/
theorem selected_ckm_principal_chain :
    alpha = AlphaAnalyticChart.precoordinate HMT.I.TerminalSelector.regionalRegister ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (Incidence.markedFace.card = 4 ∧ Incidence.hexadSupport.card = 6 ∧
      Incidence.tritAlphabet.card = 3 ∧
      (∀ s : Incidence.DeclaredSectorFrame,
        Incidence.incidenceReader s coordinates = mixingDegrees)) ∧
    recover mixingDegrees = coordinates ∧
    (matrixᴴ * matrix = 1 ∧ matrix * matrixᴴ = 1) ∧
    0 < jarlskog matrix ∧
    (∀ m : Fin 3 → ℝ,
      (transportedMass m).IsHermitian ∧
      (transportedMass m).charpoly = (diagonal (fun i => (m i : ℂ))).charpoly ∧
      spectrum ℂ (transportedMass m) = spectrum ℂ (diagonal (fun i => (m i : ℂ)))) ∧
    (∀ u d : Fin 3 → ℝ,
      (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det =
        2 * I * (jarlskog matrix * Generated.spectralSeparation u *
          Generated.spectralSeparation d : ℝ)) :=
  ⟨rfl, action_decimal_order, selected_sector_incidence, selected_recovery,
    selected_unitary, selected_jarlskog_positive, selected_mass_transport,
    selected_commutator_determinant⟩

end HMT.II.CKM.SelectedPublication
end

#print axioms HMT.II.CKM.SelectedPublication.selected_ckm_principal_chain
#print axioms HMT.II.CKM.SelectedPublication.selected_no_real_rephasing
#print axioms HMT.II.CKM.SelectedPublication.selected_commutator_nonzero
