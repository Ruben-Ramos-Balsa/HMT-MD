import LatticeHalfFockGeneration
import LatticeHalfConformalCentralizer
import LatticeHalfConformalVacuum
import LatticeHalfConformalCentralVacuum

/-! Operator-level base values of the half-integer quadratic defect.
The vacuum calculations and the rank/16 shift are inherited unchanged.
Commutation with the actual creators extends those values to the whole Fock
space by its proved generation from 1. No further mode calculation occurs. -/

noncomputable section
namespace HMT.IV.LatticeHalfVirasoroBase
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfFockGeneration LatticeHalfConformalCentralizer
open LatticeHalfConformalVacuum LatticeHalfConformalCentralVacuum

theorem defect_comm_create (o : Fin 12) (m n : ℤ) (a : ℕ)
    (i : Fin (BasisSize o)) :
    (defect o m n).comp (create o a i) = (create o a i).comp (defect o m n) := by
  have h := sub_eq_zero.mp (defect_comm_half o i m n (Int.negSucc a))
  simpa only [halfMode_negSucc] using h

theorem defect_one_neg_one_vacuum (o : Fin 12) : defect o 1 (-1) 1=0 := by
  have h := (vacuum_shift_forced o ((BasisSize o:ℂ)/16)).mpr rfl
  change shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 1
      (shiftedQuadraticMode o ((BasisSize o:ℂ)/16) (-1) 1) -
    shiftedQuadraticMode o ((BasisSize o:ℂ)/16) (-1)
      (shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 1 1) -
      (2:ℂ) • shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 0 1=0
  exact sub_eq_zero.mpr h

theorem defect_two_neg_two_vacuum (o : Fin 12) :
    defect o 2 (-2) 1 = ((BasisSize o:ℂ)/2) • (1 : HalfFock o) := by
  change shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 2
      (shiftedQuadraticMode o ((BasisSize o:ℂ)/16) (-2) 1) -
    shiftedQuadraticMode o ((BasisSize o:ℂ)/16) (-2)
      (shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 2 1) -
      (4:ℂ) • shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 0 1 = _
  exact forced_shift_central_vacuum o

theorem defect_one_neg_one (o : Fin 12) : defect o 1 (-1)=0 :=
  commuting_creators_eq_zero o (defect o 1 (-1))
    (defect_comm_create o 1 (-1)) (defect_one_neg_one_vacuum o)

theorem defect_two_neg_two (o : Fin 12) :
    defect o 2 (-2) = ((BasisSize o:ℂ)/2) •
      (LinearMap.id : Module.End ℂ (HalfFock o)) :=
  commuting_creators_eq_scalar o (defect o 2 (-2))
    (defect_comm_create o 2 (-2)) ((BasisSize o:ℂ)/2) (defect_two_neg_two_vacuum o)

end HMT.IV.LatticeHalfVirasoroBase
end

#print axioms HMT.IV.LatticeHalfVirasoroBase.defect_comm_create
#print axioms HMT.IV.LatticeHalfVirasoroBase.defect_one_neg_one_vacuum
#print axioms HMT.IV.LatticeHalfVirasoroBase.defect_two_neg_two_vacuum
#print axioms HMT.IV.LatticeHalfVirasoroBase.defect_one_neg_one
#print axioms HMT.IV.LatticeHalfVirasoroBase.defect_two_neg_two
