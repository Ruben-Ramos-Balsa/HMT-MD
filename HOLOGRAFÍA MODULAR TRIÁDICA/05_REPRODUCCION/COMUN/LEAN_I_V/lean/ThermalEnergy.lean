import BosonicMoment
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

noncomputable section
open Set MeasureTheory Real

namespace HMT.V.BosonicMoments

theorem scaled_energy_integral {b : ℝ} (hb : 0 < b) :
    (∫ x in Ioi (0 : ℝ), x ^ 3 * occupation (b * x)) =
      Real.pi ^ 4 / (15 * b ^ 4) := by
  have h := integral_comp_mul_left_Ioi (fun x : ℝ => x ^ 3 * occupation x) 0 hb
  simp only [mul_zero, smul_eq_mul, energy_kernel_integral, mul_pow,
    mul_assoc, integral_const_mul] at h
  calc
    _ = (b ^ 3)⁻¹ * (b ^ 3 * (∫ x in Ioi (0 : ℝ), x ^ 3 * occupation (b * x))) := by
      rw [inv_mul_cancel_left₀ (pow_ne_zero _ hb.ne')]
    _ = (b ^ 3)⁻¹ * (b⁻¹ * (Real.pi ^ 4 / 15)) := by rw [h]
    _ = _ := by field_simp; ring

def energyProfile (c hbar beta omega : ℝ) : ℝ :=
  hbar * omega ^ 3 / (Real.pi ^ 2 * c ^ 3) * occupation (beta * hbar * omega)

def thermalEnergy (c hbar beta : ℝ) : ℝ :=
  ∫ omega in Ioi (0 : ℝ), energyProfile c hbar beta omega

theorem thermalEnergy_eq {c hbar beta : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (hb : 0 < beta) :
    thermalEnergy c hbar beta = Real.pi ^ 2 / (15 * c ^ 3 * hbar ^ 3 * beta ^ 4) := by
  have hf : energyProfile c hbar beta = fun x =>
      hbar / (Real.pi ^ 2 * c ^ 3) * (x ^ 3 * occupation ((beta * hbar) * x)) := by
    ext x
    dsimp [energyProfile]
    ring
  rw [thermalEnergy, hf, integral_const_mul, scaled_energy_integral (mul_pos hb hh)]
  field_simp [Real.pi_ne_zero, hc.ne', hh.ne', hb.ne']
  ring

theorem energyProfile_integrable {c hbar beta : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (hb : 0 < beta) :
    IntegrableOn (energyProfile c hbar beta) (Ioi 0) := by
  apply Integrable.of_integral_ne_zero
  change thermalEnergy c hbar beta ≠ 0
  rw [thermalEnergy_eq hc hh hb]
  positivity

def stefanCoefficient (c hbar kB : ℝ) : ℝ :=
  Real.pi ^ 2 * kB ^ 4 / (60 * hbar ^ 3 * c ^ 2)

def isotropicFlux (c hbar beta : ℝ) : ℝ :=
  c * thermalEnergy c hbar beta / 4

def angularFlux (c density : ℝ) : ℝ :=
  c * density / (4 * Real.pi) *
    (∫ _phi in (0 : ℝ)..(2 * Real.pi),
      ∫ theta in (0 : ℝ)..(Real.pi / 2), Real.cos theta * Real.sin theta)

theorem angularFlux_eq (c density : ℝ) : angularFlux c density = c * density / 4 := by
  have h : (∫ theta in (0 : ℝ)..(Real.pi / 2), Real.cos theta * Real.sin theta) = 1 / 2 := by
    simp_rw [mul_comm (Real.cos _)]
    rw [integral_sin_mul_cos₁]
    norm_num
  rw [angularFlux, h, intervalIntegral.integral_const]
  simp only [sub_zero, smul_eq_mul]
  field_simp
  ring

theorem isotropicFlux_angular (c hbar beta : ℝ) :
    isotropicFlux c hbar beta = angularFlux c (thermalEnergy c hbar beta) := by
  rw [angularFlux_eq, isotropicFlux]

theorem stefan_law {c hbar kB temperature : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (hk : 0 < kB) (ht : 0 < temperature) :
    isotropicFlux c hbar ((kB * temperature)⁻¹) =
      stefanCoefficient c hbar kB * temperature ^ 4 := by
  rw [isotropicFlux, thermalEnergy_eq hc hh (inv_pos.mpr (mul_pos hk ht)), stefanCoefficient]
  field_simp [hc.ne', hh.ne', hk.ne', ht.ne']
  ring

theorem stefan_full_turn {c hbar kB : ℝ} (hc : 0 < c) (hh : 0 < hbar) :
    stefanCoefficient c hbar kB =
      2 * Real.pi ^ 5 * kB ^ 4 / (15 * (2 * Real.pi * hbar) ^ 3 * c ^ 2) := by
  rw [stefanCoefficient]
  field_simp [Real.pi_ne_zero, hc.ne', hh.ne']
  ring

theorem calendar_energy_ratio {c hbar tP : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (ht : 0 < tP) :
    thermalEnergy c hbar (tP * Real.log 3 / hbar) * (c * tP)^3 / (hbar / tP) =
      Real.pi ^ 2 / (15 * Real.log 3 ^ 4) := by
  have hl : 0 < Real.log 3 := Real.log_pos (by norm_num)
  rw [thermalEnergy_eq hc hh (div_pos (mul_pos ht hl) hh)]
  field_simp [hc.ne', hh.ne', ht.ne', hl.ne']
  ring

theorem calendar_flux {h ell0 t0 : ℝ} (hh : 0 < h)
    (hl : 0 < ell0) (ht : 0 < t0) :
    isotropicFlux (ell0 / t0) (h / (2 * Real.pi)) (108 * t0 * Real.log 3 / h) =
      (2 * Real.pi ^ 5 / (15 * 108 ^ 4 * Real.log 3 ^ 4)) *
        (h / (ell0 ^ 2 * t0 ^ 2)) := by
  have hlog : 0 < Real.log 3 := Real.log_pos (by norm_num)
  rw [isotropicFlux, thermalEnergy_eq (div_pos hl ht)
    (div_pos hh (by positivity)) (by positivity)]
  field_simp [Real.pi_ne_zero, hh.ne', hl.ne', ht.ne', hlog.ne']
  ring

#print axioms scaled_energy_integral
#print axioms thermalEnergy_eq
#print axioms energyProfile_integrable
#print axioms stefan_law
#print axioms stefan_full_turn
#print axioms angularFlux_eq
#print axioms isotropicFlux_angular
#print axioms calendar_energy_ratio
#print axioms calendar_flux

end HMT.V.BosonicMoments
