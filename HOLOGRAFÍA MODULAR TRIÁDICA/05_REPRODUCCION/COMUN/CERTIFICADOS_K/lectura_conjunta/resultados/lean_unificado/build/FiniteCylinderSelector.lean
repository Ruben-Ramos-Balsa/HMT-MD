import RegionalCylinderTransition
import RationalCellIntegerShift

/-!
The finite max/min singleton selector of `generate_blocks` (lines 865–885).
Its inputs are the current cylinder and rational enclosure endpoints. It does
not read a future publication, target block, transition matrix, or real value.
The equality to the regional publication is proved after the constructor.

This is a component operation. No nine-step enriched-state calendar is defined
here or inferred merely from the number of block refinements.
-/

namespace HMT.I.FiniteCylinderSelector

open HMT.I.RegionalPublicationComposition HMT.I.RegionalCylinderTransition

def firstCandidate (lower : ℚ) (base depth parent : Nat) : Int :=
  max ((base : Int) * parent) (RadixCellSelection.first lower (base^(depth + 1)))

def lastCandidate (upper : ℚ) (base depth parent : Nat) : Int :=
  min ((base : Int) * parent + base - 1)
    (RadixCellSelection.last upper (base^(depth + 1)))

/-- A partial, finite operation: ambiguity returns `none`, not an arbitrary digit. -/
def choose (lower upper : ℚ) (base : Nat) (hb : 0 < base)
    (depth parent : Nat) : Option (Fin base) :=
  if h : firstCandidate lower base depth parent = lastCandidate upper base depth parent then
    some ⟨(firstCandidate lower base depth parent - (base : Int) * parent).toNat, by
      have ha : (base : Int) * parent ≤ firstCandidate lower base depth parent :=
        le_max_left _ _
      have hz : lastCandidate upper base depth parent ≤ (base : Int) * parent + base - 1 :=
        min_le_left _ _
      omega⟩
  else none

theorem choose_of_singleton (lower upper : ℚ) (base : Nat) (hb : 0 < base)
    (depth parent : Nat) (u : Fin base)
    (ha : firstCandidate lower base depth parent = (base : Int) * parent + u.val)
    (hz : lastCandidate upper base depth parent = (base : Int) * parent + u.val) :
    choose lower upper base hb depth parent = some u := by
  unfold choose
  split
  · apply congrArg some
    apply Fin.ext
    change (firstCandidate lower base depth parent - (base : Int) * parent).toNat = u.val
    rw [ha]
    omega
  · rename_i hn
    exact (hn (ha.trans hz.symm)).elim

theorem chosen_is_singleton (lower upper : ℚ) (base : Nat) (hb : 0 < base)
    (depth parent : Nat) (u : Fin base)
    (hu : choose lower upper base hb depth parent = some u) :
    firstCandidate lower base depth parent = (base : Int) * parent + u.val ∧
    lastCandidate upper base depth parent = (base : Int) * parent + u.val := by
  unfold choose at hu
  split at hu
  · rename_i he
    have hv := congrArg (fun x : Fin base => x.val) (Option.some.inj hu)
    have ha : (base : Int) * parent ≤ firstCandidate lower base depth parent :=
      le_max_left _ _
    dsimp only at hv
    constructor <;> omega
  · contradiction

theorem choose_iff_singleton (lower upper : ℚ) (base : Nat) (hb : 0 < base)
    (depth parent : Nat) (u : Fin base) :
    choose lower upper base hb depth parent = some u ↔
      firstCandidate lower base depth parent = (base : Int) * parent + u.val ∧
      lastCandidate upper base depth parent = (base : Int) * parent + u.val :=
  ⟨chosen_is_singleton lower upper base hb depth parent u,
    fun h => choose_of_singleton lower upper base hb depth parent u h.1 h.2⟩

theorem first_candidate_integer_shift (q : ℚ) (m base depth parent : Nat) :
    firstCandidate (q + m) base depth (parent + m * base^depth) =
      firstCandidate q base depth parent + (m : Int) * (base^(depth + 1) : Nat) := by
  unfold firstCandidate
  have ht : (base : Int) * (parent + m * base^depth : Nat) =
      (base : Int) * parent + (m : Int) * (base^(depth + 1) : Nat) := by
    push_cast
    rw [pow_succ]
    ring
  rw [ht]
  simpa only [Int.cast_natCast] using
    RationalCellIntegerShift.max_first_integer_shift q (m : Int)
      ((base : Int) * parent) (base^(depth + 1))

