import SelectedConstitutivePublication
import ExteriorModes
import SymmetricModes
import ThermalGibbsBridge
import PeriodicThermodynamicLimit

/-!
Concrete downstream consumer of the same selected regional publication.
The reduced action is the returned action section of SelectedAction;
the propagation speed is the SelectedConstitutivePublication output, in a
positive velocity chart. Neither is fitted to a target value. The finite
Fock realization uses two explicit orthonormal polarizations and chemical
potential zero. The periodic realization excludes its zero mode before
summing, with a = beta*hbar*c and b = hbar*c.

This composes existing proofs. It does not identify arbitrary interacting
systems with the free homogeneous three-dimensional thermal realization,
nor assert a Hilbert completion or a trace-class Fock operator.
-/

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.SelectedPublication

open HMT.I.SelectedAction
open HMT.V.ThermodynamicLimit HMT.V.BosonicMoments

def reducedAction (U : ℝ) : ℝ :=
  HMT.II.ActionReturn.hbarRet alpha phi pi U

def speed (C : ℝ) : ℝ := HMT.III.SelectedPublication.speed * C

theorem reducedAction_pos {U : ℝ} (hU : 0 < U) : 0 < reducedAction U :=
  action_domain.hbarRet_pos hU

theorem speed_pos {C : ℝ} (hC : 0 < C) : 0 < speed C :=
  mul_pos HMT.III.SelectedPublication.speed_pos hC

theorem same_regional_action :
    alpha = AlphaAnalyticChart.precoordinate HMT.I.TerminalSelector.regionalRegister := rfl

def momentumEnergy (U C r : ℝ) : ℝ := reducedAction U * speed C * r

theorem momentumEnergy_pos {U C r : ℝ} (hU : 0 < U) (hC : 0 < C)
    (hr : 0 < r) : 0 < momentumEnergy U C r :=
  mul_pos (mul_pos (reducedAction_pos hU) (speed_pos hC)) hr

def twoEnergies (U C r : ℝ) : List ℝ :=
  [momentumEnergy U C r, momentumEnergy U C r]

def twoFugacities (beta U C r : ℝ) : List ℝ :=
  [Real.exp (-(beta * momentumEnergy U C r)),
   Real.exp (-(beta * momentumEnergy U C r))]

abbrev PolarizationSpace := EuclideanSpace ℂ (Fin 2)

def polarization (i : Fin 2) : PolarizationSpace := EuclideanSpace.single i 1

theorem polarization_orthonormal : Orthonormal ℂ polarization :=
  EuclideanSpace.orthonormal_single

theorem exterior_two_polarizations (beta U C r : ℝ) (i : Fin 2) :
    (∀ s : HMT.FockBridge.Occupation 2,
      HMT.FockTransport.Exterior.occupation (polarization i)
        (HMT.FockTransport.Exterior.innerDual (𝕜 := ℂ) (polarization i))
        (HMT.FockTransport.Exterior.configurationVector (R := ℂ) polarization s) =
      (HMT.FockBridge.stateCoordinateValue 2 i s : ℂ) •
        HMT.FockTransport.Exterior.configurationVector (R := ℂ) polarization s) ∧
    HMT.FockBridge.coordinateMean (twoFugacities beta U C r) i =
      (twoFugacities beta U C r).get i /
        (1 + (twoFugacities beta U C r).get i) := by
  apply HMT.FockTransport.Exterior.exterior_gibbs_occupation
    (twoFugacities beta U C r) _ polarization polarization_orthonormal i
  intro u hu
  simp only [twoFugacities, List.mem_cons, List.not_mem_nil, or_false, or_self] at hu
  subst u
  exact (Real.exp_pos _).le

theorem symmetric_two_polarizations {beta U C r : ℝ}
    (hb : 0 < beta) (hU : 0 < U) (hC : 0 < C) (hr : 0 < r) :
    (∀ (i : Fin 2) (s : QuantumOccupations.BosonStates 2),
      HMT.FockTransport.Symmetric.occupation (polarization i)
        (innerₛₗ ℂ (polarization i))
        (HMT.FockTransport.Symmetric.configurationVector (R := ℂ) polarization s) =
      (QuantumOccupations.bosonStateOccupation 2 i s : ℂ) •
        HMT.FockTransport.Symmetric.configurationVector (R := ℂ) polarization s) ∧
    QuantumOccupations.bosonGibbsMeanNumber beta 0 (twoEnergies U C r) =
      2 / (Real.exp (beta * momentumEnergy U C r) - 1) := by
  have he : ∀ E ∈ twoEnergies U C r, (0 : ℝ) < E := by
    intro E hE
    simp only [twoEnergies, List.mem_cons, List.not_mem_nil, or_false, or_self] at hE
    subst E
    exact momentumEnergy_pos hU hC hr
  have h := HMT.FockTransport.Symmetric.symmetric_gibbs_total_occupation
    (β := beta) (μ := 0) (energies := twoEnergies U C r)
    hb he polarization polarization_orthonormal
  refine ⟨h.1, ?_⟩
  rw [h.2]
  simp only [twoEnergies, List.map_cons, List.map_nil, List.sum_cons,
    List.sum_nil, add_zero, sub_zero]
  ring

