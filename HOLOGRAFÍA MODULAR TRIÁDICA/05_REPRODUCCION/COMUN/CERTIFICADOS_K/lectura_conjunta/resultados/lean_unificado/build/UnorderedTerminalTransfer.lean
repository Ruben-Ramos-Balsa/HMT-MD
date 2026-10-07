import SelectedFromRegionalInputs

/-!
Transport of the existing terminal selection across a permutation of its
unordered input. This does not regenerate that input or assume a new axiom.
It removes an unnecessary ordering obligation when composing a source proof
of the generated repertory with the existing selector. All regional inputs,
the finite rules and the selected-register theorem are reused unchanged.
-/

namespace HMT.I.UnorderedTerminalTransfer

open HMT.I.TerminalSelector

theorem mem_fold_insert (xs : List Nat) (s : Std.HashSet Nat) (n : Nat) :
    n ∈ xs.foldl (fun acc k => acc.insert k) s ↔ n ∈ xs ∨ n ∈ s := by
  induction xs generalizing s with
  | nil => simp
  | cons k xs ih =>
      rw [List.foldl_cons, ih]
      simp only [Std.HashSet.mem_insert, beq_iff_eq, List.mem_cons]
      tauto

theorem decimal_membership (initial : Nat) (suffix panel : List Nat) (n : Nat) :
    n ∈ decimalCandidatesFrom initial suffix panel ↔
      n ∈ indexedCandidatesFrom initial suffix panel := by
  simp only [decimalCandidatesFrom, List.mem_mergeSort, Std.HashSet.mem_toList,
    mem_fold_insert]
  simp

theorem indexed_membership_perm (initial : Nat) (s t panel : List Nat)
    (h : s.Perm t) (n : Nat) :
    n ∈ indexedCandidatesFrom initial s panel ↔
      n ∈ indexedCandidatesFrom initial t panel := by
  exact (List.Perm.flatMap_right _ h.permutations).mem_iff

theorem selector_membership_perm (initial : Nat) (s t panel : List Nat)
    (rows : Array N69Row) (h : s.Perm t) (n : Nat) :
    n ∈ selectFrom initial s panel rows ↔ n ∈ selectFrom initial t panel rows := by
  simp only [selectFrom, List.mem_filter, decimal_membership,
    indexed_membership_perm initial s t panel h n]

/-- The inherited singleton is independent of the order in which the source
enumerates its eight members. The source-membership premise stays explicit. -/
theorem regional_unique_for_any_order (s : List Nat) (h : s.Perm s8Input) (n : Nat) :
    n ∈ selectFrom RegionalW24.regionalW24 s regionalPanel
      (GeneratedN69Rows.generatedRows GeneratedN69Rows.regionalPrefixes) ↔
      n = 234543140729659824621058914794146601 := by
  rw [selector_membership_perm _ s s8Input _ _ h]
  change n ∈ regionalSelectedCandidates ↔ _
  rw [regional_terminal_selection]
  simp

end HMT.I.UnorderedTerminalTransfer

#print axioms HMT.I.UnorderedTerminalTransfer.mem_fold_insert
#print axioms HMT.I.UnorderedTerminalTransfer.selector_membership_perm
#print axioms HMT.I.UnorderedTerminalTransfer.regional_unique_for_any_order
