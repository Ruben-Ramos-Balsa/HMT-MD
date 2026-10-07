import LatticeHalfConformalEnergy
import LatticeHalfConformalCentralizer
import LatticeVirasoroDefect

/-! The actual half-integer commutator defect vanishes off resonance.
Its energy is computed from the quadratic sums, while its commutation with
the same energy follows from the proved oscillator centralizer. -/
noncomputable section
namespace HMT.IV.LatticeHalfVirasoroDefect
open LatticeHalfIntegerHeisenberg LatticeHalfConformalCentralizer
open LatticeHalfConformalEnergy
open LatticeConformalCentralizer hiding defect

theorem energy_defect (o : Fin 12) (m n : ℤ) :
    comm (shiftedModes o 0) (defect o m n) =
      (-((m+n:ℤ):ℂ)) • defect o m n := by
  change comm (shiftedModes o 0) (comm (shiftedModes o m) (shiftedModes o n) -
    ((m-n:ℤ):ℂ) • shiftedModes o (m+n)) = _
  rw [LatticeVirasoroDefect.comm_sub_right, LatticeVirasoroDefect.comm_jacobi_left,
    comm_smul_right]
  have h (k : ℤ) : comm (shiftedModes o 0) (shiftedModes o k) =
      (-(k:ℂ)) • shiftedModes o k := shifted_energy_comm o _ k
  simp only [h, comm_smul_left, comm_smul_right, defect]
  push_cast
  module

theorem defect_eq_zero_of_nonresonant (o : Fin 12) (m n : ℤ) (h : m+n≠0) :
    defect o m n=0 := by
  have hz := defect_comm_shifted o m n 0
  have hz' : comm (shiftedModes o 0) (defect o m n)=0 := by
    rw [LatticeVirasoroDefect.comm_skew, hz, neg_zero]
  rw [energy_defect] at hz'
  have hc : -((m+n:ℤ):ℂ)≠0 := by
    exact neg_ne_zero.mpr (by exact_mod_cast h)
  have hmul := congrArg (fun A : Module.End ℂ (HalfFock o) =>
    (-((m+n:ℤ):ℂ))⁻¹ • A) hz'
  simpa only [smul_smul, inv_mul_cancel₀ hc, one_smul, smul_zero] using hmul

theorem conformal_comm_nonresonant (o : Fin 12) (m n : ℤ) (h : m+n≠0) :
    comm (shiftedModes o m) (shiftedModes o n) =
      ((m-n:ℤ):ℂ) • shiftedModes o (m+n) :=
  sub_eq_zero.mp (defect_eq_zero_of_nonresonant o m n h)

theorem defect_skew (o : Fin 12) (m n : ℤ) : defect o m n = -defect o n m := by
  rw [defect, defect, LatticeVirasoroDefect.comm_skew (shiftedModes o m)]
  rw [show n+m=m+n by omega]
  push_cast
  module

theorem comm_eq_defect (o : Fin 12) (m n : ℤ) :
    comm (shiftedModes o m) (shiftedModes o n) =
      ((m-n:ℤ):ℂ) • shiftedModes o (m+n) + defect o m n := by
  rw [defect]
  abel

theorem resonant_comm_eq_defect (o : Fin 12) (m : ℤ) :
    comm (shiftedModes o m) (shiftedModes o (-m)) =
      (2*(m:ℂ)) • shiftedModes o 0 + defect o m (-m) := by
  rw [comm_eq_defect]
  simp only [add_neg_cancel, Int.cast_sub, Int.cast_neg]
  congr 2
  ring

end HMT.IV.LatticeHalfVirasoroDefect
end
#print axioms HMT.IV.LatticeHalfVirasoroDefect.energy_defect
#print axioms HMT.IV.LatticeHalfVirasoroDefect.defect_eq_zero_of_nonresonant
#print axioms HMT.IV.LatticeHalfVirasoroDefect.conformal_comm_nonresonant
#print axioms HMT.IV.LatticeHalfVirasoroDefect.defect_skew
#print axioms HMT.IV.LatticeHalfVirasoroDefect.comm_eq_defect
#print axioms HMT.IV.LatticeHalfVirasoroDefect.resonant_comm_eq_defect