theorem last_candidate_integer_shift (q : ℚ) (m base depth parent : Nat) :
    lastCandidate (q + m) base depth (parent + m * base^depth) =
      lastCandidate q base depth parent + (m : Int) * (base^(depth + 1) : Nat) := by
  unfold lastCandidate
  have ht : (base : Int) * (parent + m * base^depth : Nat) + base - 1 =
      ((base : Int) * parent + base - 1) + (m : Int) * (base^(depth + 1) : Nat) := by
    push_cast
    rw [pow_succ]
    ring
  rw [ht]
  simpa only [Int.cast_natCast] using
    RationalCellIntegerShift.min_last_integer_shift q (m : Int)
      ((base : Int) * parent + base - 1) (base^(depth + 1))

/-- Removing or restoring the integer part leaves the emitted digit unchanged. -/
theorem choose_integer_shift (lower upper : ℚ) (m base : Nat) (hb : 0 < base)
    (depth parent : Nat) :
    choose (lower + m) (upper + m) base hb depth (parent + m * base^depth) =
      choose lower upper base hb depth parent := by
  unfold choose
  simp only [first_candidate_integer_shift, last_candidate_integer_shift, add_left_inj]
  split_ifs
  · apply congrArg some
    apply Fin.ext
    change Int.toNat _ = Int.toNat _
    congr 1
    push_cast
    rw [pow_succ]
    ring
  · rfl

-- Exact rational regression examples for singleton selection and ambiguity.
example : choose (3/10) (31/100) 10 (by decide) 0 0 = some ⟨3, by decide⟩ := by
  norm_num [choose, firstCandidate, lastCandidate, RadixCellSelection.first,
    RadixCellSelection.last]
  rfl
example : choose (3/10) (41/100) 10 (by decide) 0 0 = none := by
  norm_num [choose, firstCandidate, lastCandidate, RadixCellSelection.first,
    RadixCellSelection.last]

#eval (choose (3/10) (31/100) 10 (by decide) 0 0).map Fin.val
#eval (choose (3/10) (41/100) 10 (by decide) 0 0).map Fin.val

noncomputable section

/-- Stopping tests only the rational enclosure. The published digit is a conclusion. -/
theorem choose_at_stopping (c : Channel) (base : Nat) (hb : 0 < base)
    (n j : Nat) (hj : Stops c (base^(n + 1)) j) :
    choose (lower c j) (upper c j) base hb n (publish c base hb n) =
      some (⟨publish c base hb (n + 1) % base, Nat.mod_lt _ hb⟩ : Fin base) := by
  have hf : RadixCellSelection.first (lower c j) (base^(n + 1)) =
      (publish c base hb (n + 1) : Int) := by
    rw [stopped_cell_correct c _ j (by positivity) hj, publish_eq_prefix]
    exact (RadixCellSelection.prefix_as_cell _ (value_nonnegative c) base (n + 1)).symm
  have hz : RadixCellSelection.last (upper c j) (base^(n + 1)) =
      (publish c base hb (n + 1) : Int) := by
    exact hj.symm.trans hf
  have hp := publication_step c base hb n
  have hd := Nat.mod_lt (publish c base hb (n + 1)) hb
  have hc : (base : Int) * publish c base hb n ≤ publish c base hb (n + 1) ∧
      (publish c base hb (n + 1) : Int) < (base : Int) * publish c base hb n + base := by
    exact_mod_cast (show base * publish c base hb n ≤ publish c base hb (n + 1) ∧
      publish c base hb (n + 1) < base * publish c base hb n + base by omega)
  obtain ⟨hfirst, hlast⟩ := RadixCellSelection.clipped_single_cell
    (lower c j) (upper c j) (base^(n + 1)) ((base : Int) * publish c base hb n)
    base (publish c base hb (n + 1)) hc hf hz
  have hpi : (publish c base hb (n + 1) : Int) =
      (base : Int) * publish c base hb n + (publish c base hb (n + 1) % base : Nat) := by
    exact_mod_cast hp
  apply choose_of_singleton
  · exact hfirst.trans hpi
  · exact hlast.trans hpi

