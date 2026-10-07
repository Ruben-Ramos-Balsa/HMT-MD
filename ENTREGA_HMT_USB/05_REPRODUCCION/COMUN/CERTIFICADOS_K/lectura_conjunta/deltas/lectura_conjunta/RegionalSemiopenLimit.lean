import IteratedCylinderSelector

/-!
Half-open cylinders of the already generated regional publications.
This module composes the existing rational selector with its real limit;
it does not prescribe digits or identify refinement time with microscopic
TPK time. It does not supply the terminal S8 interface.
-/

noncomputable section
namespace HMT.I.RegionalSemiopenLimit

open Filter Topology HMT.I.RegionalPublicationComposition

def left (c : Channel) (n : Nat) : ℝ :=
  (publish c 729 (by decide) n : ℝ) / (729 : ℝ)^n

def right (c : Channel) (n : Nat) : ℝ := left c n + 1 / (729 : ℝ)^n

def cylinder (c : Channel) (n : Nat) : Set ℝ := Set.Ico (left c n) (right c n)

theorem publication_floor (c : Channel) (n : Nat) :
    publish c 729 (by decide) n = ⌊value c * (729 : ℝ)^n⌋₊ := by
  rw [publish_eq_prefix]
  simp only [RadixCellSelection.positionalPrefix, Nat.cast_ofNat]

theorem value_mem (c : Channel) (n : Nat) : value c ∈ cylinder c n := by
  have hp : (0 : ℝ) < 729^n := by positivity
  have hx : 0 ≤ value c * (729 : ℝ)^n :=
    mul_nonneg (value_nonnegative c) hp.le
  have hL := Nat.floor_le hx
  have hU := Nat.lt_floor_add_one (value c * (729 : ℝ)^n)
  change left c n ≤ value c ∧ value c < right c n
  rw [left, right, left, publication_floor]
  constructor
  · exact (div_le_iff₀ hp).2 hL
  · have hu : value c < (⌊value c * (729 : ℝ)^n⌋₊ + 1 : ℝ) / 729^n :=
      (lt_div_iff₀ hp).2 hU
    simpa only [add_div, one_div] using hu

theorem positive_width (c : Channel) (n : Nat) :
    0 < right c n - left c n := by
  simp only [right, add_sub_cancel_left]
  positivity

theorem next_endpoints_nested (c : Channel) (n : Nat) :
    left c n ≤ left c (n+1) ∧ right c (n+1) ≤ right c n := by
  have hp : (0 : ℝ) < 729^n := by positivity
  have hd0 : (0 : ℝ) ≤ ((publish c 729 (by decide) (n+1) % 729 : Nat) : ℝ) := by positivity
  have hd1 : ((publish c 729 (by decide) (n+1) % 729 : Nat) : ℝ) + 1 ≤ 729 := by
    exact_mod_cast (Nat.succ_le_of_lt
      (Nat.mod_lt (publish c 729 (by decide) (n+1)) (by decide : 0 < 729)))
  have he : (publish c 729 (by decide) (n+1) : ℝ) =
      729 * (publish c 729 (by decide) n : ℝ) +
        ((publish c 729 (by decide) (n+1) % 729 : Nat) : ℝ) := by
    exact_mod_cast (publication_step c 729 (by decide) n)
  simp only [left, right, pow_succ, he]
  constructor
  · apply (div_le_div_iff₀ hp (mul_pos hp (by norm_num))).2
    nlinarith
  · rw [← add_div, ← add_div]
    apply (div_le_div_iff₀ (mul_pos hp (by norm_num)) hp).2
    nlinarith

theorem next_cylinder_subset (c : Channel) (n : Nat) :
    cylinder c (n+1) ⊆ cylinder c n := by
  intro x hx
  have h := next_endpoints_nested c n
  exact ⟨h.1.trans hx.1, hx.2.trans_le h.2⟩

theorem cylinders_nested (c : Channel) (n m : Nat) :
    cylinder c (n+m) ⊆ cylinder c n := by
  induction m with
  | zero => exact Set.Subset.rfl
  | succ m ih => exact (next_cylinder_subset c (n+m)).trans ih

