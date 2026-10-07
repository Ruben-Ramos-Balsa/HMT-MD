import QuantumOccupations

/-!
# Bosonic grand-canonical factorization over finitely many modes

The number of modes is finite, but every mode admits all natural-number
occupations. The partition function is an actual convergent sum over that
infinite product state space. It is not defined as a product of modal factors.
-/

noncomputable section

namespace QuantumOccupations

def BosonStates : ℕ → Type
  | 0 => Unit
  | n + 1 => ℕ × BosonStates n

def bosonStateWeight : (us : List ℝ) → BosonStates us.length → ℝ
  | [], _ => 1
  | u :: us, s => u ^ s.1 * bosonStateWeight us s.2

def bosonFactors : List ℝ → ℝ
  | [] => 1
  | u :: us => (1 - u)⁻¹ * bosonFactors us

def BosonAdmissible (us : List ℝ) : Prop := ∀ u ∈ us, 0 ≤ u ∧ u < 1

def bosonManyPartition (us : List ℝ) : ℝ := ∑' s, bosonStateWeight us s

def bosonManyProbability (us : List ℝ) (s : BosonStates us.length) : ℝ :=
  bosonStateWeight us s / bosonManyPartition us

theorem bosonFactors_eq_product (us : List ℝ) :
    bosonFactors us = (us.map (fun u => (1 - u)⁻¹)).prod := by
  induction us with
  | nil => rfl
  | cons u us ih => simp only [bosonFactors, List.map_cons, List.prod_cons, ih]

theorem bosonFactors_pos {us : List ℝ} (hu : BosonAdmissible us) :
    0 < bosonFactors us := by
  induction us with
  | nil => exact zero_lt_one
  | cons u us ih =>
    apply mul_pos (inv_pos.mpr (sub_pos.mpr (hu u (by simp)).2))
    apply ih
    intro v hv
    exact hu v (by simp [hv])

theorem bosonStateWeight_nonneg {us : List ℝ} (hu : BosonAdmissible us)
    (s : BosonStates us.length) : 0 ≤ bosonStateWeight us s := by
  induction us with
  | nil => exact zero_le_one
  | cons u us ih =>
    exact mul_nonneg (pow_nonneg (hu u (by simp)).1 s.1)
      (ih (fun v hv => hu v (by simp [hv])) s.2)

/-- The infinite sum over every finite tuple of occupations converges and factorizes. -/
theorem bosonManyWeight_hasSum {us : List ℝ} (hu : BosonAdmissible us) :
    HasSum (bosonStateWeight us) (bosonFactors us) := by
  induction us with
  | nil => simp [bosonStateWeight, bosonFactors, BosonStates]
  | cons u us ih =>
    have hhead := boson_weight_hasSum (hu u (by simp)).1 (hu u (by simp)).2
    have htail := ih (fun v hv => hu v (by simp [hv]))
    have hmul := hhead.summable.mul_of_nonneg htail.summable
      (fun n => pow_nonneg (hu u (by simp)).1 n)
      (fun s => bosonStateWeight_nonneg (fun v hv => hu v (by simp [hv])) s)
    exact hhead.mul htail hmul

theorem bosonMany_partition_factors {us : List ℝ} (hu : BosonAdmissible us) :
    bosonManyPartition us = bosonFactors us := (bosonManyWeight_hasSum hu).tsum_eq

theorem bosonMany_partition_eq {us : List ℝ} (hu : BosonAdmissible us) :
    bosonManyPartition us = (us.map (fun u => (1 - u)⁻¹)).prod := by
  exact (bosonManyWeight_hasSum hu).tsum_eq.trans (bosonFactors_eq_product us)

theorem bosonMany_partition_pos {us : List ℝ} (hu : BosonAdmissible us) :
    0 < bosonManyPartition us := by
  rw [bosonMany_partition_factors hu]
  exact bosonFactors_pos hu

theorem bosonMany_probability_nonneg {us : List ℝ} (hu : BosonAdmissible us)
    (s : BosonStates us.length) : 0 ≤ bosonManyProbability us s :=
  div_nonneg (bosonStateWeight_nonneg hu s) (le_of_lt (bosonMany_partition_pos hu))

theorem bosonMany_probability_hasSum {us : List ℝ} (hu : BosonAdmissible us) :
    HasSum (bosonManyProbability us) 1 := by
  have h := (bosonManyWeight_hasSum hu).div_const (bosonManyPartition us)
  rw [← bosonMany_partition_factors hu,
    div_self (ne_of_gt (bosonMany_partition_pos hu))] at h
  exact h

