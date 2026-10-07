import LatticeNormalEnergy
import LatticeStateFieldCoherence

/-! The whole state-field map respects the existing energy operator.
The charged case is inherited; normal ordering supplies the induction,
and the already fixed carrier basis supplies the linear extension. -/

noncomputable section
namespace HMT.IV.LatticeStateFieldEnergy

open LatticeCocycle LatticeOscillatorFock LatticeEnergyGrading
open LatticeNormalEnergy LatticeDescendantFields LatticeStateFieldMap
open LatticeFockMonomialParity LatticeOscillatorWords LatticeNormalProductCommutation

def descendantWeight (o : Fin 12) (x : Lattice o) : List (Mode o) → ℂ
  | [] => (LatticeWeightShells.halfnormNat o x : ℂ)
  | m :: w => descendantWeight o x w + (m.1 : ℂ) + 1

theorem descendant_energy_covariant (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) :
    EnergyCovariant o (descendantWeight o x w) (descendantField o x w) := by
  induction w with
  | nil =>
    intro k
    simpa only [descendantWeight, descendantField, add_comm] using
      LatticeChargedFieldEnergy.energy_fieldCoefficient o x k
  | cons m w ih => exact normalField_energy_covariant o m.2 m.1 _ _ ih

theorem energy_of_creative_field (o : Fin 12) (B : VertexOperator ℂ (LatticeCarrier o))
    (u : LatticeCarrier o) (d : ℂ) (hB : EnergyCovariant o d B)
    (hcreate : Creates o B u) : energy o u = d • u := by
  have h := LinearMap.congr_fun (hB 0) (vacuum o)
  simpa only [LinearMap.sub_apply, Module.End.mul_apply, energy_vacuum,
    map_zero, sub_zero, LinearMap.smul_apply, hcreate.2, Int.cast_zero, add_zero] using h

theorem descendantState_energy (o : Fin 12) (x : Lattice o) (w : List (Mode o)) :
    energy o (descendantState o x w) =
      descendantWeight o x w • descendantState o x w :=
  energy_of_creative_field o _ _ _ (descendant_energy_covariant o x w)
    (descendantField_creates o x w)

theorem descendant_energy_identity (o : Fin 12) (x : Lattice o) (w : List (Mode o))
    (k : ℤ) :
    energy o * HVertexOperator.coeff (stateField o (descendantState o x w)) k -
      HVertexOperator.coeff (stateField o (descendantState o x w)) k * energy o =
      HVertexOperator.coeff (stateField o (energy o (descendantState o x w))) k +
      (k : ℂ) • HVertexOperator.coeff (stateField o (descendantState o x w)) k := by
  rw [descendantState_energy, map_smul, HVertexOperator.coeff_smul]
  simp only [Pi.smul_apply, stateField_descendant]
  rw [descendant_energy_covariant o x w k, add_smul]

/-- No homogeneity assumption is imposed on u: both energy actions are
the pre-existing ones on the full carrier. -/
theorem stateField_energy (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    energy o * HVertexOperator.coeff (stateField o u) k -
      HVertexOperator.coeff (stateField o u) k * energy o =
      HVertexOperator.coeff (stateField o (energy o u)) k +
      (k : ℂ) • HVertexOperator.coeff (stateField o u) k := by
  classical
  let coefficientMap : LatticeCarrier o →ₗ[ℂ] Module.End ℂ (LatticeCarrier o) :=
    { toFun := fun v => HVertexOperator.coeff (stateField o v) k
      map_add' := by
        intro v w
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply]
      map_smul' := by
        intro c v
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          RingHom.id_apply] }
  let defect : LatticeCarrier o →ₗ[ℂ] Module.End ℂ (LatticeCarrier o) :=
    { toFun := fun v => energy o * coefficientMap v - coefficientMap v * energy o -
        coefficientMap (energy o v) - (k : ℂ) • coefficientMap v
      map_add' := by
        intro v w
        simp only [map_add, mul_add, add_mul, smul_add]
        abel
      map_smul' := by
        intro c v
        simp only [map_smul, mul_smul_comm, smul_mul_assoc, RingHom.id_apply,
          smul_sub, smul_comm c (k : ℂ)] }
  have hz : defect = 0 := by
    apply (carrierBasis o).ext
    rintro ⟨a,x⟩
    change energy o * coefficientMap _ - coefficientMap _ * energy o -
      coefficientMap (energy o _) - (k : ℂ) • coefficientMap _ = 0
    dsimp only [coefficientMap, LinearMap.coe_mk, AddHom.coe_mk]
    rw [← carrierBasis_wordForOccupation o a x, ← descendantState_eq_word]
    rw [descendant_energy_identity]
    abel
  have h := LinearMap.congr_fun hz u
  change energy o * HVertexOperator.coeff (stateField o u) k -
    HVertexOperator.coeff (stateField o u) k * energy o -
    HVertexOperator.coeff (stateField o (energy o u)) k -
    (k : ℂ) • HVertexOperator.coeff (stateField o u) k = 0 at h
  exact sub_eq_zero.mp (by simpa only [sub_sub, add_assoc] using h)

theorem stateField_homogeneous_energy (o : Fin 12) (u : LatticeCarrier o)
    (d : ℂ) (hu : energy o u = d • u) : EnergyCovariant o d (stateField o u) := by
  intro k
  rw [stateField_energy, hu, map_smul, HVertexOperator.coeff_smul]
  simp only [Pi.smul_apply, add_smul]

end HMT.IV.LatticeStateFieldEnergy
end

#print axioms HMT.IV.LatticeStateFieldEnergy.descendant_energy_covariant
#print axioms HMT.IV.LatticeStateFieldEnergy.energy_of_creative_field
#print axioms HMT.IV.LatticeStateFieldEnergy.descendantState_energy
#print axioms HMT.IV.LatticeStateFieldEnergy.descendant_energy_identity
#print axioms HMT.IV.LatticeStateFieldEnergy.stateField_energy
#print axioms HMT.IV.LatticeStateFieldEnergy.stateField_homogeneous_energy
