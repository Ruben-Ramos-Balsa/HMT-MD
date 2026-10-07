import ArticleIIFromSharedBase
import GeneratedCKMClosure

/-!
CKM continuation on the same selected Article I register and the Article II
angular publication. The historical GeneratedCKMClosure adapter asks for an
incidence Ledger and PublishedRegister. Neither is manufactured here: its
generic coordinate, torsion, unitary and spectral theorems are instantiated
directly on SelectedAction.action_domain.

The only re-specialized step is the historical interval argument, now fed by
the proved PrintedDomain instead of the old Ledger wrapper. No measured CKM
angle, phase, target register or additional interval premise is supplied.
The torsion is ElectronComposition.regionalFull, NOT VacancyDelta.

LaTeX owners in AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/
USB_ES_EN_STAGE10_20260917/ES/PAQUETES/02_BARBERO_CKM_CONSTANTES_ES/
documentacion_original/payload/source_es/manuscrito/sections/:
* 08b_reglas_sectoriales.tex: def:ii09-sistema-sectorial and
  thm:ii09-matriz-sectorial (the declared sector system and its evaluation).
* 08_propagacion_angular.tex: eq:ii-angular-chart, eq:ii-ckm-map,
  eq:ii-jarlskog, eq:ii-ckm-mass-transport and eq:ii-ckm-commutator.

The declared sector rules, upstream S8 interface and Article I native
evaluation boundary are preserved. The arbitrary spectra below are inputs
to a transport identity, not newly generated quark masses or a PMNS result.
-/

noncomputable section
namespace HMT.II.CKMFromSharedBase

open HMT.I.SelectedAction HMT.II.ActionReturn HMT.II.FromSharedBase
open HMT.II.CKM HMT.CKM.ComplexRealization HMT.CKM.Spectral
open Matrix Complex
open scoped ComplexConjugate

def torsionDegrees : ℝ := HMT.II.CKM.Generated.torsionDegrees
def coordinates : Vec3 := ![angleDegrees, contraAngleDegrees / 6, torsionDegrees]
def mixingDegrees : Vec3 := chart coordinates
def phaseDegrees : ℝ := 9 * angleDegrees
def mixingRadians : Vec3 := fun i => HMT.II.CKM.Generated.radians (mixingDegrees i)
def phaseRadians : ℝ := HMT.II.CKM.Generated.radians phaseDegrees
def matrix : HMT.CKM.ComplexRealization.M3 :=
  HMT.CKM.ComplexRealization.CKM
    (mixingRadians 0) (mixingRadians 1) (mixingRadians 2) phaseRadians

theorem coordinate_sources :
    coordinates =
      ![1000 * alpha, 2 * (etaRet alpha phi pi + alpha) / 6,
        (180 / pi) * ElectronComposition.regionalFull] := rfl

theorem generated_pi_conversion (d : ℝ) :
    HMT.II.CKM.Generated.radians d = (pi / 180) * d := rfl

theorem sector_evaluation : sectorRules 4 5 7 6 8 3 coordinates = mixingDegrees :=
  sector_rules_evaluate _

theorem incidence_evaluation (s : Incidence.DeclaredSectorFrame) :
    Incidence.incidenceReader s coordinates = mixingDegrees :=
  Incidence.incidence_reader_is_chart s _

theorem mixing_degrees_formula :
    mixingDegrees =
      ![2 * angleDegrees - 5 * (contraAngleDegrees / 6) + 28 * torsionDegrees,
        7 * (contraAngleDegrees / 6) - (25 / 2) * torsionDegrees,
        angleDegrees - 20 * (contraAngleDegrees / 6) - (2 / 3) * torsionDegrees] := by
  ext i
  fin_cases i <;>
    simp [mixingDegrees, chart, chartMatrix, coordinates, Matrix.mulVec,
      dotProduct, Fin.sum_univ_succ] <;> ring

theorem coordinate_recovery : recover mixingDegrees = coordinates := recover_chart _

theorem phase_check :
    3857 * phaseDegrees =
      9 * (1528 * mixingDegrees 0 + 3380 * mixingDegrees 1 +
        801 * mixingDegrees 2) := by
  simpa [HMT.II.CKM.phase, phaseDegrees, coordinates, mixingDegrees] using
    phase_linear_check coordinates

/-- The old numerical enclosure is a conclusion of the selected action
domain, not a premise about a published incidence ledger. -/
theorem angular_input_bounds :
    (7297 : ℝ) / 1000 < angleDegrees ∧ angleDegrees < (7298 : ℝ) / 1000 ∧
    (34 : ℝ) / 100 < contraAngleDegrees / 6 ∧
    contraAngleDegrees / 6 < (36 : ℝ) / 100 ∧
    0 < torsionDegrees ∧ torsionDegrees < (12 : ℝ) / 100 := by
  have h := action_domain
  have hr := HMT.II.CKM.Generated.return_tight h
  have hp : 0 < 180 / HMT.II.GeneratedAction.pi :=
    div_pos (by norm_num) h.pi_pos
  have hfac : 180 / HMT.II.GeneratedAction.pi < (60 : ℝ) := by
    apply (div_lt_iff₀ h.pi_pos).mpr
    linarith [h.pi_lower]
  have htd : torsionDegrees < (12 : ℝ) / 100 := by
    unfold torsionDegrees HMT.II.CKM.Generated.torsionDegrees
    have ht := mul_lt_mul hfac HMT.II.CKM.Generated.torsion_upper.le
      HMT.II.CKM.Generated.torsion_positive (by norm_num : (0 : ℝ) ≤ 60)
    norm_num at ht ⊢
    exact ht
  refine ⟨?_, ?_, ?_, ?_,
    mul_pos hp HMT.II.CKM.Generated.torsion_positive, htd⟩
  · dsimp [angleDegrees, directDegrees]; linarith [h.alpha_lower]
  · dsimp [angleDegrees, directDegrees]; linarith [h.alpha_upper]
  · dsimp [contraAngleDegrees, conjugateDegrees]; linarith [h.alpha_pos]
  · dsimp [contraAngleDegrees, conjugateDegrees]; linarith [h.alpha_upper]

