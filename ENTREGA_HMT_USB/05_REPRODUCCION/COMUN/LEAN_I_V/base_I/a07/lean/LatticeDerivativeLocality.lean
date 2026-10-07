import LatticeFieldDerivative
import LatticeFieldLocality

/-! Locality is preserved by differentiation of a Laurent field. The
additional order is obtained from the actual crossing/derivative
commutator, with no assumption about the derivative field's locality. -/

noncomputable section
namespace HMT.IV.LatticeDerivativeLocality

open HMT.IV.LatticeFieldDerivative HMT.IV.LatticeFieldLocality
open HMT.IV.LatticeFactorConvolution
variable {V : Type*} [AddCommGroup V] [Module ℂ V]

def firstDerivative : Module.End ℂ (BiStates V) where
  toFun F := fun k l => ((k : ℂ)+1) • F (k+1) l
  map_add' F G := by funext k l; simp [smul_add]
  map_smul' c F := by funext k l; simp only [Pi.smul_apply]; exact smul_comm _ _ _

theorem derivative_crossing (F : BiStates V) :
    firstDerivative (crossing F) = F + crossing (firstDerivative F) := by
  funext k l
  change ((k : ℂ)+1) • (F (k+1-1) l - F (k+1) (l-1)) =
    F k l + (((k-1 : ℤ)+1 : ℂ) • F (k-1+1) l -
      ((k : ℂ)+1) • F (k+1) (l-1))
  simp only [add_sub_cancel_right, sub_add_cancel]
  push_cast
  module

theorem crossing_derivative (F : BiStates V) :
    crossing (firstDerivative F) = firstDerivative (crossing F) - F := by
  rw [derivative_crossing]
  abel

theorem crossing_pow_derivative (F : BiStates V) (n : ℕ) :
    (crossing^(n+1)) (firstDerivative F) =
      firstDerivative ((crossing^(n+1)) F) -
        (n+1 : ℂ) • ((crossing^n) F) := by
  induction n with
  | zero => simpa only [zero_add, pow_one, pow_zero, Module.End.one_apply,
      Nat.cast_zero, one_smul] using crossing_derivative F
  | succ n ih =>
    rw [show n+1+1 = (n+1)+1 by rfl, pow_succ', Module.End.mul_apply,
      ih, map_sub, map_smul, crossing_derivative]
    have hstep (j : ℕ) : crossing ((crossing^j) F) = (crossing^(j+1)) F := by
      rw [pow_succ', Module.End.mul_apply]
    rw [hstep (n+1), hstep n]
    rw [← pow_succ']
    push_cast
    module

theorem derivative_annihilated (F : BiStates V) (n : ℕ)
    (h : (crossing^n) F = 0) : (crossing^(n+1)) (firstDerivative F) = 0 := by
  rw [crossing_pow_derivative]
  have hs : (crossing^(n+1)) F = 0 := by
    rw [pow_succ', Module.End.mul_apply, h, map_zero]
  rw [hs, map_zero, h, smul_zero, sub_self]

theorem derivative_localAt {N : ℕ} {A B : VertexOperator ℂ V}
    (h : LocalAt N A B) : LocalAt (N+1) (derivativeField A) B := by
  have hz : (crossing^N) (forward A B - backward A B) = 0 := by
    rw [map_sub]
    exact sub_eq_zero.mpr h
  have hd : forward (derivativeField A) B - backward (derivativeField A) B =
      firstDerivative (forward A B - backward A B) := by
    funext k l
    simp only [Pi.sub_apply, forward, backward, derivativeField_coefficient,
      smul_mul_assoc, mul_smul_comm]
    simp only [firstDerivative, LinearMap.coe_mk, AddHom.coe_mk, Pi.sub_apply,
      forward, backward, smul_sub]
  apply sub_eq_zero.mp
  rw [← map_sub, hd]
  exact derivative_annihilated _ N hz

theorem derivative_local {A B : VertexOperator ℂ V} (h : Local A B) :
    Local (derivativeField A) B := by
  obtain ⟨N,hN⟩ := h
  exact ⟨N+1, derivative_localAt hN⟩

end HMT.IV.LatticeDerivativeLocality
end

#print axioms HMT.IV.LatticeDerivativeLocality.derivative_crossing
#print axioms HMT.IV.LatticeDerivativeLocality.crossing_pow_derivative
#print axioms HMT.IV.LatticeDerivativeLocality.derivative_annihilated
#print axioms HMT.IV.LatticeDerivativeLocality.derivative_localAt
#print axioms HMT.IV.LatticeDerivativeLocality.derivative_local
