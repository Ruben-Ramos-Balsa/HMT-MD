import NaturalMeshLimit
import PeriodicRealScale

/-!
Complete formalization of `v:lem:limite-termodinamico` for all three
observables, at arbitrary real positive box lengths tending to infinity.
The mode zero is excluded before forming the infinite sum. The limit is a
conclusion, not an axiom, a structure field, or a premise of these theorems.
-/

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.ThermodynamicLimit

theorem excitation_tsum_eq_nonzero (F : ℝ → ℝ) (Δ : ℝ) :
    (∑' ν : Lattice, excitationValue F Δ ν) =
      ∑' ν : {ν : Lattice // ν ≠ 0}, F (Δ * radius ν) := by
  have heq : excitationValue F Δ =
      ({ν : Lattice | ν ≠ 0} : Set Lattice).indicator (fun ν => F (Δ * radius ν)) := by
    funext ν
    by_cases hν : ν = 0 <;> simp [excitationValue, Set.indicator_apply, hν]
  rw [heq, ← tsum_subtype]
  rfl

theorem thermal_periodic_limit {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) :
    Tendsto (periodicOccupationDensity (thermalObservable a b kind)) atTop
      (𝓝 ((1 / Real.pi ^ 2) * thermalRadialIntegral a b kind)) := by
  apply thermal_periodic_limit_of_natural ha hb kind
  convert thermal_natural_mesh_limit ha hb kind using 1
  funext n
  dsimp [inverseMeshSum, meshLatticeSum]
  ring

/-- Literal nonzero-lattice form of the manuscript's thermodynamic-limit lemma. -/
theorem thermal_periodic_limit_nonzero {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) :
    Tendsto (fun L : ℝ => 2 / L^3 *
      ∑' ν : {ν : Lattice // ν ≠ 0},
        thermalObservable a b kind ((2*Real.pi/L) * radius ν)) atTop
      (𝓝 ((1 / Real.pi^2) *
        ∫ r in Ioi (0 : ℝ), r^2 * thermalObservable a b kind r)) := by
  apply (thermal_periodic_limit ha hb kind).congr'
  filter_upwards [] with L
  exact congrArg (fun z => 2 / L^3 * z)
    (excitation_tsum_eq_nonzero (thermalObservable a b kind) (2*Real.pi/L))

theorem thermal_periodic_sums_finite {a b L : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hL : 0 < L) (kind : ThermalKind) :
    Summable (fun ν : {ν : Lattice // ν ≠ 0} =>
      thermalObservable a b kind ((2*Real.pi/L) * radius ν)) := by
  apply excitation_subtype_summable (tailConstant_pos ha hb).le (decayRate_pos ha)
    (by positivity) (fun r hr => (thermal_pos ha hb hr kind).le)
  intro r hr
  simpa only [neg_mul] using thermal_tail ha hb hr kind

theorem periodic_number_density_limit {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Tendsto (periodicOccupationDensity (thermalObservable a b .number)) atTop
      (𝓝 (2 * HMT.V.BosonicMoments.zetaSeries 3 / (Real.pi^2 * a^3))) := by
  have h := thermal_periodic_limit ha hb ThermalKind.number
  rw [thermal_radial_integral_number ha] at h
  convert h using 1
  congr 1
  ring

theorem periodic_energy_density_limit {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Tendsto (periodicOccupationDensity (thermalObservable a b .energy)) atTop
      (𝓝 (b * Real.pi^2 / (15*a^4))) := by
  have h := thermal_periodic_limit ha hb ThermalKind.energy
  rw [thermal_radial_integral_energy ha] at h
  convert h using 1
  congr 1
  field_simp [Real.pi_ne_zero, ha.ne']
  ring

theorem periodic_log_partition_density_limit {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Tendsto (periodicOccupationDensity (thermalObservable a b .partition)) atTop
      (𝓝 (Real.pi^2 / (45*a^3))) := by
  have h := thermal_periodic_limit ha hb ThermalKind.partition
  rw [thermal_radial_integral_partition ha] at h
  convert h using 1
  congr 1
  field_simp [Real.pi_ne_zero, ha.ne']
  ring

#print axioms excitation_tsum_eq_nonzero
#print axioms thermal_periodic_limit
#print axioms thermal_periodic_limit_nonzero
#print axioms thermal_periodic_sums_finite
#print axioms periodic_number_density_limit
#print axioms periodic_energy_density_limit
#print axioms periodic_log_partition_density_limit

end HMT.V.ThermodynamicLimit
