import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
Article III, `iii:sec:constitutiva`: the declared response of a fixed transport.
The channel is a downstream argument; this file does not generate TPK channels.
The interval bijection and cubic inversion below are conclusions, not inputs.
-/
namespace HMT.III.Constitutive

open Set
noncomputable section

def numerator (s : ℝ) : ℝ := 1 + s + s ^ 2
def denominator (s : ℝ) : ℝ := 1 + s + s ^ 2 + s ^ 3
def response (s : ℝ) : ℝ := numerator s / denominator s

theorem numerator_pos {s : ℝ} (hs : 0 ≤ s) : 0 < numerator s := by
  unfold numerator
  positivity

theorem denominator_pos {s : ℝ} (hs : 0 ≤ s) : 0 < denominator s := by
  unfold denominator
  positivity

theorem response_pos {s : ℝ} (hs : 0 ≤ s) : 0 < response s :=
  div_pos (numerator_pos hs) (denominator_pos hs)

@[simp] theorem response_zero : response 0 = 1 := by
  norm_num [response, numerator, denominator]

@[simp] theorem response_one : response 1 = 3 / 4 := by
  norm_num [response, numerator, denominator]

-- An exact positive difference proves strict decrease, including the endpoints.
theorem response_strictAntiOn : StrictAntiOn response (Ici 0) := by
  intro x hx y hy hxy
  change 0 ≤ x at hx
  change 0 ≤ y at hy
  have hypos : 0 < y := lt_of_le_of_lt hx hxy
  have hpoly : 0 < y ^ 2 + x * y + x ^ 2 + x * y * (x + y) + x ^ 2 * y ^ 2 := by
    positivity
  have hdifference := mul_pos (sub_pos.mpr hxy) hpoly
  apply (div_lt_div_iff₀ (denominator_pos hy) (denominator_pos hx)).mpr
  unfold numerator denominator
  calc
    (1 + y + y ^ 2) * (1 + x + x ^ 2 + x ^ 3)
        < (1 + y + y ^ 2) * (1 + x + x ^ 2 + x ^ 3) +
          (y - x) * (y ^ 2 + x * y + x ^ 2 + x * y * (x + y) + x ^ 2 * y ^ 2) :=
      lt_add_of_pos_right _ hdifference
    _ = (1 + x + x ^ 2) * (1 + y + y ^ 2 + y ^ 3) := by ring

theorem response_bounds {s : ℝ} (hs : s ∈ Ioo 0 1) :
    response s ∈ Ioo (3 / 4) 1 := by
  constructor
  · simpa using response_strictAntiOn hs.1.le (by norm_num : (1 : ℝ) ∈ Ici 0) hs.2
  · simpa using response_strictAntiOn (by norm_num : (0 : ℝ) ∈ Ici 0) hs.1.le hs.1

theorem response_continuousOn : ContinuousOn response (Ici 0) := by
  apply ContinuousOn.div
  · exact (by unfold numerator; fun_prop : Continuous numerator).continuousOn
  · exact (by unfold denominator; fun_prop : Continuous denominator).continuousOn
  · intro s hs
    exact ne_of_gt (denominator_pos hs)

theorem response_surjOn : SurjOn response (Ioo 0 1) (Ioo (3 / 4) 1) := by
  intro r hr
  have hc : ContinuousOn response (Icc 0 1) :=
    response_continuousOn.mono (fun _ hx => hx.1)
  have hr' : r ∈ Icc (response 1) (response 0) := by
    simpa using And.intro hr.1.le hr.2.le
  rcases intermediate_value_Icc' (by norm_num : (0 : ℝ) ≤ 1) hc hr' with ⟨s, hs, hsr⟩
  refine ⟨s, ⟨?_, ?_⟩, hsr⟩
  · have hs0 : s ≠ 0 := by
      intro hz
      rw [hz, response_zero] at hsr
      linarith [hr.2]
    exact lt_of_le_of_ne hs.1 (Ne.symm hs0)
  · have hs1 : s ≠ 1 := by
      intro hz
      rw [hz, response_one] at hsr
      linarith [hr.1]
    exact lt_of_le_of_ne hs.2 hs1

theorem response_bijOn : BijOn response (Ioo 0 1) (Ioo (3 / 4) 1) := by
  refine ⟨fun _ hs => response_bounds hs, ?_, response_surjOn⟩
  intro s hs t ht hst
  exact response_strictAntiOn.injOn hs.1.le ht.1.le hst

theorem response_exists_unique {r : ℝ} (hr : r ∈ Ioo (3 / 4) 1) :
    ∃! s : ℝ, s ∈ Ioo 0 1 ∧ response s = r := by
  rcases response_surjOn hr with ⟨s, hs, hsr⟩
  refine ⟨s, ⟨hs, hsr⟩, ?_⟩
  intro t ht
  exact response_bijOn.injOn ht.1 hs (ht.2.trans hsr.symm)

theorem response_eq_iff_cubic {s r : ℝ} (hs : 0 ≤ s) :
    response s = r ↔ r * s ^ 3 + (r - 1) * (1 + s + s ^ 2) = 0 := by
  rw [response, div_eq_iff (ne_of_gt (denominator_pos hs))]
  unfold numerator denominator
  constructor <;> intro h <;> nlinarith only [h]

theorem cubic_exists_unique {r : ℝ} (hr : r ∈ Ioo (3 / 4) 1) :
    ∃! s : ℝ, s ∈ Ioo 0 1 ∧
      r * s ^ 3 + (r - 1) * (1 + s + s ^ 2) = 0 := by
  rcases response_exists_unique hr with ⟨s, hs, hu⟩
  refine ⟨s, ⟨hs.1, (response_eq_iff_cubic hs.1.1.le).mp hs.2⟩, ?_⟩
  intro t ht
  exact hu t ⟨ht.1, (response_eq_iff_cubic ht.1.1.le).mpr ht.2⟩

-- Classical selection is explicit and follows the proved existence/uniqueness.
noncomputable def recover (r : ℝ) (hr : r ∈ Ioo (3 / 4) 1) : ℝ :=
  Classical.choose (response_exists_unique hr)

theorem recover_spec (r : ℝ) (hr : r ∈ Ioo (3 / 4) 1) :
    recover r hr ∈ Ioo 0 1 ∧ response (recover r hr) = r :=
  (Classical.choose_spec (response_exists_unique hr)).1

theorem recover_response {s : ℝ} (hs : s ∈ Ioo 0 1) :
    recover (response s) (response_bounds hs) = s :=
  response_bijOn.injOn (recover_spec _ _).1 hs (recover_spec _ _).2

#print axioms response_pos
#print axioms response_strictAntiOn
#print axioms response_bijOn
#print axioms response_eq_iff_cubic
#print axioms cubic_exists_unique
#print axioms recover_response

end

end HMT.III.Constitutive
