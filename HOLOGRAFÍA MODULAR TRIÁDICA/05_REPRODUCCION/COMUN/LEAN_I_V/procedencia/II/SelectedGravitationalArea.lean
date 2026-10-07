import SelectedAreaInformation
import SelectedActionGravityThermal

/-! The physical area uses the very same selected action, circular gravity
and constitutive velocity. This is the specialization ell_P^2 = G*hbar/c^3
in 09c_entropia_sectorial.tex and 10_gravedad.tex. No external gravitational
constant or free Barbero/area factor is supplied. -/

noncomputable section
namespace HMT.II.SelectedGravitationalArea

open HMT.II.SelectedAreaInformation HMT.II.SectorialAreaInformation
open HMT.II.SelectedActionGravityThermal

def physicalSpeed (C : ℝ) : ℝ := HMT.III.SelectedPublication.speed * C

theorem physicalSpeed_pos {C : ℝ} (hC : 0 < C) : 0 < physicalSpeed C :=
  mul_pos HMT.III.SelectedPublication.speed_pos hC

def gravitationalAreaScale (U C t0 : ℝ) : ℝ :=
  sectionAction U .ret * circularGravity U (physicalSpeed C) t0 .ret / physicalSpeed C ^ 3

theorem gravitationalAreaScale_eq {U C : ℝ} (t0 : ℝ)
    (hU : 0 < U) (hC : 0 < C) :
    gravitationalAreaScale U C t0 = radius (physicalSpeed C) t0 ^ 2 :=
  circular_area_invariant t0 hU (physicalSpeed_pos hC) .ret

theorem gravitationalAreaScale_pos {U C t0 : ℝ}
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0) :
    0 < gravitationalAreaScale U C t0 := by
  rw [gravitationalAreaScale_eq t0 hU hC]
  apply sq_pos_of_pos
  unfold radius
  exact div_pos (physicalSpeed_pos hC) (frequency_pos ht0)

def physicalSectorArea (U C t0 : ℝ) (s : Sector) (v : Occupation) : ℝ :=
  gravitationalAreaScale U C t0 * normalizedSectorArea gamma a0 s v

def physicalModularCoefficient (U C t0 delta : ℝ) (s : Sector) : ℝ :=
  modularCoefficient gamma a0 delta s / gravitationalAreaScale U C t0

theorem same_physical_modular_pair {U C t0 : ℝ} (delta : ℝ)
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0) (s : Sector) (v : Occupation) :
    physicalModularCoefficient U C t0 delta s * physicalSectorArea U C t0 s v =
      modularCoefficient gamma a0 delta s * normalizedSectorArea gamma a0 s v := by
  have hg := ne_of_gt (gravitationalAreaScale_pos hU hC ht0)
  unfold physicalModularCoefficient physicalSectorArea
  field_simp
  ring

theorem selected_physical_modular_area {U C t0 : ℝ} (delta : ℝ)
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0) (v : Occupation) :
    -Real.log (reducedDensity delta v v) = logPartition delta +
      physicalModularCoefficient U C t0 delta 0 * physicalSectorArea U C t0 0 v +
      physicalModularCoefficient U C t0 delta 1 * physicalSectorArea U C t0 1 v := by
  rw [same_physical_modular_pair delta hU hC ht0,
    same_physical_modular_pair delta hU hC ht0]
  exact selected_modular_area a0 delta (ne_of_gt a0_pos) v

theorem selected_physical_area_scale_pos {U C t0 : ℝ}
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0) :
    0 < gamma * a0 * gravitationalAreaScale U C t0 :=
  mul_pos generated_area_quantum_pos (gravitationalAreaScale_pos hU hC ht0)

theorem selected_gravity_area_information {U C t0 : ℝ} (delta : ℝ)
    (hU : 0 < U) (hC : 0 < C) (ht0 : 0 < t0) :
    gravitationalAreaScale U C t0 = radius (physicalSpeed C) t0 ^ 2 ∧
    0 < gamma * a0 * gravitationalAreaScale U C t0 ∧
    (∀ v, -Real.log (reducedDensity delta v v) = logPartition delta +
      physicalModularCoefficient U C t0 delta 0 * physicalSectorArea U C t0 0 v +
      physicalModularCoefficient U C t0 delta 1 * physicalSectorArea U C t0 1 v) ∧
    entropy delta = logPartition delta + delta * expectedIncidence delta :=
  ⟨gravitationalAreaScale_eq t0 hU hC, selected_physical_area_scale_pos hU hC ht0,
    selected_physical_modular_area delta hU hC ht0, entropy_state_equation delta⟩

end HMT.II.SelectedGravitationalArea
end

#print axioms HMT.II.SelectedGravitationalArea.gravitationalAreaScale_eq
#print axioms HMT.II.SelectedGravitationalArea.selected_gravity_area_information
