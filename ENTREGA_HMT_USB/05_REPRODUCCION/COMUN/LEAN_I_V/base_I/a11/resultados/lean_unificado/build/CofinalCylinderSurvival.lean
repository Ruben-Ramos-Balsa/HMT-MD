import SurvivalCylinderSelection

/-!
Cofinal observation suffices for cylinder survival. The key step proves
that overlap with a finer generated decimal cylinder implies overlap with
each of its truncations, using the already proved prefix compatibility.

No assertion about the depth growth or preservation of the full enriched
TPK update is introduced. The cofinality hypothesis is explicit.
-/

noncomputable section
namespace HMT.I.CofinalCylinderSurvival

open HMT.I.RegionalPublicationComposition HMT.I.RegionalCylinderTransition
open HMT.I.SurvivalCylinderSelection

def CofinalDepth (κ : Nat → Nat) : Prop := ∀ k : Nat, ∃ t : Nat, k ≤ κ t

def ObservedSurvival (c : Channel) (n N : Nat) (κ : Nat → Nat) : Prop :=
  ∀ t : Nat, Compatible ⟨n, κ t, N, publish c 1000 (by decide) (κ t)⟩

theorem compatible_truncate_decimal (c : Channel) (n N k a : Nat)
    (h : Compatible ⟨n, k + a, N, publish c 1000 (by decide) (k + a)⟩) :
    Compatible ⟨n, k, N, publish c 1000 (by decide) k⟩ := by
  have hq : (0 : ℝ) < 1000^a := by positivity
  have hb : (0 : ℝ) < 729^n := by positivity
  have he := Nat.div_add_mod (publish c 1000 (by decide) (k + a)) (1000^a)
  rw [publications_compatible c 1000 (by decide) k a] at he
  have hr := Nat.mod_lt (publish c 1000 (by decide) (k + a))
    (show 0 < 1000^a by positivity)
  have hdl : 1000^a * publish c 1000 (by decide) k ≤
      publish c 1000 (by decide) (k + a) := by omega
  have hdu : publish c 1000 (by decide) (k + a) + 1 ≤
      1000^a * (publish c 1000 (by decide) k + 1) := by nlinarith only [he, hr]
  have hdlR : (1000 : ℝ)^a * (publish c 1000 (by decide) k : ℝ) ≤
      (publish c 1000 (by decide) (k + a) : ℝ) := by exact_mod_cast hdl
  have hduR : (publish c 1000 (by decide) (k + a) : ℝ) + 1 ≤
      (1000 : ℝ)^a * ((publish c 1000 (by decide) k : ℝ) + 1) := by exact_mod_cast hdu
  obtain ⟨hlo, hhi⟩ := h
  change (N : Int) * (1000 : Int)^(k + a) -
    (publish c 1000 (by decide) (k + a) : Int) * (729 : Int)^n < (729 : Int)^n at hlo
  change (0 : Int) < ((N : Int) + 1) * (1000 : Int)^(k + a) -
    (publish c 1000 (by decide) (k + a) : Int) * (729 : Int)^n at hhi
  have hloR : (N : ℝ) * (1000 : ℝ)^(k + a) -
      (publish c 1000 (by decide) (k + a) : ℝ) * (729 : ℝ)^n < (729 : ℝ)^n := by
    exact_mod_cast hlo
  have hhiR : (0 : ℝ) < ((N : ℝ) + 1) * (1000 : ℝ)^(k + a) -
      (publish c 1000 (by decide) (k + a) : ℝ) * (729 : ℝ)^n := by
    exact_mod_cast hhi
  rw [pow_add] at hloR hhiR
  have hu := mul_le_mul_of_nonneg_right hduR hb.le
  have hl := mul_le_mul_of_nonneg_right hdlR hb.le
  have hlow : (N : ℝ) * (1000 : ℝ)^k <
      ((publish c 1000 (by decide) k : ℝ) + 1) * (729 : ℝ)^n := by
    apply (mul_lt_mul_right hq).mp
    nlinarith only [hloR, hu]
  have hupp : (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n <
      ((N : ℝ) + 1) * (1000 : ℝ)^k := by
    apply (mul_lt_mul_right hq).mp
    nlinarith only [hhiR, hl]
  constructor
  · change (N : Int) * (1000 : Int)^k -
      (publish c 1000 (by decide) k : Int) * (729 : Int)^n < (729 : Int)^n
    have : (N : ℝ) * (1000 : ℝ)^k -
        (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n < (729 : ℝ)^n := by
      nlinarith only [hlow]
    exact_mod_cast this
  · change (0 : Int) < ((N : Int) + 1) * (1000 : Int)^k -
      (publish c 1000 (by decide) k : Int) * (729 : Int)^n
    have : (0 : ℝ) < ((N : ℝ) + 1) * (1000 : ℝ)^k -
        (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n := by
      linarith only [hupp]
    exact_mod_cast this

theorem compatible_at_smaller_depth (c : Channel) (n N k l : Nat) (hkl : k ≤ l)
    (h : Compatible ⟨n, l, N, publish c 1000 (by decide) l⟩) :
    Compatible ⟨n, k, N, publish c 1000 (by decide) k⟩ := by
  have he : k + (l - k) = l := by omega
  have h' : Compatible ⟨n, k + (l - k), N,
      publish c 1000 (by decide) (k + (l - k))⟩ := by simpa only [he] using h
  exact compatible_truncate_decimal c n N k (l - k) h'

theorem cofinal_observation_implies_survival (c : Channel) (n N : Nat) (κ : Nat → Nat)
    (hκ : CofinalDepth κ) (h : ObservedSurvival c n N κ) :
    SurvivesAllDecimals c n N := by
  intro k
  obtain ⟨t, ht⟩ := hκ k
  exact compatible_at_smaller_depth c n N k (κ t) ht (h t)

theorem cofinal_observation_iff_survival (c : Channel) (n N : Nat) (κ : Nat → Nat)
    (hκ : CofinalDepth κ) :
    ObservedSurvival c n N κ ↔ SurvivesAllDecimals c n N := by
  constructor
  · exact cofinal_observation_implies_survival c n N κ hκ
  · intro h t
    exact h (κ t)

theorem cofinal_survival_selects_publication (c : Channel) (n N : Nat) (κ : Nat → Nat)
    (hκ : CofinalDepth κ) (h : ObservedSurvival c n N κ) :
    N = publish c 729 (by decide) n :=
  survival_selects_publication c n N (cofinal_observation_implies_survival c n N κ hκ h)

theorem cofinal_child_admissible_iff (c : Channel) (n : Nat) (u : Fin 729)
    (κ : Nat → Nat) (hκ : CofinalDepth κ) :
    ChildAdmissible c n u ↔
      ObservedSurvival c (n + 1) (729 * publish c 729 (by decide) n + u.val) κ := by
  rw [cofinal_observation_iff_survival c (n + 1) _ κ hκ]
  exact child_admissible_iff_survival c n u

theorem nonselected_prefix_has_observed_rejection (c : Channel) (n N : Nat)
    (κ : Nat → Nat) (hκ : CofinalDepth κ) (hN : N ≠ publish c 729 (by decide) n) :
    ∃ t : Nat, ¬ Compatible ⟨n, κ t, N, publish c 1000 (by decide) (κ t)⟩ := by
  obtain ⟨k, hk⟩ := nonselected_prefix_has_finite_rejection c n N hN
  obtain ⟨t, ht⟩ := hκ k
  refine ⟨t, ?_⟩
  intro h
  exact hk (compatible_at_smaller_depth c n N k (κ t) ht h)

end HMT.I.CofinalCylinderSurvival
end

#print axioms HMT.I.CofinalCylinderSurvival.compatible_truncate_decimal
#print axioms HMT.I.CofinalCylinderSurvival.compatible_at_smaller_depth
#print axioms HMT.I.CofinalCylinderSurvival.cofinal_observation_implies_survival
#print axioms HMT.I.CofinalCylinderSurvival.cofinal_observation_iff_survival
#print axioms HMT.I.CofinalCylinderSurvival.cofinal_survival_selects_publication
#print axioms HMT.I.CofinalCylinderSurvival.cofinal_child_admissible_iff
#print axioms HMT.I.CofinalCylinderSurvival.nonselected_prefix_has_observed_rejection
