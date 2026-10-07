import Mathlib.Tactic

/-! The positive (nonempty-word) height semigroup of Article VI. -/

namespace HMTMassCharacter

def SmallHeight (n : ℕ) : Prop := ∃ a b : ℕ, 0 < a + b ∧ n = 3 * a + 4 * b

theorem smallHeight_of_ge_six : ∀ n : ℕ, 6 ≤ n → SmallHeight n := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro hn
    by_cases h9 : n < 9
    · have hcases : n = 6 ∨ n = 7 ∨ n = 8 := by omega
      rcases hcases with rfl | rfl | rfl
      · exact ⟨2, 0, by omega, by omega⟩
      · exact ⟨1, 1, by omega, by omega⟩
      · exact ⟨0, 2, by omega, by omega⟩
    · obtain ⟨a, b, hab, he⟩ := ih (n - 3) (by omega) (by omega)
      exact ⟨a + 1, b, by omega, by omega⟩

theorem smallHeight_iff (n : ℕ) : SmallHeight n ↔ n = 3 ∨ n = 4 ∨ 6 ≤ n := by
  constructor
  · rintro ⟨a, b, hab, rfl⟩
    omega
  · rintro (rfl | rfl | hn)
    · exact ⟨1, 0, by omega, by omega⟩
    · exact ⟨0, 1, by omega, by omega⟩
    · exact smallHeight_of_ge_six n hn

def IsHeight (n : ℕ) : Prop := ∃ a b : ℕ, 0 < a + b ∧ n = 90 * a + 120 * b

theorem isHeight_iff (n : ℕ) :
    IsHeight n ↔ n = 90 ∨ n = 120 ∨ ∃ r : ℕ, 6 ≤ r ∧ n = 30 * r := by
  constructor
  · rintro ⟨a, b, hab, hn⟩
    have hs : SmallHeight (3 * a + 4 * b) := ⟨a, b, hab, rfl⟩
    rcases (smallHeight_iff _).mp hs with h3 | h4 | h6
    · left; omega
    · right; left; omega
    · right; right
      exact ⟨3 * a + 4 * b, h6, by omega⟩
  · rintro (rfl | rfl | ⟨r, hr, rfl⟩)
    · exact ⟨1, 0, by omega, by omega⟩
    · exact ⟨0, 1, by omega, by omega⟩
    · obtain ⟨a, b, hab, he⟩ := smallHeight_of_ge_six r hr
      exact ⟨a, b, hab, by omega⟩

theorem height_add {m n : ℕ} (hm : IsHeight m) (hn : IsHeight n) : IsHeight (m + n) := by
  obtain ⟨a, b, hab, rfl⟩ := hm
  obtain ⟨c, d, hcd, rfl⟩ := hn
  exact ⟨a + c, b + d, by omega, by omega⟩

theorem height_positive {n : ℕ} (hn : IsHeight n) : 0 < n := by
  obtain ⟨a, b, hab, rfl⟩ := hn
  omega

abbrev Height := {n : ℕ // IsHeight n}

def genealogyValue (word : List Bool) : ℕ :=
  (word.map fun x => if x then 90 else 120).sum

theorem genealogy_concat (u v : List Bool) :
    genealogyValue (u ++ v) = genealogyValue u + genealogyValue v := by
  simp [genealogyValue]

theorem two_distinct_genealogies_at_360 :
    (List.replicate 4 true) ≠ List.replicate 3 false ∧
      genealogyValue (List.replicate 4 true) = 360 ∧
      genealogyValue (List.replicate 3 false) = 360 := by
  decide

#print axioms isHeight_iff
#print axioms height_add
#print axioms height_positive
#print axioms two_distinct_genealogies_at_360

end HMTMassCharacter
