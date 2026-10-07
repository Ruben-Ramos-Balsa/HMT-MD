import LatticeFieldLocality
import LatticeFieldBiOperators
import LatticeStateFieldMap

/-!
Uniqueness from genuine locality and the proved creation property of the
state-field map. Crossing powers preserve regularity in the second variable;
their constant coefficient extracts exactly a shifted first coefficient.
-/

noncomputable section
namespace HMT.IV.LatticeLocalFieldUniqueness

open LatticeFactorConvolution LatticeFieldLocality LatticeFieldBiOperators
open LatticeOscillatorFock LatticeStateFieldMap

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem crossing_pow_negative_second (f : BiStates V)
    (hf : ∀ k l : ℤ, l < 0 → f k l = 0) (N : ℕ) (k l : ℤ) (hl : l < 0) :
    (crossing^N) f k l = 0 := by
  induction N generalizing k l with
  | zero => exact hf k l hl
  | succ N ih =>
    rw [crossing_pow_succ_apply, ih (k-1) l hl, ih k (l-1) (by omega), sub_self]

theorem crossing_pow_constant_second (f : BiStates V)
    (hf : ∀ k l : ℤ, l < 0 → f k l = 0) (N : ℕ) (k : ℤ) :
    (crossing^N) f k 0 = f (k-(N : ℤ)) 0 := by
  induction N generalizing k with
  | zero => simp
  | succ N ih =>
    rw [crossing_pow_succ_apply, ih,
      crossing_pow_negative_second f hf N k (0-1) (by omega), sub_zero]
    congr 1
    omega

theorem local_field_coefficient_zero (o : Fin 12)
    (F : VertexOperator ℂ (LatticeCarrier o))
    (hlocal : ∀ v : LatticeCarrier o, Local F (stateField o v))
    (hvac : ∀ k : ℤ, HVertexOperator.coeff F k (vacuum o) = 0)
    (v : LatticeCarrier o) (k : ℤ) : HVertexOperator.coeff F k v = 0 := by
  obtain ⟨N,hN⟩ := hlocal v
  have hc := stateField_creates o v
  have hreg : ∀ a b : ℤ, b < 0 →
      forward F (stateField o v) a b (vacuum o) = 0 := by
    intro a b hb
    simp only [forward, Module.End.mul_apply, hc.1 b hb, map_zero]
  have hz : (fun a b => backward F (stateField o v) a b (vacuum o)) =
      (0 : BiStates (LatticeCarrier o)) := by
    funext a b
    simp only [backward, Module.End.mul_apply, hvac, map_zero, Pi.zero_apply]
  have he := LinearMap.congr_fun (congrFun (congrFun hN (k+(N : ℤ))) 0) (vacuum o)
  rw [crossing_pow_apply, crossing_pow_apply, hz, map_zero] at he
  rw [crossing_pow_constant_second _ hreg] at he
  simpa only [add_sub_cancel_right, forward, Module.End.mul_apply, hc.2,
    Pi.zero_apply] using he

theorem local_field_zero (o : Fin 12)
    (F : VertexOperator ℂ (LatticeCarrier o))
    (hlocal : ∀ v : LatticeCarrier o, Local F (stateField o v))
    (hvac : ∀ k : ℤ, HVertexOperator.coeff F k (vacuum o) = 0) : F = 0 := by
  apply LinearMap.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  exact local_field_coefficient_zero o F hlocal hvac v k

end HMT.IV.LatticeLocalFieldUniqueness
end

#print axioms HMT.IV.LatticeLocalFieldUniqueness.crossing_pow_negative_second
#print axioms HMT.IV.LatticeLocalFieldUniqueness.crossing_pow_constant_second
#print axioms HMT.IV.LatticeLocalFieldUniqueness.local_field_coefficient_zero
#print axioms HMT.IV.LatticeLocalFieldUniqueness.local_field_zero