/-- Refine the ternary cylinder using only its present prefix and the enclosure. -/
def selectTernary (lower upper : ℚ) (s : CylinderState) : Option CylinderState :=
  (choose lower upper 729 (by decide) s.ternaryDepth s.ternaryPrefix).map
    (ternaryStep s)

/-- Joint refinement is requested explicitly; this does not invent its calendar. -/
def selectJoint (lower upper : ℚ) (s : CylinderState) : Option CylinderState := do
  let u ← choose lower upper 729 (by decide) s.ternaryDepth s.ternaryPrefix
  let d ← choose lower upper 1000 (by decide) s.decimalDepth s.decimalPrefix
  pure (jointStep s u d)

theorem select_ternary_at_stopping (c : Channel) (n k j : Nat)
    (hj : Stops c (729^(n + 1)) j) :
    selectTernary (lower c j) (upper c j) (generated c n k) =
      some (generated c (n + 1) k) := by
  unfold selectTernary
  change (choose (lower c j) (upper c j) 729 (by decide) n
    (publish c 729 (by decide) n)).map (ternaryStep (generated c n k)) = _
  rw [choose_at_stopping c 729 (by decide) n j hj]
  change some (ternaryStep (generated c n k) (nextTernary c n)) = _
  rw [← generated_ternary_step]

theorem select_joint_at_stopping (c : Channel) (n k j : Nat)
    (ht : Stops c (729^(n + 1)) j) (hd : Stops c (1000^(k + 1)) j) :
    selectJoint (lower c j) (upper c j) (generated c n k) =
      some (generated c (n + 1) (k + 1)) := by
  unfold selectJoint
  dsimp only [generated]
  rw [choose_at_stopping c 729 (by decide) n j ht,
    choose_at_stopping c 1000 (by decide) k j hd]
  change some (jointStep (generated c n k) (nextTernary c n) (nextDecimal c k)) = _
  rw [← generated_joint_step]
  rfl

theorem every_depth_has_joint_selection (c : Channel) (n k : Nat) :
    ∃ J : Nat, ∀ j, J ≤ j →
      selectJoint (lower c j) (upper c j) (generated c n k) =
        some (generated c (n + 1) (k + 1)) := by
  obtain ⟨a, ha⟩ := eventual_publication c (729^(n + 1)) (by positivity)
  obtain ⟨b, hb⟩ := eventual_publication c (1000^(k + 1)) (by positivity)
  refine ⟨max a b, ?_⟩
  intro j hj
  have ht := ha j (le_trans (le_max_left _ _) hj)
  have hd := hb j (le_trans (le_max_right _ _) hj)
  exact select_joint_at_stopping c n k j (ht.1.trans ht.2.symm) (hd.1.trans hd.2.symm)

theorem selected_joint_is_compatible (c : Channel) (n k j : Nat)
    (ht : Stops c (729^(n + 1)) j) (hd : Stops c (1000^(k + 1)) j)
    (s : CylinderState)
    (hs : selectJoint (lower c j) (upper c j) (generated c n k) = some s) :
    Compatible s := by
  rw [select_joint_at_stopping c n k j ht hd] at hs
  cases Option.some.inj hs
  exact generated_compatible c (n + 1) (k + 1)

end
end HMT.I.FiniteCylinderSelector

#print axioms HMT.I.FiniteCylinderSelector.choose_of_singleton
#print axioms HMT.I.FiniteCylinderSelector.chosen_is_singleton
#print axioms HMT.I.FiniteCylinderSelector.choose_iff_singleton
#print axioms HMT.I.FiniteCylinderSelector.first_candidate_integer_shift
#print axioms HMT.I.FiniteCylinderSelector.last_candidate_integer_shift
#print axioms HMT.I.FiniteCylinderSelector.choose_integer_shift
#print axioms HMT.I.FiniteCylinderSelector.choose_at_stopping
#print axioms HMT.I.FiniteCylinderSelector.select_ternary_at_stopping
#print axioms HMT.I.FiniteCylinderSelector.select_joint_at_stopping
#print axioms HMT.I.FiniteCylinderSelector.every_depth_has_joint_selection
#print axioms HMT.I.FiniteCylinderSelector.selected_joint_is_compatible
