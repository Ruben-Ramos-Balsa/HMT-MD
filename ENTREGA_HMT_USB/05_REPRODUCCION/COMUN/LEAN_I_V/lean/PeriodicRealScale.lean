import RealMeshLimit
import LatticeSummabilityTail
import ThermalRadialIntegrals

/-!
# From natural reciprocal meshes to arbitrary periodic lengths

The real-scale limit is derived from a natural-mesh limit, not assumed.
Monotonicity is proved for the actual zero-excluded lattice `tsum` from
antitonicity of the radial profile and summability at positive meshes.
The thermal specialization discharges those two analytic hypotheses.
-/

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.ThermodynamicLimit

def inverseMeshSum (F : ℝ → ℝ) (t : ℝ) : ℝ :=
  ∑' nu : Lattice, excitationValue F (1 / t) nu

def periodicOccupationDensity (F : ℝ → ℝ) (L : ℝ) : ℝ :=
  2 / L ^ 3 * ∑' nu : Lattice, excitationValue F (2 * Real.pi / L) nu

theorem inverseMeshSum_monotoneOn {F : ℝ → ℝ}
    (hanti : AntitoneOn F (Ioi 0))
    (hsum : ∀ delta : ℝ, 0 < delta → Summable (excitationValue F delta)) :
    MonotoneOn (inverseMeshSum F) (Ioi 0) := by
  intro s hs t ht hst
  apply (hsum (1 / s) (one_div_pos.mpr hs)).tsum_le_tsum _
    (hsum (1 / t) (one_div_pos.mpr ht))
  intro nu
  unfold excitationValue
  split_ifs with hnu
  · rfl
  · have hr : 0 < radius nu := (radius_pos_iff nu).mpr hnu
    apply hanti (mul_pos (one_div_pos.mpr ht) hr) (mul_pos (one_div_pos.mpr hs) hr)
    exact mul_le_mul_of_nonneg_right (one_div_le_one_div_of_le hs hst) hr.le

theorem periodic_limit_of_natural {F : ℝ → ℝ} {I : ℝ}
    (hanti : AntitoneOn F (Ioi 0))
    (hsum : ∀ delta : ℝ, 0 < delta → Summable (excitationValue F delta))
    (hnat : Tendsto (fun n : ℕ => inverseMeshSum F n / (n : ℝ) ^ 3) atTop (𝓝 I)) :
    Tendsto (periodicOccupationDensity F) atTop (𝓝 (I / (4 * Real.pi ^ 3))) := by
  have hreal := real_scale_limit_of_natural 3 (inverseMeshSum_monotoneOn hanti hsum) hnat
  have hscale : Tendsto (fun L : ℝ => L / (2 * Real.pi)) atTop atTop :=
    Tendsto.atTop_div_const (by positivity) tendsto_id
  have h := (hreal.comp hscale).div_const (4 * Real.pi ^ 3)
  apply h.congr'
  filter_upwards [eventually_gt_atTop (0 : ℝ)] with L hL
  simp only [Function.comp_apply]
  have hmesh : 1 / (L / (2 * Real.pi)) = 2 * Real.pi / L := by field_simp
  rw [inverseMeshSum, hmesh, periodicOccupationDensity]
  field_simp [Real.pi_ne_zero, hL.ne']
  ring

theorem periodic_limit_radial_of_natural {F : ℝ → ℝ}
    (hanti : AntitoneOn F (Ioi 0))
    (hsum : ∀ delta : ℝ, 0 < delta → Summable (excitationValue F delta))
    (hnat : Tendsto (fun n : ℕ => inverseMeshSum F n / (n : ℝ) ^ 3) atTop
      (𝓝 (∫ x : CoordinateSpace, F (euclideanRadius x)))) :
    Tendsto (periodicOccupationDensity F) atTop
      (𝓝 ((1 / Real.pi ^ 2) * ∫ r in Ioi (0 : ℝ), r ^ 2 * F r)) := by
  have h := periodic_limit_of_natural hanti hsum hnat
  rw [coordinate_radial_integral] at h
  convert h using 1
  congr 1
  field_simp [Real.pi_ne_zero]
  ring

theorem thermal_excitation_summable {a b delta : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hdelta : 0 < delta) (kind : ThermalKind) :
    Summable (excitationValue (thermalObservable a b kind) delta) := by
  apply excitation_summable (tailConstant_pos ha hb).le (decayRate_pos ha) hdelta
    (fun r hr => (thermal_pos ha hb hr kind).le)
  intro r hr
  simpa only [neg_mul] using thermal_tail ha hb hr kind

theorem thermal_inverseMeshSum_monotoneOn {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) : MonotoneOn (inverseMeshSum (thermalObservable a b kind)) (Ioi 0) :=
  inverseMeshSum_monotoneOn (thermal_antitoneOn ha hb kind)
    (fun _ hdelta => thermal_excitation_summable ha hb hdelta kind)

theorem thermal_periodic_limit_of_natural {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind)
    (hnat : Tendsto
      (fun n : ℕ => inverseMeshSum (thermalObservable a b kind) n / (n : ℝ) ^ 3) atTop
      (𝓝 (∫ x : CoordinateSpace, thermalObservable a b kind (euclideanRadius x)))) :
    Tendsto (periodicOccupationDensity (thermalObservable a b kind)) atTop
      (𝓝 ((1 / Real.pi ^ 2) * thermalRadialIntegral a b kind)) :=
  periodic_limit_radial_of_natural (thermal_antitoneOn ha hb kind)
    (fun _ hdelta => thermal_excitation_summable ha hb hdelta kind) hnat

#print axioms inverseMeshSum_monotoneOn
#print axioms periodic_limit_of_natural
#print axioms periodic_limit_radial_of_natural
#print axioms thermal_excitation_summable
#print axioms thermal_inverseMeshSum_monotoneOn
#print axioms thermal_periodic_limit_of_natural

end HMT.V.ThermodynamicLimit
