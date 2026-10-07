import LatticeHalfVirasoroDefect
import LatticeHalfVirasoroBase
import LatticeVirasoroPolynomial

/-!
The cubic central polynomial for the actual shifted half-integer modes.
The scalar polynomial and its identities are reused from the previous
realization. The present commutator defect is not that previous operator:
its recurrence follows here from associative Jacobi, its proved vanishing
off resonance and the zero defect at (1,-1). No central charge is postulated.
-/

noncomputable section
namespace HMT.IV.LatticeHalfVirasoroPolynomial

open LatticeHalfIntegerHeisenberg LatticeHalfConformalCentralizer
open LatticeHalfVirasoroDefect LatticeHalfVirasoroBase
open LatticeConformalCentralizer
  (comm comm_jacobi_associative comm_smul_left comm_smul_right)
open LatticeVirasoroPolynomial
  (centralPolynomial centralPolynomial_recurrence centralPolynomial_neg)

theorem defect_recurrence (o : Fin 12) (m : ℤ) (hm : 2 ≤ m) :
    ((m:ℂ)-1) • defect o (m+1) (-(m+1)) =
      ((m:ℂ)+2) • defect o m (-m) := by
  have h := comm_jacobi_associative (shiftedModes o 1)
    (shiftedModes o m) (shiftedModes o (-(m+1)))
  have h1 : comm (shiftedModes o 1) (shiftedModes o m) =
      (1-(m:ℂ)) • shiftedModes o (m+1) := by
    rw [conformal_comm_nonresonant o 1 m (by omega)]
    rw [show 1+m=m+1 by omega]
    simp only [Int.cast_sub, Int.cast_one]
  have h2 : comm (shiftedModes o m) (shiftedModes o (-(m+1))) =
      (2*(m:ℂ)+1) • shiftedModes o (-1) := by
    rw [conformal_comm_nonresonant o m (-(m+1)) (by omega)]
    rw [show m+(-(m+1))=(-1:ℤ) by omega]
    congr 1
    push_cast
    ring
  have h3 : comm (shiftedModes o 1) (shiftedModes o (-(m+1))) =
      ((m:ℂ)+2) • shiftedModes o (-m) := by
    rw [conformal_comm_nonresonant o 1 (-(m+1)) (by omega)]
    rw [show 1+(-(m+1))=(-m:ℤ) by omega]
    congr 1
    push_cast
    ring
  rw [h1, h2, h3, comm_smul_left, comm_smul_right, comm_smul_right,
    resonant_comm_eq_defect o (m+1), resonant_comm_eq_defect o m] at h
  have h11 : comm (shiftedModes o 1) (shiftedModes o (-1)) =
      (2:ℂ) • shiftedModes o 0 := by
    rw [resonant_comm_eq_defect o 1, defect_one_neg_one]
    norm_num
  rw [h11] at h
  push_cast at h
  have heq :
      (1-(m:ℂ)) • ((2*((m:ℂ)+1)) • shiftedModes o 0 + defect o (m+1) (-(m+1))) -
      ((2*(m:ℂ)+1) • ((2:ℂ) • shiftedModes o 0) -
       ((m:ℂ)+2) • ((2*(m:ℂ)) • shiftedModes o 0 + defect o m (-m))) =
      -(((m:ℂ)-1) • defect o (m+1) (-(m+1)) -
         ((m:ℂ)+2) • defect o m (-m)) := by module
  rw [h, sub_self] at heq
  exact sub_eq_zero.mp (neg_eq_zero.mp heq.symm)

private theorem cancel_half_smul (o : Fin 12) (c : ℂ) (hc : c≠0)
    (A B : Module.End ℂ (HalfFock o)) (h : c•A=c•B) : A=B := by
  have hh := congrArg (fun X : Module.End ℂ (HalfFock o) => c⁻¹•X) h
  simpa only [smul_smul, inv_mul_cancel₀ hc, one_smul] using hh

theorem resonant_defect_from_two (o : Fin 12) (n : ℕ) :
    defect o ((n:ℤ)+2) (-((n:ℤ)+2)) =
      centralPolynomial ((n:ℤ)+2) • defect o 2 (-2) := by
  induction n with
  | zero => norm_num [centralPolynomial]
  | succ n ih =>
    have hr := defect_recurrence o ((n:ℤ)+2) (by omega)
    have hc : (((n:ℤ)+2:ℤ):ℂ)-1≠0 := by
      push_cast
      have hpos : (0:ℝ) < (n:ℝ)+1 := by positivity
      have hn : (n:ℂ)+1≠0 := by exact_mod_cast (ne_of_gt hpos)
      convert hn using 1
      ring
    have hindex : ((n+1:ℕ):ℤ)+2 = ((n:ℤ)+2)+1 := by omega
    rw [hindex]
    apply cancel_half_smul o _ hc
    rw [hr, ih, smul_smul, smul_smul, centralPolynomial_recurrence]

theorem resonant_defect_nat (o : Fin 12) (n : ℕ) :
    defect o (n:ℤ) (-(n:ℤ)) = centralPolynomial (n:ℤ) • defect o 2 (-2) := by
  rcases n with _ | n
  · simp only [Nat.cast_zero, neg_zero]
    simp [defect, LatticeConformalCentralizer.comm, centralPolynomial]
  · rcases n with _ | n
    · norm_num [centralPolynomial, defect_one_neg_one]
    · have h := resonant_defect_from_two o n
      convert h using 1

theorem resonant_defect_all (o : Fin 12) (m : ℤ) :
    defect o m (-m) = centralPolynomial m • defect o 2 (-2) := by
  cases m with
  | ofNat n => exact resonant_defect_nat o n
  | negSucc n =>
    have heq : Int.negSucc n = -((n+1:ℕ):ℤ) := by omega
    rw [heq, neg_neg, defect_skew, resonant_defect_nat, centralPolynomial_neg]
    module

theorem defect_all (o : Fin 12) (m n : ℤ) :
    defect o m n = if m+n=0 then centralPolynomial m • defect o 2 (-2) else 0 := by
  by_cases h : m+n=0
  · rw [if_pos h, show n = -m by omega, resonant_defect_all]
  · rw [if_neg h, defect_eq_zero_of_nonresonant o m n h]

theorem shifted_commutator_polynomial (o : Fin 12) (m n : ℤ) :
    comm (shiftedModes o m) (shiftedModes o n) =
      ((m-n:ℤ):ℂ) • shiftedModes o (m+n) +
      if m+n=0 then centralPolynomial m • defect o 2 (-2) else 0 := by
  rw [comm_eq_defect, defect_all]

end HMT.IV.LatticeHalfVirasoroPolynomial
end

#print axioms HMT.IV.LatticeHalfVirasoroPolynomial.defect_recurrence
#print axioms HMT.IV.LatticeHalfVirasoroPolynomial.resonant_defect_from_two
#print axioms HMT.IV.LatticeHalfVirasoroPolynomial.resonant_defect_nat
#print axioms HMT.IV.LatticeHalfVirasoroPolynomial.resonant_defect_all
#print axioms HMT.IV.LatticeHalfVirasoroPolynomial.defect_all
#print axioms HMT.IV.LatticeHalfVirasoroPolynomial.shifted_commutator_polynomial
