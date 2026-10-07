import SelectedThermalPublication
import SelectedActionGravityThermal

/-!
The Article V thermal parameter is the transducer already constructed in
Article II from the selected action and the declared positive clock and
temperature sections. It is not an independently supplied Boltzmann value.
The velocity is the same constitutive output of Article III. The positive
unit charts and thermodynamic temperature remain explicit.
-/

noncomputable section
namespace HMT.V.SelectedBoltzmannRadiation

open Set MeasureTheory
open HMT.V.SelectedPublication HMT.V.BosonicMoments
open HMT.II.SelectedActionGravityThermal

def boltzmann (U t0 Theta : ℝ) : ℝ := thermalCoefficient U t0 Theta .pre

def inverseTemperature (U t0 Theta T : ℝ) : ℝ := (boltzmann U t0 Theta * T)⁻¹

theorem boltzmann_pos {U t0 Theta : ℝ}
    (hU : 0 < U) (ht0 : 0 < t0) (hTheta : 0 < Theta) :
    0 < boltzmann U t0 Theta := thermalCoefficient_pos hU ht0 hTheta .pre

theorem inverseTemperature_pos {U t0 Theta T : ℝ}
    (hU : 0 < U) (ht0 : 0 < t0) (hTheta : 0 < Theta) (hT : 0 < T) :
    0 < inverseTemperature U t0 Theta T :=
  inv_pos.mpr (mul_pos (boltzmann_pos hU ht0 hTheta) hT)

theorem same_returned_action (U : ℝ) :
    HMT.II.SelectedActionGravityThermal.sectionAction U .ret = reducedAction U := rfl

theorem thermal_section_coherence {U Theta : ℝ} (t0 : ℝ)
    (hU : 0 < U) (hTheta : 0 < Theta) :
    boltzmann U t0 Theta = thermalCoefficient U t0 (returnTemperature U Theta) .ret :=
  return_preserves_transducer t0 hU hTheta

theorem selected_transducer_unique {U t0 Theta : ℝ}
    (hU : 0 < U) (ht0 : 0 < t0) (hTheta : 0 < Theta) (b : ℝ) :
    (0 < b ∧ b * Theta * Real.log 3 = cycleEnergy U t0 .pre) ↔
      b = boltzmann U t0 Theta := by
  constructor
  · intro hb
    exact (thermal_coefficient_characterization U t0 Theta b hTheta .pre).mp hb.2
  · rintro rfl
    exact ⟨boltzmann_pos hU ht0 hTheta,
      (thermal_coefficient_characterization U t0 Theta _ hTheta .pre).mpr rfl⟩

theorem generated_bosonic_occupation {U C t0 Theta T r : ℝ}
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0)
    (hTheta : 0 < Theta) (hT : 0 < T) (hr : 0 < r) :
    QuantumOccupations.bosonGibbsMeanNumber (inverseTemperature U t0 Theta T)
      0 (twoEnergies U C r) =
      2 / (Real.exp (inverseTemperature U t0 Theta T * momentumEnergy U C r) - 1) :=
  (symmetric_two_polarizations (inverseTemperature_pos hU ht0 hTheta hT)
    hU hC hr).2

theorem generated_stefan_flux {U C t0 Theta T : ℝ}
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0)
    (hTheta : 0 < Theta) (hT : 0 < T) :
    angularFlux (speed C) (∫ omega in Ioi (0 : ℝ),
      HMT.V.Radiation.angularEnergyDensity (inverseTemperature U t0 Theta T)
        (reducedAction U) (speed C) omega) =
      stefanCoefficient (speed C) (reducedAction U) (boltzmann U t0 Theta) * T ^ 4 :=
  selected_stefan_flux hU hC (boltzmann_pos hU ht0 hTheta) hT

/-- One selected chain supplies the constitutive velocity, the action and the
thermal transducer to the already proved radiation theorem. -/
theorem selected_II_III_V_thermal_chain {U C t0 Theta T : ℝ}
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0)
    (hTheta : 0 < Theta) (hT : 0 < T) :
    0 < boltzmann U t0 Theta ∧
    (∀ b : ℝ, (0 < b ∧ b * Theta * Real.log 3 = cycleEnergy U t0 .pre) ↔
      b = boltzmann U t0 Theta) ∧
    boltzmann U t0 Theta = thermalCoefficient U t0 (returnTemperature U Theta) .ret ∧
    angularFlux (speed C) (∫ omega in Ioi (0 : ℝ),
      HMT.V.Radiation.angularEnergyDensity (inverseTemperature U t0 Theta T)
        (reducedAction U) (speed C) omega) =
      stefanCoefficient (speed C) (reducedAction U) (boltzmann U t0 Theta) * T ^ 4 :=
  ⟨boltzmann_pos hU ht0 hTheta, selected_transducer_unique hU ht0 hTheta,
    thermal_section_coherence t0 hU hTheta, generated_stefan_flux hU hC ht0 hTheta hT⟩

end HMT.V.SelectedBoltzmannRadiation
end

#print axioms HMT.V.SelectedBoltzmannRadiation.same_returned_action
#print axioms HMT.V.SelectedBoltzmannRadiation.selected_transducer_unique
#print axioms HMT.V.SelectedBoltzmannRadiation.generated_bosonic_occupation
#print axioms HMT.V.SelectedBoltzmannRadiation.selected_II_III_V_thermal_chain
