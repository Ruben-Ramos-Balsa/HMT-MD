import TerminalOrbitalSelection
import AlphaTightBounds
import VacancyDeltaBounds

/-!
Composition of the finite orbital selector with the existing dodecaphase and
analytic alpha proofs. This does not manufacture an incidence history whose
digits were fitted to K. The register here is explicitly the output of the
finite selector, with the declared input domain documented in TerminalInputs.
-/
namespace HMT.I.TerminalSelector

def selectedNumerator : Nat := selectedCandidates.headD 0

def selectedDigits : List Nat := (List.range 12).map (decimalCoordinate selectedNumerator)

def selectedRegister : RadixRecovery.K12 where
  digits := selectedDigits
  valid := by
    intro digit hd
    obtain ⟨i, _, rfl⟩ := List.mem_map.mp hd
    exact Nat.mod_lt _ (by decide)
  length_eq := by simp [selectedDigits]

theorem selected_register_digits : selectedRegister.digits =
    [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601] := by
  change (List.range 12).map (decimalCoordinate (selectedCandidates.headD 0)) = _
  rw [terminal_selection]
  exact terminal_coordinates

theorem selected_register_recovery :
    RadixRecovery.decode 1000 12 selectedRegister.publish = selectedRegister.digits :=
  RadixRecovery.k12_recover selectedRegister

noncomputable section

theorem selected_terminal_alpha :
    ∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart selectedRegister VacancyDeltaBounds.vacancyDelta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication selectedRegister n).outgoing = 0 ∧
        (AlphaPublications.publication selectedRegister n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat) := by
  have hk := AlphaSourceBounds.periodic_in_unit selectedRegister selected_register_digits
  have ha := AlphaSourceBounds.precoordinate_bounds selectedRegister selected_register_digits
  have hlink := AlphaTightBounds.stateLink_bound_of_vacancy_enclosure
    selectedRegister selected_register_digits VacancyDeltaBounds.vacancyDelta
    VacancyDeltaBounds.vacancyDelta_enclosure.1 VacancyDeltaBounds.vacancyDelta_enclosure.2
  exact AlphaPublications.unique_root_with_all_publications
    selectedRegister VacancyDeltaBounds.vacancyDelta hk ha.1 ha.2 hlink

end
end HMT.I.TerminalSelector

#print axioms HMT.I.TerminalSelector.selected_register_digits
#print axioms HMT.I.TerminalSelector.selected_register_recovery
#print axioms HMT.I.TerminalSelector.selected_terminal_alpha
