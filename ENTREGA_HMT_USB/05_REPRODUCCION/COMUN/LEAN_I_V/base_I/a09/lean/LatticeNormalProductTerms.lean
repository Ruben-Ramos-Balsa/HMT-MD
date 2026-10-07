import LatticeNormalOrderedField

/-! The four genuine pointwise contributions to two successive normal products.
The lattice and Heisenberg representation are inherited unchanged. -/
noncomputable section
namespace HMT.IV.LatticeNormalProductTerms
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeNormalOrderedField

def cc (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) : LatticeCarrier o :=
  (Nat.choose (a+n) n : ℂ) • onCarrier o (create o (a+n) i)
    (creationTerm o j m B (k-a) b v)

def ca (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) : LatticeCarrier o :=
  (Nat.choose (a+n) n : ℂ) • onCarrier o (create o (a+n) i)
    (annihilationTerm o j m B (k-a) b v)

def ac (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) : LatticeCarrier o :=
  ((-1 : ℂ)^n * (Nat.choose (a+n) n : ℂ)) •
    creationTerm o j m B (k+a+n+1) b (hmode o i (a : ℤ) v)

def aa (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o)
    (a b : ℕ) : LatticeCarrier o :=
  ((-1 : ℂ)^n * (Nat.choose (a+n) n : ℂ)) •
    annihilationTerm o j m B (k+a+n+1) b (hmode o i (a : ℤ) v)

end HMT.IV.LatticeNormalProductTerms
end
