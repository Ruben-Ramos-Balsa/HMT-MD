import LatticeOscillatorFock
import Mathlib.LinearAlgebra.Matrix.BilinearForm
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

/-!
The inverse of the existing lattice Gram matrix. Nondegeneracy is derived
from the already proved positive rational pairing on the constructed marked
neighbour, before taking a matrix in its actual integral basis. No inverse
identity, determinant value, target lattice or conformal axiom is assumed.
-/

noncomputable section
namespace HMT.IV.LatticeGramDual

open LatticeCocycle LatticeOscillatorFock CoxeterNeighbor
open scoped BigOperators Matrix

def integerForm (o : Fin 12) : LinearMap.BilinForm ℤ (Lattice o) where
  toFun x :=
    { toFun := integerPair o x
      map_add' y z := integerPair_add_right o x y z
      map_smul' r y := integerPair_smul_right o r x y }
  map_add' x y := by
    ext z
    exact integerPair_add_left o x y z
  map_smul' r x := by
    ext y
    exact integerPair_smul_left o r x y

theorem integerForm_nondegenerate (o : Fin 12) : (integerForm o).Nondegenerate := by
  intro x hx
  have hz : integerPair o x x = 0 := hx x
  apply Subtype.ext
  apply (pairing_self_eq_zero_iff (x : Space 12)).mp
  rw [← cast_integerPair, hz]
  rfl

def integerGram (o : Fin 12) : Matrix (Fin (BasisSize o)) (Fin (BasisSize o)) ℤ :=
  BilinForm.toMatrix (latticeBasis o) (integerForm o)

theorem integerGram_apply (o : Fin 12) (i j : Fin (BasisSize o)) :
    integerGram o i j = integerPair o (latticeBasis o i) (latticeBasis o j) := by
  exact BilinForm.toMatrix_apply (latticeBasis o) (integerForm o) i j

theorem integerGram_det_ne_zero (o : Fin 12) : (integerGram o).det ≠ 0 :=
  (LinearMap.BilinForm.nondegenerate_iff_det_ne_zero (latticeBasis o)).mp
    (integerForm_nondegenerate o)

def gramMatrix (o : Fin 12) : Matrix (Fin (BasisSize o)) (Fin (BasisSize o)) ℂ := gram o

theorem gram_eq_integerGram_cast (o : Fin 12) :
    gramMatrix o = (integerGram o).map (fun z : ℤ => (z : ℂ)) := by
  ext i j
  simp only [gramMatrix, gram, Matrix.map_apply, integerGram_apply]

theorem gram_det_ne_zero (o : Fin 12) : (gramMatrix o).det ≠ 0 := by
  rw [gram_eq_integerGram_cast, ← Int.cast_det]
  exact_mod_cast integerGram_det_ne_zero o

def gramInv (o : Fin 12) : Matrix (Fin (BasisSize o)) (Fin (BasisSize o)) ℂ :=
  (gramMatrix o)⁻¹

theorem gramInv_mul_gram (o : Fin 12) : gramInv o * gramMatrix o = 1 :=
  Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr (gram_det_ne_zero o))

theorem gram_mul_gramInv (o : Fin 12) : gramMatrix o * gramInv o = 1 :=
  Matrix.mul_nonsing_inv _ (isUnit_iff_ne_zero.mpr (gram_det_ne_zero o))

theorem gramInv_pairing (o : Fin 12) (i k : Fin (BasisSize o)) :
    ∑ j, gramInv o i j * gram o j k = if i=k then 1 else 0 := by
  have h := congrArg (fun M => M i k) (gramInv_mul_gram o)
  simpa only [Matrix.mul_apply, Matrix.one_apply] using h

theorem pairing_gramInv (o : Fin 12) (i k : Fin (BasisSize o)) :
    ∑ j, gram o i j * gramInv o j k = if i=k then 1 else 0 := by
  have h := congrArg (fun M => M i k) (gram_mul_gramInv o)
  simpa only [Matrix.mul_apply, Matrix.one_apply] using h

end HMT.IV.LatticeGramDual
end

#print axioms HMT.IV.LatticeGramDual.integerForm_nondegenerate
#print axioms HMT.IV.LatticeGramDual.integerGram_det_ne_zero
#print axioms HMT.IV.LatticeGramDual.gram_det_ne_zero
#print axioms HMT.IV.LatticeGramDual.gramInv_mul_gram
#print axioms HMT.IV.LatticeGramDual.gram_mul_gramInv
#print axioms HMT.IV.LatticeGramDual.gramInv_pairing
#print axioms HMT.IV.LatticeGramDual.pairing_gramInv