/-- Expectation of the first occupation in the complete multimode probability distribution. -/
def bosonHeadMean (u : ℝ) (us : List ℝ) : ℝ :=
  ∑' s : BosonStates (u :: us).length, (s.1 : ℝ) * bosonManyProbability (u :: us) s

theorem bosonHeadMoment_hasSum {u : ℝ} {us : List ℝ} (hu : BosonAdmissible (u :: us)) :
    HasSum (fun s : BosonStates (u :: us).length => (s.1 : ℝ) * bosonStateWeight (u :: us) s)
      ((u / (1 - u) ^ 2) * bosonFactors us) := by
  have hhead := boson_firstMoment_hasSum (hu u (by simp)).1 (hu u (by simp)).2
  have htail : HasSum (bosonStateWeight us) (bosonFactors us) :=
    bosonManyWeight_hasSum (fun v hv => hu v (by simp [hv]))
  have hmul := hhead.summable.mul_of_nonneg htail.summable
    (fun n => mul_nonneg (Nat.cast_nonneg n) (pow_nonneg (hu u (by simp)).1 n))
    (fun s => bosonStateWeight_nonneg (us := us) (fun v hv => hu v (by simp [hv])) s)
  simpa only [bosonStateWeight, bosonWeight, mul_assoc] using hhead.mul htail hmul

/-- The joint distribution has the proved single-mode mean as its marginal expectation. -/
theorem bosonHead_mean_eq {u : ℝ} {us : List ℝ} (hu : BosonAdmissible (u :: us)) :
    bosonHeadMean u us = bosonMean u := by
  have h := (bosonHeadMoment_hasSum hu).div_const (bosonManyPartition (u :: us))
  have htail : BosonAdmissible us := fun v hv => hu v (by simp [hv])
  have hd : 1 - u ≠ 0 := ne_of_gt (sub_pos.mpr (hu u (by simp)).2)
  have hp : bosonFactors us ≠ 0 := ne_of_gt (bosonFactors_pos htail)
  have hv : ((u / (1 - u) ^ 2) * bosonFactors us) / bosonManyPartition (u :: us) =
      u / (1 - u) := by
    rw [bosonMany_partition_factors hu]
    simp only [bosonFactors]
    field_simp
    ring
  rw [hv] at h
  rw [boson_mean_eq (hu u (by simp)).1 (hu u (by simp)).2]
  exact (by simpa only [bosonManyProbability, div_eq_mul_inv, mul_assoc] using h.tsum_eq)

/-- Degeneracy is repeated modal weight in the actual infinite state sum. -/
theorem boson_partition_degeneracy (g : ℕ) {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    bosonManyPartition (List.replicate g u) = ((1 - u)⁻¹) ^ g := by
  have hu : BosonAdmissible (List.replicate g u) := by
    intro v hv
    have : v = u := List.eq_of_mem_replicate hv
    simpa [this] using And.intro hu0 hu1
  rw [bosonMany_partition_eq hu]
  simp

def thermalWeights (β μ : ℝ) (energies : List ℝ) : List ℝ :=
  energies.map (fun E => fugacity β E μ)

theorem thermalWeights_admissible {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    BosonAdmissible (thermalWeights β μ energies) := by
  intro u hu
  obtain ⟨E, hE, rfl⟩ := List.mem_map.mp hu
  exact ⟨le_of_lt (fugacity_pos β E μ), fugacity_lt_one hβ (hμ E hE)⟩

/-- Grand-canonical Bose factorization on any finite list of energies. -/
theorem boson_grandCanonical_factorization {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    bosonManyPartition (thermalWeights β μ energies) =
      (energies.map (fun E => (1 - Real.exp (-(β * (E - μ))))⁻¹)).prod := by
  rw [bosonMany_partition_eq (thermalWeights_admissible hβ hμ)]
  simp [thermalWeights, fugacity, List.map_map, Function.comp_def]

#print axioms bosonManyWeight_hasSum
#print axioms bosonMany_partition_eq
#print axioms bosonMany_probability_hasSum
#print axioms bosonHead_mean_eq
#print axioms boson_partition_degeneracy
#print axioms boson_grandCanonical_factorization

end QuantumOccupations
