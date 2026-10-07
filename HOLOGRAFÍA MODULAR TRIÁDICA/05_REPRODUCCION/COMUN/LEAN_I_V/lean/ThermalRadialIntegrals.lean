import ThermalEnvelopes
import RadialMeasure
import ThermalDensities

/-!
# Radial integrals of the three literal thermal observables

This module composes the already proved bosonic moments with the observables
of `71_limite_termodinamico.tex`. The positive radial integral yields genuine
integrability in three-dimensional coordinate space through `RadialMeasure`;
neither radial nor three-dimensional integrability is an assumed field.
-/

noncomputable section
open Set MeasureTheory

namespace HMT.V.ThermodynamicLimit

open HMT.V.BosonicMoments

def thermalRadialIntegral (a b : ℝ) (kind : ThermalKind) : ℝ :=
  ∫ r in Ioi (0 : ℝ), r ^ 2 * thermalObservable a b kind r

theorem thermal_radial_integral_number {a b : ℝ} (ha : 0 < a) :
    thermalRadialIntegral a b .number = 2 * zetaSeries 3 / a ^ 3 := by
  simpa only [thermalRadialIntegral, thermalObservable, FN, occupation, one_div] using
    scaled_number_integral ha

theorem thermal_radial_integral_energy {a b : ℝ} (ha : 0 < a) :
    thermalRadialIntegral a b .energy = b * Real.pi ^ 4 / (15 * a ^ 4) := by
  have hf : (fun r : ℝ => r ^ 2 * thermalObservable a b .energy r) =
      fun r => b * (r ^ 3 * occupation (a * r)) := by
    ext r
    dsimp [thermalObservable, FE, occupation]
    ring
  rw [thermalRadialIntegral, hf, integral_const_mul, scaled_energy_integral ha]
  ring

theorem thermal_radial_integral_partition {a b : ℝ} (ha : 0 < a) :
    thermalRadialIntegral a b .partition = Real.pi ^ 4 / (45 * a ^ 3) := by
  have hf : (fun r : ℝ => r ^ 2 * thermalObservable a b .partition r) =
      fun r => -r ^ 2 * Real.log (1 - Real.exp (-(a * r))) := by
    ext r
    simp only [thermalObservable, FZ, neg_mul, mul_neg]
  rw [thermalRadialIntegral, hf, scaled_partition_integral ha]

theorem thermal_radial_integral_number_riemannZeta {a b : ℝ} (ha : 0 < a) :
    thermalRadialIntegral a b .number = 2 * (riemannZeta 3).re / a ^ 3 := by
  rw [thermal_radial_integral_number ha]
  have h := riemannZeta_real_eq_series (s := 3) (by norm_num)
  norm_num only [Complex.ofReal_ofNat] at h
  rw [h, Complex.ofReal_re]

theorem thermal_radial_integral_pos {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) : 0 < thermalRadialIntegral a b kind := by
  cases kind
  · rw [thermal_radial_integral_number ha]
    exact div_pos (mul_pos (by norm_num) (zetaSeries_pos (by norm_num))) (pow_pos ha 3)
  · rw [thermal_radial_integral_energy ha]
    positivity
  · rw [thermal_radial_integral_partition ha]
    positivity

theorem thermal_radial_integral_ne_zero {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) : thermalRadialIntegral a b kind ≠ 0 :=
  (thermal_radial_integral_pos ha hb kind).ne'

theorem thermal_radial_integrable {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) :
    IntegrableOn (fun r : ℝ => r ^ 2 * thermalObservable a b kind r) (Ioi 0) :=
  Integrable.of_integral_ne_zero (thermal_radial_integral_ne_zero ha hb kind)

theorem thermal_coordinate_integrable {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) :
    Integrable (fun x : CoordinateSpace => thermalObservable a b kind (euclideanRadius x)) :=
  coordinate_radial_integrable (thermal_radial_integral_ne_zero ha hb kind)

theorem thermal_coordinate_integral {a b : ℝ} (kind : ThermalKind) :
    (∫ x : CoordinateSpace, thermalObservable a b kind (euclideanRadius x)) =
      4 * Real.pi * thermalRadialIntegral a b kind :=
  coordinate_radial_integral (thermalObservable a b kind)

theorem thermal_coordinate_integral_pos {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (kind : ThermalKind) :
    0 < ∫ x : CoordinateSpace, thermalObservable a b kind (euclideanRadius x) := by
  rw [thermal_coordinate_integral]
  exact mul_pos (mul_pos (by norm_num) Real.pi_pos) (thermal_radial_integral_pos ha hb kind)

#print axioms thermal_radial_integral_number
#print axioms thermal_radial_integral_energy
#print axioms thermal_radial_integral_partition
#print axioms thermal_radial_integral_number_riemannZeta
#print axioms thermal_radial_integral_pos
#print axioms thermal_radial_integral_ne_zero
#print axioms thermal_radial_integrable
#print axioms thermal_coordinate_integrable
#print axioms thermal_coordinate_integral
#print axioms thermal_coordinate_integral_pos

end HMT.V.ThermodynamicLimit
