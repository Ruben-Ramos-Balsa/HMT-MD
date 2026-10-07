import LatticeHeisenbergModes
import LatticeFieldTruncation
import Mathlib.Algebra.Vertex.VertexOperator

/-!
# Actual lattice Heisenberg fields

The integer modes are read from the integral pairing of the same marked
lattice, and act on its algebraic oscillator/group-algebra carrier.
Pointwise lower truncation is proved from finite support, not requested as
an additional input. It makes the field a `VertexOperator` in Mathlib's
precise sense: a linear map into vector-valued Laurent series.

This supplies the Heisenberg generating fields of the lattice construction.
It does not rename those fields the full state-field correspondence, nor
assert an orbifold or a Monster automorphism group.
-/

noncomputable section
namespace HMT.IV.LatticeHeisenbergField

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeFieldTruncation

def fieldCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    Module.End ℂ (LatticeCarrier o) := hmode o i (-k-1)

theorem fieldCoefficient_bounded_pole (o : Fin 12) (i : Fin (BasisSize o))
    (v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, fieldCoefficient o i k v = 0 := by
  obtain ⟨N, hN⟩ := exists_carrier_annihilation_bound o v
  refine ⟨-(N : ℤ)-2, ?_⟩
  intro k hk
  have hpos : 0 < -k-1 := by omega
  have hn : N ≤ (-k-2).toNat := by omega
  have heq : -k-1 = (((-k-2).toNat + 1 : ℕ) : ℤ) := by omega
  rw [fieldCoefficient, heq, hmode_castSucc]
  exact hN _ hn i

def heisenbergField (o : Fin 12) (i : Fin (BasisSize o)) :
    VertexOperator ℂ (LatticeCarrier o) :=
  VertexOperator.of_coeff (fieldCoefficient o i)
    (fieldCoefficient_bounded_pole o i)

/-- Normalized field modes are precisely the generated Heisenberg modes. -/
theorem heisenbergField_ncoeff (o : Fin 12) (i : Fin (BasisSize o)) (n : ℤ) :
    VertexOperator.ncoeff (heisenbergField o i) n = hmode o i n := by
  rw [heisenbergField, VertexOperator.ncoeff_of_coeff]
  simp [fieldCoefficient]

/-- The field coefficient at every exponent is fixed by the mode action. -/
theorem heisenbergField_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (v : LatticeCarrier o) (k : ℤ) :
    ((HahnModule.of ℂ).symm (heisenbergField o i v)).coeff k =
      hmode o i (-k-1) v := by
  rfl

/-- Nonnegative normalized modes annihilate the vacuum. -/
theorem heisenbergField_vacuum_annihilation (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) :
    VertexOperator.ncoeff (heisenbergField o i) (n : ℤ) (vacuum o) = 0 := by
  rw [heisenbergField_ncoeff]
  cases n with
  | zero =>
    simp only [Nat.cast_zero, hmode_zero, vacuum, onLattice_pure,
      LatticeZeroModes.zeroMode_vacuum, TensorProduct.tmul_zero]
  | succ n =>
    rw [hmode_castSucc]
    exact carrier_vacuum_annihilated o n i

/-- The coefficients on the vacuum are the generated oscillator states. -/
theorem heisenbergField_vacuum_creation (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) :
    ((HahnModule.of ℂ).symm (heisenbergField o i (vacuum o))).coeff (n : ℤ) =
      onCarrier o (create o n i) (vacuum o) := by
  rw [heisenbergField_coefficient]
  have heq : -(n : ℤ)-1 = Int.negSucc n := by omega
  rw [heq, hmode_negSucc]

theorem heisenbergField_mode_relation (o : Fin 12)
    (i j : Fin (BasisSize o)) (m n : ℤ) :
    (VertexOperator.ncoeff (heisenbergField o i) m).comp
        (VertexOperator.ncoeff (heisenbergField o j) n) -
      (VertexOperator.ncoeff (heisenbergField o j) n).comp
        (VertexOperator.ncoeff (heisenbergField o i) m) =
      (if m+n=0 then (m : ℂ) * gram o i j else 0) •
        (LinearMap.id : Module.End ℂ (LatticeCarrier o)) := by
  simp only [heisenbergField_ncoeff]
  exact heisenberg_relation o i j m n

/-- The coefficient of the commutator multiplied by `(z-w)^2`.
The two formal variables are kept separate; this does not substitute a
diagonal evaluation for formal-distribution locality. -/
def orderTwoLocalityCoefficient (o : Fin 12)
    (i j : Fin (BasisSize o)) (m n : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  ((hmode o i (m+2)).comp (hmode o j n) -
      (hmode o j n).comp (hmode o i (m+2))) -
    (2 : ℂ) • ((hmode o i (m+1)).comp (hmode o j (n+1)) -
      (hmode o j (n+1)).comp (hmode o i (m+1))) +
    ((hmode o i m).comp (hmode o j (n+2)) -
      (hmode o j (n+2)).comp (hmode o i m))

/-- Coefficientwise order-two locality of the actual Heisenberg fields. -/
theorem heisenbergField_locality_order_two (o : Fin 12)
    (i j : Fin (BasisSize o)) (m n : ℤ) :
    orderTwoLocalityCoefficient o i j m n = 0 := by
  unfold orderTwoLocalityCoefficient
  rw [heisenberg_relation, heisenberg_relation, heisenberg_relation]
  by_cases h : m+n+2 = 0
  · have h₁ : m+2+n=0 := by omega
    have h₂ : m+1+(n+1)=0 := by omega
    have h₃ : m+(n+2)=0 := by omega
    simp only [if_pos h₁, if_pos h₂, if_pos h₃, smul_smul]
    have hc : ((m+2 : ℤ) : ℂ) * gram o i j -
        2 * (((m+1 : ℤ) : ℂ) * gram o i j) + (m : ℂ) * gram o i j = 0 := by
      push_cast
      ring
    calc
      _ = (((m+2 : ℤ) : ℂ) * gram o i j -
          2 * (((m+1 : ℤ) : ℂ) * gram o i j) + (m : ℂ) * gram o i j) •
          (LinearMap.id : Module.End ℂ (LatticeCarrier o)) := by
        simp only [add_smul, sub_smul]
      _ = 0 := by rw [hc, zero_smul]
  · have h₁ : m+2+n≠0 := by omega
    have h₂ : m+1+(n+1)≠0 := by omega
    have h₃ : m+(n+2)≠0 := by omega
    simp [h₁, h₂, h₃]

end HMT.IV.LatticeHeisenbergField
end

#print axioms HMT.IV.LatticeHeisenbergField.fieldCoefficient_bounded_pole
#print axioms HMT.IV.LatticeHeisenbergField.heisenbergField_ncoeff
#print axioms HMT.IV.LatticeHeisenbergField.heisenbergField_coefficient
#print axioms HMT.IV.LatticeHeisenbergField.heisenbergField_vacuum_annihilation
#print axioms HMT.IV.LatticeHeisenbergField.heisenbergField_vacuum_creation
#print axioms HMT.IV.LatticeHeisenbergField.heisenbergField_mode_relation
#print axioms HMT.IV.LatticeHeisenbergField.heisenbergField_locality_order_two
