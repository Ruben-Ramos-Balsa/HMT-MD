import LatticeHalfWeightBasis

/-! The actual conformal zero mode on the tensor carrier has no eigenvectors
of weights zero or one. The proof uses its existing monomial tensor basis,
not a declared truncation of the space. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedLowWeights
open TensorProduct
open LatticeOscillatorFock LatticeFockMonomialParity LatticeFiniteIrreducible
open LatticeTwistedOscillatorTensor LatticeTwistedCarrier LatticeHalfWeightBasis

def finiteBasis (o : Fin 12) := Module.finBasis ℂ (FiniteSpace o)

abbrev BasisIndex (o : Fin 12) := Occupation o × Fin (Module.finrank ℂ (FiniteSpace o))

def twistedBasis (o : Fin 12) : Basis (BasisIndex o) ℂ (Carrier o) :=
  (monomialBasis o).tensorProduct (finiteBasis o)

theorem conformal_basis_weight (o : Fin 12) (p : BasisIndex o) :
    conformalMode o 0 (twistedBasis o p) =
      (((twiceWeight o p.1 : ℂ)+3)/2) • twistedBasis o p := by
  simp only [twistedBasis, Basis.tensorProduct_apply']
  change conformalModeTensor (FiniteSpace o) o 0
    ((monomialBasis o p.1) ⊗ₜ[ℂ] (finiteBasis o p.2)) = _
  rw [conformalModeTensor_tmul, shifted_zero_monomial, TensorProduct.smul_tmul']

theorem conformal_coefficient (o : Fin 12) (v : Carrier o) (p : BasisIndex o) :
    (twistedBasis o).repr (conformalMode o 0 v) p =
      (((twiceWeight o p.1 : ℂ)+3)/2) * (twistedBasis o).repr v p := by
  classical
  have h : ((twistedBasis o).coord p).comp (conformalMode o 0) =
      (((twiceWeight o p.1 : ℂ)+3)/2) • (twistedBasis o).coord p := by
    apply (twistedBasis o).ext
    intro q
    simp only [LinearMap.comp_apply, conformal_basis_weight, map_smul,
      LinearMap.smul_apply, Basis.coord_apply, Basis.repr_self,
      Finsupp.single_apply, smul_eq_mul]
    split_ifs with hq
    · subst q
      rfl
    · simp
  exact LinearMap.congr_fun h v

theorem low_weight_vector_zero (o : Fin 12) (v : Carrier o) (e : ℕ) (he : e ≤ 1)
    (hv : conformalMode o 0 v = (e:ℂ) • v) : v=0 := by
  classical
  apply (twistedBasis o).repr.injective
  apply Finsupp.ext
  intro p
  change (twistedBasis o).repr v p = 0
  by_contra hp
  have h := congrArg (fun w : Carrier o => (twistedBasis o).repr w p) hv
  dsimp only at h
  rw [conformal_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hw : ((twiceWeight o p.1 : ℂ)+3)/2 = (e:ℂ) := mul_right_cancel₀ hp h
  have hn : twiceWeight o p.1 + 3 = 2*e := by
    have hc : (twiceWeight o p.1 : ℂ)+3 = 2*(e:ℂ) := by linear_combination 2*hw
    exact_mod_cast hc
  omega

theorem weight_zero_vanishes (o : Fin 12) :
    Module.End.eigenspace (conformalMode o 0) (0:ℂ) = ⊥ := by
  apply le_antisymm _ bot_le
  intro v hv
  apply (Submodule.mem_bot ℂ).mpr
  apply low_weight_vector_zero o v 0 (by omega)
  simpa using Module.End.mem_eigenspace_iff.mp hv

theorem weight_one_vanishes (o : Fin 12) :
    Module.End.eigenspace (conformalMode o 0) (1:ℂ) = ⊥ := by
  apply le_antisymm _ bot_le
  intro v hv
  apply (Submodule.mem_bot ℂ).mpr
  apply low_weight_vector_zero o v 1 (by omega)
  simpa using Module.End.mem_eigenspace_iff.mp hv

end HMT.IV.LatticeTwistedLowWeights
end
