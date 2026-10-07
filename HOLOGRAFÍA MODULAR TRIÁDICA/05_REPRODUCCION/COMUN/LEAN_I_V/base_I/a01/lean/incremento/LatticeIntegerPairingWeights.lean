import LatticeIntegerFockPairing

/-! Orthogonality for the existing untwisted contravariant Fock pairing.
The weight is `occupationWeight = ∑ (n+1) a(n,i)`, not the half-integer
grading. Weight orthogonality follows from the already proved creation /
annihilation adjointness. Negation is the existing `fockTheta` on this same
symmetric algebra; no new pairing, energy operator or parity is introduced. -/

noncomputable section
namespace HMT.IV.LatticeIntegerPairingWeights

open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeModeWeights LatticeFactorialPairing LatticeIntegerFockPairing
open LatticeParityCarrier HMT.FockTransport.Symmetric
open scoped BigOperators

private theorem weight_orthogonal_create (o : Fin 12) (a : Occupation o)
    (ha : ∀ b : Occupation o, occupationWeight o a ≠ occupationWeight o b →
      contravariantPairing o (monomialBasis o a) (monomialBasis o b) = 0)
    (n : ℕ) (i : Fin (BasisSize o)) (b : Occupation o)
    (hab : occupationWeight o (Finsupp.single (n,i) 1+a) ≠ occupationWeight o b) :
    contravariantPairing o (create o n i (monomialBasis o a))
      (monomialBasis o b) = 0 := by
  classical
  rw [contravariantPairing_create, annihilate_monomial]
  simp only [Finsupp.sum, map_sum, map_smul]
  apply neg_eq_zero.mpr
  apply Finset.sum_eq_zero
  intro p _
  by_cases hc : (b p : ℂ) *
      (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0) = 0
  · rw [hc, zero_smul]
  · have hw := annihilate_nonzero_term_weight o n i b p hc
    have hn : occupationWeight o a ≠ occupationWeight o (b-Finsupp.single p 1) := by
      intro he
      apply hab
      rw [create_monomial_weight, he]
      exact hw
    rw [ha _ hn, smul_zero]

theorem contravariantPairing_weight_orthogonal (o : Fin 12) (a b : Occupation o)
    (hab : occupationWeight o a ≠ occupationWeight o b) :
    contravariantPairing o (monomialBasis o a) (monomialBasis o b) = 0 := by
  classical
  have hm (a : Occupation o) : ∀ b : Occupation o,
      occupationWeight o a ≠ occupationWeight o b →
      contravariantPairing o (monomialBasis o a) (monomialBasis o b) = 0 := by
    induction a using Finsupp.induction with
    | zero =>
      intro b hb
      have hb0 : b ≠ 0 := by intro h; subst b; exact hb rfl
      have ht : integerGramTransport o (monomialBasis o 0) = monomialBasis o 0 := by
        rw [monomialBasis_product, Finsupp.prod_zero_index, map_one]
      rw [contravariantPairing_apply, ht, factorialPairing_left]
      simp [Basis.repr_self, Finsupp.single_apply, hb0, Ne.symm hb0]
    | @single_add p k a _ hk0 ih =>
      clear hk0
      induction k with
      | zero => simpa using ih
      | succ k hk =>
        have heq : Finsupp.single p (k+1)+a =
            Finsupp.single p 1+(Finsupp.single p k+a) := by
          rw [← add_assoc, ← Finsupp.single_add]
          congr 2
          omega
        rw [heq]
        intro b hb
        rw [← create_monomial]
        exact weight_orthogonal_create o _ hk p.1 p.2 b hb
  exact hm a b hab

theorem integerGramTransport_theta (o : Fin 12) (v : Fock o) :
    integerGramTransport o (fockTheta o v) =
      fockTheta o (integerGramTransport o v) := by
  induction v using SymmetricAlgebra.induction with
  | algebraMap r => simp
  | ι x => simp [integerGramTransport, gamma_generator]
  | mul x y hx hy => simp only [map_mul, hx, hy]
  | add x y hx hy => simp only [map_add, hx, hy]

theorem factorialPairing_theta (o : Fin 12) (u v : Fock o) :
    factorialPairing o (fockTheta o u) v = factorialPairing o u (fockTheta o v) := by
  have he : LinearMap.comp (factorialPairing o) (fockTheta o).toLinearMap =
      (factorialPairing o).compl₂ (fockTheta o).toLinearMap := by
    apply (monomialBasis o).ext
    intro a
    apply (monomialBasis o).ext
    intro b
    change factorialPairing o (fockTheta o (monomialBasis o a)) (monomialBasis o b) =
      factorialPairing o (monomialBasis o a) (fockTheta o (monomialBasis o b))
    rw [fockTheta_monomial, fockTheta_monomial]
    simp only [map_smul, LinearMap.smul_apply, factorialPairing_left,
      Basis.repr_self, Finsupp.single_apply, smul_eq_mul]
    split_ifs with hab
    · subst b; rfl
    · simp
  exact LinearMap.congr_fun (LinearMap.congr_fun he u) v

theorem contravariantPairing_theta (o : Fin 12) (u v : Fock o) :
    contravariantPairing o (fockTheta o u) v =
      contravariantPairing o u (fockTheta o v) := by
  rw [contravariantPairing_apply, integerGramTransport_theta, factorialPairing_theta,
    contravariantPairing_apply]

theorem contravariantPairing_parity_orthogonal (o : Fin 12) (a b : Occupation o)
    (hab : occupationLength o a % 2 ≠ occupationLength o b % 2) :
    contravariantPairing o (monomialBasis o a) (monomialBasis o b) = 0 := by
  have ht := contravariantPairing_theta o (monomialBasis o a) (monomialBasis o b)
  rw [fockTheta_monomial, fockTheta_monomial] at ht
  simp only [map_smul, LinearMap.smul_apply, smul_eq_mul] at ht
  by_contra hz
  have hs := mul_right_cancel₀ hz ht
  rw [neg_one_pow_eq_ite, neg_one_pow_eq_ite] at hs
  simp only [Nat.even_iff] at hs
  have ha2 := Nat.mod_lt (occupationLength o a) (by decide : 0 < 2)
  have hb2 := Nat.mod_lt (occupationLength o b) (by decide : 0 < 2)
  split_ifs at hs <;> norm_num at hs
  all_goals omega

end HMT.IV.LatticeIntegerPairingWeights
end

#print axioms HMT.IV.LatticeIntegerPairingWeights.contravariantPairing_weight_orthogonal
#print axioms HMT.IV.LatticeIntegerPairingWeights.integerGramTransport_theta
#print axioms HMT.IV.LatticeIntegerPairingWeights.factorialPairing_theta
#print axioms HMT.IV.LatticeIntegerPairingWeights.contravariantPairing_theta
#print axioms HMT.IV.LatticeIntegerPairingWeights.contravariantPairing_parity_orthogonal
