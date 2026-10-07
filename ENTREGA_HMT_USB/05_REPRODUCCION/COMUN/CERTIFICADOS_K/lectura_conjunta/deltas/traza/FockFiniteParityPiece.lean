import LatticeFockMonomialParity
import Mathlib.LinearAlgebra.Trace

/-!
Finite spans of distinct monomials inside the existing oscillator algebra.
The finite endomorphism is proved to be the restriction of fockTheta, not
an unrelated diagonal model. Its trace is then computed in that actual span.
-/

noncomputable section
namespace HMT.IV.FockFiniteParityPiece

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeFockMonomialParity

variable (o : Fin 12) {ι : Type*} (labels : ι → Occupation o)
  (hinj : Function.Injective labels)

def piece : Submodule ℂ (Fock o) :=
  Submodule.span ℂ (Set.range (fun i => monomialBasis o (labels i)))

include hinj

theorem labels_independent :
    LinearIndependent ℂ (fun i => monomialBasis o (labels i)) :=
  (monomialBasis o).linearIndependent.comp labels hinj

def pieceBasis : Basis ι ℂ (piece o labels) :=
  Basis.span (labels_independent o labels hinj)

@[simp] theorem pieceBasis_coe (i : ι) :
    (pieceBasis o labels hinj i : Fock o) = monomialBasis o (labels i) :=
  Basis.span_apply _ i

def pieceTheta : Module.End ℂ (piece o labels) :=
  (pieceBasis o labels hinj).constr ℂ (fun i =>
    (-1 : ℂ) ^ occupationLength o (labels i) • pieceBasis o labels hinj i)

@[simp] theorem pieceTheta_basis (i : ι) :
    pieceTheta o labels hinj (pieceBasis o labels hinj i) =
      (-1 : ℂ) ^ occupationLength o (labels i) • pieceBasis o labels hinj i :=
  Basis.constr_basis _ _ _ _

theorem restriction_intertwines :
    (piece o labels).subtype.comp (pieceTheta o labels hinj) =
      (fockTheta o).toLinearMap.comp (piece o labels).subtype := by
  apply (pieceBasis o labels hinj).ext
  intro i
  simp only [LinearMap.comp_apply, pieceTheta_basis, map_smul,
    Submodule.subtype_apply, pieceBasis_coe, AlgHom.toLinearMap_apply,
    fockTheta_monomial]

theorem pieceTheta_is_actual_restriction (v : piece o labels) :
    (pieceTheta o labels hinj v : Fock o) = fockTheta o (v : Fock o) :=
  LinearMap.congr_fun (restriction_intertwines o labels hinj) v

theorem actual_piece_trace [Fintype ι] :
    LinearMap.trace ℂ (piece o labels) (pieceTheta o labels hinj) =
      ∑ i, (-1 : ℂ) ^ occupationLength o (labels i) := by
  classical
  rw [LinearMap.trace_eq_matrix_trace ℂ (pieceBasis o labels hinj)]
  unfold Matrix.trace
  apply Finset.sum_congr rfl
  intro i _
  change LinearMap.toMatrix (pieceBasis o labels hinj)
    (pieceBasis o labels hinj) (pieceTheta o labels hinj) i i = _
  rw [LinearMap.toMatrix_apply]
  rw [pieceTheta_basis, LinearEquiv.map_smul, Basis.repr_self]
  simp only [Finsupp.smul_apply, Finsupp.single_eq_same, smul_eq_mul, mul_one]

end HMT.IV.FockFiniteParityPiece
end

#print axioms HMT.IV.FockFiniteParityPiece.labels_independent
#print axioms HMT.IV.FockFiniteParityPiece.pieceTheta_is_actual_restriction
#print axioms HMT.IV.FockFiniteParityPiece.actual_piece_trace
