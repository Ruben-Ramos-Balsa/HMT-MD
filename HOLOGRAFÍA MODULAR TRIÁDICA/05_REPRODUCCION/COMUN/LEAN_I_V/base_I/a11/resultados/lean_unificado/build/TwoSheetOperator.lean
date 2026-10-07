import ContractiveChannels

/-!
Algebraic operator bridge for `iii:eq:vacuum-op` and `iii:eq:completion-response`.
The ambient real algebra need not commute. Complementary orthogonal
idempotents are the explicit interface; neither powers nor inverses nor the
response identity are fields of that interface. No TPK realization is asserted.
-/
namespace HMT.III.Constitutive
noncomputable section

variable {A : Type*} [Ring A] [Algebra ℝ A]

structure TwoSheetProjectors (A : Type*) [Ring A] [Algebra ℝ A] where
  plus : A
  minus : A
  plus_idempotent : plus * plus = plus
  minus_idempotent : minus * minus = minus
  plus_minus : plus * minus = 0
  minus_plus : minus * plus = 0
  complete : plus + minus = 1

namespace TwoSheetProjectors

def diagonal (P : TwoSheetProjectors A) (x y : ℝ) : A := x • P.plus + y • P.minus

theorem diagonal_one (P : TwoSheetProjectors A) : P.diagonal 1 1 = 1 := by
  simpa only [diagonal, one_smul] using P.complete

theorem diagonal_add (P : TwoSheetProjectors A) (x y z w : ℝ) :
    P.diagonal x y + P.diagonal z w = P.diagonal (x + z) (y + w) := by
  simp only [diagonal, add_smul]
  abel

theorem diagonal_sub (P : TwoSheetProjectors A) (x y z w : ℝ) :
    P.diagonal x y - P.diagonal z w = P.diagonal (x - z) (y - w) := by
  simp only [diagonal, sub_smul]
  abel

theorem diagonal_mul (P : TwoSheetProjectors A) (x y z w : ℝ) :
    P.diagonal x y * P.diagonal z w = P.diagonal (x * z) (y * w) := by
  simp only [diagonal, add_mul, mul_add, Algebra.smul_mul_assoc,
    Algebra.mul_smul_comm, smul_smul, P.plus_idempotent, P.minus_idempotent,
    P.plus_minus, P.minus_plus, smul_zero, zero_add, add_zero]
  rw [mul_comm z x, mul_comm w y]

theorem diagonal_pow (P : TwoSheetProjectors A) (x y : ℝ) (n : ℕ) :
    P.diagonal x y ^ n = P.diagonal (x ^ n) (y ^ n) := by
  induction n with
  | zero => simpa using P.diagonal_one.symm
  | succ n ih => rw [pow_succ, ih, P.diagonal_mul, pow_succ, pow_succ]

def transport (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) : A :=
  P.diagonal qPlus qMinus

theorem transport_pow (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) (n : ℕ) :
    P.transport qPlus qMinus ^ n = qPlus ^ n • P.plus + qMinus ^ n • P.minus :=
  P.diagonal_pow qPlus qMinus n

theorem one_sub_transport_pow (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) (n : ℕ) :
    1 - P.transport qPlus qMinus ^ n =
      P.diagonal (1 - qPlus ^ n) (1 - qMinus ^ n) := by
  change 1 - P.diagonal qPlus qMinus ^ n = _
  rw [P.diagonal_pow, ← P.diagonal_one, P.diagonal_sub]

def denominatorInverse (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) : A :=
  P.diagonal (1 / (1 - qPlus ^ 120)) (1 / (1 - qMinus ^ 120))