theorem mixing_intervals : ∀ i, 0 < mixingDegrees i ∧ mixingDegrees i < 90 := by
  rcases angular_input_bounds with ⟨ha0, ha1, hu0, hu1, hd0, hd1⟩
  intro i
  rw [mixing_degrees_formula]
  fin_cases i <;> dsimp <;> constructor <;> linarith

theorem phase_interval : 0 < phaseDegrees ∧ phaseDegrees < 90 := by
  have h := angular_input_bounds
  unfold phaseDegrees
  constructor <;> linarith [h.1, h.2.1]

theorem radian_intervals :
    (∀ i, 0 < mixingRadians i ∧ mixingRadians i < Real.pi / 2) ∧
      (0 < phaseRadians ∧ phaseRadians < Real.pi / 2) :=
  ⟨fun i => HMT.II.CKM.Generated.radians_chamber (mixing_intervals i),
    HMT.II.CKM.Generated.radians_chamber phase_interval⟩

theorem unitary : matrixᴴ * matrix = 1 ∧ matrix * matrixᴴ = 1 :=
  ⟨CKM_left_unitary _ _ _ _, CKM_right_unitary _ _ _ _⟩

theorem jarlskog_formula :
    jarlskog matrix =
      Real.cos (mixingRadians 0) * Real.cos (mixingRadians 1) *
      Real.cos (mixingRadians 2) ^ 2 * Real.sin (mixingRadians 0) *
      Real.sin (mixingRadians 1) * Real.sin (mixingRadians 2) *
      Real.sin phaseRadians := CKM_jarlskog _ _ _ _

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
  nonzero_jarlskog_obstructs_real_rephasing matrix
    (ne_of_gt jarlskog_positive) u d hu hd

def transportedMass (m : Fin 3 → ℝ) : HMT.CKM.Spectral.Mat3 :=
  massTransport (mixingRadians 0) (mixingRadians 1) (mixingRadians 2) phaseRadians m

abbrev spectralSeparation := HMT.II.CKM.Generated.spectralSeparation

theorem mass_transport (m : Fin 3 → ℝ) :
    (transportedMass m).IsHermitian ∧
    (transportedMass m).charpoly = (diagonal (fun i => (m i : ℂ))).charpoly ∧
    spectrum ℂ (transportedMass m) = spectrum ℂ (diagonal (fun i => (m i : ℂ))) :=
  ⟨massTransport_hermitian _ _ _ _ m,
    massTransport_charpoly _ _ _ _ m, massTransport_spectrum _ _ _ _ m⟩

theorem commutator_determinant (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det =
      2 * I * (jarlskog matrix * spectralSeparation u * spectralSeparation d : ℝ) :=
  massTransport_jarlskog_determinant _ _ _ _ u d

/-- Mass nondegeneracy remains explicit; no mass spectrum is chosen here. -/
theorem commutator_nonzero (u d : Fin 3 → ℝ)
    (hu : spectralSeparation u ≠ 0) (hd : spectralSeparation d ≠ 0) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det ≠ 0 := by
  rw [commutator_determinant]
  apply mul_ne_zero
  · exact mul_ne_zero (by norm_num) Complex.I_ne_zero
  · exact_mod_cast mul_ne_zero (mul_ne_zero (ne_of_gt jarlskog_positive) hu) hd

/-- The selected register has no remaining Ledger or numerical-domain
premise in its CKM angular, unitary and spectral publication. -/
theorem principal_ckm_publication :
    alpha = AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (∀ s : Incidence.DeclaredSectorFrame,
      Incidence.incidenceReader s coordinates = mixingDegrees) ∧
    recover mixingDegrees = coordinates ∧
    (matrixᴴ * matrix = 1 ∧ matrix * matrixᴴ = 1) ∧
    0 < jarlskog matrix ∧
    (∀ m : Fin 3 → ℝ,
      spectrum ℂ (transportedMass m) = spectrum ℂ (diagonal (fun i => (m i : ℂ)))) ∧
    (∀ u d : Fin 3 → ℝ,
      (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass d)).det =
        2 * I * (jarlskog matrix * spectralSeparation u * spectralSeparation d : ℝ)) :=
  ⟨alpha_uses_shared_register, action_decimal_order, incidence_evaluation,
    coordinate_recovery, unitary, jarlskog_positive,
    fun m => (mass_transport m).2.2, commutator_determinant⟩

end HMT.II.CKMFromSharedBase
end

#print axioms HMT.II.CKMFromSharedBase.coordinate_sources
#print axioms HMT.II.CKMFromSharedBase.angular_input_bounds
#print axioms HMT.II.CKMFromSharedBase.coordinate_recovery
#print axioms HMT.II.CKMFromSharedBase.phase_check
#print axioms HMT.II.CKMFromSharedBase.unitary
#print axioms HMT.II.CKMFromSharedBase.jarlskog_positive
#print axioms HMT.II.CKMFromSharedBase.no_real_rephasing
#print axioms HMT.II.CKMFromSharedBase.mass_transport
#print axioms HMT.II.CKMFromSharedBase.commutator_determinant
#print axioms HMT.II.CKMFromSharedBase.commutator_nonzero
#print axioms HMT.II.CKMFromSharedBase.principal_ckm_publication
