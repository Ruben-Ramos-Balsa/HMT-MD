import LatticeModeWeights
import Mathlib.Data.Finsupp.Multiset

/-!
# Finite oscillator words on the existing lattice carrier

This is an explicit presentation of the already constructed monomial basis
of M(1) tensor C_epsilon[Lambda]. A finite occupation determines a finite word
with exactly those multiplicities. Acting by the existing creation operators
on the charged vacuum gives the corresponding existing carrier-basis vector.
The choice of list order does not select a lattice or change its incidence.
-/

noncomputable section
namespace HMT.IV.LatticeOscillatorWords

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeModeWeights HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open scoped TensorProduct

/-- The actual iterated oscillator action on a charged vacuum. -/
def stateForWord (o : Fin 12) : List (Mode o) → Lattice o → LatticeCarrier o
  | [], x => (1 : Fock o) ⊗ₜ[ℂ] basisElement o x
  | m :: w, x => onCarrier o (create o m.1 m.2) (stateForWord o w x)

/-- Occupations count repetitions, not just the support of a word. -/
def wordOccupation (o : Fin 12) : List (Mode o) → Occupation o
  | [] => 0
  | m :: w => Finsupp.single m 1 + wordOccupation o w

@[simp] theorem stateForWord_nil (o : Fin 12) (x : Lattice o) :
    stateForWord o [] x = (1 : Fock o) ⊗ₜ[ℂ] basisElement o x := rfl

@[simp] theorem stateForWord_cons (o : Fin 12) (m : Mode o)
    (w : List (Mode o)) (x : Lattice o) :
    stateForWord o (m :: w) x =
      onCarrier o (create o m.1 m.2) (stateForWord o w x) := rfl

theorem wordOccupation_toFinsupp (o : Fin 12) (w : List (Mode o)) :
    wordOccupation o w = (w : Multiset (Mode o)).toFinsupp := by
  classical
  induction w with
  | nil => simp [wordOccupation]
  | cons m w ih =>
    change Finsupp.single m 1 + wordOccupation o w =
      Multiset.toFinsupp ({m} + (w : Multiset (Mode o)))
    rw [ih, Multiset.toFinsupp_add, Multiset.toFinsupp_singleton]

/-- A concrete representative obtained from the occupation multiset. -/
def wordForOccupation (o : Fin 12) (a : Occupation o) : List (Mode o) :=
  a.toMultiset.toList

@[simp] theorem wordForOccupation_zero (o : Fin 12) :
    wordForOccupation o 0 = [] := by
  simp [wordForOccupation]

@[simp] theorem wordForOccupation_counts (o : Fin 12) (a : Occupation o) :
    wordOccupation o (wordForOccupation o a) = a := by
  classical
  rw [wordOccupation_toFinsupp]
  simp [wordForOccupation]

theorem stateForWord_basis (o : Fin 12) (w : List (Mode o)) (x : Lattice o) :
    stateForWord o w x = carrierBasis o (wordOccupation o w, x) := by
  classical
  induction w with
  | nil =>
    simp [stateForWord, wordOccupation, carrierBasis, Basis.tensorProduct_apply,
      monomialBasis_product, latticeBasisComplex, basisElement,
      Finsupp.coe_basisSingleOne]
    rfl
  | cons m w ih =>
    rw [stateForWord_cons, ih]
    simp only [carrierBasis, Basis.tensorProduct_apply, onCarrier_pure,
      create_monomial, wordOccupation]

theorem carrierBasis_wordForOccupation (o : Fin 12) (a : Occupation o)
    (x : Lattice o) :
    stateForWord o (wordForOccupation o a) x = carrierBasis o (a, x) := by
  rw [stateForWord_basis, wordForOccupation_counts]

theorem every_carrierBasis_has_word (o : Fin 12) (a : Occupation o)
    (x : Lattice o) : ∃ w : List (Mode o), stateForWord o w x = carrierBasis o (a, x) :=
  ⟨wordForOccupation o a, carrierBasis_wordForOccupation o a x⟩

theorem equal_occupations_same_state (o : Fin 12) (u v : List (Mode o))
    (h : wordOccupation o u = wordOccupation o v) (x : Lattice o) :
    stateForWord o u x = stateForWord o v x := by
  rw [stateForWord_basis, stateForWord_basis, h]

end HMT.IV.LatticeOscillatorWords
end

#print axioms HMT.IV.LatticeOscillatorWords.carrierBasis_wordForOccupation
#print axioms HMT.IV.LatticeOscillatorWords.every_carrierBasis_has_word
#print axioms HMT.IV.LatticeOscillatorWords.equal_occupations_same_state
