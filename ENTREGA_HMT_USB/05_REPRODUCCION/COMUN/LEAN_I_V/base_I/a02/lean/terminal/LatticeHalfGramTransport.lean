import LatticeFactorialPairing
import LatticeHalfIntegerHeisenberg

/-! The block Gram automorphism and its explicit inverse on the inherited
oscillators. The minus sign is the contragredient convention; positive
frequency is n+1/2. No orthonormal basis replaces the marked lattice basis. -/

noncomputable section
namespace HMT.IV.LatticeHalfGramTransport
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeGramDual LatticeGramSymmetry LatticeModeWeights
open HMT.FockTransport.Symmetric
open scoped BigOperators

def halfScale (n : ℕ) : ℂ := -((n:ℂ)+1/2)

theorem halfScale_ne_zero (n : ℕ) : halfScale n ≠ 0 := by
  unfold halfScale
  apply neg_ne_zero.mpr
  intro h
  have h2 : (2*(n:ℂ)+1) = 0 := by linear_combination 2*h
  have hn : 2*n+1=0 := by exact_mod_cast h2
  omega

def blockMap (o : Fin 12) (A : Fin (BasisSize o) → Fin (BasisSize o) → ℂ)
    (s : ℕ → ℂ) : Module.End ℂ (Oscillators o) :=
  (oscillatorBasis o).constr ℂ (fun p => ∑ j, (s p.1*A p.2 j) • modeVector o p.1 j)

theorem blockMap_mode (o : Fin 12) (A : Fin (BasisSize o) → Fin (BasisSize o) → ℂ)
    (s : ℕ → ℂ) (n : ℕ) (i : Fin (BasisSize o)) :
    blockMap o A s (modeVector o n i) = ∑ j, (s n*A i j) • modeVector o n j := by
  exact Basis.constr_basis _ _ _ (n,i)

theorem blockMap_comp (o : Fin 12)
    (A B : Fin (BasisSize o) → Fin (BasisSize o) → ℂ) (s t : ℕ → ℂ)
    (hAB : ∀ i k, ∑ j, A i j*B j k = if i=k then 1 else 0)
    (hst : ∀ n, s n*t n=1) :
    (blockMap o B t).comp (blockMap o A s) = LinearMap.id := by
  classical
  apply (oscillatorBasis o).ext
  rintro ⟨n,i⟩
  change blockMap o B t (blockMap o A s (modeVector o n i)) = modeVector o n i
  simp only [blockMap_mode, map_sum, map_smul, Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  have inner (k : Fin (BasisSize o)) :
      (∑ j, (s n*A i j*(t n*B j k)) • modeVector o n k) =
        (if i=k then (1:ℂ) else 0) • modeVector o n k := by
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = (s n*t n) * ∑ j, A i j*B j k := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by rw [hst, one_mul, hAB]
  simp_rw [inner]
  simp

def halfGram (o : Fin 12) : Module.End ℂ (Oscillators o) :=
  blockMap o (gram o) halfScale

def halfGramInverse (o : Fin 12) : Module.End ℂ (Oscillators o) :=
  blockMap o (gramInv o) (fun n => (halfScale n)⁻¹)

theorem halfGram_left_inverse (o : Fin 12) :
    (halfGramInverse o).comp (halfGram o) = LinearMap.id :=
  blockMap_comp o (gram o) (gramInv o) halfScale (fun n => (halfScale n)⁻¹)
    (pairing_gramInv o) (fun n => mul_inv_cancel₀ (halfScale_ne_zero n))

theorem halfGram_right_inverse (o : Fin 12) :
    (halfGram o).comp (halfGramInverse o) = LinearMap.id :=
  blockMap_comp o (gramInv o) (gram o) (fun n => (halfScale n)⁻¹) halfScale
    (gramInv_pairing o) (fun n => inv_mul_cancel₀ (halfScale_ne_zero n))

def halfGramEquiv (o : Fin 12) : Oscillators o ≃ₗ[ℂ] Oscillators o :=
  LinearEquiv.ofLinear (halfGram o) (halfGramInverse o)
    (halfGram_right_inverse o) (halfGram_left_inverse o)

def gramTransport (o : Fin 12) : Fock o →ₐ[ℂ] Fock o := gamma (halfGram o)
def gramTransportInverse (o : Fin 12) : Fock o →ₐ[ℂ] Fock o := gamma (halfGramInverse o)

theorem gramTransport_left_inverse (o : Fin 12) :
    Function.LeftInverse (gramTransportInverse o) (gramTransport o) := by
  intro v
  have h := congrArg (fun T => gamma T v) (halfGram_left_inverse o)
  simpa only [gamma_composition, AlgHom.comp_apply, gamma_identity, AlgHom.id_apply,
    gramTransport, gramTransportInverse] using h

theorem gramTransport_right_inverse (o : Fin 12) :
    Function.RightInverse (gramTransportInverse o) (gramTransport o) := by
  intro v
  have h := congrArg (fun T => gamma T v) (halfGram_right_inverse o)
  simpa only [gamma_composition, AlgHom.comp_apply, gamma_identity, AlgHom.id_apply,
    gramTransport, gramTransportInverse] using h

theorem gramTransport_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) (v : Fock o) :
    gramTransport o (create o n i v) =
      ∑ j, (halfScale n*gram o i j) • create o n j (gramTransport o v) := by
  change gramTransport o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i)*v) = _
  rw [map_mul, gramTransport, gamma_generator]
  simp only [halfGram, blockMap_mode, map_sum, map_smul, Finset.sum_mul, smul_mul_assoc]
  rfl

end HMT.IV.LatticeHalfGramTransport
end
