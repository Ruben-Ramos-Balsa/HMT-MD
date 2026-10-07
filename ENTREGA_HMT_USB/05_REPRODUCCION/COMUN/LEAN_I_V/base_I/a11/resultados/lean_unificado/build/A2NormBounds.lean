import Mathlib

namespace HMT.IV.CoxeterNeighbor

def a2IntNorm (a b : ℤ) : ℤ := a * a - a * b + b * b

theorem a2IntNorm_nonneg (a b : ℤ) : 0 ≤ a2IntNorm a b := by
  dsimp [a2IntNorm]
  nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg (a-b)]

theorem a2IntNorm_eq_zero_iff (a b : ℤ) :
    a2IntNorm a b = 0 ↔ a = 0 ∧ b = 0 := by
  constructor
  · intro h
    dsimp [a2IntNorm] at h
    have ha : a * a = 0 := by
      nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg (a-b)]
    have hb : b * b = 0 := by
      nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg (a-b)]
    exact ⟨mul_self_eq_zero.mp ha, mul_self_eq_zero.mp hb⟩
  · rintro ⟨rfl, rfl⟩
    rfl

theorem a2IntNorm_ge_one (a b : ℤ) (h : a ≠ 0 ∨ b ≠ 0) :
    1 ≤ a2IntNorm a b := by
  have hn := a2IntNorm_nonneg a b
  have hz : a2IntNorm a b ≠ 0 := by
    intro hz
    obtain ⟨ha, hb⟩ := (a2IntNorm_eq_zero_iff a b).mp hz
    aesop
  omega

theorem a2IntNorm_mod_three (a b : ℤ) :
    a2IntNorm a b % 3 = (a + b) ^ 2 % 3 := by
  have h : (a + b) ^ 2 = a2IntNorm a b + 3 * (a*b) := by
    dsimp [a2IntNorm]
    ring
  rw [h]
  omega

theorem a2IntNorm_ge_three (a b : ℤ)
    (h : a ≠ 0 ∨ b ≠ 0) (hd : 3 ∣ a+b) :
    3 ≤ a2IntNorm a b := by
  have hn := a2IntNorm_ge_one a b h
  have hm : a2IntNorm a b % 3 = 0 := by
    rw [a2IntNorm_mod_three]
    obtain ⟨k, hk⟩ := hd
    rw [hk]
    apply Int.emod_eq_zero_of_dvd
    exact ⟨3*k*k, by ring⟩
  omega

theorem a2IntNorm_one_sum_not_divisible (a b : ℤ)
    (h : a2IntNorm a b = 1) : ¬ 3 ∣ a+b := by
  intro hd
  have hn : a ≠ 0 ∨ b ≠ 0 := by
    by_contra hh
    push_neg at hh
    rcases hh with ⟨rfl, rfl⟩
    simp [a2IntNorm] at h
  have := a2IntNorm_ge_three a b hn hd
  omega

theorem a2IntNorm_sum_one_has_single_support {n : ℕ}
    (a b : Fin n → ℤ) (hs : ∑ i, a2IntNorm (a i) (b i) = 1) :
    ∃ j, a2IntNorm (a j) (b j) = 1 ∧
      ∀ i, i ≠ j → a i = 0 ∧ b i = 0 := by
  have hex : ∃ j, a2IntNorm (a j) (b j) ≠ 0 := by
    by_contra hn
    push_neg at hn
    have hz : ∑ i, a2IntNorm (a i) (b i) = 0 := by simp [hn]
    omega
  obtain ⟨j, hj⟩ := hex
  have hjle : a2IntNorm (a j) (b j) ≤ 1 := by
    rw [← hs]
    exact Finset.single_le_sum (fun i _ => a2IntNorm_nonneg (a i) (b i))
      (Finset.mem_univ j)
  have hjone : a2IntNorm (a j) (b j) = 1 := by
    have := a2IntNorm_nonneg (a j) (b j)
    omega
  refine ⟨j, hjone, ?_⟩
  intro i hij
  have he : ∑ k ∈ Finset.univ.erase j, a2IntNorm (a k) (b k) = 0 := by
    have hh := Finset.sum_erase_add Finset.univ
      (fun k => a2IntNorm (a k) (b k)) (Finset.mem_univ j)
    dsimp only at hh
    rw [hs, hjone] at hh
    omega
  have hile : a2IntNorm (a i) (b i) ≤ 0 := by
    rw [← he]
    exact Finset.single_le_sum (fun k _ => a2IntNorm_nonneg (a k) (b k))
      (Finset.mem_erase.mpr ⟨hij, Finset.mem_univ i⟩)
  apply (a2IntNorm_eq_zero_iff (a i) (b i)).mp
  have := a2IntNorm_nonneg (a i) (b i)
  omega

theorem integer_root_radial_pair_not_divisible {n : ℕ}
    (a b t : Fin n → ℤ) (hs : ∑ i, a2IntNorm (a i) (b i) = 1) :
    ¬ 3 ∣ ∑ i, (a i + b i) * (1 + 3 * t i) := by
  obtain ⟨j, hj, hrest⟩ := a2IntNorm_sum_one_has_single_support a b hs
  have hp : (∑ i, (a i + b i) * (1 + 3 * t i)) =
      (a j + b j) * (1 + 3 * t j) := by
    apply Finset.sum_eq_single j
    · intro i _ hij
      obtain ⟨ha, hb⟩ := hrest i hij
      simp [ha, hb]
    · simp
  rw [hp]
  intro hd
  have he : (a j + b j) * (1 + 3 * t j) =
      (a j + b j) + 3 * ((a j + b j) * t j) := by ring
  rw [he] at hd
  have hd' : 3 ∣ a j + b j := by
    obtain ⟨k, hk⟩ := hd
    refine ⟨k - (a j + b j) * t j, ?_⟩
    nlinarith [hk]
  exact a2IntNorm_one_sum_not_divisible (a j) (b j) hj hd'

#print axioms a2IntNorm_nonneg
#print axioms a2IntNorm_eq_zero_iff
#print axioms a2IntNorm_ge_one
#print axioms a2IntNorm_mod_three
#print axioms a2IntNorm_ge_three
#print axioms a2IntNorm_one_sum_not_divisible
#print axioms a2IntNorm_sum_one_has_single_support
#print axioms integer_root_radial_pair_not_divisible

end HMT.IV.CoxeterNeighbor
