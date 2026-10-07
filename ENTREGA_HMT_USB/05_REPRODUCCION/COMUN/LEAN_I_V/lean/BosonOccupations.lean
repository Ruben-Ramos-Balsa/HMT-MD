import BosonManyModes

/-! Marginals at every mode and the actual expected total occupation of a degenerate block. -/

noncomputable section

open scoped BigOperators

namespace QuantumOccupations

def bosonStateOccupation : (n : ℕ) → Fin n → BosonStates n → ℕ
  | 0, i, _ => Fin.elim0 i
  | n + 1, i, s => Fin.cases s.1 (fun j => bosonStateOccupation n j s.2) i

def bosonCoordinateMean (us : List ℝ) (i : Fin us.length) : ℝ :=
  ∑' s, (bosonStateOccupation us.length i s : ℝ) * bosonManyProbability us s

/-- The weighted first moment of every coordinate, before normalization. -/
theorem bosonCoordinateMoment_hasSum {us : List ℝ} (hu : BosonAdmissible us)
    (i : Fin us.length) :
    HasSum (fun s => (bosonStateOccupation us.length i s : ℝ) * bosonStateWeight us s)
      (bosonMean (us.get i) * bosonFactors us) := by
  induction us with
  | nil => exact Fin.elim0 i
  | cons u us ih =>
    have htail : BosonAdmissible us := fun v hv => hu v (by simp [hv])
    have hu0 : 0 ≤ u := (hu u (by simp)).1
    have hu1 : u < 1 := (hu u (by simp)).2
    refine Fin.cases ?_ (fun j => ?_) i
    · have hh := bosonHeadMoment_hasSum hu
      have hv : bosonMean u * ((1 - u)⁻¹ * bosonFactors us) =
          (u / (1 - u) ^ 2) * bosonFactors us := by
        rw [boson_mean_eq hu0 hu1]
        have hd : 1 - u ≠ 0 := ne_of_gt (sub_pos.mpr hu1)
        field_simp [hd]
        ring_nf
        simp
      simpa only [List.length_cons, bosonStateOccupation, Fin.cases_zero, List.get_cons_zero, bosonFactors, hv]
        using hh
    · have hhead := boson_weight_hasSum hu0 hu1
      have hj := ih htail j
      have hmul := hhead.summable.mul_of_nonneg hj.summable
        (fun n => pow_nonneg hu0 n)
        (fun s => mul_nonneg (Nat.cast_nonneg _) (bosonStateWeight_nonneg htail s))
      simpa only [List.length_cons, bosonStateOccupation, Fin.cases_succ,
        List.get_cons_succ', bosonFactors, bosonStateWeight, bosonWeight,
        mul_assoc, mul_left_comm, mul_comm] using hhead.mul hj hmul

/-- Every modal expectation in the joint distribution equals the modal BE expectation. -/
theorem bosonCoordinate_mean_hasSum {us : List ℝ} (hu : BosonAdmissible us)
    (i : Fin us.length) :
    HasSum (fun s => (bosonStateOccupation us.length i s : ℝ) * bosonManyProbability us s)
      (bosonMean (us.get i)) := by
  have h := (bosonCoordinateMoment_hasSum hu i).div_const (bosonManyPartition us)
  have hv : (bosonMean (us.get i) * bosonFactors us) / bosonManyPartition us =
      bosonMean (us.get i) := by
    rw [bosonMany_partition_factors hu]
    exact mul_div_cancel_right₀ _ (ne_of_gt (bosonFactors_pos hu))
  rw [hv] at h
  simpa only [bosonManyProbability, div_eq_mul_inv, mul_assoc] using h

theorem bosonCoordinate_mean_eq {us : List ℝ} (hu : BosonAdmissible us)
    (i : Fin us.length) : bosonCoordinateMean us i = bosonMean (us.get i) :=
  (bosonCoordinate_mean_hasSum hu i).tsum_eq

def bosonTotalMean (us : List ℝ) : ℝ :=
  ∑' s, (∑ i : Fin us.length, (bosonStateOccupation us.length i s : ℝ)) *
    bosonManyProbability us s

/-- The total expectation is derived by summing the convergent coordinate moments. -/
theorem bosonTotal_mean_eq {us : List ℝ} (hu : BosonAdmissible us) :
    bosonTotalMean us = ∑ i : Fin us.length, bosonMean (us.get i) := by
  have h := hasSum_sum (s := Finset.univ) (fun i _ => bosonCoordinate_mean_hasSum hu i)
  have hh : HasSum (fun s =>
      (∑ i : Fin us.length, (bosonStateOccupation us.length i s : ℝ)) * bosonManyProbability us s)
      (∑ i : Fin us.length, bosonMean (us.get i)) := by
    simpa only [Finset.sum_mul] using h
  exact hh.tsum_eq

/-- Degeneracy multiplies the expectation of the actual total occupation random variable. -/
theorem bosonTotal_mean_degeneracy (g : ℕ) {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    bosonTotalMean (List.replicate g u) = (g : ℝ) * bosonMean u := by
  have hu : BosonAdmissible (List.replicate g u) := by
    intro v hv
    have : v = u := List.eq_of_mem_replicate hv
    simpa [this] using And.intro hu0 hu1
  rw [bosonTotal_mean_eq hu]
  simp [List.get_eq_getElem, nsmul_eq_mul]

/-- The grand-canonical BE law for a degenerate level, from the joint state sum. -/
theorem bosonTotal_mean_exponential (g : ℕ) {β E μ : ℝ} (hβ : 0 < β) (hμ : μ < E) :
    bosonTotalMean (List.replicate g (fugacity β E μ)) =
      (g : ℝ) / (Real.exp (β * (E - μ)) - 1) := by
  rw [bosonTotal_mean_degeneracy g (le_of_lt (fugacity_pos β E μ)) (fugacity_lt_one hβ hμ),
    boson_mean_exponential hβ hμ]
  ring

#print axioms bosonCoordinateMoment_hasSum
#print axioms bosonCoordinate_mean_eq
#print axioms bosonTotal_mean_eq
#print axioms bosonTotal_mean_degeneracy
#print axioms bosonTotal_mean_exponential

end QuantumOccupations
