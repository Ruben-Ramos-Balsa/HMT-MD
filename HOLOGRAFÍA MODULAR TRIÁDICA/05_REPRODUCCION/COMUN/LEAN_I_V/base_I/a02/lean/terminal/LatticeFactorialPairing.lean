import WeightedBasisPairing
import LatticeGramContractions

/-! The factorial pairing on the inherited oscillator monomial basis.
This coordinate pairing is a proof device; the contravariant Gram transport
is applied in the following module, before any physical identification. -/

noncomputable section
namespace HMT.IV.LatticeFactorialPairing
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeModeWeights LatticeGramContractions LatticeGramDual
open scoped BigOperators

def occupationFactorial (o : Fin 12) (a : Occupation o) : ℂ :=
  a.prod (fun _ k => (k.factorial : ℂ))

theorem occupationFactorial_ne_zero (o : Fin 12) (a : Occupation o) :
    occupationFactorial o a ≠ 0 := by
  classical
  apply Finsupp.prod_ne_zero_iff.mpr
  intro p _
  exact_mod_cast Nat.factorial_ne_zero (a p)

@[simp] theorem occupationFactorial_zero (o : Fin 12) : occupationFactorial o 0 = 1 := by
  simp [occupationFactorial]

theorem occupationFactorial_succ (o : Fin 12) (a : Occupation o) (p : Mode o) :
    occupationFactorial o (Finsupp.single p 1 + a) =
      ((a p : ℂ)+1) * occupationFactorial o a := by
  classical
  have h0 (i : Mode o) : ((0:ℕ).factorial : ℂ) = 1 := by simp
  have h1 := Finsupp.mul_prod_erase' (Finsupp.single p 1+a) p
    (fun _ k => (k.factorial : ℂ)) h0
  have h2 := Finsupp.mul_prod_erase' a p (fun _ k => (k.factorial : ℂ)) h0
  have he : (Finsupp.single p 1+a).erase p = a.erase p := by
    ext q
    by_cases h : q=p
    · subst q; simp
    · simp [Finsupp.erase_ne h, h, Ne.symm h]
  rw [he] at h1
  simp only [Finsupp.add_apply, Finsupp.single_eq_same] at h1
  rw [show 1+a p = a p+1 by omega, Nat.factorial_succ, Nat.cast_mul,
    Nat.cast_add, Nat.cast_one] at h1
  change (Finsupp.single p 1+a).prod (fun _ k => (k.factorial : ℂ)) =
    ((a p : ℂ)+1) * a.prod (fun _ k => (k.factorial : ℂ))
  rw [← h2, ← h1, mul_assoc]

def factorialPairing (o : Fin 12) : LinearMap.BilinForm ℂ (Fock o) :=
  WeightedBasisPairing.form (monomialBasis o) (occupationFactorial o)

theorem factorialPairing_left (o : Fin 12) (a : Occupation o) (v : Fock o) :
    factorialPairing o (monomialBasis o a) v =
      occupationFactorial o a * (monomialBasis o).repr v a :=
  WeightedBasisPairing.basis_left _ _ _ _

theorem factorialPairing_right (o : Fin 12) (v : Fock o) (a : Occupation o) :
    factorialPairing o v (monomialBasis o a) =
      occupationFactorial o a * (monomialBasis o).repr v a :=
  WeightedBasisPairing.basis_right _ _ _ _

theorem factorialPairing_symmetric (o : Fin 12) (v w : Fock o) :
    factorialPairing o v w = factorialPairing o w v :=
  WeightedBasisPairing.symmetric _ _ _ _

theorem factorialPairing_nondegenerate (o : Fin 12) :
    (factorialPairing o).Nondegenerate :=
  WeightedBasisPairing.nondegenerate _ _ (occupationFactorial_ne_zero o)

def coordinateDerivative (o : Fin 12) (p : Mode o) : Module.End ℂ (Fock o) :=
  ((p.1+1:ℂ)⁻¹) • ∑ j, gramInv o p.2 j • annihilate o p.1 j

theorem coordinateDerivative_monomial (o : Fin 12) (p : Mode o) (a : Occupation o) :
    coordinateDerivative o p (monomialBasis o a) =
      (a p : ℂ) • monomialBasis o (a-Finsupp.single p 1) := by
  have hn : (p.1+1:ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero p.1
  simp only [coordinateDerivative, LinearMap.smul_apply, LinearMap.sum_apply]
  rw [dualAnnihilate_monomial, smul_smul]
  congr 1
  field_simp

theorem factorialPairing_create_monomial (o : Fin 12) (p : Mode o)
    (a b : Occupation o) :
    factorialPairing o (create o p.1 p.2 (monomialBasis o a)) (monomialBasis o b) =
      factorialPairing o (monomialBasis o a) (coordinateDerivative o p (monomialBasis o b)) := by
  classical
  rw [create_monomial, coordinateDerivative_monomial, map_smul,
    factorialPairing_left, factorialPairing_left]
  simp only [Basis.repr_self, Finsupp.single_apply, smul_eq_mul]
  by_cases hb : b=Finsupp.single p 1+a
  · subst b
    rw [occupationFactorial_succ]
    have he : Finsupp.single p 1+a-Finsupp.single p 1 = a := by
      exact add_tsub_cancel_left _ _
    simp [he, Finsupp.add_apply, Finsupp.single_eq_same, mul_comm, add_comm]
  · by_cases hz : b p=0
    · simp [hb, hz]
    · have ha : b-Finsupp.single p 1 ≠ a := by
        intro he
        apply hb
        have hle : Finsupp.single p 1 ≤ b := by
          rw [Finsupp.single_le_iff]
          omega
        have hh := tsub_add_cancel_of_le hle
        rw [he] at hh
        exact hh.symm.trans (add_comm _ _)
      simp [hb, ha]

theorem factorialPairing_create (o : Fin 12) (p : Mode o) (u v : Fock o) :
    factorialPairing o (create o p.1 p.2 u) v =
      factorialPairing o u (coordinateDerivative o p v) := by
  have h : LinearMap.comp (factorialPairing o) (create o p.1 p.2) =
      (factorialPairing o).compl₂ (coordinateDerivative o p) := by
    apply (monomialBasis o).ext
    intro a
    apply (monomialBasis o).ext
    intro b
    exact factorialPairing_create_monomial o p a b
  exact LinearMap.congr_fun (LinearMap.congr_fun h u) v

end HMT.IV.LatticeFactorialPairing
end
