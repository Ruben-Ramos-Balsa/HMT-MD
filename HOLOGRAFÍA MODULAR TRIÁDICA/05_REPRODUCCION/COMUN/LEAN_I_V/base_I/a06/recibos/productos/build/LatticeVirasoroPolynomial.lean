import LatticeVirasoroDefect

/-! The cubic central coefficient is forced by the proved recurrence of the
actual commutator defect. Its value at (2,-2) remains the same explicit
operator throughout; no central charge or Virasoro relation is postulated. -/
noncomputable section
namespace HMT.IV.LatticeVirasoroPolynomial
open LatticeOscillatorFock LatticeConformalState LatticeConformalCentralizer
open LatticeVirasoroDefect

def centralPolynomial (m : ℤ) : ℂ := ((m:ℂ)^3-(m:ℂ))/6

theorem centralPolynomial_recurrence (m : ℤ) :
    ((m:ℂ)-1) * centralPolynomial (m+1) =
      ((m:ℂ)+2) * centralPolynomial m := by
  unfold centralPolynomial
  push_cast
  ring

theorem centralPolynomial_neg (m : ℤ) : centralPolynomial (-m) = -centralPolynomial m := by
  unfold centralPolynomial
  push_cast
  ring

theorem cancel_smul_end (o : Fin 12) (c : ℂ) (hc : c≠0)
    (A B : Module.End ℂ (LatticeCarrier o)) (h : c•A=c•B) : A=B := by
  have hh := congrArg (fun X : Module.End ℂ (LatticeCarrier o) => c⁻¹•X) h
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
    apply cancel_smul_end o _ hc
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

theorem conformal_commutator_polynomial (o : Fin 12) (m n : ℤ) :
    comm (conformalMode o m) (conformalMode o n) =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) +
      if m+n=0 then centralPolynomial m • defect o 2 (-2) else 0 := by
  rw [comm_eq_defect, defect_all]

end HMT.IV.LatticeVirasoroPolynomial
end
#print axioms HMT.IV.LatticeVirasoroPolynomial.centralPolynomial_recurrence
#print axioms HMT.IV.LatticeVirasoroPolynomial.centralPolynomial_neg
#print axioms HMT.IV.LatticeVirasoroPolynomial.resonant_defect_from_two
#print axioms HMT.IV.LatticeVirasoroPolynomial.resonant_defect_nat
#print axioms HMT.IV.LatticeVirasoroPolynomial.resonant_defect_all
#print axioms HMT.IV.LatticeVirasoroPolynomial.defect_all
#print axioms HMT.IV.LatticeVirasoroPolynomial.conformal_commutator_polynomial
