import LatticeStateFieldMap

/-!
# Occupations, permutations and the remaining normal-product interface

The occupation/permutation equivalence and the equality of descendant states
below are unconditional consequences of the existing oscillator construction.
The last results are deliberately auxiliary implications: their explicit
normal-product commutation hypothesis must be supplied by a separate proof.
They do not assert that field invariance follows from creativity alone.
-/

noncomputable section
namespace HMT.IV.LatticeWordPermutation

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeOscillatorWords
open HMT.IV.LatticeDescendantFields HMT.IV.LatticeStateFieldMap
open HMT.IV.LatticeNormalOrderedField

theorem wordOccupation_eq_iff_perm (o : Fin 12) (u v : List (Mode o)) :
    wordOccupation o u = wordOccupation o v ↔ List.Perm u v := by
  classical
  rw [wordOccupation_toFinsupp, wordOccupation_toFinsupp]
  constructor
  · intro h
    exact Multiset.coe_eq_coe.mp (Multiset.toFinsupp.injective h)
  · intro h
    exact congrArg Multiset.toFinsupp (Multiset.coe_eq_coe.mpr h)

theorem wordForOccupation_perm (o : Fin 12) (w : List (Mode o)) :
    List.Perm (wordForOccupation o (wordOccupation o w)) w :=
  (wordOccupation_eq_iff_perm o _ _).mp (wordForOccupation_counts o _)

theorem canonical_words_equal_of_perm (o : Fin 12) (u v : List (Mode o))
    (h : List.Perm u v) :
    wordForOccupation o (wordOccupation o u) =
      wordForOccupation o (wordOccupation o v) := by
  rw [(wordOccupation_eq_iff_perm o u v).mpr h]

theorem descendantState_perm (o : Fin 12) (x : Lattice o)
    (u v : List (Mode o)) (h : List.Perm u v) :
    descendantState o x u = descendantState o x v := by
  rw [descendantState_eq_word, descendantState_eq_word]
  exact equal_occupations_same_state o u v
    ((wordOccupation_eq_iff_perm o u v).mpr h) x

/-- Auxiliary implication only: normal-product commutation is an explicit
premise, not a theorem asserted by this module. -/
theorem descendantField_perm_of_normal_commute (o : Fin 12)
    (hcomm : ∀ (i : Fin (BasisSize o)) (n : ℕ) (j : Fin (BasisSize o)) (m : ℕ)
      (B : VertexOperator ℂ (LatticeCarrier o)),
      normalField o i n (normalField o j m B) =
        normalField o j m (normalField o i n B))
    (x : Lattice o) {u v : List (Mode o)} (h : List.Perm u v) :
    descendantField o x u = descendantField o x v := by
  induction h with
  | nil => rfl
  | cons a _ ih => simp only [descendantField, ih]
  | swap a b w => exact hcomm _ _ _ _ _
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

/-- The canonical assignment agrees with every oscillator-word
presentation once normal-product commutation has actually been proved. -/
theorem stateField_descendant_of_normal_commute (o : Fin 12)
    (hcomm : ∀ (i : Fin (BasisSize o)) (n : ℕ) (j : Fin (BasisSize o)) (m : ℕ)
      (B : VertexOperator ℂ (LatticeCarrier o)),
      normalField o i n (normalField o j m B) =
        normalField o j m (normalField o i n B))
    (x : Lattice o) (w : List (Mode o)) :
    stateField o (descendantState o x w) = descendantField o x w := by
  rw [descendantState_eq_word, stateForWord_basis, stateField_basis]
  exact descendantField_perm_of_normal_commute o hcomm x (wordForOccupation_perm o w)

theorem descendantField_eq_of_occupation_of_normal_commute (o : Fin 12)
    (hcomm : ∀ (i : Fin (BasisSize o)) (n : ℕ) (j : Fin (BasisSize o)) (m : ℕ)
      (B : VertexOperator ℂ (LatticeCarrier o)),
      normalField o i n (normalField o j m B) =
        normalField o j m (normalField o i n B))
    (x : Lattice o) (u v : List (Mode o))
    (h : wordOccupation o u = wordOccupation o v) :
    descendantField o x u = descendantField o x v :=
  descendantField_perm_of_normal_commute o hcomm x
    ((wordOccupation_eq_iff_perm o u v).mp h)

end HMT.IV.LatticeWordPermutation
end

#print axioms HMT.IV.LatticeWordPermutation.wordOccupation_eq_iff_perm
#print axioms HMT.IV.LatticeWordPermutation.wordForOccupation_perm
#print axioms HMT.IV.LatticeWordPermutation.canonical_words_equal_of_perm
#print axioms HMT.IV.LatticeWordPermutation.descendantState_perm
#print axioms HMT.IV.LatticeWordPermutation.descendantField_perm_of_normal_commute
#print axioms HMT.IV.LatticeWordPermutation.stateField_descendant_of_normal_commute
#print axioms HMT.IV.LatticeWordPermutation.descendantField_eq_of_occupation_of_normal_commute
