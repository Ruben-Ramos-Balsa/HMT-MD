import LatticeContragredientWeightSupport
import LatticeEvenRestrictedDual

/-! The twisted--twisted product on the actual even lattice carrier.
Representability and Laurent truncation follow from the proven weight support;
neither property is supplied as an axiom or a product-valued input. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedPairProduct
open LatticeEvenVertexFields LatticeEvenGrading LatticeEvenPairingRepresentability
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading
open LatticeTwistedContragredientCoefficients LatticeContragredientWeightSupport
open LatticeEvenRestrictedDual LatticeTwistedEvenProduct

theorem contragredientCoefficient_bounded (o : Fin 12) (k : ℤ)
    (v w : positiveSector o) : contragredientCoefficient o k v w ∈ boundedDual o := by
  have hv : v ∈ ⨆ d : ℕ, positiveWeightSpace o d := by
    rw [positive_weights_span o]
    trivial
  have hall : ∀ w, contragredientCoefficient o k v w ∈ boundedDual o := by
    refine Submodule.iSup_induction (positiveWeightSpace o)
      (motive := fun v => ∀ w, contragredientCoefficient o k v w ∈ boundedDual o)
      hv ?_ ?_ ?_
    · intro d v hd w
      have hw : w ∈ ⨆ e : ℕ, positiveWeightSpace o e := by
        rw [positive_weights_span o]
        trivial
      refine Submodule.iSup_induction (positiveWeightSpace o)
        (motive := fun w => contragredientCoefficient o k v w ∈ boundedDual o)
        hw ?_ ?_ ?_
      · intro e w he
        refine ⟨d+e+k.toNat+1, ?_⟩
        intro r hr a ha
        apply contragredientCoefficient_off_weight o d e r k v w hd he a ha
        have hk : k ≤ (k.toNat:ℤ) := by omega
        omega
      · simp only [map_zero]
        exact (boundedDual o).zero_mem
      · intro x y hx hy
        rw [map_add]
        exact (boundedDual o).add_mem hx hy
    · intro w
      simp only [map_zero, LinearMap.zero_apply]
      exact (boundedDual o).zero_mem
    · intro x y hx hy w
      simp only [map_add, LinearMap.add_apply]
      exact (boundedDual o).add_mem (hx w) (hy w)
  exact hall w

