import LatticeTwistedNormalCommutation
import LatticeTwistedNormalLinear
import LatticeTwistedRawStateField
import LatticeWordPermutation

/-! The constructed raw W-map agrees with every oscillator-word presentation
of the actual lattice state, not just its chosen occupation representative.
Its creation recursion holds on the entire existing lattice carrier. -/
noncomputable section
namespace HMT.IV.LatticeTwistedWordCoherence
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeOscillatorWords LatticeWordPermutation LatticeTwistedCarrier
open LatticeTwistedNormalDerivative LatticeTwistedNormalCommutation
open LatticeTwistedNormalLinear LatticeTwistedRawStateField

theorem rawDescendantField_perm (o : Fin 12) (x : Lattice o)
    {u v : List (Mode o)} (h : List.Perm u v) :
    rawDescendantField o x u = rawDescendantField o x v := by
  induction h with
  | nil => rfl
  | cons a _ ih => simp only [rawDescendantField, ih]
  | swap a b w => exact derivativeNormalField_commute o _ _ _ _ _
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

theorem rawStateField_stateForWord (o : Fin 12) (w : List (Mode o)) (x : Lattice o) :
    rawStateField o (stateForWord o w x) = rawDescendantField o x w := by
  rw [stateForWord_basis, rawStateField_basis]
  exact rawDescendantField_perm o x (wordForOccupation_perm o w)

theorem rawDescendantField_eq_of_occupation (o : Fin 12) (x : Lattice o)
    (u v : List (Mode o)) (h : wordOccupation o u = wordOccupation o v) :
    rawDescendantField o x u = rawDescendantField o x v :=
  rawDescendantField_perm o x ((wordOccupation_eq_iff_perm o u v).mp h)

theorem rawStateField_create_intertwines (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    (rawStateField o).comp (onCarrier o (create o n i)) =
      (derivativeNormalFieldLinear o i n).comp (rawStateField o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [LinearMap.comp_apply]
  rw [← carrierBasis_wordForOccupation o a x]
  change rawStateField o (stateForWord o ((n,i)::wordForOccupation o a) x) =
    derivativeNormalField o i n (rawStateField o (stateForWord o (wordForOccupation o a) x))
  rw [rawStateField_stateForWord, rawStateField_stateForWord]
  rfl

theorem rawStateField_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (u : LatticeCarrier o) :
    rawStateField o (onCarrier o (create o n i) u) =
      derivativeNormalField o i n (rawStateField o u) :=
  LinearMap.congr_fun (rawStateField_create_intertwines o n i) u

end HMT.IV.LatticeTwistedWordCoherence
end

#print axioms HMT.IV.LatticeTwistedWordCoherence.rawDescendantField_perm
#print axioms HMT.IV.LatticeTwistedWordCoherence.rawStateField_stateForWord
#print axioms HMT.IV.LatticeTwistedWordCoherence.rawDescendantField_eq_of_occupation
#print axioms HMT.IV.LatticeTwistedWordCoherence.rawStateField_create_intertwines
#print axioms HMT.IV.LatticeTwistedWordCoherence.rawStateField_create