def thermalA (beta U C : ℝ) : ℝ := beta * reducedAction U * speed C
def thermalB (U C : ℝ) : ℝ := reducedAction U * speed C

theorem thermal_parameters_pos {beta U C : ℝ}
    (hb : 0 < beta) (hU : 0 < U) (hC : 0 < C) :
    0 < thermalA beta U C ∧ 0 < thermalB U C :=
  ⟨mul_pos (mul_pos hb (reducedAction_pos hU)) (speed_pos hC),
   mul_pos (reducedAction_pos hU) (speed_pos hC)⟩

theorem selected_periodic_limit {beta U C : ℝ}
    (hb : 0 < beta) (hU : 0 < U) (hC : 0 < C) (kind : ThermalKind) :
    Tendsto (fun L : ℝ => 2 / L ^ 3 *
      ∑' nu : {nu : Lattice // nu ≠ 0},
        thermalObservable (thermalA beta U C) (thermalB U C) kind
          ((2 * Real.pi / L) * radius nu)) atTop
      (𝓝 ((1 / Real.pi ^ 2) *
        ∫ r in Ioi (0 : ℝ), r ^ 2 *
          thermalObservable (thermalA beta U C) (thermalB U C) kind r)) :=
  thermal_periodic_limit_nonzero (thermal_parameters_pos hb hU hC).1
    (thermal_parameters_pos hb hU hC).2 kind

theorem selected_periodic_sums_finite {beta U C L : ℝ}
    (hb : 0 < beta) (hU : 0 < U) (hC : 0 < C) (hL : 0 < L)
    (kind : ThermalKind) :
    Summable (fun nu : {nu : Lattice // nu ≠ 0} =>
      thermalObservable (thermalA beta U C) (thermalB U C) kind
        ((2 * Real.pi / L) * radius nu)) :=
  thermal_periodic_sums_finite (thermal_parameters_pos hb hU hC).1
    (thermal_parameters_pos hb hU hC).2 hL kind

theorem selected_radial_integrable {beta U C : ℝ}
    (hb : 0 < beta) (hU : 0 < U) (hC : 0 < C) (kind : ThermalKind) :
    IntegrableOn (fun r : ℝ => r ^ 2 *
      thermalObservable (thermalA beta U C) (thermalB U C) kind r) (Ioi 0) :=
  thermal_radial_integrable (thermal_parameters_pos hb hU hC).1
    (thermal_parameters_pos hb hU hC).2 kind

theorem selected_planck_density {beta U C omega : ℝ}
    (hb : 0 < beta) (hU : 0 < U) (hw : 0 < omega) :
    HMT.V.Radiation.angularEnergyDensity beta (reducedAction U) (speed C) omega =
      reducedAction U * omega ^ 3 / (Real.pi ^ 2 * speed C ^ 3) *
        (1 / (Real.exp (beta * reducedAction U * omega) - 1)) :=
  HMT.V.Radiation.angularEnergyDensity_eq hb (reducedAction_pos hU) hw

theorem selected_stefan_flux {U C kB temperature : ℝ}
    (hU : 0 < U) (hC : 0 < C) (hk : 0 < kB) (ht : 0 < temperature) :
    angularFlux (speed C) (∫ omega in Ioi (0 : ℝ),
      HMT.V.Radiation.angularEnergyDensity ((kB * temperature)⁻¹)
        (reducedAction U) (speed C) omega) =
      stefanCoefficient (speed C) (reducedAction U) kB * temperature ^ 4 :=
  gibbs_flux_stefan (speed_pos hC) (reducedAction_pos hU) hk ht

end HMT.V.SelectedPublication
end

#print axioms HMT.V.SelectedPublication.same_regional_action
#print axioms HMT.V.SelectedPublication.reducedAction_pos
#print axioms HMT.V.SelectedPublication.speed_pos
#print axioms HMT.V.SelectedPublication.exterior_two_polarizations
#print axioms HMT.V.SelectedPublication.symmetric_two_polarizations
#print axioms HMT.V.SelectedPublication.selected_periodic_limit
#print axioms HMT.V.SelectedPublication.selected_periodic_sums_finite
#print axioms HMT.V.SelectedPublication.selected_radial_integrable
#print axioms HMT.V.SelectedPublication.selected_planck_density
#print axioms HMT.V.SelectedPublication.selected_stefan_flux
