import SelectedTerminalAlpha
import RegionalPanelBridge
import GeneratedN69Rows
import RegionalW24

/-!
Composition with generated regional inputs. Both the nine-position panel and
the N69 rows are evaluated from the existing regional readers; the literal
tables are used only by the equality certificates imported below. W24 is
computed by the oriented regional descriptor. Only unordered S8 remains an
explicit source interface not generated in this module.
-/
noncomputable section
namespace HMT.I.TerminalSelector

def regionalSelectedCandidates : List Nat :=
  selectFrom RegionalW24.regionalW24 s8Input regionalPanel
    (GeneratedN69Rows.generatedRows GeneratedN69Rows.regionalPrefixes)

theorem regional_selection_eq : regionalSelectedCandidates = selectedCandidates := by
  unfold regionalSelectedCandidates
  rw [RegionalW24.regionalW24_eq_input, regionalPanel_eq,
    GeneratedN69Rows.regional_generatedRows_eq_n69Input]
  exact selectFrom_published_inputs

theorem regional_terminal_selection :
    regionalSelectedCandidates = [234543140729659824621058914794146601] :=
  regional_selection_eq.trans terminal_selection

def regionalRegister : RadixRecovery.K12 where
  digits := (List.range 12).map (decimalCoordinate (regionalSelectedCandidates.headD 0))
  valid := by
    intro digit hd
    obtain ⟨i, _, rfl⟩ := List.mem_map.mp hd
    exact Nat.mod_lt _ (by decide)
  length_eq := by simp

theorem regionalRegister_eq_selected : regionalRegister = selectedRegister := by
  unfold regionalRegister
  simp only [regional_selection_eq]
  rfl

theorem regional_terminal_alpha :
    ∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart regionalRegister VacancyDeltaBounds.vacancyDelta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication regionalRegister n).outgoing = 0 ∧
        (AlphaPublications.publication regionalRegister n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat) := by
  rw [regionalRegister_eq_selected]
  exact selected_terminal_alpha

end HMT.I.TerminalSelector
end

#print axioms HMT.I.TerminalSelector.regional_terminal_selection
#print axioms HMT.I.TerminalSelector.regionalRegister_eq_selected
#print axioms HMT.I.TerminalSelector.regional_terminal_alpha
