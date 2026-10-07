import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.List.Nodup
import Mathlib.Algebra.Order.BigOperators.Group.List
import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Configurations

/-!
Finite fermionic distributions constructed by summing over binary occupation
states. The generic coefficient result is a proved extension from integer
weights to commutative semirings; the real distribution is an instance.

This is the finite diagonal occupation representation. It does not silently
assume a realization of general exterior Hilbert space or TPK refinement maps.
The already formalized two-mode exterior representation is connected explicitly
in `Configurations.two_mode_number_reads_bit`.
-/

namespace HMT.FockBridge

open scoped BigOperators

instance occupationFintype : (n : Nat) → Fintype (Occupation n)
  | 0 => inferInstanceAs (Fintype Unit)
  | n + 1 => by
    letI := occupationFintype n
    exact inferInstanceAs (Fintype (Bool × Occupation n))

theorem enumeration_has_no_duplicates (n : Nat) : (allStates n).Nodup := by
  induction n with
  | zero => simp [allStates]
  | succ n ih =>
    rw [allStates, List.nodup_append]
    refine ⟨List.Nodup.map (fun _ _ h => congrArg Prod.snd h) ih,
      List.Nodup.map (fun _ _ h => congrArg Prod.snd h) ih, ?_⟩
    intro s hs ht
    obtain ⟨x, _, hx⟩ := List.mem_map.mp hs
    obtain ⟨y, _, hy⟩ := List.mem_map.mp ht
    have impossible := congrArg Prod.fst (hx.trans hy.symm)
    cases impossible

noncomputable def partition {R : Type} [CommSemiring R] (us : List R) : R :=
  ∑ s : Occupation us.length, stateWeight us s

theorem partition_nil {R : Type} [CommSemiring R] : partition ([] : List R) = 1 := by
  simp [partition, stateWeight, Occupation]

theorem partition_cons {R : Type} [CommSemiring R] (u : R) (us : List R) :
    partition (u :: us) = (1 + u) * partition us := by
  change (∑ s : Bool × Occupation us.length,
    if s.1 then u * stateWeight us s.2 else stateWeight us s.2) = _
  rw [Fintype.sum_prod_type]
  rw [Fintype.sum_bool]
  change (∑ s : Occupation us.length, u * stateWeight us s) +
    (∑ s : Occupation us.length, stateWeight us s) = _
  rw [← Finset.mul_sum]
  change u * partition us + partition us = (1 + u) * partition us
  ring

/-- Every mode contributes its two possible occupations; no state is omitted. -/
theorem partition_factors {R : Type} [CommSemiring R] (us : List R) :
    partition us = (us.map (fun u => 1 + u)).prod := by
  induction us with
  | nil => simp [partition_nil]
  | cons u us ih => rw [partition_cons, ih]; rfl

/-- The type-indexed partition and the original integer certificate agree. -/
theorem integer_partition_matches_original (us : List Int) :
    partition us = VFactores.total ((allStates us.length).map (stateWeight us)) := by
  rw [original_partition_is_state_sum, partition_factors]
  induction us with
  | nil => rfl
  | cons u us ih => simp only [List.map_cons, List.prod_cons, VFactores.factors, ih]

theorem stateWeight_nonnegative (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u)
    (s : Occupation us.length) : 0 ≤ stateWeight us s := by
  induction us with
  | nil => simp [stateWeight]
  | cons u us ih =>
    rcases s with ⟨b, tail⟩
    have hu := h u (by simp)
    have ht := ih (fun v hv => h v (by simp [hv])) tail
    cases b
    · exact ht
    · exact mul_nonneg hu ht

theorem partition_positive (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u) : 0 < partition us := by
  induction us with
  | nil => rw [partition_nil]; norm_num
  | cons u us ih =>
    rw [partition_cons]
    have hu := h u (by simp)
    exact mul_pos (by linarith) (ih (fun v hv => h v (by simp [hv])))

noncomputable def probability (us : List ℝ) (s : Occupation us.length) : ℝ :=
  stateWeight us s / partition us

theorem probability_nonnegative (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u)
    (s : Occupation us.length) : 0 ≤ probability us s :=
  div_nonneg (stateWeight_nonnegative us h s) (le_of_lt (partition_positive us h))

theorem probability_normalized (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u) :
    ∑ s : Occupation us.length, probability us s = 1 := by
  simp only [probability, ← Finset.sum_div]
  change partition us / partition us = 1
  exact div_self (ne_of_gt (partition_positive us h))

noncomputable def headNumerator (u : ℝ) (us : List ℝ) : ℝ :=
  ∑ s : Occupation (u :: us).length, if s.1 then stateWeight (u :: us) s else 0

theorem headNumerator_eq (u : ℝ) (us : List ℝ) :
    headNumerator u us = u * partition us := by
  unfold headNumerator
  change (∑ s : Bool × Occupation us.length,
    if s.1 then (if s.1 then u * stateWeight us s.2 else stateWeight us s.2) else 0) = _
  rw [Fintype.sum_prod_type]
  simp [Fintype.sum_bool, ← Finset.mul_sum, partition]

noncomputable def headMean (u : ℝ) (us : List ℝ) : ℝ :=
  ∑ s : Occupation (u :: us).length, if s.1 then probability (u :: us) s else 0

theorem headMean_eq_ratio (u : ℝ) (us : List ℝ) :
    headMean u us = headNumerator u us / partition (u :: us) := by
  unfold headMean headNumerator probability
  rw [Finset.sum_div]
  apply Finset.sum_congr rfl
  intro s _
  cases s.1 <;> simp

/-- The one-mode marginal is derived from the full finite distribution. -/
theorem headMean_eq (u : ℝ) (us : List ℝ)
    (h : ∀ v ∈ us, 0 ≤ v) : headMean u us = u / (1 + u) := by
  rw [headMean_eq_ratio, headNumerator_eq, partition_cons]
  have hp : partition us ≠ 0 := ne_of_gt (partition_positive us h)
  exact mul_div_mul_right u (1 + u) hp

/-- Complete joint probabilities factor, not only their normalization constants. -/
theorem probability_cons (u : ℝ) (us : List ℝ) (b : Bool) (s : Occupation us.length) :
    probability (u :: us) (b, s) =
      ((if b then u else 1) / (1 + u)) * probability us s := by
  unfold probability
  rw [partition_cons]
  cases b
  · change stateWeight us s / ((1 + u) * partition us) =
      (1 / (1 + u)) * (stateWeight us s / partition us)
    simpa only [one_mul] using
      (mul_div_mul_comm (1 : ℝ) (stateWeight us s) (1 + u) (partition us))
  · exact mul_div_mul_comm u (stateWeight us s) (1 + u) (partition us)

/-- Repeated equal-energy modes retain their multiplicity in the partition. -/
theorem partition_degenerate_block {R : Type} [CommSemiring R]
    (g : Nat) (u : R) (us : List R) :
    partition (List.replicate g u ++ us) = (1 + u) ^ g * partition us := by
  rw [partition_factors, partition_factors]
  simp

#print axioms enumeration_has_no_duplicates
#print axioms partition_factors
#print axioms integer_partition_matches_original
#print axioms probability_normalized
#print axioms headMean_eq
#print axioms probability_cons
#print axioms partition_degenerate_block

end HMT.FockBridge
