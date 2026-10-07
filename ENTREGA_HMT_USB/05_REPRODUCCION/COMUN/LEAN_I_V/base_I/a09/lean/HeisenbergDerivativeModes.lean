import LatticeHeisenbergField
import Mathlib.RingTheory.Binomial

/-!
# Divided derivatives of the constructed Heisenberg fields

The coefficients are the generalized binomial coefficients of the actual
Laurent field, not a new family of oscillator operators.  All lattice and
oscillator inputs are inherited unchanged from the selected construction.
The split into creation and nonnegative Heisenberg modes is proved, together
with the vacuum state and the pointwise truncation needed by normal products.
No state-field reconstruction, Jacobi or orbifold assertion is assumed.
-/

noncomputable section
namespace HMT.IV.HeisenbergDerivativeModes

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeHeisenbergField
open HMT.IV.LatticeFieldTruncation

set_option synthInstance.maxHeartbeats 200000

/-- Coefficient of `z^k` in `1/n! * d^n H(z)/dz^n`. -/
def derivativeCoefficient (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) : Module.End ℂ (LatticeCarrier o) :=
  Ring.choose ((k : ℂ) + (n : ℂ)) n •
    LatticeHeisenbergField.fieldCoefficient o i (k + n)

/-- The binomial coefficient is exactly the falling-factorial coefficient
divided by `n!`; this fixes the normalization at every Laurent exponent. -/
theorem derivativeCoefficient_factorial (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) :
    (n.factorial : ℂ) • derivativeCoefficient o i n k =
      (descPochhammer ℤ n).smeval ((k : ℂ) + n) •
        LatticeHeisenbergField.fieldCoefficient o i (k+n) := by
  rw [Ring.descPochhammer_eq_factorial_smul_choose]
  simp only [derivativeCoefficient, nsmul_eq_mul, smul_smul]

