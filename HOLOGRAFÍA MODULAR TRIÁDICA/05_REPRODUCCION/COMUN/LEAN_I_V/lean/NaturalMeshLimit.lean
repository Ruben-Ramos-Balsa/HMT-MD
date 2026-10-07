import AnnularLatticeEstimate
import AnnularExhaustion
import CutoffError
import ThermalRadialIntegrals

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.ThermodynamicLimit

/-- The complete natural-mesh lattice limit. No convergence or lattice-tail
estimate is an input: both are derived from scalar envelopes and continuity. -/
theorem natural_mesh_limit {F : ℝ → ℝ} {C₀ C₁ d : ℝ}
    (hC₀ : 0 ≤ C₀) (hC₁ : 0 ≤ C₁) (hd : 0 < d)
    (hcont : ContinuousOn F (Ioi 0)) (hF : ∀ r, 0 < r → 0 ≤ F r)
    (horigin : ∀ r, 0 < r → r ≤ 1 → F r ≤ C₀ / r)
    (htail : ∀ r, 1 ≤ r → F r ≤ C₁ * Real.exp (-(d*r)))
    (hfi : Integrable (fun x : CoordinateSpace => F (euclideanRadius x))) :
    Tendsto (fun n : ℕ => meshLatticeSum F (1 / (n : ℝ))) atTop
      (𝓝 (∫ x : CoordinateSpace, F (euclideanRadius x))) := by
  apply tendsto_of_annular_approximation
    (A := fun j n => meshAnnularSum F (1/(n : ℝ)) (1/(j+1 : ℝ)) (j+1))
    (I := fun j => ∫ x in annularExhaustion j, F (euclideanRadius x))
  · intro j
    have h := annular_discrete_tendsto hcont
      (by positivity : (0 : ℝ) < 1 / (j+1 : ℝ)) (j+1)
    apply h.congr'
    filter_upwards [eventually_gt_atTop (0 : ℕ)] with n hn
    exact (scaled_annularValue_tsum F hn (by positivity) (j+1)).symm
  · exact annular_integrals_tendsto hfi
  · intro ε hε
    obtain ⟨j₀, hj₀⟩ := Filter.eventually_atTop.1
      ((tendsto_order.1 (annularErrorBound_tendsto C₀ C₁ hd)).2 ε hε)
    refine ⟨max j₀ 1, fun j hj => ?_⟩
    filter_upwards [eventually_ge_atTop (1 : ℕ)] with n hn
    have hn' : (1 : ℝ) ≤ n := by exact_mod_cast hn
    have hnp : (0 : ℝ) < n := lt_of_lt_of_le zero_lt_one hn'
    have hΔ : (0 : ℝ) < 1/(n : ℝ) := by positivity
    have hΔ1 : 1/(n : ℝ) ≤ 1 := (div_le_one hnp).2 hn'
    have hj1 : 1 ≤ j := (le_max_right _ _).trans hj
    have hsum := excitation_summable hC₁ hd hΔ hF htail
    have hb := annular_remainder_bound hΔ hΔ1 (by positivity : (0 : ℝ) < 1/(j+1 : ℝ))
      (exhaustion_inner_small hj1)
      (by have h := (Nat.cast_nonneg j : (0 : ℝ) ≤ j); linarith : (1 : ℝ) ≤ j+1)
      hC₀ hC₁ hd hF horigin htail hsum
    exact hb.trans_lt (hj₀ j ((le_max_left _ _).trans hj))

theorem thermal_natural_mesh_limit {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) :
    Tendsto (fun n : ℕ => meshLatticeSum (thermalObservable a b kind) (1/(n : ℝ)))
      atTop (𝓝 (∫ x : CoordinateSpace, thermalObservable a b kind (euclideanRadius x))) := by
  apply natural_mesh_limit (originConstant_pos ha hb).le (tailConstant_pos ha hb).le
    (decayRate_pos ha) (thermal_continuousOn ha kind)
  · exact fun r hr => (thermal_pos ha hb hr kind).le
  · exact fun r hr hr1 => thermal_origin ha hb hr hr1 kind
  · intro r hr
    simpa only [neg_mul] using thermal_tail ha hb hr kind
  · exact thermal_coordinate_integrable ha hb kind

#print axioms natural_mesh_limit
#print axioms thermal_natural_mesh_limit

end HMT.V.ThermodynamicLimit
