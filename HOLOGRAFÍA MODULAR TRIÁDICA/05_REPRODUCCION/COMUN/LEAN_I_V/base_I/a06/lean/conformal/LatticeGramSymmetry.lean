import LatticeGramDual

/-! Symmetry of the inverse of the actual inherited Gram matrix. -/

noncomputable section
namespace HMT.IV.LatticeGramSymmetry

open LatticeCocycle LatticeOscillatorFock LatticeGramDual

theorem gramMatrix_transpose (o : Fin 12) :
    (gramMatrix o).transpose = gramMatrix o := by
  ext i j
  exact gram_symmetric o j i

theorem gramInv_transpose (o : Fin 12) :
    (gramInv o).transpose = gramInv o := by
  rw [gramInv, Matrix.transpose_nonsing_inv, gramMatrix_transpose]

theorem gramInv_symmetric (o : Fin 12) (i j : Fin (BasisSize o)) :
    gramInv o i j = gramInv o j i := by
  have h := congrArg (fun M => M j i) (gramInv_transpose o)
  simpa only [Matrix.transpose_apply] using h

end HMT.IV.LatticeGramSymmetry
end

#print axioms HMT.IV.LatticeGramSymmetry.gramMatrix_transpose
#print axioms HMT.IV.LatticeGramSymmetry.gramInv_transpose
#print axioms HMT.IV.LatticeGramSymmetry.gramInv_symmetric
