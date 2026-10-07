import LatticeContractionFactor

/-!
Recurrence in the integral pairing of the constructed contraction factor.
This is the coefficient identity needed to multiply either expansion region
by the same polynomial z-w. It is deduced from the established recurrence,
not adopted as a locality axiom.
-/
noncomputable section
namespace HMT.IV.LatticeContractionPascal

open HMT.IV.LatticeExponentialContraction
open HMT.IV.LatticeContractionFactor

theorem contraction_pascal (p : ℤ) (n : ℕ) :
    scalarContraction (p+1) (n+1) =
      scalarContraction p (n+1) - scalarContraction p n := by
  induction n with
  | zero => simp [scalarContraction]; ring
  | succ n ih =>
    have h0 := scalarContraction_step (p+1) (n+1)
    have h1 := scalarContraction_step p (n+1)
    have h2 := scalarContraction_step p n
    rw [ih] at h0
    have hn : (n+2 : ℂ) ≠ 0 := by exact_mod_cast (by omega : n+2 ≠ 0)
    apply mul_left_cancel₀ hn
    push_cast at h0 h1 h2 ⊢
    linear_combination h0 - h1 + h2

theorem contraction_zero_pairing (n : ℕ) :
    scalarContraction 0 n = if n=0 then 1 else 0 := by
  cases n with
  | zero => simp
  | succ n =>
    rw [if_neg (by omega)]
    exact scalarContraction_nat_above 0 (n+1) (by omega)

end HMT.IV.LatticeContractionPascal
end

#print axioms HMT.IV.LatticeContractionPascal.contraction_pascal
#print axioms HMT.IV.LatticeContractionPascal.contraction_zero_pairing