/-- One enclosure precision certifies all nine refinement positions and all
three regional channels together. These are the indices of the existing
nonadic publication reader, not nine newly postulated microscopic updates. -/
theorem common_nine_position_precision (start : Nat) :
    ∃ j : Nat, ∀ c : Channel, ∀ r : Fin 9,
      Stops c (729^(start+r.val+1)) j := by
  have h : ∀ r : Fin 9, ∀ᶠ j : Nat in atTop,
      ∀ c : Channel, Stops c (729^(start+r.val+1)) j := by
    intro r
    obtain ⟨N,hN⟩ := joint_eventual_publication (729^(start+r.val+1)) (by positivity)
    exact Filter.eventually_atTop.2 ⟨N, fun j hj c =>
      (hN c j hj).1.trans (hN c j hj).2.symm⟩
  obtain ⟨j,hj⟩ := (Filter.eventually_all.mpr h).exists
  exact ⟨j, fun c r => hj r c⟩

theorem common_nine_position_selection (start : Nat) :
    ∃ j : Nat, ∀ c : Channel, ∀ r : Fin 9,
      FiniteCylinderSelector.choose (lower c j) (upper c j) 729 (by decide)
        (start+r.val) (publish c 729 (by decide) (start+r.val)) =
      some (⟨publish c 729 (by decide) (start+r.val+1) % 729,
        Nat.mod_lt _ (by decide)⟩ : Fin 729) := by
  obtain ⟨j,hj⟩ := common_nine_position_precision start
  exact ⟨j, fun c r => FiniteCylinderSelector.choose_at_stopping c 729
    (by decide) (start+r.val) j (hj c r)⟩

theorem width_tendsto_zero (c : Channel) :
    Tendsto (fun n => right c n - left c n) atTop (𝓝 0) := by
  simpa only [right, add_sub_cancel_left, one_div, inv_pow] using
    tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (0 : ℝ) ≤ 729⁻¹)
      (by norm_num : (729 : ℝ)⁻¹ < 1)

theorem joint_distance_bound (c : Channel) (n : Nat) (x : ℝ)
    (hx : x ∈ cylinder c n) : |x - value c| ≤ right c n - left c n := by
  have hv := value_mem c n
  change left c n ≤ x ∧ x < right c n at hx
  change left c n ≤ value c ∧ value c < right c n at hv
  rw [abs_le]
  constructor <;> linarith

theorem intersection_singleton (c : Channel) :
    (⋂ n : Nat, cylinder c n) = {value c} := by
  ext x
  constructor
  · intro hx
    have hd : |x - value c| ≤ 0 := ge_of_tendsto (width_tendsto_zero c)
      (Filter.Eventually.of_forall (fun n => joint_distance_bound c n x
        (Set.mem_iInter.mp hx n)))
    have he : |x - value c| = 0 := le_antisymm hd (abs_nonneg _)
    exact Set.mem_singleton_iff.mpr (sub_eq_zero.mp (abs_eq_zero.mp he))
  · intro hx
    rw [Set.mem_singleton_iff] at hx
    subst x
    exact Set.mem_iInter.mpr (value_mem c)

/-- The finite parent is obtained by the existing recursive execution. -/
theorem emitted_parent_and_limit (c : Channel) (n : Nat) :
    IteratedCylinderSelector.run c 729 (by decide) n =
      some (publish c 729 (by decide) n) ∧
    value c ∈ cylinder c n ∧
    (⋂ m : Nat, cylinder c m) = {value c} :=
  ⟨IteratedCylinderSelector.run_correct c 729 (by decide) n,
    value_mem c n, intersection_singleton c⟩

end HMT.I.RegionalSemiopenLimit
end

#print axioms HMT.I.RegionalSemiopenLimit.value_mem
#print axioms HMT.I.RegionalSemiopenLimit.cylinders_nested
#print axioms HMT.I.RegionalSemiopenLimit.common_nine_position_selection
#print axioms HMT.I.RegionalSemiopenLimit.intersection_singleton
#print axioms HMT.I.RegionalSemiopenLimit.emitted_parent_and_limit
