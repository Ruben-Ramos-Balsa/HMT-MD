import LatticeConformalCentralizer
import LatticeConformalCovariance
import LatticeConformalTranslation

/-! The defect of the Virasoro commutator on the actual lattice carrier.
Its non-resonant vanishing and recurrence are derived from the associative
endomorphism algebra and the already established Heisenberg action. -/
noncomputable section
namespace HMT.IV.LatticeVirasoroDefect
open LatticeOscillatorFock LatticeConformalState LatticeConformalCentralizer
open LatticeConformalEnergy LatticeConformalTranslation LatticeConformalCovariance
open LatticeEnergyGrading

theorem comm_skew {V : Type*} [AddCommGroup V] [Module ℂ V]
    (A B : Module.End ℂ V) : comm A B = -comm B A := by
  simp only [LatticeConformalCentralizer.comm]
  abel

theorem comm_sub_right {V : Type*} [AddCommGroup V] [Module ℂ V]
    (A B C : Module.End ℂ V) : comm A (B-C)=comm A B-comm A C := by
  simp only [LatticeConformalCentralizer.comm]
  noncomm_ring

theorem comm_jacobi_left {V : Type*} [AddCommGroup V] [Module ℂ V]
    (A B C : Module.End ℂ V) :
    comm A (comm B C)=comm (comm A B) C+comm B (comm A C) := by
  simp only [LatticeConformalCentralizer.comm]
  noncomm_ring

theorem energy_defect (o : Fin 12) (m n : ℤ) :
    comm (energy o) (defect o m n) =
      (-((m+n:ℤ):ℂ)) • defect o m n := by
  change comm (energy o) (comm (conformalMode o m) (conformalMode o n) -
    ((m-n:ℤ):ℂ) • conformalMode o (m+n)) = _
  rw [comm_sub_right, comm_jacobi_left, comm_smul_right]
  have h (k : ℤ) : comm (energy o) (conformalMode o k) =
      (-(k:ℂ)) • conformalMode o k := conformalMode_energy o k
  simp only [h, comm_smul_left, comm_smul_right, defect]
  push_cast
  module

theorem defect_eq_zero_of_nonresonant (o : Fin 12) (m n : ℤ) (h : m+n≠0) :
    defect o m n=0 := by
  have hz := defect_comm_conformal o m n 0
  rw [conformalMode_zero_eq_energy] at hz
  have hz' : comm (energy o) (defect o m n)=0 := by
    rw [comm_skew, hz, neg_zero]
  rw [energy_defect] at hz'
  have hc : -((m+n:ℤ):ℂ)≠0 := by
    exact neg_ne_zero.mpr (by exact_mod_cast h)
  have hmul := congrArg (fun A : Module.End ℂ (LatticeCarrier o) =>
    (-((m+n:ℤ):ℂ))⁻¹ • A) hz'
  simpa only [smul_smul, inv_mul_cancel₀ hc, one_smul, smul_zero] using hmul

theorem conformal_comm_nonresonant (o : Fin 12) (m n : ℤ) (h : m+n≠0) :
    comm (conformalMode o m) (conformalMode o n) =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) :=
  sub_eq_zero.mp (defect_eq_zero_of_nonresonant o m n h)

theorem defect_skew (o : Fin 12) (m n : ℤ) : defect o m n = -defect o n m := by
  rw [defect, defect, comm_skew (conformalMode o m)]
  rw [show n+m=m+n by omega]
  push_cast
  module

theorem comm_eq_defect (o : Fin 12) (m n : ℤ) :
    comm (conformalMode o m) (conformalMode o n) =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) + defect o m n := by
  rw [defect]
  abel

theorem defect_one_neg_one (o : Fin 12) : defect o 1 (-1)=0 := by
  have h := conformalMode_translation o 1
  rw [← conformalMode_neg_one_eq_translation] at h
  have h' : comm (conformalMode o (-1)) (conformalMode o 1)=
      (-2:ℂ) • conformalMode o 0 := by
    convert h using 1
    norm_num [LatticeConformalCentralizer.comm]
  rw [defect, comm_skew, h']
  norm_num
  module

theorem resonant_comm_eq_defect (o : Fin 12) (m : ℤ) :
    comm (conformalMode o m) (conformalMode o (-m)) =
      (2*(m:ℂ)) • conformalMode o 0 + defect o m (-m) := by
  rw [comm_eq_defect]
  simp only [add_neg_cancel, Int.cast_sub, Int.cast_neg]
  congr 2
  ring

theorem defect_recurrence (o : Fin 12) (m : ℤ) (hm : 2 ≤ m) :
    ((m:ℂ)-1) • defect o (m+1) (-(m+1)) =
      ((m:ℂ)+2) • defect o m (-m) := by
  have h := comm_jacobi_associative (conformalMode o 1)
    (conformalMode o m) (conformalMode o (-(m+1)))
  have h1 : comm (conformalMode o 1) (conformalMode o m) =
      (1-(m:ℂ)) • conformalMode o (m+1) := by
    rw [conformal_comm_nonresonant o 1 m (by omega)]
    rw [show 1+m=m+1 by omega]
    simp only [Int.cast_sub, Int.cast_one]
  have h2 : comm (conformalMode o m) (conformalMode o (-(m+1))) =
      (2*(m:ℂ)+1) • conformalMode o (-1) := by
    rw [conformal_comm_nonresonant o m (-(m+1)) (by omega)]
    rw [show m+(-(m+1))=(-1:ℤ) by omega]
    congr 1
    push_cast
    ring
  have h3 : comm (conformalMode o 1) (conformalMode o (-(m+1))) =
      ((m:ℂ)+2) • conformalMode o (-m) := by
    rw [conformal_comm_nonresonant o 1 (-(m+1)) (by omega)]
    rw [show 1+(-(m+1))=(-m:ℤ) by omega]
    congr 1
    push_cast
    ring
  rw [h1, h2, h3, comm_smul_left, comm_smul_right, comm_smul_right,
    resonant_comm_eq_defect o (m+1), resonant_comm_eq_defect o m] at h
  have h11 : comm (conformalMode o 1) (conformalMode o (-1)) =
      (2:ℂ) • conformalMode o 0 := by
    rw [resonant_comm_eq_defect o 1, defect_one_neg_one]
    norm_num
  rw [h11] at h
  push_cast at h
  have heq :
      (1-(m:ℂ)) • ((2*((m:ℂ)+1)) • conformalMode o 0 + defect o (m+1) (-(m+1))) -
      ((2*(m:ℂ)+1) • ((2:ℂ) • conformalMode o 0) -
       ((m:ℂ)+2) • ((2*(m:ℂ)) • conformalMode o 0 + defect o m (-m))) =
      -(((m:ℂ)-1) • defect o (m+1) (-(m+1)) -
         ((m:ℂ)+2) • defect o m (-m)) := by module
  rw [h, sub_self] at heq
  exact sub_eq_zero.mp (neg_eq_zero.mp heq.symm)

end HMT.IV.LatticeVirasoroDefect
end
#print axioms HMT.IV.LatticeVirasoroDefect.energy_defect
#print axioms HMT.IV.LatticeVirasoroDefect.defect_eq_zero_of_nonresonant
#print axioms HMT.IV.LatticeVirasoroDefect.conformal_comm_nonresonant
#print axioms HMT.IV.LatticeVirasoroDefect.defect_skew
#print axioms HMT.IV.LatticeVirasoroDefect.defect_one_neg_one
#print axioms HMT.IV.LatticeVirasoroDefect.resonant_comm_eq_defect
#print axioms HMT.IV.LatticeVirasoroDefect.defect_recurrence
