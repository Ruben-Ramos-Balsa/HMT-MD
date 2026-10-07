import APPGlobalPrefactor
import GeneratedElectronicTorsion

/-! The global APP operator, its phase mode, and the correct torsion reader
are joined to the already constructed electronic formula. The terminal
incidence-register interface remains visible rather than supplied backwards.
-/

noncomputable section
namespace HMT.I.ElectronicAPPClosure

open HMT.I.GeneratedElectronicTorsion HMT.I.APPGlobalPrefactor
open HMT.II.GeneratedAction HMT.IncidenceRegister AlphaIncidencePublications
open Matrix

theorem local_prefactor_is_global_APP_norm :
    ElectronComposition.localPrefactor = ‖incompatibility‖ := by
  rw [ElectronComposition.local_prefactor_value, incompatibility_norm]

/-- The formula's coefficient now comes from the global 729-point operator,
not just from the entry of a principal block assumed in advance. -/
theorem electronic_formula_from_APP (l : Ledger) (U : ℝ) :
    electronicComposition l U = ‖incompatibility‖ *
      (Real.exp (phi / pi ^ 2) - 22 * (alpha l) ^ 3) *
      (1 + 15 * electronicTorsion) *
      Real.exp ((80 - 54 * alpha l + 6 * electronicTorsion) *
        Real.log (actionRatio l U)) := by
  rw [electronic_composition_correct_reader, ElectronComposition.composition_formula,
    incompatibility_norm]

/-- The optimizing nonzero arithmetic mode is the TRIT phase selector.
Its orientation is retained in the mode, not reconstructed from the scalar norm. -/
theorem phase_mode_and_prefactor :
    APPPhaseMode.phaseMode ≠ 0 ∧
    APPGramSpectrum.gram *ᵥ APPPhaseMode.phaseMode =
      (1 / 4 : ℚ) • APPPhaseMode.phaseMode ∧
    ‖incompatibility‖ = Real.sqrt 3 / 4 :=
  ⟨APPPhaseMode.phase_mode_nonzero, APPPhaseMode.gram_phase_mode, incompatibility_norm⟩

#print axioms local_prefactor_is_global_APP_norm
#print axioms electronic_formula_from_APP
#print axioms phase_mode_and_prefactor

end HMT.I.ElectronicAPPClosure
