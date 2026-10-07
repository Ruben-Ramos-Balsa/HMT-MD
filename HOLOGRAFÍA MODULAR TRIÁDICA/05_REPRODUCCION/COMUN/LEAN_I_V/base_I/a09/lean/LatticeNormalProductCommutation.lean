import LatticeNormalProductExpansion
import LatticeNormalProductBounds
import LatticeNormalProductSymmetry
import LatticeWordPermutation

/-! Order independence of the actual normal-product fields on the same
marked lattice. Every double sum is locally finite before rearrangement.
No normal-product commutation or field equality is assumed. -/
noncomputable section
namespace HMT.IV.LatticeNormalProductCommutation
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeNormalOrderedField HMT.IV.LatticeNormalProductTerms
open HMT.IV.LatticeFiniteDoubleSums HMT.IV.LatticeNormalProductBounds
open HMT.IV.LatticeNormalProductExpansion HMT.IV.LatticeNormalProductSymmetry
open HMT.IV.LatticeDescendantFields HMT.IV.LatticeStateFieldMap
open HMT.IV.LatticeOscillatorWords HMT.IV.LatticeWordPermutation
open scoped BigOperators

theorem normalCoefficient_four_terms (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ)
    (v : LatticeCarrier o) :
    normalCoefficient o i n (normalField o j m B) k v =
      ((∑ᶠ a, ∑ᶠ b, cc o i j n m B k v a b) +
       ∑ᶠ a, ∑ᶠ b, ca o i j n m B k v a b) +
      ((∑ᶠ a, ∑ᶠ b, ac o i j n m B k v a b) +
       ∑ᶠ a, ∑ᶠ b, aa o i j n m B k v a b) := by
  obtain ⟨Nc, Mc, hcc, _⟩ := cc_rectangle o i j n m B k v
  obtain ⟨Na, Ma, hca, _⟩ := ca_rectangle o i j n m B k v
  obtain ⟨Nb, Mb, hac, _⟩ := ac_rectangle o i j n m B k v
  obtain ⟨Nd, Md, haa, _⟩ := aa_rectangle o i j n m B k v
  rw [normalCoefficient_apply]
  simp only [creationTerm_normalField, annihilationTerm_normalField]
  rw [finsum_add_distrib (finite_support_row_sums _ Nc hcc)
      (finite_support_row_sums _ Na hca),
    finsum_add_distrib (finite_support_row_sums _ Nb hac)
      (finite_support_row_sums _ Nd haa)]

theorem normalCoefficient_commute (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ)
    (v : LatticeCarrier o) :
    normalCoefficient o i n (normalField o j m B) k v =
      normalCoefficient o j m (normalField o i n B) k v := by
  rw [normalCoefficient_four_terms, normalCoefficient_four_terms]
  obtain ⟨Nc, Mc, hcc, hcc'⟩ := cc_rectangle o i j n m B k v
  obtain ⟨Na, Ma, hca, hca'⟩ := ca_rectangle o i j n m B k v
  obtain ⟨Nb, Mb, hac, hac'⟩ := ac_rectangle o i j n m B k v
  obtain ⟨Nd, Md, haa, haa'⟩ := aa_rectangle o i j n m B k v
  rw [finsum_comm_of_rectangle _ Nc Mc hcc hcc',
    finsum_comm_of_rectangle _ Na Ma hca hca',
    finsum_comm_of_rectangle _ Nb Mb hac hac',
    finsum_comm_of_rectangle _ Nd Md haa haa']
  simp only [cc_swap o i j n m B k v, ca_swap o i j n m B k v,
    ac_swap o i j n m B k v, aa_swap o i j n m B k v]
  abel

theorem normalField_commute (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (j : Fin (BasisSize o)) (m : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) :
    normalField o i n (normalField o j m B) =
      normalField o j m (normalField o i n B) := by
  apply VertexOperator.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  change normalCoefficient o i n (normalField o j m B) k v =
    normalCoefficient o j m (normalField o i n B) k v
  exact normalCoefficient_commute o i j n m B k v

theorem descendantField_perm (o : Fin 12) (x : Lattice o)
    {u v : List (Mode o)} (h : List.Perm u v) :
    descendantField o x u = descendantField o x v :=
  descendantField_perm_of_normal_commute o (normalField_commute o) x h

theorem stateField_descendant (o : Fin 12) (x : Lattice o) (w : List (Mode o)) :
    stateField o (descendantState o x w) = descendantField o x w :=
  stateField_descendant_of_normal_commute o (normalField_commute o) x w

theorem descendantField_eq_of_occupation (o : Fin 12) (x : Lattice o)
    (u v : List (Mode o)) (h : wordOccupation o u = wordOccupation o v) :
    descendantField o x u = descendantField o x v :=
  descendantField_eq_of_occupation_of_normal_commute o (normalField_commute o) x u v h

end HMT.IV.LatticeNormalProductCommutation
end

#print axioms HMT.IV.LatticeNormalProductCommutation.normalField_commute
#print axioms HMT.IV.LatticeNormalProductCommutation.descendantField_perm
#print axioms HMT.IV.LatticeNormalProductCommutation.stateField_descendant
#print axioms HMT.IV.LatticeNormalProductCommutation.descendantField_eq_of_occupation
