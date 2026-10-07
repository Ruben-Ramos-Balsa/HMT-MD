import Bridge
import QuantumOccupations

/-!
The complete finite distribution is connected to the independently proved
single-mode laws. The total particle mean is defined as a state expectation,
not as a sum of already-known modal means.
-/

namespace HMT.FockBridge

open scoped BigOperators

theorem probability_cons_single_mode (u : ℝ) (us : List ℝ)
    (b : Bool) (s : Occupation us.length) :
    probability (u :: us) (b, s) =
      QuantumOccupations.fermionProbability u b * probability us s := by
  rw [probability_cons]
  simp only [QuantumOccupations.fermionProbability,
    QuantumOccupations.fermion_partition_eq, QuantumOccupations.fermionWeight]

theorem headMean_eq_single_mode (u : ℝ) (us : List ℝ)
    (h : ∀ v ∈ us, 0 ≤ v) :
    headMean u us = QuantumOccupations.fermionMean u := by
  rw [headMean_eq u us h, QuantumOccupations.fermion_mean_eq]

theorem tail_marginal (u : ℝ) (us : List ℝ) (hu : 0 ≤ u)
    (s : Occupation us.length) :
    (∑ b : Bool, probability (u :: us) (b, s)) = probability us s := by
  simp only [probability_cons_single_mode, ← Finset.sum_mul,
    QuantumOccupations.fermion_probability_sum hu, one_mul]

def particleNumber : (n : Nat) → Occupation n → ℝ
  | 0, _ => 0
  | _ + 1, (b, s) => (if b then 1 else 0) + particleNumber _ s

noncomputable def meanNumber (us : List ℝ) : ℝ :=
  ∑ s : Occupation us.length, particleNumber us.length s * probability us s

theorem meanNumber_nil : meanNumber [] = 0 := by
  simp [meanNumber, particleNumber]

theorem meanNumber_cons (u : ℝ) (us : List ℝ) (hu : 0 ≤ u)
    (h : ∀ v ∈ us, 0 ≤ v) :
    meanNumber (u :: us) = QuantumOccupations.fermionMean u + meanNumber us := by
  have split : meanNumber (u :: us) = headMean u us +
      ∑ s : Bool × Occupation us.length,
        particleNumber us.length s.2 * probability (u :: us) s := by
    unfold meanNumber headMean
    change (∑ s : Bool × Occupation us.length,
      particleNumber (us.length + 1) s * probability (u :: us) s) = _
    calc
      _ = ∑ s : Bool × Occupation us.length,
          ((if s.1 then probability (u :: us) s else 0) +
            particleNumber us.length s.2 * probability (u :: us) s) := by
        apply Finset.sum_congr rfl
        intro s _
        rcases s with ⟨b, s⟩
        cases b <;> simp [particleNumber, add_mul]
      _ = _ := Finset.sum_add_distrib
  rw [split, headMean_eq_single_mode u us h]
  congr 1
  rw [Fintype.sum_prod_type_right]
  unfold meanNumber
  apply Finset.sum_congr rfl
  intro s _
  change (∑ b : Bool, particleNumber us.length s * probability (u :: us) (b, s)) = _
  rw [← Finset.mul_sum, tail_marginal u us hu s]

/-- The sum of modal means is a theorem about the full state expectation. -/
theorem meanNumber_eq_sum (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u) :
    meanNumber us = (us.map QuantumOccupations.fermionMean).sum := by
  induction us with
  | nil => simp [meanNumber_nil]
  | cons u us ih =>
    have hu := h u (by simp)
    have ht : ∀ v ∈ us, 0 ≤ v := fun v hv => h v (by simp [hv])
    rw [meanNumber_cons u us hu ht, ih ht]
    rfl

/-- Equal-energy degeneracy is obtained from the joint distribution itself. -/
theorem degenerate_mean_eq (g : Nat) (u : ℝ) (hu : 0 ≤ u) :
    meanNumber (List.replicate g u) = QuantumOccupations.fermionLevelMean g u := by
  rw [meanNumber_eq_sum _ (fun v hv => (List.mem_replicate.mp hv).2 ▸ hu)]
  simp [QuantumOccupations.fermionLevelMean]

#print axioms probability_cons_single_mode
#print axioms meanNumber_eq_sum
#print axioms degenerate_mean_eq

end HMT.FockBridge