theorem denominator_inverse_right (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    (1 - P.transport qPlus qMinus ^ 120) * P.denominatorInverse qPlus qMinus = 1 := by
  have hp0 := ne_of_gt (channel_denominator_pos hp)
  have hm0 := ne_of_gt (channel_denominator_pos hm)
  rw [P.one_sub_transport_pow, denominatorInverse, P.diagonal_mul]
  simpa only [one_div, mul_inv_cancel₀ hp0, mul_inv_cancel₀ hm0] using P.diagonal_one

theorem denominator_inverse_left (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    P.denominatorInverse qPlus qMinus * (1 - P.transport qPlus qMinus ^ 120) = 1 := by
  have hp0 := ne_of_gt (channel_denominator_pos hp)
  have hm0 := ne_of_gt (channel_denominator_pos hm)
  rw [P.one_sub_transport_pow, denominatorInverse, P.diagonal_mul]
  simpa only [one_div, inv_mul_cancel₀ hp0, inv_mul_cancel₀ hm0] using P.diagonal_one

-- A genuine unit packages the two proved inverse identities.
def denominatorUnit (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) : Aˣ where
  val := 1 - P.transport qPlus qMinus ^ 120
  inv := P.denominatorInverse qPlus qMinus
  val_inv := P.denominator_inverse_right hp hm
  inv_val := P.denominator_inverse_left hp hm

def vacuum (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) : A :=
  (1 - P.transport qPlus qMinus ^ 90) * P.denominatorInverse qPlus qMinus

theorem vacuum_uses_unit_inverse (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    P.vacuum qPlus qMinus =
      (1 - P.transport qPlus qMinus ^ 90) * ((P.denominatorUnit hp hm)⁻¹ : Aˣ) := rfl

theorem vacuum_decomposition (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) :
    P.vacuum qPlus qMinus =
      channelResponse qPlus • P.plus + channelResponse qMinus • P.minus := by
  rw [vacuum, P.one_sub_transport_pow, denominatorInverse, P.diagonal_mul]
  simp only [diagonal, channelResponse, div_eq_mul_inv, one_mul]

theorem vacuum_response (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    P.vacuum qPlus qMinus = P.diagonal (response (qPlus ^ 30)) (response (qMinus ^ 30)) := by
  rw [P.vacuum_decomposition, channelResponse_eq hp, channelResponse_eq hm]
  rfl

def sigma3 (S : A) : A := 1 + S + S ^ 2
def sigma4 (S : A) : A := 1 + S + S ^ 2 + S ^ 3

theorem sigma3_diagonal (P : TwoSheetProjectors A) (s t : ℝ) :
    sigma3 (P.diagonal s t) = P.diagonal (numerator s) (numerator t) := by
  rw [sigma3, P.diagonal_pow, ← P.diagonal_one, P.diagonal_add, P.diagonal_add]
  rfl

theorem sigma4_diagonal (P : TwoSheetProjectors A) (s t : ℝ) :
    sigma4 (P.diagonal s t) = P.diagonal (denominator s) (denominator t) := by
  change sigma3 (P.diagonal s t) + P.diagonal s t ^ 3 = _
  rw [P.sigma3_diagonal, P.diagonal_pow, P.diagonal_add]
  rfl

def completionInverse (P : TwoSheetProjectors A) (qPlus qMinus : ℝ) : A :=
  P.diagonal (1 / denominator (qPlus ^ 30)) (1 / denominator (qMinus ^ 30))

theorem completion_inverse_right (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    sigma4 (P.transport qPlus qMinus ^ 30) * P.completionInverse qPlus qMinus = 1 := by
  have hp0 := ne_of_gt (denominator_pos (channel_power_mem hp).1.le)
  have hm0 := ne_of_gt (denominator_pos (channel_power_mem hm).1.le)
  rw [transport, P.diagonal_pow, P.sigma4_diagonal, completionInverse, P.diagonal_mul]
  simpa only [one_div, mul_inv_cancel₀ hp0, mul_inv_cancel₀ hm0] using P.diagonal_one

theorem completion_inverse_left (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    P.completionInverse qPlus qMinus * sigma4 (P.transport qPlus qMinus ^ 30) = 1 := by
  have hp0 := ne_of_gt (denominator_pos (channel_power_mem hp).1.le)
  have hm0 := ne_of_gt (denominator_pos (channel_power_mem hm).1.le)
  rw [transport, P.diagonal_pow, P.sigma4_diagonal, completionInverse, P.diagonal_mul]
  simpa only [one_div, inv_mul_cancel₀ hp0, inv_mul_cancel₀ hm0] using P.diagonal_one

theorem completion_equation (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    P.vacuum qPlus qMinus * sigma4 (P.transport qPlus qMinus ^ 30) =
      sigma3 (P.transport qPlus qMinus ^ 30) := by
  have hp0 := ne_of_gt (denominator_pos (channel_power_mem hp).1.le)
  have hm0 := ne_of_gt (denominator_pos (channel_power_mem hm).1.le)
  rw [P.vacuum_response hp hm, transport, P.diagonal_pow,
    P.sigma4_diagonal, P.sigma3_diagonal, P.diagonal_mul]
  simp only [response, div_mul_cancel₀ _ hp0, div_mul_cancel₀ _ hm0]

theorem completion_formula (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    P.vacuum qPlus qMinus = sigma3 (P.transport qPlus qMinus ^ 30) *
      P.completionInverse qPlus qMinus := by
  calc
    _ = P.vacuum qPlus qMinus * (sigma4 (P.transport qPlus qMinus ^ 30) *
        P.completionInverse qPlus qMinus) := by rw [P.completion_inverse_right hp hm, mul_one]
    _ = (P.vacuum qPlus qMinus * sigma4 (P.transport qPlus qMinus ^ 30)) *
        P.completionInverse qPlus qMinus := (mul_assoc _ _ _).symm
    _ = _ := by rw [P.completion_equation hp hm]

-- Uniqueness holds among every element of the ambient algebra, not only diagonals.
theorem completion_unique (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) {W : A}
    (hW : W * sigma4 (P.transport qPlus qMinus ^ 30) =
      sigma3 (P.transport qPlus qMinus ^ 30)) : W = P.vacuum qPlus qMinus := by
  calc
    W = W * (sigma4 (P.transport qPlus qMinus ^ 30) *
        P.completionInverse qPlus qMinus) := by rw [P.completion_inverse_right hp hm, mul_one]
    _ = (W * sigma4 (P.transport qPlus qMinus ^ 30)) *
        P.completionInverse qPlus qMinus := (mul_assoc _ _ _).symm
    _ = (P.vacuum qPlus qMinus * sigma4 (P.transport qPlus qMinus ^ 30)) *
        P.completionInverse qPlus qMinus := by rw [hW, P.completion_equation hp hm]
    _ = P.vacuum qPlus qMinus := by rw [mul_assoc, P.completion_inverse_right hp hm, mul_one]

theorem completion_exists_unique (P : TwoSheetProjectors A) {qPlus qMinus : ℝ}
    (hp : qPlus ∈ Set.Ioo 0 1) (hm : qMinus ∈ Set.Ioo 0 1) :
    ∃! W : A, W * sigma4 (P.transport qPlus qMinus ^ 30) =
      sigma3 (P.transport qPlus qMinus ^ 30) :=
  ⟨P.vacuum qPlus qMinus, P.completion_equation hp hm, fun _ hW => P.completion_unique hp hm hW⟩

end TwoSheetProjectors

#print axioms TwoSheetProjectors.transport_pow
#print axioms TwoSheetProjectors.denominator_inverse_right
#print axioms TwoSheetProjectors.denominator_inverse_left
#print axioms TwoSheetProjectors.denominatorUnit
#print axioms TwoSheetProjectors.vacuum_decomposition
#print axioms TwoSheetProjectors.completion_inverse_right
#print axioms TwoSheetProjectors.completion_inverse_left
#print axioms TwoSheetProjectors.completion_equation
#print axioms TwoSheetProjectors.completion_formula
#print axioms TwoSheetProjectors.completion_exists_unique

end
end HMT.III.Constitutive
