import GeneratedCKM
import CKMCycle
import SectorIncidenceData

/-! Composition of the exact CKM chain with the preserved incidence reading,
all-depth publications, action decade and spectral realization. The only
upstream register interface is inherited verbatim from the existing proof;
it is not replaced by a ledger manufactured from the desired digits.
Mass readers are arbitrary here: no measured mass selects the angular matrix.
-/
noncomputable section
namespace HMT.II.CKM.Generated
open HMT.IncidenceRegister AlphaIncidencePublications
open HMT.CKM.Spectral HMT.CKM.ComplexRealization
open Matrix Complex

def transportedMass (l : Ledger) (m : Fin 3 → ℝ) : HMT.CKM.Spectral.Mat3 :=
  massTransport (mixingRadians l 0) (mixingRadians l 1)
    (mixingRadians l 2) (phaseRadians l) m

def spectralSeparation (m : Fin 3 → ℝ) : ℝ :=
  (m 0 - m 1) * (m 1 - m 2) * (m 2 - m 0)

theorem generated_sector_incidence (l : Ledger) :
    Incidence.markedFace.card = 4 ∧ Incidence.hexadSupport.card = 6 ∧
    Incidence.tritAlphabet.card = 3 ∧
    (∀ s : Incidence.DeclaredSectorFrame,
      Incidence.incidenceReader s (coordinates l) = mixingDegrees l) :=
  ⟨Incidence.marked_face_card, Incidence.hexad_card, Incidence.trit_card,
    fun s => Incidence.incidence_reader_is_chart s (coordinates l)⟩

theorem generated_mass_transport (l : Ledger) (m : Fin 3 → ℝ) :
    (transportedMass l m).IsHermitian ∧
    (transportedMass l m).charpoly =
      (diagonal (fun i => (m i : ℂ))).charpoly ∧
    spectrum ℂ (transportedMass l m) =
      spectrum ℂ (diagonal (fun i => (m i : ℂ))) :=
  ⟨massTransport_hermitian _ _ _ _ m,
    massTransport_charpoly _ _ _ _ m,
    massTransport_spectrum _ _ _ _ m⟩

theorem generated_commutator_determinant (l : Ledger) (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass l d)).det =
      2 * I * (jarlskog (matrix l) * spectralSeparation u * spectralSeparation d : ℝ) := by
  exact massTransport_jarlskog_determinant _ _ _ _ u d

theorem generated_commutator_nonzero (l : Ledger) (hl : PublishedRegister l)
    (u d : Fin 3 → ℝ) (hu : spectralSeparation u ≠ 0)
    (hd : spectralSeparation d ≠ 0) :
    (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass l d)).det ≠ 0 := by
  rw [generated_commutator_determinant]
  apply mul_ne_zero
  · exact mul_ne_zero (by norm_num) Complex.I_ne_zero
  · exact Complex.ofReal_ne_zero.mpr
      (mul_ne_zero (mul_ne_zero (ne_of_gt (generated_jarlskog_positive l hl)) hu) hd)

/-- The terminal theorem joins the same incidence publication to compatible
arbitrary-depth readouts, action scale, recovered angular coordinates, unitary
mixing, a positive phase invariant and spectral transport. It does not promote
the register interface into a proof of its own upstream selection. -/
theorem generated_ckm_principal_chain (l : Ledger) (hl : PublishedRegister l) :
    (Incidence.markedFace.card = 4 ∧ Incidence.hexadSupport.card = 6 ∧
      Incidence.tritAlphabet.card = 3 ∧
      (∀ s : Incidence.DeclaredSectorFrame,
        Incidence.incidenceReader s (coordinates l) = mixingDegrees l)) ∧
    RadixRecovery.decode 1000 12 (register l).publish = (register l).digits ∧
    (∀ n m : ℕ,
      ((AlphaPublications.publication (register l) (n + m)).digits).take (12 * n) =
        (AlphaPublications.publication (register l) n).digits) ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale HMT.II.GeneratedAction.phi
        (HMT.II.GeneratedAction.alpha l)) = -34 ∧
    recover (mixingDegrees l) = coordinates l ∧
    ((matrix l)ᴴ * matrix l = 1 ∧ matrix l * (matrix l)ᴴ = 1) ∧
    0 < jarlskog (matrix l) ∧
    (∀ m : Fin 3 → ℝ,
      spectrum ℂ (transportedMass l m) =
        spectrum ℂ (diagonal (fun i => (m i : ℂ)))) ∧
    (∀ u d : Fin 3 → ℝ,
      (commutator (diagonal (fun i => (u i : ℂ))) (transportedMass l d)).det =
        2 * I * (jarlskog (matrix l) * spectralSeparation u * spectralSeparation d : ℝ)) :=
  ⟨generated_sector_incidence l,
    register_recovery l,
    compatible_publications_from_vacancy_readout l hl,
    HMT.II.GeneratedAction.generated_action_decimal_order l hl,
    generated_recovery l,
    generated_unitary l,
    generated_jarlskog_positive l hl,
    fun m => (generated_mass_transport l m).2.2,
    generated_commutator_determinant l⟩

#print axioms generated_sector_incidence
#print axioms generated_mass_transport
#print axioms generated_commutator_determinant
#print axioms generated_commutator_nonzero
#print axioms generated_ckm_principal_chain
end HMT.II.CKM.Generated
