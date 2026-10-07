import Mathlib
import BosonGibbsMean

/-!
# The Planck density from the actual bosonic Gibbs expectation

The radial density is the declared three-dimensional two-polarization reading.
This file does not assert a periodic-lattice thermodynamic-limit theorem.
The constant mode is outside the positive-energy domain before occupation is formed.
-/

noncomputable section

namespace HMT.V.Radiation

open scoped BigOperators

/-- The actual countable Gibbs mean, with chemical potential zero and one energy. -/
def modeOccupation (β E : ℝ) : ℝ :=
  QuantumOccupations.bosonGibbsMeanNumber β 0 [E]

theorem modeOccupation_eq {β E : ℝ} (hβ : 0 < β) (hE : 0 < E) :
    modeOccupation β E = 1 / (Real.exp (β * E) - 1) := by
  simpa [modeOccupation] using QuantumOccupations.bosonGibbsMeanNumber_degenerate 1 hβ hE

theorem modeGibbs_normalized {β E : ℝ} (hβ : 0 < β) (hE : 0 < E) :
    HasSum (QuantumOccupations.bosonGibbsProbability β 0 [E]) 1 := by
  apply QuantumOccupations.bosonGibbs_probability_hasSum hβ
  simpa using hE

/-- Declared radial density per volume and per angular frequency, including two polarizations. -/
def angularModeDensity (c ω : ℝ) : ℝ := ω ^ 2 / (Real.pi ^ 2 * c ^ 3)

/-- Composition of the radial reading, positive excitation energy, and Gibbs mean. -/
def angularEnergyDensity (β hbar c ω : ℝ) : ℝ :=
  angularModeDensity c ω * (hbar * ω) * modeOccupation β (hbar * ω)

theorem angularEnergyDensity_eq {β hbar c ω : ℝ}
    (hβ : 0 < β) (hh : 0 < hbar) (hω : 0 < ω) :
    angularEnergyDensity β hbar c ω =
      hbar * ω ^ 3 / (Real.pi ^ 2 * c ^ 3) *
        (1 / (Real.exp (β * hbar * ω) - 1)) := by
  unfold angularEnergyDensity
  rw [modeOccupation_eq hβ (mul_pos hh hω)]
  unfold angularModeDensity
  rw [mul_assoc β hbar ω]
  ring

theorem angularEnergyDensity_eq_div {β hbar c ω : ℝ}
    (hβ : 0 < β) (hh : 0 < hbar) (hω : 0 < ω) :
    angularEnergyDensity β hbar c ω =
      (hbar / (Real.pi ^ 2 * c ^ 3)) *
        (ω ^ 3 / (Real.exp ((β * hbar) * ω) - 1)) := by
  rw [angularEnergyDensity_eq hβ hh hω]
  ring

theorem angularEnergyDensity_pos {β hbar c ω : ℝ}
    (hβ : 0 < β) (hh : 0 < hbar) (hc : 0 < c) (hω : 0 < ω) :
    0 < angularEnergyDensity β hbar c ω := by
  rw [angularEnergyDensity_eq hβ hh hω]
  have hexp : 0 < Real.exp (β * hbar * ω) - 1 := by
    have := Real.one_lt_exp_iff.mpr (mul_pos (mul_pos hβ hh) hω)
    linarith
  exact mul_pos (div_pos (mul_pos hh (pow_pos hω 3))
    (mul_pos (pow_pos Real.pi_pos 2) (pow_pos hc 3))) (div_pos (by norm_num) hexp)

/-- Angular-to-frequency conversion, including the isotropic radiance factor and Jacobian. -/
def frequencyRadiance (β h c ν : ℝ) : ℝ :=
  (c / (4 * Real.pi)) *
    angularEnergyDensity β (h / (2 * Real.pi)) c (2 * Real.pi * ν) * (2 * Real.pi)

theorem frequencyRadiance_eq {β h c ν : ℝ}
    (hβ : 0 < β) (hh : 0 < h) (hc : 0 < c) (hν : 0 < ν) :
    frequencyRadiance β h c ν =
      2 * h * ν ^ 3 / c ^ 2 * (1 / (Real.exp (β * h * ν) - 1)) := by
  unfold frequencyRadiance
  rw [angularEnergyDensity_eq hβ (div_pos hh (mul_pos (by norm_num) Real.pi_pos))
    (mul_pos (mul_pos (by norm_num) Real.pi_pos) hν)]
  have he : β * (h / (2 * Real.pi)) * (2 * Real.pi * ν) = β * h * ν := by
    field_simp
    ring
  rw [he]
  have hden : Real.exp (β * h * ν) - 1 ≠ 0 :=
    ne_of_gt (sub_pos.mpr (Real.one_lt_exp_iff.mpr (mul_pos (mul_pos hβ hh) hν)))
  field_simp [Real.pi_ne_zero, ne_of_gt hc, hden]
  ring

theorem frequencyToWavelength_hasDerivAt (c : ℝ) {wave : ℝ} (hw : 0 < wave) :
    HasDerivAt (fun l : ℝ => c / l) (-c / wave ^ 2) wave := by
  convert (hasDerivAt_const wave c).div (hasDerivAt_id wave) (ne_of_gt hw) using 1
  simp

theorem wavelength_jacobian {c wave : ℝ} (hc : 0 < c) (hw : 0 < wave) :
    |deriv (fun l : ℝ => c / l) wave| = c / wave ^ 2 := by
  rw [(frequencyToWavelength_hasDerivAt c hw).deriv, neg_div, abs_neg,
    abs_of_pos (div_pos hc (pow_pos hw 2))]

/-- A density transformation with its actual derivative, not just argument substitution. -/
def wavelengthRadiance (β h c wave : ℝ) : ℝ :=
  frequencyRadiance β h c (c / wave) * |deriv (fun l : ℝ => c / l) wave|

theorem wavelengthRadiance_eq {β h c wave : ℝ}
    (hβ : 0 < β) (hh : 0 < h) (hc : 0 < c) (hw : 0 < wave) :
    wavelengthRadiance β h c wave =
      2 * h * c ^ 2 / wave ^ 5 * (1 / (Real.exp (β * h * c / wave) - 1)) := by
  unfold wavelengthRadiance
  rw [frequencyRadiance_eq hβ hh hc (div_pos hc hw), wavelength_jacobian hc hw]
  rw [show β * h * (c / wave) = β * h * c / wave by ring]
  have hden : Real.exp (β * h * c / wave) - 1 ≠ 0 :=
    ne_of_gt (sub_pos.mpr (Real.one_lt_exp_iff.mpr (div_pos (mul_pos (mul_pos hβ hh) hc) hw)))
  field_simp [ne_of_gt hc, ne_of_gt hw, hden]
  ring

#print axioms modeOccupation_eq
#print axioms modeGibbs_normalized
#print axioms angularEnergyDensity_eq
#print axioms angularEnergyDensity_eq_div
#print axioms angularEnergyDensity_pos
#print axioms frequencyRadiance_eq
#print axioms wavelength_jacobian
#print axioms wavelengthRadiance_eq

end HMT.V.Radiation
