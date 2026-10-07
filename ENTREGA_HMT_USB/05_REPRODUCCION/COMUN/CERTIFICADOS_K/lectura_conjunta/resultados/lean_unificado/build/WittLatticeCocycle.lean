import WittPairingParity
import IntegralBasisParity
import TriangularSignCocycle

namespace HMT.IV.LatticeCocycle

open HMT.IV.CoxeterNeighbor
namespace TC
export HMT.IV.TriangularCocycle (bilinear tau tau_zero_left tau_zero_right
  tau_cocycle tau_commutator sign sign_sq sign_add)
end TC

noncomputable abbrev BasisSize (o : Fin 12) := Module.finrank ℤ (Lattice o)

noncomputable def latticeBasis (o : Fin 12) :
    Basis (Fin (BasisSize o)) ℤ (Lattice o) := Module.finBasis ℤ (Lattice o)

noncomputable def parityCoordinates (o : Fin 12) (x : Lattice o) :
    Fin (BasisSize o) → ZMod 2 := fun i => (latticeBasis o).repr x i

noncomputable def parityGram (o : Fin 12) :
    Matrix (Fin (BasisSize o)) (Fin (BasisSize o)) (ZMod 2) :=
  fun i j => parityBilinear o (latticeBasis o i) (latticeBasis o j)

theorem parityGram_symmetric (o : Fin 12) (i j : Fin (BasisSize o)) :
    parityGram o i j = parityGram o j i := parityPair_comm o _ _

theorem parityGram_diagonal_zero (o : Fin 12) (i : Fin (BasisSize o)) :
    parityGram o i i = 0 := parityPair_self_zero o _

theorem parityCoordinates_zero (o : Fin 12) : parityCoordinates o 0 = 0 := by
  funext i
  simp [parityCoordinates]

theorem parityCoordinates_add (o : Fin 12) (x y : Lattice o) :
    parityCoordinates o (x+y) = parityCoordinates o x + parityCoordinates o y := by
  funext i
  simp [parityCoordinates]

theorem parityGram_recovers_pairing (o : Fin 12) (x y : Lattice o) :
    TC.bilinear (parityGram o) (parityCoordinates o x) (parityCoordinates o y) =
      parityBilinear o x y := by
  symm
  exact integral_basis_parity_expansion (latticeBasis o) (parityBilinear o) x y

noncomputable def wittCocycle (o : Fin 12) (x y : Lattice o) : ZMod 2 :=
  TC.tau (parityGram o) (parityCoordinates o x) (parityCoordinates o y)

theorem wittCocycle_zero_left (o : Fin 12) (x : Lattice o) :
    wittCocycle o 0 x = 0 := by
  simp only [wittCocycle, parityCoordinates_zero]
  exact TC.tau_zero_left _ _

theorem wittCocycle_zero_right (o : Fin 12) (x : Lattice o) :
    wittCocycle o x 0 = 0 := by
  simp only [wittCocycle, parityCoordinates_zero]
  exact TC.tau_zero_right _ _

theorem wittCocycle_cocycle (o : Fin 12) (x y z : Lattice o) :
    wittCocycle o x y + wittCocycle o (x+y) z =
      wittCocycle o y z + wittCocycle o x (y+z) := by
  simp only [wittCocycle, parityCoordinates_add]
  exact TC.tau_cocycle _ _ _ _

theorem wittCocycle_commutator (o : Fin 12) (x y : Lattice o) :
    wittCocycle o x y + wittCocycle o y x = parityBilinear o x y := by
  rw [← parityGram_recovers_pairing]
  exact TC.tau_commutator (parityGram o) (parityGram_symmetric o)
    (parityGram_diagonal_zero o) (parityCoordinates o x) (parityCoordinates o y)

noncomputable def wittSign (o : Fin 12) (x y : Lattice o) : ℤ :=
  TC.sign (wittCocycle o x y)

theorem wittSign_zero_left (o : Fin 12) (x : Lattice o) : wittSign o 0 x = 1 := by
  simp [wittSign, wittCocycle_zero_left, TC.sign]

theorem wittSign_zero_right (o : Fin 12) (x : Lattice o) : wittSign o x 0 = 1 := by
  simp [wittSign, wittCocycle_zero_right, TC.sign]