def boundedCoefficient (o : Fin 12) (k : ℤ) :
    positiveSector o →ₗ[ℂ] positiveSector o →ₗ[ℂ] boundedDual o where
  toFun v :=
    { toFun w := ⟨contragredientCoefficient o k v w,
        contragredientCoefficient_bounded o k v w⟩
      map_add' w u := by apply Subtype.ext; exact map_add _ w u
      map_smul' c w := by apply Subtype.ext; exact map_smul _ c w }
  map_add' v u := by
    apply LinearMap.ext
    intro w
    apply Subtype.ext
    exact LinearMap.congr_fun (map_add (contragredientCoefficient o k) v u) w
  map_smul' c v := by
    apply LinearMap.ext
    intro w
    apply Subtype.ext
    exact LinearMap.congr_fun (map_smul (contragredientCoefficient o k) c v) w

def pairCoefficient (o : Fin 12) (k : ℤ) :
    positiveSector o →ₗ[ℂ] positiveSector o →ₗ[ℂ] evenSpace o where
  toFun v := (reconstruction o).comp (boundedCoefficient o k v)
  map_add' v w := by
    ext u
    simp only [LinearMap.comp_apply, map_add, LinearMap.add_apply]
  map_smul' c v := by
    ext u
    simp only [LinearMap.comp_apply, map_smul, LinearMap.smul_apply, RingHom.id_apply]

theorem pairCoefficient_pair (o : Fin 12) (k : ℤ)
    (v w : positiveSector o) (a : evenSpace o) :
    evenPairing o (pairCoefficient o k v w) a = contragredientCoefficient o k v w a :=
  reconstruct_pair o (boundedCoefficient o k v w) a

theorem pairCoefficient_unique (o : Fin 12) (k : ℤ) (v w : positiveSector o)
    (u : evenSpace o) (hu : ∀ a, evenPairing o u a = contragredientCoefficient o k v w a) :
    u = pairCoefficient o k v w :=
  representative_unique o (contragredientCoefficient o k v w) u _ hu
    (pairCoefficient_pair o k v w)

theorem contragredientCoefficient_homogeneous_lower (o : Fin 12) (d e : ℕ)
    (v w : positiveSector o) (hv : v ∈ positiveWeightSpace o d)
    (hw : w ∈ positiveWeightSpace o e) (k : ℤ) (hk : k < -(d:ℤ)-(e:ℤ)) :
    contragredientCoefficient o k v w = 0 := by
  ext a
  have ha : a ∈ ⨆ r : ℕ, evenWeightSpace o r := by
    rw [even_weights_span o]
    trivial
  change contragredientCoefficient o k v w a = 0
  refine Submodule.iSup_induction (evenWeightSpace o)
    (motive := fun a => contragredientCoefficient o k v w a = 0) ha ?_ ?_ ?_
  · intro r a hr
    exact contragredientCoefficient_off_weight o d e r k v w hv hw a hr (by omega)
  · exact map_zero _
  · intro a b ha hb
    rw [map_add, ha, hb, add_zero]

theorem contragredientCoefficient_lower (o : Fin 12) (v w : positiveSector o) :
    ∃ b : ℤ, ∀ k < b, contragredientCoefficient o k v w = 0 := by
  have hv : v ∈ ⨆ d : ℕ, positiveWeightSpace o d := by
    rw [positive_weights_span o]
    trivial
  have hall : ∀ w, ∃ b : ℤ, ∀ k < b, contragredientCoefficient o k v w = 0 := by
    refine Submodule.iSup_induction (positiveWeightSpace o)
      (motive := fun v => ∀ w, ∃ b : ℤ, ∀ k < b, contragredientCoefficient o k v w = 0)
      hv ?_ ?_ ?_
    · intro d v hd w
      have hw : w ∈ ⨆ e : ℕ, positiveWeightSpace o e := by
        rw [positive_weights_span o]
        trivial
      refine Submodule.iSup_induction (positiveWeightSpace o)
        (motive := fun w => ∃ b : ℤ, ∀ k < b, contragredientCoefficient o k v w = 0)
        hw ?_ ?_ ?_
      · intro e w he
        exact ⟨-(d:ℤ)-(e:ℤ), contragredientCoefficient_homogeneous_lower o d e v w hd he⟩
      · exact ⟨0, fun k _ => map_zero _⟩
      · rintro x y ⟨b,hb⟩ ⟨c,hc⟩
        refine ⟨min b c, ?_⟩
        intro k hk
        rw [map_add, hb k (lt_of_lt_of_le hk (min_le_left b c)),
          hc k (lt_of_lt_of_le hk (min_le_right b c)), add_zero]
    · intro w
      exact ⟨0, fun k _ => by simp only [map_zero, LinearMap.zero_apply]⟩
    · intro x y hx hy w
      obtain ⟨b,hb⟩ := hx w
      obtain ⟨c,hc⟩ := hy w
      refine ⟨min b c, ?_⟩
      intro k hk
      simp only [map_add, LinearMap.add_apply,
        hb k (lt_of_lt_of_le hk (min_le_left b c)),
        hc k (lt_of_lt_of_le hk (min_le_right b c)), add_zero]
  exact hall w

theorem pairCoefficient_lower (o : Fin 12) (v w : positiveSector o) :
    ∃ b : ℤ, ∀ k < b, pairCoefficient o k v w = 0 := by
  obtain ⟨b,hb⟩ := contragredientCoefficient_lower o v w
  refine ⟨b, ?_⟩
  intro k hk
  have hz : boundedCoefficient o k v w = 0 := Subtype.ext (hb k hk)
  change reconstruction o (boundedCoefficient o k v w) = 0
  rw [hz, map_zero]

def twistedPairFieldAt (o : Fin 12) (v : positiveSector o) :
    HVertexOperator ℤ ℂ (positiveSector o) (evenSpace o) :=
  HVertexOperator.of_coeff (fun k => pairCoefficient o k v)
    (fun w => HahnSeries.suppBddBelow_supp_PWO (fun k => pairCoefficient o k v w)
      (HahnSeries.forallLTEqZero_supp_BddBelow (fun k => pairCoefficient o k v w)
        (Exists.choose (pairCoefficient_lower o v w))
        (Exists.choose_spec (pairCoefficient_lower o v w))))

def twistedPairField (o : Fin 12) : TwistedPairField o where
  toFun := twistedPairFieldAt o
  map_add' v w := by
    apply HVertexOperator.coeff_inj
    funext k
    rw [HVertexOperator.coeff_add]
    change pairCoefficient o k (v+w) = pairCoefficient o k v + pairCoefficient o k w
    exact map_add _ _ _
  map_smul' c v := by
    apply HVertexOperator.coeff_inj
    funext k
    rw [HVertexOperator.coeff_smul]
    change pairCoefficient o k (c • v) = c • pairCoefficient o k v
    exact map_smul _ _ _

theorem twistedPairField_coefficient (o : Fin 12) (v w : positiveSector o) (k : ℤ) :
    HVertexOperator.coeff (twistedPairField o v) k w = pairCoefficient o k v w := rfl

theorem twistedPairField_pair (o : Fin 12) (v w : positiveSector o)
    (k : ℤ) (a : evenSpace o) :
    evenPairing o (HVertexOperator.coeff (twistedPairField o v) k w) a =
      contragredientCoefficient o k v w a := pairCoefficient_pair o k v w a

end HMT.IV.LatticeTwistedPairProduct
end

#print axioms HMT.IV.LatticeTwistedPairProduct.contragredientCoefficient_bounded
#print axioms HMT.IV.LatticeTwistedPairProduct.pairCoefficient_lower
#print axioms HMT.IV.LatticeTwistedPairProduct.twistedPairField
