import BosonGibbs
import BosonOccupations

/-! Bose--Einstein total occupation directly in the additive-energy Gibbs distribution. -/

noncomputable section
namespace QuantumOccupations

open scoped BigOperators

def bosonParticleNumber : (n : ℕ) → BosonStates n → ℝ
  | 0, _ => 0
  | n + 1, s => (s.1 : ℝ) + bosonParticleNumber n s.2

theorem bosonParticleNumber_eq_sum (n : ℕ) (s : BosonStates n) :
    bosonParticleNumber n s =
      ∑ i : Fin n, (bosonStateOccupation n i s : ℝ) := by
  induction n with
  | zero => simp [bosonParticleNumber]
  | succ n ih =>
    rw [Fin.sum_univ_succ]
    simp only [bosonParticleNumber, bosonStateOccupation,
      Fin.cases_zero, Fin.cases_succ]
    rw [ih]

theorem bosonParticleNumber_reindex (β μ : ℝ) (energies : List ℝ)
    (s : BosonStates energies.length) :
    bosonParticleNumber (thermalWeights β μ energies).length
        (thermalStateEquiv β μ energies s) = bosonParticleNumber energies.length s := by
  induction energies with
  | nil => rfl
  | cons E energies ih =>
    change (s.1 : ℝ) + bosonParticleNumber (thermalWeights β μ energies).length
      (thermalStateEquiv β μ energies s.2) = (s.1 : ℝ) + bosonParticleNumber energies.length s.2
    rw [ih]

def bosonGibbsMeanNumber (β μ : ℝ) (energies : List ℝ) : ℝ :=
  ∑' s : BosonStates energies.length,
    bosonParticleNumber energies.length s * bosonGibbsProbability β μ energies s

theorem bosonGibbsMeanNumber_eq (β μ : ℝ) (energies : List ℝ) :
    bosonGibbsMeanNumber β μ energies = bosonTotalMean (thermalWeights β μ energies) := by
  unfold bosonGibbsMeanNumber bosonTotalMean
  calc
    _ = ∑' s : BosonStates energies.length,
        bosonParticleNumber (thermalWeights β μ energies).length
          (thermalStateEquiv β μ energies s) *
        bosonManyProbability (thermalWeights β μ energies) (thermalStateEquiv β μ energies s) := by
      apply tsum_congr
      intro s
      rw [bosonParticleNumber_reindex, bosonGibbs_probability_eq_many]
    _ = ∑' s : BosonStates (thermalWeights β μ energies).length,
        bosonParticleNumber (thermalWeights β μ energies).length s *
          bosonManyProbability (thermalWeights β μ energies) s :=
      (thermalStateEquiv β μ energies).tsum_eq
        (fun s => bosonParticleNumber (thermalWeights β μ energies).length s *
          bosonManyProbability (thermalWeights β μ energies) s)
    _ = _ := by
      apply tsum_congr
      intro s
      rw [bosonParticleNumber_eq_sum]

theorem bosonGibbsMeanNumber_hasSum {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    HasSum (fun s : BosonStates energies.length =>
      bosonParticleNumber energies.length s * bosonGibbsProbability β μ energies s)
      (∑ i : Fin (thermalWeights β μ energies).length,
        bosonMean ((thermalWeights β μ energies).get i)) := by
  have hadm := thermalWeights_admissible hβ hμ
  have h := hasSum_sum (s := Finset.univ)
    (fun i _ => bosonCoordinate_mean_hasSum hadm i)
  have hm : HasSum (fun s : BosonStates (thermalWeights β μ energies).length =>
      bosonParticleNumber (thermalWeights β μ energies).length s *
        bosonManyProbability (thermalWeights β μ energies) s)
      (∑ i : Fin (thermalWeights β μ energies).length,
        bosonMean ((thermalWeights β μ energies).get i)) := by
    simpa only [bosonParticleNumber_eq_sum, Finset.sum_mul] using h
  have transported := (thermalStateEquiv β μ energies).hasSum_iff.mpr hm
  simpa only [Function.comp_def, bosonParticleNumber_reindex,
    ← bosonGibbs_probability_eq_many] using transported

theorem sum_get_map (xs : List ℝ) (f : ℝ → ℝ) :
    (∑ i : Fin xs.length, f (xs.get i)) = (xs.map f).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    change (∑ i : Fin (xs.length + 1), f ((x :: xs).get i)) = _
    rw [Fin.sum_univ_succ]
    simpa only [List.get_cons_zero, List.get_cons_succ', List.map_cons,
      List.sum_cons] using congrArg (fun y => f x + y) ih

/-- Finite many-mode BE occupation from the convergent additive-energy Gibbs sum. -/
theorem bosonGibbsMeanNumber_exponential {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    bosonGibbsMeanNumber β μ energies =
      (energies.map (fun E => 1 / (Real.exp (β * (E - μ)) - 1))).sum := by
  unfold bosonGibbsMeanNumber
  rw [(bosonGibbsMeanNumber_hasSum hβ hμ).tsum_eq, sum_get_map]
  simp only [thermalWeights, List.map_map, Function.comp_def]
  congr 1
  apply List.map_congr_left
  intro E hE
  exact boson_mean_exponential hβ (hμ E hE)

/-- The degenerate-level law is an expectation in the Gibbs distribution itself. -/
theorem bosonGibbsMeanNumber_degenerate (g : ℕ) {β E μ : ℝ}
    (hβ : 0 < β) (hμ : μ < E) :
    bosonGibbsMeanNumber β μ (List.replicate g E) =
      (g : ℝ) / (Real.exp (β * (E - μ)) - 1) := by
  rw [bosonGibbsMeanNumber_eq]
  simpa only [thermalWeights, List.map_replicate] using
    bosonTotal_mean_exponential g hβ hμ

#print axioms bosonParticleNumber_eq_sum
#print axioms bosonGibbsMeanNumber_eq
#print axioms bosonGibbsMeanNumber_hasSum
#print axioms bosonGibbsMeanNumber_exponential
#print axioms bosonGibbsMeanNumber_degenerate

end QuantumOccupations
