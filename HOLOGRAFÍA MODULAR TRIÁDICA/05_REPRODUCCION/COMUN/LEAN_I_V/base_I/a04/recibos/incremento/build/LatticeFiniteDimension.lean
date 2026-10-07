import LatticeFiniteCharacter

/-! The dimension and uniqueness are consequences of the inherited pairing
and the finite character theorem. In particular 4096 is not an input to the
choice of the representation. -/

noncomputable section
namespace HMT.IV.LatticeFiniteDimension
open LatticeTwistedFiniteQuotient LatticeFiniteCharacter
open CategoryTheory

theorem irreducible_dimension (o : Fin 12) (V : FDRep ℂ (FiniteExtension o))
    [Simple V] (hneg : V.ρ (1,0) = -1) : Module.finrank ℂ V = 4096 := by
  letI : Invertible (Fintype.card (FiniteExtension o) : ℂ) :=
    invertibleOfNonzero (by exact_mod_cast Fintype.card_ne_zero)
  have h := FDRep.char_orthonormal V V
  rw [if_pos ⟨Iso.refl V⟩, character_pair_sum o V V hneg hneg] at h
  have hc : (Fintype.card (FiniteExtension o) : ℂ) = 2^25 := by
    rw [finiteExtension_card_rank24]
    norm_cast
  rw [smul_eq_mul, invOf_eq_inv, hc] at h
  have hn : (Module.finrank ℂ V)^2 = 4096^2 := by
    have hx : (Module.finrank ℂ V : ℂ)^2 = (4096:ℂ)^2 := by
      linear_combination (16777216:ℂ) * h
    exact_mod_cast hx
  nlinarith

theorem irreducible_unique (o : Fin 12) (V W : FDRep ℂ (FiniteExtension o))
    [Simple V] [Simple W] (hV : V.ρ (1,0) = -1) (hW : W.ρ (1,0) = -1) :
    Nonempty (V ≅ W) := by
  classical
  letI : Invertible (Fintype.card (FiniteExtension o) : ℂ) :=
    invertibleOfNonzero (by exact_mod_cast Fintype.card_ne_zero)
  have h := FDRep.char_orthonormal V W
  rw [character_pair_sum o V W hV hW, irreducible_dimension o V hV,
    irreducible_dimension o W hW, smul_eq_mul, invOf_eq_inv,
    finiteExtension_card_rank24] at h
  by_contra hn
  rw [if_neg hn] at h
  norm_num at h

end HMT.IV.LatticeFiniteDimension
end
