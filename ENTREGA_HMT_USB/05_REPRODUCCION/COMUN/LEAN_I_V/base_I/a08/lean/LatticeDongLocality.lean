import LatticeDongIntegrand
import LatticeResidueConvolution

/-!
Dong locality for the genuine fields and their actual residue products.
The three pairwise localities are composed through proved ordered
convolutions, annihilators and residue extraction. The normal product is
the one already used to define stateField, not a new axiomatic operation.
-/

noncomputable section
namespace HMT.IV.LatticeDongLocality

open HMT.IV.LatticeFieldLocality HMT.IV.LatticeFactorConvolution
open HMT.IV.LatticeOrderedConvolution HMT.IV.LatticeDongBinomial
open HMT.IV.LatticeResidueProducts HMT.IV.LatticeDongIntegrand
open HMT.IV.LatticeResidueConvolution

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- The sufficient locality order is p+q+s+n for the residue of index
-n-1. No locality assumption is made about the resulting field. -/
theorem residueField_localAt {A B C : VertexOperator ℂ V} {p q s : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) (hAB : LocalAt s A B) (n : ℕ) :
    LocalAt (p+q+s+n) (residueField (-(n : ℤ)-1) A B) C := by
  let D := residueField (-(n : ℤ)-1) A B
  change (crossing^(p+q+s+n)) (forward D C) =
    (crossing^(p+q+s+n)) (backward D C)
  apply sub_eq_zero.mp
  rw [← map_sub]
  funext k l
  apply LinearMap.ext
  intro v
  have hi : residue (integrand (-(n : ℤ)-1) A B C v) =
      (fun a b => (forward D C a b - backward D C a b) v) := by
    funext a b
    exact residue_convolution_commutator (-(n : ℤ)-1) A B C v a b
  have he := congrFun (congrFun
    (crossing_pow_evaluate (forward D C-backward D C) (p+q+s+n) v) k) l
  change ((crossing^(p+q+s+n)) (forward D C-backward D C) k l) v = 0
  rw [he]
  change (crossing^(p+q+s+n)) (fun a b => (forward D C a b-backward D C a b) v) k l = 0
  rw [← hi, integrand_residue_locality hAC hBC hAB n v]
  rfl

theorem residueField_local {A B C : VertexOperator ℂ V}
    (hAC : Local A C) (hBC : Local B C) (hAB : Local A B) (n : ℕ) :
    Local (residueField (-(n : ℤ)-1) A B) C := by
  obtain ⟨p,hp⟩ := hAC
  obtain ⟨q,hq⟩ := hBC
  obtain ⟨s,hs⟩ := hAB
  exact ⟨p+q+s+n,residueField_localAt hp hq hs n⟩

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergField HMT.IV.LatticeNormalOrderedField

theorem normalField_localAt (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (LatticeCarrier o)) {p q s : ℕ}
    (hHC : LocalAt p (heisenbergField o i) C) (hBC : LocalAt q B C)
    (hHB : LocalAt s (heisenbergField o i) B) :
    LocalAt (p+q+s+n) (normalField o i n B) C := by
  rw [← heisenberg_residueField]
  exact residueField_localAt hHC hBC hHB n

theorem normalField_local (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (LatticeCarrier o))
    (hHC : Local (heisenbergField o i) C) (hBC : Local B C)
    (hHB : Local (heisenbergField o i) B) : Local (normalField o i n B) C := by
  rw [← heisenberg_residueField]
  exact residueField_local hHC hBC hHB n

end HMT.IV.LatticeDongLocality
end

#print axioms HMT.IV.LatticeDongLocality.residueField_localAt
#print axioms HMT.IV.LatticeDongLocality.residueField_local
#print axioms HMT.IV.LatticeDongLocality.normalField_localAt
#print axioms HMT.IV.LatticeDongLocality.normalField_local
