import LatticeFiniteRepresentation
import Mathlib.RepresentationTheory.Character

/-! Character consequences of the actual mod-two nondegenerate pairing.
No character or representation dimension is prescribed by the construction. -/

noncomputable section
namespace HMT.IV.LatticeFiniteCharacter
open LatticeCocycle LatticeTwistedFiniteQuotient LatticeParityNondegenerate
open LatticeFiniteRepresentation

def centralElement (o : Fin 12) (s : ZMod 2) : FiniteExtension o := (s,0)

def parityLift (o : Fin 12) (v : ParityVector o) : FiniteExtension o := (0,v)

theorem exists_pairing_one (o : Fin 12) (v : ParityVector o) (hv : v ≠ 0) :
    ∃ w : ParityVector o, TC.bilinear (parityGram o) v w = 1 := by
  by_contra! h
  apply hv
  apply parityGram_nondegenerate o v
  intro w
  have hw := h w
  generalize TC.bilinear (parityGram o) v w = b at *
  fin_cases b <;> simp_all

theorem conjugate_to_central_negative (o : Fin 12) (a : FiniteExtension o)
    (ha : a.2 ≠ 0) :
    ∃ b : FiniteExtension o, b*a*b⁻¹ = centralElement o 1 * a := by
  obtain ⟨w,hw⟩ := exists_pairing_one o a.2 ha
  refine ⟨parityLift o w, ?_⟩
  apply @mul_right_cancel (FiniteExtension o) _ _ _ (parityLift o w)
  simp only [mul_assoc, inv_mul_cancel, mul_one]
  have ht := TC.tau_commutator (parityGram o) (parityGram_symmetric o)
    (parityGram_diagonal_zero o) a.2 w
  rw [hw] at ht
  apply Prod.ext
  · change 0+a.1+TC.tau (parityGram o) w a.2 =
      1+(a.1+0+TC.tau (parityGram o) a.2 w)+
        TC.tau (parityGram o) 0 (a.2+w)
    simp only [TC.tau_zero_left, zero_add, add_zero]
    have hd : TC.tau (parityGram o) a.2 w + TC.tau (parityGram o) a.2 w = 0 := by
      simpa only [ZMod.neg_eq_self_mod_two] using
        add_neg_cancel (TC.tau (parityGram o) a.2 w)
    linear_combination ht - hd
  · change w+a.2=0+(a.2+w)
    simp only [zero_add, add_zero, add_comm]

theorem character_off_center (o : Fin 12) (V : FDRep ℂ (FiniteExtension o))
    (hneg : V.ρ (1,0) = -1) (a : FiniteExtension o) (ha : a.2 ≠ 0) :
    V.character a = 0 := by
  obtain ⟨b,hb⟩ := conjugate_to_central_negative o a ha
  have hchar := FDRep.char_conj V a b
  rw [hb] at hchar
  have hm : V.character (centralElement o 1 * a) = -V.character a := by
    simp only [FDRep.character, map_mul, centralElement, hneg, neg_mul, one_mul, map_neg]
  rw [hm] at hchar
  linear_combination - (1/2:ℂ) * hchar

theorem character_center (o : Fin 12) (V : FDRep ℂ (FiniteExtension o))
    (hneg : V.ρ (1,0) = -1) (s : ZMod 2) :
    V.character (s,0) = complexSign s * Module.finrank ℂ V := by
  fin_cases s
  · change V.character 1 = complexSign 0 * Module.finrank ℂ V
    simp only [FDRep.char_one, complexSign_zero, one_mul]
  · change V.character (1,0) = complexSign 1 * Module.finrank ℂ V
    simp only [FDRep.character, hneg, map_neg, LinearMap.trace_one,
      complexSign_one, neg_mul, one_mul]

theorem character_formula (o : Fin 12) (V : FDRep ℂ (FiniteExtension o))
    (hneg : V.ρ (1,0) = -1) (a : FiniteExtension o) :
    V.character a = if a.2=0 then complexSign a.1 * Module.finrank ℂ V else 0 := by
  classical
  by_cases ha : a.2=0
  · rw [if_pos ha]
    have heq : a=(a.1,0) := Prod.ext rfl ha
    rw [heq]
    exact character_center o V hneg a.1
  · rw [if_neg ha]
    exact character_off_center o V hneg a ha

theorem central_inverse (o : Fin 12) (s : ZMod 2) :
    (centralElement o s)⁻¹ = centralElement o s := by
  change (-s-TC.tau (parityGram o) 0 (-0), -0) = (s,0)
  simp [TC.tau_zero_left, ZMod.neg_eq_self_mod_two]

theorem character_pair_sum (o : Fin 12) (V W : FDRep ℂ (FiniteExtension o))
    (hV : V.ρ (1,0) = -1) (hW : W.ρ (1,0) = -1) :
    (∑ a : FiniteExtension o, V.character a * W.character a⁻¹) =
      2 * (Module.finrank ℂ V : ℂ) * Module.finrank ℂ W := by
  classical
  let f : FiniteExtension o → ℂ := fun a => V.character a * W.character a⁻¹
  change (∑ a : ZMod 2 × ParityVector o, f a) = _
  rw [Fintype.sum_prod_type]
  have hs (s : ZMod 2) :
      (∑ v : ParityVector o, f (s,v)) =
      (Module.finrank ℂ V : ℂ) * Module.finrank ℂ W := by
    rw [Finset.sum_eq_single (0 : ParityVector o)]
    · change V.character (centralElement o s) * W.character (centralElement o s)⁻¹ = _
      rw [central_inverse]
      change V.character (s,0) * W.character (s,0) = _
      rw [character_center o V hV, character_center o W hW]
      calc
        _ = (complexSign s * complexSign s) *
            ((Module.finrank ℂ V : ℂ) * Module.finrank ℂ W) := by ring
        _ = _ := by rw [complexSign_sq, one_mul]
    · intro v _ hv
      dsimp only [f]
      rw [character_off_center o V hV (s,v) hv, zero_mul]
    · simp
  simp only [hs, Finset.sum_const, Finset.card_univ, ZMod.card]
  simp only [nsmul_eq_mul, Nat.cast_ofNat]
  ring

end HMT.IV.LatticeFiniteCharacter
end
