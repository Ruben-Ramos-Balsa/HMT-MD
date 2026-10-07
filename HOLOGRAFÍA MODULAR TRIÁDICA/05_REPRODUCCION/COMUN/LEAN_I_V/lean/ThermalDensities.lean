import PartitionMoment
import ZetaMomentAdapter

noncomputable section
open Set MeasureTheory Real

namespace HMT.V.BosonicMoments

theorem number_kernel_integral :
    (∫ x in Ioi (0 : ℝ), x ^ 2 * occupation x) = 2 * zetaSeries 3 := by
  have h := bosonic_moment (s := 3) (by norm_num)
  norm_num [Real.rpow_natCast] at h
  exact h

theorem scaled_number_integral {b : ℝ} (hb : 0 < b) :
    (∫ x in Ioi (0 : ℝ), x ^ 2 * occupation (b*x)) = 2 * zetaSeries 3 / b ^ 3 := by
  have h := integral_comp_mul_left_Ioi (fun x : ℝ => x ^ 2 * occupation x) 0 hb
  simp only [mul_zero, smul_eq_mul, number_kernel_integral, mul_pow,
    mul_assoc, integral_const_mul] at h
  calc
    _ = (b ^ 2)⁻¹ * (b ^ 2 * (∫ x in Ioi (0 : ℝ), x ^ 2 * occupation (b*x))) := by
      rw [inv_mul_cancel_left₀ (pow_ne_zero _ hb.ne')]
    _ = (b ^ 2)⁻¹ * (b⁻¹ * (2 * zetaSeries 3)) := by rw [h]
    _ = _ := by
      field_simp [hb.ne']
      ring_nf
      simp

def photonDensity (c hbar beta : ℝ) : ℝ :=
  (1 / (Real.pi ^ 2 * c ^ 3)) *
    ∫ omega in Ioi (0 : ℝ), omega ^ 2 * occupation (beta * hbar * omega)

def logPartitionDensity (c hbar beta : ℝ) : ℝ :=
  (1 / (Real.pi ^ 2 * c ^ 3)) *
    ∫ omega in Ioi (0 : ℝ), -omega ^ 2 * Real.log (1 - Real.exp (-(beta * hbar * omega)))

def gibbsEntropyDensity (c hbar beta kB : ℝ) : ℝ :=
  kB * (logPartitionDensity c hbar beta + beta * thermalEnergy c hbar beta)

theorem photonDensity_eq {c hbar beta : ℝ} (hh : 0 < hbar) (hb : 0 < beta) :
    photonDensity c hbar beta =
      2 * zetaSeries 3 / (Real.pi ^ 2 * c ^ 3 * (beta * hbar) ^ 3) := by
  rw [photonDensity, scaled_number_integral (mul_pos hb hh)]
  ring

theorem photonDensity_riemannZeta {c hbar beta : ℝ} (hh : 0 < hbar) (hb : 0 < beta) :
    photonDensity c hbar beta =
      2 * (riemannZeta 3).re / (Real.pi ^ 2 * c ^ 3 * (beta * hbar) ^ 3) := by
  rw [photonDensity_eq hh hb]
  have h := riemannZeta_real_eq_series (s := 3) (by norm_num)
  norm_num only [Complex.ofReal_ofNat] at h
  rw [h, Complex.ofReal_re]

theorem logPartitionDensity_eq {c hbar beta : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (hb : 0 < beta) :
    logPartitionDensity c hbar beta =
      Real.pi ^ 2 / (45 * c ^ 3 * (beta * hbar) ^ 3) := by
  rw [logPartitionDensity, scaled_partition_integral (mul_pos hb hh)]
  field_simp [Real.pi_ne_zero, hc.ne', hh.ne', hb.ne']
  ring

theorem gibbsEntropyDensity_eq {c hbar beta kB : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (hb : 0 < beta) :
    gibbsEntropyDensity c hbar beta kB =
      4 * Real.pi ^ 2 * kB / (45 * c ^ 3 * (beta * hbar) ^ 3) := by
  rw [gibbsEntropyDensity, logPartitionDensity_eq hc hh hb, thermalEnergy_eq hc hh hb]
  field_simp [hc.ne', hh.ne', hb.ne']
  ring

theorem calendar_photon_ratio {c hbar tP : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (ht : 0 < tP) :
    photonDensity c hbar (tP * Real.log 3 / hbar) * (c * tP) ^ 3 =
      2 * zetaSeries 3 / (Real.pi ^ 2 * Real.log 3 ^ 3) := by
  have hl : 0 < Real.log 3 := Real.log_pos (by norm_num)
  rw [photonDensity_eq hh (div_pos (mul_pos ht hl) hh)]
  field_simp [Real.pi_ne_zero, hc.ne', hh.ne', ht.ne', hl.ne']
  ring

theorem calendar_entropy_ratio {c hbar tP kB : ℝ} (hc : 0 < c)
    (hh : 0 < hbar) (ht : 0 < tP) (hk : 0 < kB) :
    gibbsEntropyDensity c hbar (tP * Real.log 3 / hbar) kB * (c * tP) ^ 3 / kB =
      4 * Real.pi ^ 2 / (45 * Real.log 3 ^ 3) := by
  have hl : 0 < Real.log 3 := Real.log_pos (by norm_num)
  rw [gibbsEntropyDensity_eq hc hh (div_pos (mul_pos ht hl) hh)]
  field_simp [hc.ne', hh.ne', ht.ne', hk.ne', hl.ne']
  ring

#print axioms number_kernel_integral
#print axioms scaled_number_integral
#print axioms photonDensity_eq
#print axioms photonDensity_riemannZeta
#print axioms logPartitionDensity_eq
#print axioms gibbsEntropyDensity_eq
#print axioms calendar_photon_ratio
#print axioms calendar_entropy_ratio

end HMT.V.BosonicMoments
