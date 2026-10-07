import LatticeHalfIntegerHeisenberg
import Mathlib.Algebra.Vertex.VertexOperator

/-! The half-integer Heisenberg field in the ramified coordinate t, z=t^2.
A frequency r=m+1/2 has Laurent exponent -2r-2=-2m-3 in t. This is a genuine
pointwise lower-truncated Laurent field on the existing Fock algebra; it is
not a declaration of the twisted lattice-module state-field correspondence. -/

noncomputable section
namespace HMT.IV.LatticeHalfIntegerField
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg

def ramifiedExponent (m : ℤ) : ℤ := -2*m-3

theorem ramifiedExponent_frequency (m : ℤ) :
    (ramifiedExponent m : ℚ)/2 = -frequency m-1 := by
  simp only [ramifiedExponent, frequency, Int.cast_sub, Int.cast_mul,
    Int.cast_neg, Int.cast_ofNat]
  ring

def halfFieldCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    Module.End ℂ (HalfFock o) :=
  if k%2=1 then halfMode o i ((-k-3)/2) else 0

theorem halfFieldCoefficient_mode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    halfFieldCoefficient o i (ramifiedExponent m) = halfMode o i m := by
  have hp : ramifiedExponent m%2=1 := by dsimp [ramifiedExponent]; omega
  have hi : (-ramifiedExponent m-3)/2=m := by dsimp [ramifiedExponent]; omega
  rw [halfFieldCoefficient, if_pos hp, hi]

theorem halfFieldCoefficient_even (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    halfFieldCoefficient o i (2*k)=0 := by
  rw [halfFieldCoefficient, if_neg (by omega)]

theorem halfFieldCoefficient_bounded_pole (o : Fin 12) (i : Fin (BasisSize o))
    (v : HalfFock o) : ∃ b : ℤ, ∀ k < b, halfFieldCoefficient o i k v=0 := by
  obtain ⟨N,hN⟩ := halfMode_annihilation_bound o v
  refine ⟨-2*(N:ℤ)-3, ?_⟩
  intro k hk
  by_cases hp : k%2=1
  · rw [halfFieldCoefficient, if_pos hp]
    have hi : (-k-3)/2 = (((-k-3)/2).toNat:ℤ) := by omega
    rw [hi]
    exact hN _ (by omega) i
  · simp only [halfFieldCoefficient, if_neg hp, LinearMap.zero_apply]

def halfHeisenbergField (o : Fin 12) (i : Fin (BasisSize o)) :
    VertexOperator ℂ (HalfFock o) :=
  VertexOperator.of_coeff (halfFieldCoefficient o i) (halfFieldCoefficient_bounded_pole o i)

theorem halfHeisenbergField_coefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    HVertexOperator.coeff (halfHeisenbergField o i) k = halfFieldCoefficient o i k := by
  apply LinearMap.ext
  intro v
  rfl

theorem halfHeisenbergField_mode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    HVertexOperator.coeff (halfHeisenbergField o i) (ramifiedExponent m) =
      halfMode o i m := by
  rw [halfHeisenbergField_coefficient, halfFieldCoefficient_mode]

theorem halfHeisenbergField_even_coefficient (o : Fin 12)
    (i : Fin (BasisSize o)) (k : ℤ) :
    HVertexOperator.coeff (halfHeisenbergField o i) (2*k)=0 := by
  rw [halfHeisenbergField_coefficient, halfFieldCoefficient_even]

theorem halfHeisenbergField_vacuum_annihilation (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) :
    HVertexOperator.coeff (halfHeisenbergField o i) (ramifiedExponent (n:ℤ)) 1=0 := by
  rw [halfHeisenbergField_mode, halfMode_ofNat, halfAnnihilate_vacuum]

theorem halfHeisenbergField_vacuum_creation (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) :
    HVertexOperator.coeff (halfHeisenbergField o i) (2*(n:ℤ)-1) 1=create o n i 1 := by
  have hk : 2*(n:ℤ)-1=ramifiedExponent (Int.negSucc n) := by
    dsimp [ramifiedExponent]
    omega
  rw [hk, halfHeisenbergField_mode, halfMode_negSucc]

theorem halfHeisenbergField_mode_relation (o : Fin 12)
    (i j : Fin (BasisSize o)) (m n : ℤ) :
    (HVertexOperator.coeff (halfHeisenbergField o i) (ramifiedExponent m)).comp
        (HVertexOperator.coeff (halfHeisenbergField o j) (ramifiedExponent n)) -
      (HVertexOperator.coeff (halfHeisenbergField o j) (ramifiedExponent n)).comp
        (HVertexOperator.coeff (halfHeisenbergField o i) (ramifiedExponent m)) =
      (if frequency m+frequency n=0 then ((frequency m:ℂ)*gram o i j) else 0) •
        (LinearMap.id : Module.End ℂ (HalfFock o)) := by
  simp only [halfHeisenbergField_mode]
  exact half_heisenberg_relation o i j m n

end HMT.IV.LatticeHalfIntegerField
end

#print axioms HMT.IV.LatticeHalfIntegerField.ramifiedExponent
#print axioms HMT.IV.LatticeHalfIntegerField.ramifiedExponent_frequency
#print axioms HMT.IV.LatticeHalfIntegerField.halfFieldCoefficient
#print axioms HMT.IV.LatticeHalfIntegerField.halfFieldCoefficient_mode
#print axioms HMT.IV.LatticeHalfIntegerField.halfFieldCoefficient_even
#print axioms HMT.IV.LatticeHalfIntegerField.halfFieldCoefficient_bounded_pole
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField_coefficient
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField_mode
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField_even_coefficient
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField_vacuum_annihilation
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField_vacuum_creation
#print axioms HMT.IV.LatticeHalfIntegerField.halfHeisenbergField_mode_relation