theorem derivativeCoefficient_bounded_pole (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) (v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, derivativeCoefficient o i n k v = 0 := by
  obtain ⟨b, hb⟩ := fieldCoefficient_bounded_pole o i v
  refine ⟨b-n, ?_⟩
  intro k hk
  have hkn : k+(n : ℤ) < b := by omega
  simp only [derivativeCoefficient, LinearMap.smul_apply, hb _ hkn, smul_zero]

def derivativeField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    VertexOperator ℂ (LatticeCarrier o) :=
  VertexOperator.of_coeff (derivativeCoefficient o i n)
    (derivativeCoefficient_bounded_pole o i n)

theorem derivativeField_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (v : LatticeCarrier o) (k : ℤ) :
    ((HahnModule.of ℂ).symm (derivativeField o i n v)).coeff k =
      derivativeCoefficient o i n k v := rfl

theorem derivativeCoefficient_zero (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    derivativeCoefficient o i 0 k = LatticeHeisenbergField.fieldCoefficient o i k := by
  simp [derivativeCoefficient, Ring.choose_zero_right]

/-- The creation part has nonnegative Laurent exponents. -/
theorem derivativeCoefficient_creation (o : Fin 12) (i : Fin (BasisSize o))
    (n r : ℕ) :
    derivativeCoefficient o i n (r : ℤ) =
      ((r+n).choose n : ℂ) • onCarrier o (create o (r+n) i) := by
  have hs : ((r : ℤ) : ℂ) + (n : ℂ) = ((r+n : ℕ) : ℂ) := by push_cast; rfl
  have hm : -((r : ℤ)+(n : ℤ))-1 = Int.negSucc (r+n) := by omega
  simp only [derivativeCoefficient, hs, Ring.choose_natCast,
    LatticeHeisenbergField.fieldCoefficient, hm, hmode_negSucc]

/-- Between the creation part and the shifted zero mode, the divided
derivative coefficients vanish by the binomial factor itself. -/
theorem derivativeCoefficient_gap (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) (hk : k < 0) (hkn : -(n : ℤ) ≤ k) :
    derivativeCoefficient o i n k = 0 := by
  have hn : (k+(n : ℤ)).toNat < n := by omega
  have hc : (k : ℂ) + (n : ℂ) = (((k+(n : ℤ)).toNat : ℕ) : ℂ) := by
    have hz : (((k+(n : ℤ)).toNat : ℕ) : ℤ) = k+(n : ℤ) :=
      Int.toNat_of_nonneg (by omega)
    have h := congrArg (fun z : ℤ => (z : ℂ)) hz
    push_cast at h
    exact h.symm
  simp only [derivativeCoefficient, hc, Ring.choose_natCast,
    Nat.choose_eq_zero_of_lt hn, Nat.cast_zero, zero_smul]

/-- Negative Laurent exponents that survive correspond exactly to the
nonnegative Heisenberg modes, with their differentiated binomial coefficient. -/
theorem derivativeCoefficient_nonnegativeMode (o : Fin 12)
    (i : Fin (BasisSize o)) (n m : ℕ) :
    derivativeCoefficient o i n (-(m : ℤ)-(n : ℤ)-1) =
      ((-1 : ℂ)^n * ((m+n).choose n : ℂ)) • hmode o i (m : ℤ) := by
  have hs : (((-(m : ℤ)-(n : ℤ)-1 : ℤ) : ℂ)+(n : ℂ)) = -((m : ℂ)+1) := by
    push_cast; ring
  have hm : -(-(m : ℤ)-(n : ℤ)-1+(n : ℤ))-1 = m := by omega
  have hc : (m : ℂ)+1+(n : ℂ)-1 = ((m+n : ℕ) : ℂ) := by push_cast; ring
  simp only [derivativeCoefficient, hs, Ring.choose_neg, hc,
    Ring.choose_natCast, LatticeHeisenbergField.fieldCoefficient, hm]
  congr 1
  simp only [Units.smul_def, zsmul_eq_mul, Int.cast_negOnePow_natCast]

theorem derivativeCoefficient_vacuum_negative (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) (k : ℤ) (hk : k < 0) :
    derivativeCoefficient o i n k (vacuum o) = 0 := by
  by_cases hkn : -(n : ℤ) ≤ k
  · rw [derivativeCoefficient_gap o i n k hk hkn]
    rfl
  · let m := (-k-(n : ℤ)-1).toNat
    have hm : k = -(m : ℤ)-(n : ℤ)-1 := by dsimp [m]; omega
    rw [hm, derivativeCoefficient_nonnegativeMode]
    simp only [LinearMap.smul_apply]
    have hv := heisenbergField_vacuum_annihilation o i m
    rw [heisenbergField_ncoeff] at hv
    rw [hv, smul_zero]

theorem derivativeCoefficient_vacuum_constant (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) :
    derivativeCoefficient o i n 0 (vacuum o) =
      onCarrier o (create o n i) (vacuum o) := by
  simpa using congrArg (fun f : Module.End ℂ (LatticeCarrier o) => f (vacuum o))
    (derivativeCoefficient_creation o i n 0)

/-- A bound inherited directly from algebraic Fock finite support, uniform
in the derivative order and lattice-basis index when indexed by original mode. -/
theorem exists_nonnegativeMode_bound (o : Fin 12) (v : LatticeCarrier o) :
    ∃ N : ℕ, ∀ m ≥ N, ∀ n : ℕ, ∀ i : Fin (BasisSize o),
      derivativeCoefficient o i n (-(m : ℤ)-(n : ℤ)-1) v = 0 := by
  obtain ⟨N, hN⟩ := exists_carrier_annihilation_bound o v
  refine ⟨N+1, ?_⟩
  intro m hm n i
  obtain ⟨a, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : m ≠ 0)
  rw [derivativeCoefficient_nonnegativeMode, hmode_castSucc]
  simp only [LinearMap.smul_apply, hN a (by omega) i, smul_zero]

/-- Creation and nonnegative-mode parts at fixed Laurent exponent. -/
def creationPart (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) (k : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  if 0 ≤ k then derivativeCoefficient o i n k else 0

def nonnegativePart (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) (k : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  if k < 0 then derivativeCoefficient o i n k else 0

theorem derivativeCoefficient_split (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) :
    derivativeCoefficient o i n k = creationPart o i n k + nonnegativePart o i n k := by
  unfold creationPart nonnegativePart
  split_ifs <;> simp_all
  omega

theorem creationPart_negative (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) (hk : k < 0) : creationPart o i n k = 0 := by
  simp [creationPart, not_le.mpr hk]

theorem nonnegativePart_nonnegative (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) (hk : 0 ≤ k) : nonnegativePart o i n k = 0 := by
  simp [nonnegativePart, not_lt.mpr hk]

theorem nonnegativePart_bounded_pole (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, nonnegativePart o i n k v = 0 := by
  obtain ⟨b, hb⟩ := derivativeCoefficient_bounded_pole o i n v
  refine ⟨b, ?_⟩
  intro k hk
  unfold nonnegativePart
  split_ifs
  · exact hb k hk
  · rfl

theorem nonnegativePart_vacuum (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) : nonnegativePart o i n k (vacuum o) = 0 := by
  unfold nonnegativePart
  split_ifs with hk
  · exact derivativeCoefficient_vacuum_negative o i n k hk
  · rfl

end HMT.IV.HeisenbergDerivativeModes
end

#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_factorial
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_bounded_pole
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_creation
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_gap
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_nonnegativeMode
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_vacuum_negative
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_vacuum_constant
#print axioms HMT.IV.HeisenbergDerivativeModes.exists_nonnegativeMode_bound
#print axioms HMT.IV.HeisenbergDerivativeModes.derivativeCoefficient_split
#print axioms HMT.IV.HeisenbergDerivativeModes.nonnegativePart_vacuum
