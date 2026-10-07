import MassCharacter
import TowerHeights

noncomputable section

namespace HMTMassCharacter

def evenMoment (p q : ℝ) (n : ℕ) := q ^ n + p ^ n
def orientedMoment (p q : ℝ) (n : ℕ) := q ^ n - p ^ n

theorem moment_norm (p q : ℝ) (n : ℕ) :
    evenMoment p q n ^ 2 - orientedMoment p q n ^ 2 = 4 * (p * q) ^ n := by
  simp only [evenMoment, orientedMoment, mul_pow]
  ring

theorem evenMoment_add (p q : ℝ) (m n : ℕ) :
    evenMoment p q (m + n) =
      (evenMoment p q m * evenMoment p q n + orientedMoment p q m * orientedMoment p q n) / 2 := by
  simp only [evenMoment, orientedMoment, pow_add]
  ring

theorem orientedMoment_add (p q : ℝ) (m n : ℕ) :
    orientedMoment p q (m + n) =
      (orientedMoment p q m * evenMoment p q n + evenMoment p q m * orientedMoment p q n) / 2 := by
  simp only [evenMoment, orientedMoment, pow_add]
  ring

theorem evenMoment_recurrence (p q : ℝ) (n : ℕ) :
    evenMoment p q (n + 2) =
      evenMoment p q 1 * evenMoment p q (n + 1) - (p * q) * evenMoment p q n := by
  simp only [evenMoment, pow_one, pow_succ]
  ring

theorem orientedMoment_recurrence (p q : ℝ) (n : ℕ) :
    orientedMoment p q (n + 2) =
      evenMoment p q 1 * orientedMoment p q (n + 1) - (p * q) * orientedMoment p q n := by
  simp only [evenMoment, orientedMoment, pow_one, pow_succ]
  ring

def qPlus (x y : ℝ) := Real.exp (-x - y)
def qMinus (x y : ℝ) := Real.exp (-x + y)

theorem channel_chamber {x y : ℝ} (hy : 0 < y) (hxy : y < x) :
    0 < qPlus x y ∧ qPlus x y < qMinus x y ∧ qMinus x y < 1 := by
  refine ⟨Real.exp_pos _, Real.exp_lt_exp.mpr (by linarith), ?_⟩
  exact Real.exp_lt_one_iff.mpr (by linarith)

theorem channel_product (x y : ℝ) : qPlus x y * qMinus x y = Real.exp (-2 * x) := by
  rw [qPlus, qMinus, ← Real.exp_add]
  congr 1
  ring

theorem source_norm_identity (x y : ℝ) (n : ℕ) :
    evenMoment (qPlus x y) (qMinus x y) n ^ 2 -
      orientedMoment (qPlus x y) (qMinus x y) n ^ 2 =
      4 * Real.exp (-2 * (n : ℝ) * x) := by
  rw [moment_norm, channel_product, ← Real.exp_nat_mul]
  congr 2
  ring

theorem orientedMoment_pos {p q : ℝ} (hp : 0 ≤ p) (hpq : p < q)
    {n : ℕ} (hn : 0 < n) : 0 < orientedMoment p q n := by
  exact sub_pos.mpr (pow_lt_pow_left₀ hpq hp (Nat.ne_of_gt hn))

#print axioms moment_norm
#print axioms evenMoment_add
#print axioms orientedMoment_add
#print axioms evenMoment_recurrence
#print axioms orientedMoment_recurrence
#print axioms channel_chamber
#print axioms source_norm_identity

end HMTMassCharacter
