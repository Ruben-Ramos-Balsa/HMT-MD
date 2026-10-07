import LatticeTwistedNormalDerivative
import LatticeFiniteDoubleSums

/-! Four contributions to iterated divided half-normal products. The weighted
same-sign operators commute by the inherited half-Heisenberg CCR. -/
noncomputable section
namespace HMT.IV.LatticeTwistedNormalTerms
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeHalfIntegerHeisenberg hiding halfMode
open LatticeTwistedOscillatorTensor LatticeFiniteIrreducible
open LatticeTwistedNormalDerivative

def creator (o : Fin 12) (i : Fin (BasisSize o)) (n a : ℕ) : Module.End ℂ (Carrier o) :=
  dividedFactor (2*(a:ℤ)-1) n • halfMode o i (Int.negSucc a)

def annihilator (o : Fin 12) (i : Fin (BasisSize o)) (n a : ℕ) : Module.End ℂ (Carrier o) :=
  dividedFactor (-2*(a:ℤ)-3) n • halfMode o i (a:ℤ)

theorem creators_commute (o : Fin 12) (i j : Fin (BasisSize o)) (n m a b : ℕ)
    (v : Carrier o) : creator o i n a (creator o j m b v) =
      creator o j m b (creator o i n a v) := by
  have h := half_heisenberg_tensor (FiniteSpace o) o i j (Int.negSucc a) (Int.negSucc b)
  have hn : frequency (Int.negSucc a) + frequency (Int.negSucc b) ≠ 0 := by
    intro he
    have hz := (frequency_sum_zero (Int.negSucc a) (Int.negSucc b)).mp he
    omega
  rw [if_neg hn, zero_smul, sub_eq_zero] at h
  have hv := LinearMap.congr_fun h v
  simp only [Module.End.mul_apply] at hv
  simp only [creator, LinearMap.smul_apply, map_smul]
  rw [hv, smul_comm]

theorem annihilators_commute (o : Fin 12) (i j : Fin (BasisSize o)) (n m a b : ℕ)
    (v : Carrier o) : annihilator o i n a (annihilator o j m b v) =
      annihilator o j m b (annihilator o i n a v) := by
  have h := half_heisenberg_tensor (FiniteSpace o) o i j (a:ℤ) (b:ℤ)
  have hn : frequency (a:ℤ) + frequency (b:ℤ) ≠ 0 := by
    intro he
    have hz := (frequency_sum_zero (a:ℤ) (b:ℤ)).mp he
    omega
  rw [if_neg hn, zero_smul, sub_eq_zero] at h
  have hv := LinearMap.congr_fun h v
  simp only [Module.End.mul_apply] at hv
  simp only [annihilator, LinearMap.smul_apply, map_smul]
  rw [hv, smul_comm]

theorem annihilators_bounded (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (v : Carrier o) : ∃ N : ℕ, ∀ a ≥ N, annihilator o i n a v = 0 := by
  obtain ⟨N,hN⟩ := LatticeTwistedNormalProduct.nonnegative_modes_bounded o i v
  exact ⟨N, fun a ha => by simp only [annihilator, LinearMap.smul_apply, hN a ha, smul_zero]⟩

theorem creationTerm_apply (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) (v : Carrier o) :
    creationTerm o i n B k a v = creator o i n a
      (HVertexOperator.coeff B (k+2*n-2*a+1) v) := rfl

theorem annihilationTerm_apply (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) (v : Carrier o) :
    annihilationTerm o i n B k a v = HVertexOperator.coeff B (k+2*n+2*a+3)
      (annihilator o i n a v) := by
  simp only [annihilationTerm, LatticeTwistedNormalProduct.annihilationTerm,
    annihilator, LinearMap.smul_apply, LinearMap.comp_apply, map_smul]

def cc (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) : Carrier o :=
  creator o i n a (creationTerm o j m B (k+2*n-2*a+1) b v)
def ca (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) : Carrier o :=
  creator o i n a (annihilationTerm o j m B (k+2*n-2*a+1) b v)
def ac (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) : Carrier o :=
  creationTerm o j m B (k+2*n+2*a+3) b (annihilator o i n a v)
def aa (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) : Carrier o :=
  annihilationTerm o j m B (k+2*n+2*a+3) b (annihilator o i n a v)

theorem cc_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) :
    cc o i j n m B k v a b = cc o j i m n B k v b a := by
  simp only [cc, creationTerm_apply]
  rw [show k+2*(n:ℤ)-2*a+1+2*m-2*b+1 = k+2*m-2*b+1+2*n-2*a+1 by omega,
    creators_commute]

theorem ca_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) :
    ca o i j n m B k v a b = ac o j i m n B k v b a := by
  simp only [ca, ac, creationTerm_apply, annihilationTerm_apply]
  rw [show k+2*(n:ℤ)-2*a+1+2*m+2*b+3 = k+2*m+2*b+3+2*n-2*a+1 by omega]

theorem ac_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) :
    ac o i j n m B k v a b = ca o j i m n B k v b a :=
  (ca_swap o j i m n B k v b a).symm

theorem aa_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) (a b : ℕ) :
    aa o i j n m B k v a b = aa o j i m n B k v b a := by
  simp only [aa, annihilationTerm_apply]
  rw [show k+2*(n:ℤ)+2*a+3+2*m+2*b+3 = k+2*m+2*b+3+2*n+2*a+3 by omega,
    annihilators_commute]

end HMT.IV.LatticeTwistedNormalTerms
end

#print axioms HMT.IV.LatticeTwistedNormalTerms.creator
#print axioms HMT.IV.LatticeTwistedNormalTerms.annihilator
#print axioms HMT.IV.LatticeTwistedNormalTerms.creators_commute
#print axioms HMT.IV.LatticeTwistedNormalTerms.annihilators_commute
#print axioms HMT.IV.LatticeTwistedNormalTerms.annihilators_bounded
#print axioms HMT.IV.LatticeTwistedNormalTerms.creationTerm_apply
#print axioms HMT.IV.LatticeTwistedNormalTerms.annihilationTerm_apply
#print axioms HMT.IV.LatticeTwistedNormalTerms.cc
#print axioms HMT.IV.LatticeTwistedNormalTerms.ca
#print axioms HMT.IV.LatticeTwistedNormalTerms.ac
#print axioms HMT.IV.LatticeTwistedNormalTerms.aa
#print axioms HMT.IV.LatticeTwistedNormalTerms.cc_swap
#print axioms HMT.IV.LatticeTwistedNormalTerms.ca_swap
#print axioms HMT.IV.LatticeTwistedNormalTerms.ac_swap
#print axioms HMT.IV.LatticeTwistedNormalTerms.aa_swap
