import LatticeNormalOrderedField
import LatticeChargedVertexField

/-!
Fields for every finite oscillator descendant of every lattice charge.
The creation property is proved recursively from the concrete charged
field and the locally finite normal product, not inserted as a field axiom.
-/

noncomputable section
namespace HMT.IV.LatticeDescendantFields

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticeNormalOrderedField
open scoped BigOperators TensorProduct

def Creates (o : Fin 12) (B : VertexOperator ℂ (LatticeCarrier o))
    (u : LatticeCarrier o) : Prop :=
  (∀ k : ℤ, k < 0 → HVertexOperator.coeff B k (vacuum o) = 0) ∧
    HVertexOperator.coeff B 0 (vacuum o) = u

theorem nonnegative_modes_vacuum (o : Fin 12) (i : Fin (BasisSize o)) (a : ℕ) :
    hmode o i (a : ℤ) (vacuum o) = 0 := by
  cases a with
  | zero =>
    simp only [Nat.cast_zero, hmode_zero, vacuum, onLattice_pure,
      HMT.IV.LatticeZeroModes.zeroMode_vacuum, TensorProduct.tmul_zero]
  | succ a =>
    rw [hmode_castSucc]
    exact carrier_vacuum_annihilated o a i

theorem annihilationTerm_vacuum (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n B k a (vacuum o) = 0 := by
  simp only [annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    nonnegative_modes_vacuum, map_zero, smul_zero]

theorem normalField_creates (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (u : LatticeCarrier o)
    (hB : Creates o B u) :
    Creates o (normalField o i n B) (onCarrier o (create o n i) u) := by
  constructor
  · intro k hk
    rw [normalField_coefficient, normalCoefficient_apply]
    have hc : ∀ a, creationTerm o i n B k a (vacuum o) = 0 := by
      intro a
      simp only [creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
        hB.1 (k-a) (by omega), map_zero, smul_zero]
    simp only [hc, annihilationTerm_vacuum, finsum_zero, add_zero]
  · rw [normalField_coefficient, normalCoefficient_apply]
    have hc : (∑ᶠ a, creationTerm o i n B 0 a (vacuum o)) =
        creationTerm o i n B 0 0 (vacuum o) := by
      apply finsum_eq_single
      intro a ha
      simp only [creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
        hB.1 (0-a) (by omega), map_zero, smul_zero]
    rw [hc]
    simp only [annihilationTerm_vacuum, finsum_zero, add_zero]
    simp only [creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      Nat.zero_add, Nat.choose_self, Nat.cast_one, one_smul,
      Nat.cast_zero, sub_zero, hB.2]

theorem chargedField_creates (o : Fin 12) (x : Lattice o) :
    Creates o (HMT.IV.LatticeChargedVertexField.chargedField o x)
      ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) := by
  constructor
  · intro k hk
    exact HMT.IV.LatticeChargedVertexField.fieldCoefficient_vacuum_negative o x k hk
  · exact HMT.IV.LatticeChargedVertexField.fieldCoefficient_vacuum_zero o x

def descendantState (o : Fin 12) (x : Lattice o) : List (Mode o) → LatticeCarrier o
  | [] => (1 : Fock o) ⊗ₜ[ℂ] basisElement o x
  | m :: w => onCarrier o (create o m.1 m.2) (descendantState o x w)

def descendantField (o : Fin 12) (x : Lattice o) :
    List (Mode o) → VertexOperator ℂ (LatticeCarrier o)
  | [] => HMT.IV.LatticeChargedVertexField.chargedField o x
  | m :: w => normalField o m.2 m.1 (descendantField o x w)

/-- Every finite oscillator history is assigned a genuine field creating
that exact history at the vacuum. There is no bound on word length or modes. -/
theorem descendantField_creates (o : Fin 12) (x : Lattice o) (w : List (Mode o)) :
    Creates o (descendantField o x w) (descendantState o x w) := by
  induction w with
  | nil => exact chargedField_creates o x
  | cons m w ih => exact normalField_creates o m.2 m.1 _ _ ih

theorem descendantField_recovers_state (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) :
    HVertexOperator.coeff (descendantField o x w) 0 (vacuum o) =
      descendantState o x w := (descendantField_creates o x w).2

theorem descendantField_regular_at_vacuum (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) (k : ℤ) (hk : k < 0) :
    HVertexOperator.coeff (descendantField o x w) k (vacuum o) = 0 :=
  (descendantField_creates o x w).1 k hk

end HMT.IV.LatticeDescendantFields
end

#print axioms HMT.IV.LatticeDescendantFields.normalField_creates
#print axioms HMT.IV.LatticeDescendantFields.chargedField_creates
#print axioms HMT.IV.LatticeDescendantFields.descendantField_creates
#print axioms HMT.IV.LatticeDescendantFields.descendantField_recovers_state
#print axioms HMT.IV.LatticeDescendantFields.descendantField_regular_at_vacuum
