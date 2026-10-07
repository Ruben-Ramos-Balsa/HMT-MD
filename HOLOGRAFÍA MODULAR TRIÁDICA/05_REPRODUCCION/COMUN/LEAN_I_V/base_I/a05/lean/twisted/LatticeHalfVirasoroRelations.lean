import LatticeHalfVirasoroPolynomial

/-!
Virasoro relations of the real shifted half-integer oscillator modes.
The shift is rank/16 as forced by the (1,-1) vacuum calculation; the central
coefficient is calculated at (2,-2) and propagated by the proved recurrence.
This constructs the oscillator Virasoro representation, not the finite
central-extension module or the complete twisted lattice state-field map.
-/

noncomputable section
namespace HMT.IV.LatticeHalfVirasoroRelations

open LatticeCocycle LatticeHalfIntegerHeisenberg LatticeHalfConformalCentralizer
open LatticeHalfVirasoroPolynomial LatticeHalfVirasoroBase
open LatticeConformalCentralizer (comm)
open LatticeVirasoroPolynomial (centralPolynomial)

theorem virasoro_commutator (o : Fin 12) (m n : ℤ) :
    shiftedModes o m * shiftedModes o n - shiftedModes o n * shiftedModes o m =
      ((m-n:ℤ):ℂ) • shiftedModes o (m+n) +
      (if m+n=0 then ((BasisSize o : ℂ)/12 * ((m:ℂ)^3-(m:ℂ))) •
        (LinearMap.id : Module.End ℂ (HalfFock o)) else 0) := by
  change comm (shiftedModes o m) (shiftedModes o n) = _
  rw [shifted_commutator_polynomial]
  split_ifs
  · rw [defect_two_neg_two, smul_smul]
    congr 2
    unfold centralPolynomial
    ring
  · rfl

theorem virasoro_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    shiftedModes o m * shiftedModes o n - shiftedModes o n * shiftedModes o m =
      ((m-n:ℤ):ℂ) • shiftedModes o (m+n) +
      (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
        (LinearMap.id : Module.End ℂ (HalfFock o)) else 0) := by
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  rw [virasoro_commutator, hr]
  norm_num

theorem virasoro_commutator_apply (o : Fin 12) (m n : ℤ) (v : HalfFock o) :
    shiftedModes o m (shiftedModes o n v) - shiftedModes o n (shiftedModes o m v) =
      ((m-n:ℤ):ℂ) • shiftedModes o (m+n) v +
      (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) • v else 0) := by
  have h := LinearMap.congr_fun (virasoro_central_charge_twentyFour o m n) v
  by_cases hmn : m+n=0
  · simpa only [if_pos hmn, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
      LinearMap.smul_apply, LinearMap.id_apply] using h
  · simpa only [if_neg hmn, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
      LinearMap.smul_apply, LinearMap.zero_apply] using h

/-- The numerical weight is a consequence of the forced rank/16 shift. -/
theorem vacuum_conformal_weight_three_halves (o : Fin 12) :
    shiftedModes o 0 (1 : HalfFock o) = (3/2:ℂ) • (1 : HalfFock o) := by
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  change LatticeHalfConformalVacuum.shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 0 1 = _
  rw [LatticeHalfConformalVacuum.shifted_zero_vacuum, hr]
  norm_num

end HMT.IV.LatticeHalfVirasoroRelations
end

#print axioms HMT.IV.LatticeHalfVirasoroRelations.virasoro_commutator
#print axioms HMT.IV.LatticeHalfVirasoroRelations.virasoro_central_charge_twentyFour
#print axioms HMT.IV.LatticeHalfVirasoroRelations.virasoro_commutator_apply
#print axioms HMT.IV.LatticeHalfVirasoroRelations.vacuum_conformal_weight_three_halves
