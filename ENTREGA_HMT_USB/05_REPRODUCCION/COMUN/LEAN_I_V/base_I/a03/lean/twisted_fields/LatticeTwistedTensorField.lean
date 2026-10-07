import LatticeTwistedParity
import LatticeHalfIntegerField

/-! The ramified half-Heisenberg field on the actual twisted carrier.
Its coefficients are tensor transports of the existing half-integer modes.
Lower truncation is proved for every vector by tensor-product induction,
not asserted only on pure tensors. This is not yet the twisted lattice
state-field map or a multiplication on the orbifold carrier. -/

noncomputable section
namespace HMT.IV.LatticeTwistedTensorField
open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFiniteIrreducible
open LatticeHalfIntegerHeisenberg hiding halfMode
open LatticeHalfIntegerField LatticeTwistedCarrier LatticeTwistedParity
open LatticeTwistedOscillatorTensor

def tensorHalfFieldCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    Module.End ℂ (Carrier o) := (halfFieldCoefficient o i k).rTensor (FiniteSpace o)

theorem tensorHalfFieldCoefficient_tmul (o : Fin 12) (i : Fin (BasisSize o))
    (k : ℤ) (v : HalfFock o) (t : FiniteSpace o) :
    tensorHalfFieldCoefficient o i k (v ⊗ₜ[ℂ] t) =
      halfFieldCoefficient o i k v ⊗ₜ[ℂ] t :=
  LinearMap.rTensor_tmul (FiniteSpace o) (halfFieldCoefficient o i k) t v

theorem tensorHalfFieldCoefficient_mode (o : Fin 12) (i : Fin (BasisSize o))
    (m : ℤ) : tensorHalfFieldCoefficient o i (ramifiedExponent m) = halfMode o i m := by
  unfold tensorHalfFieldCoefficient
  rw [halfFieldCoefficient_mode]
  rfl

theorem tensorHalfFieldCoefficient_even (o : Fin 12) (i : Fin (BasisSize o))
    (k : ℤ) : tensorHalfFieldCoefficient o i (2*k) = 0 := by
  rw [tensorHalfFieldCoefficient, halfFieldCoefficient_even, LinearMap.rTensor_zero]

theorem tensorHalfFieldCoefficient_bounded_pole (o : Fin 12) (i : Fin (BasisSize o))
    (v : Carrier o) : ∃ b : ℤ, ∀ k < b, tensorHalfFieldCoefficient o i k v = 0 := by
  induction v using TensorProduct.induction_on with
  | zero => exact ⟨0, fun _ _ => map_zero _⟩
  | tmul v t =>
    obtain ⟨b,hb⟩ := halfFieldCoefficient_bounded_pole o i v
    refine ⟨b, ?_⟩
    intro k hk
    rw [tensorHalfFieldCoefficient_tmul, hb k hk, TensorProduct.zero_tmul]
  | add v w hv hw =>
    obtain ⟨b,hb⟩ := hv
    obtain ⟨c,hc⟩ := hw
    refine ⟨min b c, ?_⟩
    intro k hk
    rw [map_add, hb k (lt_of_lt_of_le hk (min_le_left _ _)),
      hc k (lt_of_lt_of_le hk (min_le_right _ _)), add_zero]

def twistedHalfHeisenbergField (o : Fin 12) (i : Fin (BasisSize o)) :
    VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (tensorHalfFieldCoefficient o i)
    (tensorHalfFieldCoefficient_bounded_pole o i)

theorem twistedHalfHeisenbergField_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (k : ℤ) : HVertexOperator.coeff (twistedHalfHeisenbergField o i) k =
      tensorHalfFieldCoefficient o i k := by
  apply LinearMap.ext
  intro v
  rfl

theorem twistedHalfHeisenbergField_mode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    HVertexOperator.coeff (twistedHalfHeisenbergField o i) (ramifiedExponent m) =
      halfMode o i m := by
  rw [twistedHalfHeisenbergField_coefficient, tensorHalfFieldCoefficient_mode]

theorem twistedHalfHeisenbergField_even_coefficient (o : Fin 12)
    (i : Fin (BasisSize o)) (k : ℤ) :
    HVertexOperator.coeff (twistedHalfHeisenbergField o i) (2*k) = 0 := by
  rw [twistedHalfHeisenbergField_coefficient, tensorHalfFieldCoefficient_even]

theorem twistedHalfHeisenbergField_ground_annihilation (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) (t : FiniteSpace o) :
    HVertexOperator.coeff (twistedHalfHeisenbergField o i)
      (ramifiedExponent (n:ℤ)) (groundEmbedding o t) = 0 := by
  rw [twistedHalfHeisenbergField_mode]
  exact ground_annihilated o i n t

theorem twistedHalfHeisenbergField_ground_creation (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) (t : FiniteSpace o) :
    HVertexOperator.coeff (twistedHalfHeisenbergField o i)
      (2*(n:ℤ)-1) (groundEmbedding o t) = create o n i 1 ⊗ₜ[ℂ] t := by
  rw [twistedHalfHeisenbergField_coefficient]
  change tensorHalfFieldCoefficient o i (2*(n:ℤ)-1) (1 ⊗ₜ[ℂ] t) = _
  rw [tensorHalfFieldCoefficient_tmul]
  have h := halfHeisenbergField_vacuum_creation o i n
  rw [halfHeisenbergField_coefficient] at h
  rw [h]

theorem twistedHalfHeisenbergField_mode_relation (o : Fin 12)
    (i j : Fin (BasisSize o)) (m n : ℤ) :
    (HVertexOperator.coeff (twistedHalfHeisenbergField o i) (ramifiedExponent m)).comp
        (HVertexOperator.coeff (twistedHalfHeisenbergField o j) (ramifiedExponent n)) -
      (HVertexOperator.coeff (twistedHalfHeisenbergField o j) (ramifiedExponent n)).comp
        (HVertexOperator.coeff (twistedHalfHeisenbergField o i) (ramifiedExponent m)) =
      (if frequency m+frequency n=0 then ((frequency m:ℂ)*gram o i j) else 0) •
        (LinearMap.id : Module.End ℂ (Carrier o)) := by
  simp only [twistedHalfHeisenbergField_mode]
  exact half_heisenberg_tensor (FiniteSpace o) o i j m n

theorem theta_fieldCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ)
    (v : Carrier o) :
    liftedTheta o (tensorHalfFieldCoefficient o i k v) =
      -tensorHalfFieldCoefficient o i k (liftedTheta o v) := by
  by_cases hk : k%2=1
  · have he : tensorHalfFieldCoefficient o i k = halfMode o i ((-k-3)/2) := by
      simp only [tensorHalfFieldCoefficient, halfFieldCoefficient, if_pos hk]
      rfl
    rw [he]
    exact liftedTheta_halfMode o i ((-k-3)/2) v
  · simp only [tensorHalfFieldCoefficient, halfFieldCoefficient, if_neg hk,
      LinearMap.rTensor_zero, LinearMap.zero_apply, map_zero, neg_zero]

theorem theta_twistedHalfHeisenbergField_coefficient (o : Fin 12)
    (i : Fin (BasisSize o)) (k : ℤ) :
    (liftedTheta o).comp (HVertexOperator.coeff (twistedHalfHeisenbergField o i) k) =
      -((HVertexOperator.coeff (twistedHalfHeisenbergField o i) k).comp (liftedTheta o)) := by
  apply LinearMap.ext
  intro v
  simp only [LinearMap.comp_apply, LinearMap.neg_apply,
    twistedHalfHeisenbergField_coefficient, theta_fieldCoefficient]

end HMT.IV.LatticeTwistedTensorField
end
