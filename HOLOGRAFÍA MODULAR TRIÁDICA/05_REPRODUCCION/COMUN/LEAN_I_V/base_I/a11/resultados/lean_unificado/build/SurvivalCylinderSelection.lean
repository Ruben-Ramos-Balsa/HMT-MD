import RegionalCylinderTransition
import Mathlib.Algebra.Order.Archimedean.Basic

/-!
Survival against every generated decimal cylinder selects the unique regional
ternary prefix. Compatibility is the existing pair of strict integer overlap
inequalities. It is not defined by equality to the selected prefix.

The result concerns the cylinder component. No preservation property of the
complete enriched TPK transition is assumed or claimed here.
-/

noncomputable section
namespace HMT.I.SurvivalCylinderSelection

open HMT.I.RegionalPublicationComposition HMT.I.RegionalCylinderTransition

def SurvivesAllDecimals (c : Channel) (n N : Nat) : Prop :=
  ∀ k : Nat, Compatible ⟨n, k, N, publish c 1000 (by decide) k⟩

private theorem nonpositive_of_scaled_bounds (x B : ℝ)
    (h : ∀ k : Nat, x * (1000 : ℝ)^k < B) : x ≤ 0 := by
  by_contra hx
  have hp : 0 < x := lt_of_not_ge hx
  obtain ⟨k, _, hk⟩ := exists_nat_pow_near (le_max_left 1 (B / x))
    (show (1 : ℝ) < 1000 by norm_num)
  have hq : B / x < (1000 : ℝ)^(k + 1) :=
    lt_of_le_of_lt (le_max_right 1 (B / x)) hk
  have hb : B < x * (1000 : ℝ)^(k + 1) := by
    have := (div_lt_iff₀ hp).mp hq
    nlinarith only [this]
  exact (not_lt_of_ge hb.le) (h (k + 1))

private theorem decimal_publication_bounds (c : Channel) (k : Nat) :
    (publish c 1000 (by decide) k : ℝ) ≤ value c * (1000 : ℝ)^k ∧
    value c * (1000 : ℝ)^k < (publish c 1000 (by decide) k : ℝ) + 1 := by
  rw [publish_eq_prefix]
  unfold RadixCellSelection.positionalPrefix
  exact ⟨Nat.floor_le (mul_nonneg (value_nonnegative c) (by positivity)),
    Nat.lt_floor_add_one _⟩

theorem survival_closed_bounds (c : Channel) (n N : Nat)
    (h : SurvivesAllDecimals c n N) :
    (N : ℝ) ≤ value c * (729 : ℝ)^n ∧
    value c * (729 : ℝ)^n ≤ (N : ℝ) + 1 := by
  have hscaled (k : Nat) :
      ((N : ℝ) - value c * (729 : ℝ)^n) * (1000 : ℝ)^k < (729 : ℝ)^n ∧
      (value c * (729 : ℝ)^n - ((N : ℝ) + 1)) * (1000 : ℝ)^k < (729 : ℝ)^n := by
    obtain ⟨hlo, hhi⟩ := h k
    change (N : Int) * (1000 : Int)^k -
      (publish c 1000 (by decide) k : Int) * (729 : Int)^n < (729 : Int)^n at hlo
    change (0 : Int) < ((N : Int) + 1) * (1000 : Int)^k -
      (publish c 1000 (by decide) k : Int) * (729 : Int)^n at hhi
    have hloR : (N : ℝ) * (1000 : ℝ)^k -
        (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n < (729 : ℝ)^n := by
      exact_mod_cast hlo
    have hhiR : (0 : ℝ) < ((N : ℝ) + 1) * (1000 : ℝ)^k -
        (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n := by
      exact_mod_cast hhi
    obtain ⟨hdl, hdu⟩ := decimal_publication_bounds c k
    have hp : (0 : ℝ) < 729^n := by positivity
    have hl := mul_le_mul_of_nonneg_right hdl hp.le
    have hu := mul_lt_mul_of_pos_right hdu hp
    constructor <;> nlinarith only [hloR, hhiR, hl, hu]
  have hlo := nonpositive_of_scaled_bounds
    ((N : ℝ) - value c * (729 : ℝ)^n) ((729 : ℝ)^n) (fun k => (hscaled k).1)
  have hhi := nonpositive_of_scaled_bounds
    (value c * (729 : ℝ)^n - ((N : ℝ) + 1)) ((729 : ℝ)^n) (fun k => (hscaled k).2)
  constructor <;> linarith

theorem survival_selects_publication (c : Channel) (n N : Nat)
    (h : SurvivesAllDecimals c n N) : N = publish c 729 (by decide) n := by
  obtain ⟨hlo, hhi⟩ := survival_closed_bounds c n N h
  have hboundary : value c * (729 : ℝ)^n ≠ (N : ℝ) + 1 := by
    have ha := RadixCellSelection.irrational_avoids_boundary (value_irrational c)
      (729^n) (by positivity) ((N : Int) + 1)
    simpa only [Nat.cast_pow, Nat.cast_ofNat, Int.cast_add, Int.cast_natCast,
      Int.cast_one] using ha
  have hstrict : value c * (729 : ℝ)^n < (N : ℝ) + 1 :=
    lt_of_le_of_ne hhi hboundary
  rw [publish_eq_prefix]
  unfold RadixCellSelection.positionalPrefix
  exact ((Nat.floor_eq_iff (mul_nonneg (value_nonnegative c) (by positivity))).2
    ⟨hlo, hstrict⟩).symm

theorem survival_iff_publication (c : Channel) (n N : Nat) :
    SurvivesAllDecimals c n N ↔ N = publish c 729 (by decide) n := by
  constructor
  · exact survival_selects_publication c n N
  · intro h
    subst N
    intro k
    exact generated_compatible c n k

theorem unique_surviving_prefix (c : Channel) (n : Nat) :
    ∃! N : Nat, SurvivesAllDecimals c n N := by
  refine ⟨publish c 729 (by decide) n, (survival_iff_publication c n _).2 rfl, ?_⟩
  intro N h
  exact survival_selects_publication c n N h

theorem child_admissible_iff_survival (c : Channel) (n : Nat) (u : Fin 729) :
    ChildAdmissible c n u ↔
      SurvivesAllDecimals c (n + 1) (729 * publish c 729 (by decide) n + u.val) := by
  rw [child_admissible_iff, survival_iff_publication]
  have hs := publication_step c 729 (by decide) n
  constructor
  · intro h
    subst u
    exact hs.symm
  · intro h
    apply Fin.ext
    dsimp [nextTernary]
    omega

theorem nonselected_prefix_has_finite_rejection (c : Channel) (n N : Nat)
    (h : N ≠ publish c 729 (by decide) n) :
    ∃ k : Nat, ¬ Compatible ⟨n, k, N, publish c 1000 (by decide) k⟩ := by
  by_contra hn
  push_neg at hn
  exact h (survival_selects_publication c n N hn)

end HMT.I.SurvivalCylinderSelection
end

#print axioms HMT.I.SurvivalCylinderSelection.survival_closed_bounds
#print axioms HMT.I.SurvivalCylinderSelection.survival_selects_publication
#print axioms HMT.I.SurvivalCylinderSelection.survival_iff_publication
#print axioms HMT.I.SurvivalCylinderSelection.unique_surviving_prefix
#print axioms HMT.I.SurvivalCylinderSelection.child_admissible_iff_survival
#print axioms HMT.I.SurvivalCylinderSelection.nonselected_prefix_has_finite_rejection
