import AnnularRiemann
import Mathlib.MeasureTheory.Integral.Bochner.Set

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.ThermodynamicLimit

def annularExhaustion (j : ℕ) : Set CoordinateSpace :=
  cubicAnnulus (1 / (j + 1 : ℝ)) (j + 1)

lemma annularExhaustion_mono : Monotone annularExhaustion := by
  intro j k hjk x hx
  have hx' := (mem_cubicAnnulus x _ _).1 hx
  apply (mem_cubicAnnulus x _ _).2
  constructor
  · exact (one_div_le_one_div_of_le (by positivity) (by exact_mod_cast Nat.add_le_add_right hjk 1)).trans hx'.1
  · exact hx'.2.trans (by exact_mod_cast Nat.add_le_add_right hjk 1)

lemma annularExhaustion_union : (⋃ j, annularExhaustion j) = ({0} : Set CoordinateSpace)ᶜ := by
  ext x
  simp only [Set.mem_iUnion, Set.mem_compl_iff, Set.mem_singleton_iff]
  constructor
  · rintro ⟨j, hj⟩ hzero
    have h := ((mem_cubicAnnulus x _ _).1 hj).1
    rw [hzero, norm_zero] at h
    exact (not_le_of_gt (by positivity : 0 < 1 / (j + 1 : ℝ))) h
  · intro hx
    have hnx : 0 < ‖x‖ := norm_pos_iff.2 hx
    obtain ⟨j, hj⟩ := exists_nat_gt (max ‖x‖ (1 / ‖x‖))
    refine ⟨j, (mem_cubicAnnulus x _ _).2 ⟨?_, ?_⟩⟩
    · have hjinv : 1 / ‖x‖ ≤ (j : ℝ) + 1 := by
        have := (le_max_right ‖x‖ (1 / ‖x‖)).trans_lt hj
        linarith
      have hprod := (div_le_iff₀ hnx).1 hjinv
      exact (div_le_iff₀ (by positivity : (0 : ℝ) < j + 1)).2 (by nlinarith)
    · have := (le_max_left ‖x‖ (1 / ‖x‖)).trans_lt hj
      linarith

theorem annular_integrals_tendsto {f : CoordinateSpace → ℝ} (hf : Integrable f) :
    Tendsto (fun j => ∫ x in annularExhaustion j, f x) atTop (𝓝 (∫ x, f x)) := by
  have h := tendsto_setIntegral_of_monotone
    (s := annularExhaustion)
    (fun j : ℕ => cubicAnnulus_measurable (1 / (j + 1 : ℝ)) (j + 1))
    annularExhaustion_mono (hf.integrableOn (s := ⋃ j, annularExhaustion j))
  simpa only [annularExhaustion_union, restrict_compl_singleton] using h

/-- A proved epsilon argument for removing a uniformly small truncation.
The approximation hypotheses must be discharged for the actual lattice sums.
-/
theorem tendsto_of_annular_approximation {S : ℕ → ℝ} {A : ℕ → ℕ → ℝ}
    {I : ℕ → ℝ} {L : ℝ}
    (hA : ∀ j, Tendsto (A j) atTop (𝓝 (I j)))
    (hI : Tendsto I atTop (𝓝 L))
    (herror : ∀ ε > 0, ∃ j₀, ∀ j ≥ j₀,
      ∀ᶠ n in atTop, |S n - A j n| < ε) :
    Tendsto S atTop (𝓝 L) := by
  apply Metric.tendsto_atTop.2
  intro ε hε
  have hthird : 0 < ε / 3 := by positivity
  obtain ⟨j₀, hj₀⟩ := herror (ε / 3) hthird
  obtain ⟨j₁, hj₁⟩ := Metric.tendsto_atTop.1 hI (ε / 3) hthird
  let j := max j₀ j₁
  have hji : |I j - L| < ε / 3 := by
    simpa only [Real.dist_eq] using hj₁ j (le_max_right _ _)
  have hsa := hj₀ j (le_max_left _ _)
  have hai := Metric.tendsto_atTop.1 (hA j) (ε / 3) hthird
  obtain ⟨n₀, hn₀⟩ := hai
  obtain ⟨n₁, hn₁⟩ := Filter.eventually_atTop.1 hsa
  refine ⟨max n₀ n₁, fun n hn => ?_⟩
  have h1 := hn₀ n ((le_max_left _ _).trans hn)
  have h2 := hn₁ n ((le_max_right _ _).trans hn)
  have heq : S n - L = (S n - A j n) + (A j n - I j) + (I j - L) := by ring
  rw [Real.dist_eq, heq]
  have htri := abs_add_le ((S n - A j n) + (A j n - I j)) (I j - L)
  have htri' := abs_add_le (S n - A j n) (A j n - I j)
  rw [Real.dist_eq] at h1
  linarith

#print axioms annular_integrals_tendsto
#print axioms tendsto_of_annular_approximation

end HMT.V.ThermodynamicLimit
