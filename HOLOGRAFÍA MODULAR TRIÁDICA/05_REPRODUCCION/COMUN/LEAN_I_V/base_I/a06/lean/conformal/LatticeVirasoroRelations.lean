import LatticeVirasoroPolynomial
import LatticeConformalCentralCharge

/-! Full Virasoro commutators of the conformal modes constructed on the
same marked lattice. The central coefficient is calculated on the actual
charge-ground states and extended by the proved generator spanning theorem.
No Virasoro representation, Jacobi axiom or target central charge is an input. -/
noncomputable section
namespace HMT.IV.LatticeVirasoroRelations
open LatticeOscillatorFock LatticeConformalState LatticeConformalCentralizer
open LatticeVirasoroPolynomial LatticeConformalCentralCharge LatticeCocycle

theorem virasoro_commutator (o : Fin 12) (m n : ℤ) :
    conformalMode o m * conformalMode o n - conformalMode o n * conformalMode o m =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) +
      (if m+n=0 then ((BasisSize o : ℂ)/12 * ((m:ℂ)^3-(m:ℂ))) •
        (LinearMap.id : Module.End ℂ (LatticeCarrier o)) else 0) := by
  change comm (conformalMode o m) (conformalMode o n) = _
  rw [conformal_commutator_polynomial]
  split_ifs
  · rw [defect_two_neg_two, smul_smul]
    congr 2
    unfold centralPolynomial
    ring
  · rfl

theorem virasoro_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    conformalMode o m * conformalMode o n - conformalMode o n * conformalMode o m =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) +
      (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
        (LinearMap.id : Module.End ℂ (LatticeCarrier o)) else 0) := by
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  rw [virasoro_commutator, hr]
  norm_num

theorem virasoro_commutator_apply (o : Fin 12) (m n : ℤ) (v : LatticeCarrier o) :
    conformalMode o m (conformalMode o n v) - conformalMode o n (conformalMode o m v) =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) v +
      (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) • v else 0) := by
  have h := LinearMap.congr_fun (virasoro_central_charge_twentyFour o m n) v
  by_cases hmn : m+n=0
  · simpa only [if_pos hmn, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
      LinearMap.smul_apply, LinearMap.id_apply] using h
  · simpa only [if_neg hmn, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
      LinearMap.smul_apply, LinearMap.zero_apply] using h

end HMT.IV.LatticeVirasoroRelations
end
#print axioms HMT.IV.LatticeVirasoroRelations.virasoro_commutator
#print axioms HMT.IV.LatticeVirasoroRelations.virasoro_central_charge_twentyFour
#print axioms HMT.IV.LatticeVirasoroRelations.virasoro_commutator_apply