theorem wittSign_square (o : Fin 12) (x y : Lattice o) :
    wittSign o x y * wittSign o x y = 1 := TC.sign_sq _

theorem wittSign_cocycle (o : Fin 12) (x y z : Lattice o) :
    wittSign o x y * wittSign o (x+y) z =
      wittSign o y z * wittSign o x (y+z) := by
  simp only [wittSign, ← TC.sign_add]
  rw [wittCocycle_cocycle]

theorem wittSign_commutator (o : Fin 12) (x y : Lattice o) :
    wittSign o x y * wittSign o y x = TC.sign (integerPair o x y : ZMod 2) := by
  simp only [wittSign, ← TC.sign_add]
  rw [wittCocycle_commutator, parityBilinear_apply]

noncomputable def extensionMul (o : Fin 12) (a b : ZMod 2 × Lattice o) :
    ZMod 2 × Lattice o :=
  (a.1+b.1+wittCocycle o a.2 b.2, a.2+b.2)

theorem extensionMul_assoc (o : Fin 12) (a b c : ZMod 2 × Lattice o) :
    extensionMul o (extensionMul o a b) c = extensionMul o a (extensionMul o b c) := by
  apply Prod.ext
  · dsimp [extensionMul]
    have h := wittCocycle_cocycle o a.2 b.2 c.2
    linear_combination h
  · exact add_assoc _ _ _

theorem extensionMul_zero_left (o : Fin 12) (a : ZMod 2 × Lattice o) :
    extensionMul o (0,0) a = a := by
  ext <;> simp [extensionMul, wittCocycle_zero_left]

theorem extensionMul_zero_right (o : Fin 12) (a : ZMod 2 × Lattice o) :
    extensionMul o a (0,0) = a := by
  ext <;> simp [extensionMul, wittCocycle_zero_right]

theorem wittCocycle_neg_swap (o : Fin 12) (x : Lattice o) :
    wittCocycle o x (-x) = wittCocycle o (-x) x := by
  have h := wittCocycle_cocycle o x (-x) x
  simpa only [add_neg_cancel, neg_add_cancel, wittCocycle_zero_left,
    wittCocycle_zero_right, add_zero] using h

noncomputable def extensionInv (o : Fin 12) (a : ZMod 2 × Lattice o) :
    ZMod 2 × Lattice o := (-a.1-wittCocycle o a.2 (-a.2), -a.2)

theorem extensionMul_inv_right (o : Fin 12) (a : ZMod 2 × Lattice o) :
    extensionMul o a (extensionInv o a) = (0,0) := by
  apply Prod.ext
  · dsimp [extensionMul, extensionInv]
    ring
  · simp [extensionMul, extensionInv]

theorem extensionMul_inv_left (o : Fin 12) (a : ZMod 2 × Lattice o) :
    extensionMul o (extensionInv o a) a = (0,0) := by
  apply Prod.ext
  · dsimp [extensionMul, extensionInv]
    rw [← wittCocycle_neg_swap]
    ring
  · simp [extensionMul, extensionInv]

theorem extension_kernel_central (o : Fin 12) (s : ZMod 2)
    (a : ZMod 2 × Lattice o) :
    extensionMul o (s,0) a = extensionMul o a (s,0) := by
  ext <;> simp [extensionMul, wittCocycle_zero_left, wittCocycle_zero_right, add_comm]

#print axioms parityGram_symmetric
#print axioms parityGram_diagonal_zero
#print axioms parityCoordinates_zero
#print axioms parityCoordinates_add
#print axioms parityGram_recovers_pairing
#print axioms wittCocycle_zero_left
#print axioms wittCocycle_zero_right
#print axioms wittCocycle_cocycle
#print axioms wittCocycle_commutator
#print axioms wittSign_zero_left
#print axioms wittSign_zero_right
#print axioms wittSign_square
#print axioms wittSign_cocycle
#print axioms wittSign_commutator
#print axioms extensionMul_assoc
#print axioms extensionMul_zero_left
#print axioms extensionMul_zero_right
#print axioms wittCocycle_neg_swap
#print axioms extensionMul_inv_right
#print axioms extensionMul_inv_left
#print axioms extension_kernel_central

end HMT.IV.LatticeCocycle
