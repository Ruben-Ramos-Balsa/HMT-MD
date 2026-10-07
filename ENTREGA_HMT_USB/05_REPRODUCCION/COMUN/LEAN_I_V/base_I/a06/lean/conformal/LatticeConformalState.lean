import LatticeGramDual
import LatticeStateFieldCoherence
import LatticeEnergyModes

/-!
The quadratic conformal-state expression in the existing marked-lattice
carrier. The Gram inverse is constructed from the proved nondegenerate
pairing. The field identity follows from the already proved state-field
recursion and linearity; no Virasoro commutator is an assumption here.
-/

noncomputable section
namespace HMT.IV.LatticeConformalState

open LatticeOscillatorFock LatticeCocycle LatticeGramDual
open LatticeStateFieldMap LatticeStateFieldCoherence LatticeNormalOrderedField
open HeisenbergDerivativeModes LatticeHeisenbergField
open LatticeEnergyGrading LatticeEnergyModes
open scoped BigOperators

def conformalState (o : Fin 12) : LatticeCarrier o :=
  (2 : ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j •
    onCarrier o (create o 0 i) (onCarrier o (create o 0 j) (vacuum o))

def conformalField (o : Fin 12) : VertexOperator ℂ (LatticeCarrier o) :=
  stateField o (conformalState o)

theorem derivativeField_zero (o : Fin 12) (i : Fin (BasisSize o)) :
    derivativeField o i 0 = heisenbergField o i := by
  apply LinearMap.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  change derivativeCoefficient o i 0 k v = fieldCoefficient o i k v
  rw [derivativeCoefficient_zero]

theorem conformalField_eq_normal_sum (o : Fin 12) :
    conformalField o = (2 : ℂ)⁻¹ • ∑ i, ∑ j,
      gramInv o i j • normalField o i 0 (heisenbergField o j) := by
  have h (i j : Fin (BasisSize o)) :
      stateField o (onCarrier o (create o 0 i)
        (onCarrier o (create o 0 j) (vacuum o))) =
      normalField o i 0 (heisenbergField o j) := by
    rw [stateField_create, stateField_one_oscillator, derivativeField_zero]
  simp only [conformalField, conformalState, map_smul, map_sum, h]

theorem conformalField_creates (o : Fin 12) :
    LatticeDescendantFields.Creates o (conformalField o) (conformalState o) :=
  stateField_creates o (conformalState o)

theorem energy_one_creator (o : Fin 12) (i : Fin (BasisSize o)) :
    energy o (onCarrier o (create o 0 i) (vacuum o)) =
      onCarrier o (create o 0 i) (vacuum o) := by
  have h := LinearMap.congr_fun (energy_create o 0 i) (vacuum o)
  simpa only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    Nat.cast_zero, zero_add, one_smul, energy_vacuum, map_zero, sub_zero] using h

theorem energy_two_creators (o : Fin 12) (i j : Fin (BasisSize o)) :
    energy o (onCarrier o (create o 0 i)
      (onCarrier o (create o 0 j) (vacuum o))) =
      (2 : ℂ) • onCarrier o (create o 0 i)
        (onCarrier o (create o 0 j) (vacuum o)) := by
  have h := LinearMap.congr_fun (energy_create o 0 i)
    (onCarrier o (create o 0 j) (vacuum o))
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    Nat.cast_zero, zero_add, one_smul, energy_one_creator] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem conformalState_weight_two (o : Fin 12) :
    energy o (conformalState o) = (2 : ℂ) • conformalState o := by
  simp only [conformalState, map_smul, map_sum, energy_two_creators]
  simp_rw [smul_comm (gramInv o _ _) (2 : ℂ), ← Finset.smul_sum]
  exact smul_comm (2 : ℂ)⁻¹ (2 : ℂ) _

def conformalMode (o : Fin 12) (m : ℤ) : Module.End ℂ (LatticeCarrier o) :=
  HVertexOperator.coeff (conformalField o) (-m-2)

end HMT.IV.LatticeConformalState
end

#print axioms HMT.IV.LatticeConformalState.derivativeField_zero
#print axioms HMT.IV.LatticeConformalState.conformalField_eq_normal_sum
#print axioms HMT.IV.LatticeConformalState.conformalField_creates
#print axioms HMT.IV.LatticeConformalState.energy_one_creator
#print axioms HMT.IV.LatticeConformalState.energy_two_creators
#print axioms HMT.IV.LatticeConformalState.conformalState_weight_two
