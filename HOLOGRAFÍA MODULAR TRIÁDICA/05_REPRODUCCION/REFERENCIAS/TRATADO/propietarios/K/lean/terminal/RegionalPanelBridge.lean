import RegionalSixHundred
import TerminalInputs

/-!
The nine-position functional panel is a publication of the already generated
regional prefixes. It is not an independent input to the terminal construction.
This bridge does not address the earlier choice of W24 or the unordered S8.
-/
noncomputable section
namespace HMT.I.TerminalSelector

open HMT.I.RegionalPublicationComposition HMT.I.RegionalSixHundred

def regionalPanel : List Nat :=
  [Channel.closure, Channel.propagation, Channel.autoscale].flatMap fun c =>
    (List.range 3).map fun j => (generatedPrefix c).toNat / 729 ^ (99 - j) % 729

theorem regionalPanel_eq : regionalPanel = panelInput := by
  simp only [regionalPanel, List.flatMap_cons, List.flatMap_nil,
    generatedPrefix_evaluates]
  norm_num [expectedPrefix, panelInput, List.range_succ, Int.toNat]

end HMT.I.TerminalSelector
end

#print axioms HMT.I.TerminalSelector.regionalPanel_eq
