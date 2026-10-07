import LatticeHalfGramTransport

/-! The corresponding contragredient form on the ordinary oscillator factor.
It reuses the same marked Gram matrix, factorial pairing and block-map proof;
the frequency is n+1 rather than n+1/2. No new basis or lattice is selected. -/

noncomputable section
namespace HMT.IV.LatticeIntegerFockPairing
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeFactorialPairing LatticeHalfGramTransport LatticeGramDual
open HMT.FockTransport.Symmetric
open scoped BigOperators

def integerScale (n : ℕ) : ℂ := -(n+1:ℂ)

theorem integerScale_ne_zero (n : ℕ) : integerScale n ≠ 0 := by
  exact neg_ne_zero.mpr (by exact_mod_cast Nat.succ_ne_zero n)

def integerGram (o : Fin 12) : Module.End ℂ (Oscillators o) :=
  blockMap o (gram o) integerScale

def integerGramInverse (o : Fin 12) : Module.End ℂ (Oscillators o) :=
  blockMap o (gramInv o) (fun n => (integerScale n)⁻¹)

theorem integerGram_left_inverse (o : Fin 12) :
    (integerGramInverse o).comp (integerGram o) = LinearMap.id :=
  blockMap_comp o (gram o) (gramInv o) integerScale (fun n => (integerScale n)⁻¹)
    (pairing_gramInv o) (fun n => mul_inv_cancel₀ (integerScale_ne_zero n))

theorem integerGram_right_inverse (o : Fin 12) :
    (integerGram o).comp (integerGramInverse o) = LinearMap.id :=
  blockMap_comp o (gramInv o) (gram o) (fun n => (integerScale n)⁻¹) integerScale
    (gramInv_pairing o) (fun n => inv_mul_cancel₀ (integerScale_ne_zero n))

def integerGramTransport (o : Fin 12) : Fock o →ₐ[ℂ] Fock o := gamma (integerGram o)
def integerGramTransportInverse (o : Fin 12) : Fock o →ₐ[ℂ] Fock o :=
  gamma (integerGramInverse o)

theorem integerGramTransport_left_inverse (o : Fin 12) :
    Function.LeftInverse (integerGramTransportInverse o) (integerGramTransport o) := by
  intro v
  have h := congrArg (fun T => gamma T v) (integerGram_left_inverse o)
  simpa only [gamma_composition, AlgHom.comp_apply, gamma_identity, AlgHom.id_apply,
    integerGramTransport, integerGramTransportInverse] using h

theorem integerGramTransport_right_inverse (o : Fin 12) :
    Function.RightInverse (integerGramTransportInverse o) (integerGramTransport o) := by
  intro v
  have h := congrArg (fun T => gamma T v) (integerGram_right_inverse o)
  simpa only [gamma_composition, AlgHom.comp_apply, gamma_identity, AlgHom.id_apply,
    integerGramTransport, integerGramTransportInverse] using h

theorem integerGramTransport_create (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (v : Fock o) :
    integerGramTransport o (create o n i v) =
      ∑ j, (integerScale n*gram o i j) • create o n j (integerGramTransport o v) := by
  change integerGramTransport o (SymmetricAlgebra.ι ℂ (Oscillators o)
    (modeVector o n i)*v) = _
  rw [map_mul, integerGramTransport, gamma_generator]
  simp only [integerGram, blockMap_mode, map_sum, map_smul,
    Finset.sum_mul, smul_mul_assoc]
  rfl

def contravariantPairing (o : Fin 12) : LinearMap.BilinForm ℂ (Fock o) :=
  LinearMap.comp (factorialPairing o) (integerGramTransport o).toLinearMap

theorem contravariantPairing_apply (o : Fin 12) (u v : Fock o) :
    contravariantPairing o u v = factorialPairing o (integerGramTransport o u) v := rfl

theorem contravariantPairing_nondegenerate (o : Fin 12) :
    (contravariantPairing o).Nondegenerate := by
  intro v hv
  have hg : integerGramTransport o v = 0 := factorialPairing_nondegenerate o _ hv
  apply (integerGramTransport_left_inverse o).injective
  simpa only [map_zero] using hg

theorem contravariantPairing_right_separating (o : Fin 12) (v : Fock o)
    (h : ∀ u, contravariantPairing o u v = 0) : v = 0 := by
  apply WeightedBasisPairing.right_separating (monomialBasis o)
    (occupationFactorial o) (occupationFactorial_ne_zero o) v
  intro w
  obtain ⟨u, hu⟩ := (integerGramTransport_right_inverse o).surjective w
  rw [← hu]
  exact h u

theorem annihilate_coordinate_expansion (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) :
    (∑ j, (integerScale n*gram o i j) • coordinateDerivative o (n,j)) =
      -annihilate o n i := by
  classical
  apply LinearMap.ext
  intro v
  simp only [LinearMap.sum_apply, LinearMap.smul_apply, coordinateDerivative,
    Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  have inner (k : Fin (BasisSize o)) :
      (∑ j, (integerScale n*gram o i j*((n+1:ℂ)⁻¹*gramInv o j k)) • annihilate o n k v) =
        (integerScale n*(n+1:ℂ)⁻¹*(if i=k then 1 else 0)) • annihilate o n k v := by
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = (integerScale n*(n+1:ℂ)⁻¹) * ∑ j, gram o i j*gramInv o j k := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by rw [pairing_gramInv]
  simp_rw [inner]
  simp only [mul_ite, mul_one, mul_zero, ite_smul, zero_smul]
  rw [Finset.sum_ite_eq]
  have hn : (n+1:ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
  have hc : integerScale n * (n+1:ℂ)⁻¹ = -1 := by
    rw [integerScale, neg_mul, mul_inv_cancel₀ hn]
  simp only [Finset.mem_univ, if_true, hc, neg_one_smul, LinearMap.neg_apply]

theorem contravariantPairing_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (u v : Fock o) :
    contravariantPairing o (create o n i u) v =
      -contravariantPairing o u (annihilate o n i v) := by
  rw [contravariantPairing_apply, integerGramTransport_create]
  simp only [map_sum, LinearMap.sum_apply, map_smul, LinearMap.smul_apply,
    factorialPairing_create]
  have h := LinearMap.congr_fun (annihilate_coordinate_expansion o n i) v
  simp only [LinearMap.sum_apply, LinearMap.smul_apply, LinearMap.neg_apply] at h
  calc
    _ = ∑ j, (integerScale n*gram o i j) • factorialPairing o (integerGramTransport o u)
        (coordinateDerivative o (n,j) v) := by
      apply Finset.sum_congr rfl
      intro j _
      rw [factorialPairing_create o (n,j)]
    _ = factorialPairing o (integerGramTransport o u)
        (∑ j, (integerScale n*gram o i j) • coordinateDerivative o (n,j) v) := by
      simp only [map_sum, map_smul]
    _ = _ := by rw [h, map_neg]; rfl

end HMT.IV.LatticeIntegerFockPairing
end

#print axioms HMT.IV.LatticeIntegerFockPairing.contravariantPairing_nondegenerate
#print axioms HMT.IV.LatticeIntegerFockPairing.contravariantPairing_create
