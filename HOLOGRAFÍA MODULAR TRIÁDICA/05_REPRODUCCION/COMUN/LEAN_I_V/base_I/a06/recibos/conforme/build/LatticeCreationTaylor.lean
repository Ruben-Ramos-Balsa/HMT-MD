import LatticeStateFieldTranslation

/-! Every created state has the formal Taylor coefficients forced by
the actual translation operator. The factorial is derived recursively
from covariance; no analytic exponential or vacuum series is supplied. -/

noncomputable section
namespace HMT.IV.LatticeCreationTaylor

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeStateFieldMap
open HMT.IV.LatticeStateFieldTranslation
local notation "T" => HMT.IV.LatticeTranslationOperator.translation

theorem creation_translation_recurrence (o : Fin 12) (u : LatticeCarrier o) (n : ℕ) :
    T o (HVertexOperator.coeff (stateField o u) (n : ℤ) (vacuum o)) =
      (n+1 : ℂ) • HVertexOperator.coeff (stateField o u) ((n+1 : ℕ) : ℤ) (vacuum o) := by
  have h := LinearMap.congr_fun (stateField_translation o u (n : ℤ)) (vacuum o)
  simpa only [LinearMap.sub_apply, Module.End.mul_apply,
    HMT.IV.LatticeTranslationOperator.translation_vacuum, map_zero,
    sub_zero, LinearMap.smul_apply, Nat.cast_add, Nat.cast_one,
    Int.cast_natCast] using h

theorem creation_factorial_coefficient (o : Fin 12) (u : LatticeCarrier o) (n : ℕ) :
    (n.factorial : ℂ) • HVertexOperator.coeff (stateField o u) (n : ℤ) (vacuum o) =
      ((T o)^n) u := by
  induction n with
  | zero => simpa using (stateField_creates o u).2
  | succ n ih =>
    calc
      _ = (n.factorial : ℂ) • ((n+1 : ℂ) •
          HVertexOperator.coeff (stateField o u) ((n+1 : ℕ) : ℤ) (vacuum o)) := by
            rw [smul_smul, Nat.factorial_succ, Nat.cast_mul]
            congr 1
            push_cast
            ring
      _ = (n.factorial : ℂ) •
          T o (HVertexOperator.coeff (stateField o u) (n : ℤ) (vacuum o)) := by
            rw [creation_translation_recurrence]
      _ = T o ((n.factorial : ℂ) •
          HVertexOperator.coeff (stateField o u) (n : ℤ) (vacuum o)) := by rw [map_smul]
      _ = ((T o)^(n+1)) u := by rw [ih, pow_succ', Module.End.mul_apply]

theorem creation_taylor_coefficient (o : Fin 12) (u : LatticeCarrier o) (n : ℕ) :
    HVertexOperator.coeff (stateField o u) (n : ℤ) (vacuum o) =
      (n.factorial : ℂ)⁻¹ • (((T o)^n) u) := by
  have hn : (n.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero n
  rw [← creation_factorial_coefficient, smul_smul, inv_mul_cancel₀ hn, one_smul]

end HMT.IV.LatticeCreationTaylor
end

#print axioms HMT.IV.LatticeCreationTaylor.creation_translation_recurrence
#print axioms HMT.IV.LatticeCreationTaylor.creation_factorial_coefficient
#print axioms HMT.IV.LatticeCreationTaylor.creation_taylor_coefficient
