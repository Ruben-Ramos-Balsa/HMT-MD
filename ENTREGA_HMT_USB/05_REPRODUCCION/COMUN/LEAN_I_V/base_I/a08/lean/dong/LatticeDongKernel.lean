import LatticeTwoRegionFactor

/-!
The scalar residue kernels needed for Dong's normal-product locality proof.
They are the two expansion regions already proved for the constructed
lattice fields. Here their negative-power coefficients are identified with
the actual normal-product binomials at every order, and the polynomial
clearing factor is retained explicitly.

Classical downstream reference: Michael Tuite, "Vertex Algebras According
to Isaac Newton", arXiv:1702.02902, Lemma 27. The reference is not a Lean
axiom or an imported reconstruction theorem. This file proves only the
displayed coefficient/kernel identities, not the complete Dong lemma.
-/

noncomputable section
namespace HMT.IV.LatticeDongKernel

open HMT.IV.LatticeTwoRegionFactor HMT.IV.LatticeExponentialContraction

/-- Coefficients of `(1-z)^(-n-1)` equal the normal-product binomials at
all degrees, by the already established scalar-contraction recurrence. -/
theorem negative_contraction_binomial (n a : ℕ) :
    scalarContraction (-(n : ℤ)-1) a = (Nat.choose (n+a) n : ℂ) := by
  induction a with
  | zero => simp
  | succ a ih =>
    apply mul_left_cancel₀ (show (a+1 : ℂ) ≠ 0 by exact_mod_cast Nat.succ_ne_zero a)
    change (a+1 : ℂ) * scalarContraction (-(n : ℤ)-1) (a+1) =
      (a+1 : ℂ) * (Nat.choose (n+a+1) n : ℂ)
    rw [scalarContraction_step, ih]
    have hnat := Nat.choose_mul_succ_eq (n+a) n
    rw [show n+a+1-n=a+1 by omega] at hnat
    have hc := congrArg (fun q : ℕ => (q : ℂ)) hnat
    push_cast at hc ⊢
    linear_combination hc

theorem left_residue_coefficient (n a : ℕ) :
    leftExpansion (-(n : ℤ)-1) (-(n : ℤ)-1-(a : ℤ)) (a : ℤ) =
      (Nat.choose (a+n) n : ℂ) := by
  simp only [leftExpansion, Nat.cast_nonneg,
    show -(n : ℤ)-1-(a : ℤ)+(a : ℤ)=-(n : ℤ)-1 by omega,
    and_self, if_true, Int.toNat_natCast]
  rw [negative_contraction_binomial, Nat.add_comm]

theorem right_residue_coefficient (n a : ℕ) :
    rightExpansion (-(n : ℤ)-1) (a : ℤ) (-(n : ℤ)-1-(a : ℤ)) =
      (-1 : ℂ)^(n+1) * (Nat.choose (a+n) n : ℂ) := by
  rw [rightExpansion, left_residue_coefficient]
  congr 1
  rw [show -(n : ℤ)-1 = -((n+1 : ℕ) : ℤ) by omega, zpow_neg, zpow_natCast,
    ← inv_pow]
  simp

/-- The minus sign in the residue definition gives precisely the
`(-1)^n` coefficient of the existing annihilationTerm. -/
theorem negative_right_residue_coefficient (n a : ℕ) :
    -rightExpansion (-(n : ℤ)-1) (a : ℤ) (-(n : ℤ)-1-(a : ℤ)) =
      (-1 : ℂ)^n * (Nat.choose (a+n) n : ℂ) := by
  rw [right_residue_coefficient, pow_succ]
  ring

/-- Clearing either negative-power kernel leaves the same polynomial
and explicitly retains the factor of order `s` needed for H--B locality. -/
theorem left_kernel_clear (s n r : ℕ) :
    (crossing^(s+n+1+r)) (leftExpansion (-(n : ℤ)-1)) =
      (crossing^s) (leftExpansion (r : ℤ)) := by
  rw [crossing_left_iterate, crossing_left_iterate]
  have h : -(n : ℤ)-1+((s+n+1+r : ℕ) : ℤ) = (r : ℤ)+(s : ℤ) := by
    push_cast
    ring
  rw [h]

theorem right_kernel_clear (s n r : ℕ) :
    (crossing^(s+n+1+r)) (rightExpansion (-(n : ℤ)-1)) =
      (crossing^s) (leftExpansion (r : ℤ)) := by
  rw [crossing_right_iterate, crossing_left_iterate]
  have h : -(n : ℤ)-1+((s+n+1+r : ℕ) : ℤ) = ((r+s : ℕ) : ℤ) := by
    push_cast
    ring
  rw [h, show (r : ℤ)+(s : ℤ)=((r+s : ℕ) : ℤ) by omega]
  exact (nonnegative_expansions_equal (r+s)).symm

/-- The low `(t-w)` branch of the finite binomial expansion always
contains exactly enough `(t-z)` power to apply the two clearing identities. -/
theorem dong_order_split (p s n j : ℕ) :
    p ≤ j ∨ ∃ r : ℕ, p+s+n-j = s+n+1+r := by
  by_cases h : p ≤ j
  · exact Or.inl h
  · refine Or.inr ⟨p-j-1, ?_⟩
    omega

end HMT.IV.LatticeDongKernel
end

#print axioms HMT.IV.LatticeDongKernel.negative_contraction_binomial
#print axioms HMT.IV.LatticeDongKernel.left_residue_coefficient
#print axioms HMT.IV.LatticeDongKernel.right_residue_coefficient
#print axioms HMT.IV.LatticeDongKernel.negative_right_residue_coefficient
#print axioms HMT.IV.LatticeDongKernel.left_kernel_clear
#print axioms HMT.IV.LatticeDongKernel.right_kernel_clear
#print axioms HMT.IV.LatticeDongKernel.dong_order_split
