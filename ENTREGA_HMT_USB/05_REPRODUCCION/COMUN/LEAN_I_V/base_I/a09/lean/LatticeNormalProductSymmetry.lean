import LatticeNormalProductTerms
import LatticeSameSignModes

/-!
Pointwise exchange of the four contributions to iterated normal products.
All operators are the already constructed lattice/oscillator operators.
Only the same-sign CCR consequences and scalar commutativity enter here;
the summability/reindexing of these terms is proved separately.
-/

noncomputable section
namespace HMT.IV.LatticeNormalProductSymmetry

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeNormalOrderedField
open HMT.IV.LatticeNormalProductTerms HMT.IV.LatticeSameSignModes

set_option synthInstance.maxHeartbeats 200000

theorem cc_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) :
    cc o i j n m B k v a b = cc o j i m n B k v b a := by
  simp only [cc, creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    map_smul, smul_smul]
  rw [show k-(a : ℤ)-(b : ℤ) = k-(b : ℤ)-(a : ℤ) by omega,
    carrier_creations_commute o (a+n) (b+m) i j,
    mul_comm (Nat.choose (a+n) n : ℂ) (Nat.choose (b+m) m : ℂ)]

theorem ca_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) :
    ca o i j n m B k v a b = ac o j i m n B k v b a := by
  simp only [ca, ac, creationTerm, annihilationTerm, LinearMap.smul_apply,
    LinearMap.comp_apply, map_smul, smul_smul]
  rw [show k-(a : ℤ)+(b : ℤ)+(m : ℤ)+1 = k+(b : ℤ)+(m : ℤ)+1-(a : ℤ) by omega,
    mul_comm (Nat.choose (a+n) n : ℂ) ((-1 : ℂ)^m * (Nat.choose (b+m) m : ℂ))]

theorem ac_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) :
    ac o i j n m B k v a b = ca o j i m n B k v b a := by
  exact (ca_swap o j i m n B k v b a).symm

theorem aa_swap (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) :
    aa o i j n m B k v a b = aa o j i m n B k v b a := by
  have hc := LinearMap.congr_fun (nonnegative_hmodes_commute o i j a b) v
  simp only [LinearMap.comp_apply] at hc
  simp only [aa, annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    map_smul, smul_smul]
  rw [show k+(a : ℤ)+(n : ℤ)+1+(b : ℤ)+(m : ℤ)+1 =
      k+(b : ℤ)+(m : ℤ)+1+(a : ℤ)+(n : ℤ)+1 by omega,
    ← hc, mul_comm ((-1 : ℂ)^n * (Nat.choose (a+n) n : ℂ))
      ((-1 : ℂ)^m * (Nat.choose (b+m) m : ℂ))]

end HMT.IV.LatticeNormalProductSymmetry
end

#print axioms HMT.IV.LatticeNormalProductSymmetry.cc_swap
#print axioms HMT.IV.LatticeNormalProductSymmetry.ca_swap
#print axioms HMT.IV.LatticeNormalProductSymmetry.ac_swap
#print axioms HMT.IV.LatticeNormalProductSymmetry.aa_swap
