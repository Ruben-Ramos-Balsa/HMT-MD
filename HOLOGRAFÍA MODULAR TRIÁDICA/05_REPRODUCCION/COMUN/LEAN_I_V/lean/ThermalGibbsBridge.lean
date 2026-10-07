import ThermalEnergy
import PlanckDensity

noncomputable section
open Set MeasureTheory Real

namespace HMT.V.BosonicMoments

theorem gibbs_density_eq_profile {beta hbar c omega : ℝ}
    (hb : 0 < beta) (hh : 0 < hbar) (hw : 0 < omega) :
    HMT.V.Radiation.angularEnergyDensity beta hbar c omega =
      energyProfile c hbar beta omega := by
  rw [HMT.V.Radiation.angularEnergyDensity_eq hb hh hw]
  simp only [energyProfile, occupation, one_div]

theorem gibbs_density_integral {beta hbar c : ℝ}
    (hb : 0 < beta) (hh : 0 < hbar) (hc : 0 < c) :
    (∫ omega in Ioi (0 : ℝ), HMT.V.Radiation.angularEnergyDensity beta hbar c omega) =
      Real.pi ^ 2 / (15 * c ^ 3 * hbar ^ 3 * beta ^ 4) := by
  rw [← thermalEnergy_eq hc hh hb]
  apply setIntegral_congr_fun measurableSet_Ioi
  intro omega hw
  exact gibbs_density_eq_profile hb hh hw

theorem gibbs_density_integrable {beta hbar c : ℝ}
    (hb : 0 < beta) (hh : 0 < hbar) (hc : 0 < c) :
    IntegrableOn (HMT.V.Radiation.angularEnergyDensity beta hbar c) (Ioi 0) := by
  apply (energyProfile_integrable hc hh hb).congr_fun _ measurableSet_Ioi
  intro omega hw
  exact (gibbs_density_eq_profile hb hh hw).symm

theorem gibbs_flux_stefan {c hbar kB temperature : ℝ}
    (hc : 0 < c) (hh : 0 < hbar) (hk : 0 < kB) (ht : 0 < temperature) :
    angularFlux c (∫ omega in Ioi (0 : ℝ),
      HMT.V.Radiation.angularEnergyDensity ((kB * temperature)⁻¹) hbar c omega) =
      stefanCoefficient c hbar kB * temperature ^ 4 := by
  have hb : 0 < (kB * temperature)⁻¹ := inv_pos.mpr (mul_pos hk ht)
  have he : (∫ omega in Ioi (0 : ℝ),
      HMT.V.Radiation.angularEnergyDensity ((kB * temperature)⁻¹) hbar c omega) =
      thermalEnergy c hbar ((kB * temperature)⁻¹) := by
    rw [gibbs_density_integral hb hh hc, thermalEnergy_eq hc hh hb]
  rw [he, ← isotropicFlux_angular]
  exact stefan_law hc hh hk ht

#print axioms gibbs_density_eq_profile
#print axioms gibbs_density_integral
#print axioms gibbs_density_integrable
#print axioms gibbs_flux_stefan

end HMT.V.BosonicMoments
