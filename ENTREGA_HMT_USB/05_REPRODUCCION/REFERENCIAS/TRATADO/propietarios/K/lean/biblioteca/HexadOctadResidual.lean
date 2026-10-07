import Mathlib.Data.Finset.Card
import Mathlib.Tactic

/-!
Article I, `excepcional.tex`, proposition `exc:residuo-binario` and map
`iota_D` (lines 529--570 in the REV02 Spanish source).

This is a new formal certificate of an existing manuscript argument, not a
construction of the binary Golay code from HMT. The binary code, dodecad and
its classical weight/Steiner properties are explicit input data. No new
axioms are declared. The result does not discharge the terminal-K interface.

Binary addition is represented by symmetric difference of supports. The
residual hexads and their unique octad lifts are outputs, not input fields.
-/

namespace HMT.I.HexadOctadResidual

abbrev Support := Finset (Fin 24)

def binarySum (s t : Support) : Support := (s \ t) ∪ (t \ s)

theorem binarySum_card (s t : Support) :
    (binarySum s t).card + 2 * (s ∩ t).card = s.card + t.card := by
  have hd : Disjoint (s \ t) (t \ s) := by
    rw [Finset.disjoint_left]
    intro x hx hy
    exact (Finset.mem_sdiff.mp hx).2 (Finset.mem_sdiff.mp hy).1
  have h1 := Finset.card_sdiff_add_card_inter s t
  have h2 := Finset.card_sdiff_add_card_inter t s
  rw [Finset.inter_comm t s] at h2
  rw [binarySum, Finset.card_union_of_disjoint hd]
  omega

/-- The exact classical data used in the manuscript's residual proof.
No residual-design or hexad-lifting assertion is assumed. -/
structure BinaryGolayData where
  code : Set Support
  sum_closed : ∀ s ∈ code, ∀ t ∈ code, binarySum s t ∈ code
  allowed_weights : ∀ s ∈ code,
    s.card = 0 ∨ s.card = 8 ∨ s.card = 12 ∨ s.card = 16 ∨ s.card = 24
  dodecad : Support
  dodecad_mem : dodecad ∈ code
  dodecad_card : dodecad.card = 12
  steiner_5_8_24 : ∀ A : Support, A.card = 5 →
    ∃! O : Support, O ∈ code ∧ O.card = 8 ∧ A ⊆ O

namespace BinaryGolayData

variable (G : BinaryGolayData)

def IsOctad (O : Support) : Prop := O ∈ G.code ∧ O.card = 8

def IsResidualHexad (H : Support) : Prop :=
  H.card = 6 ∧ ∃ O : Support, G.IsOctad O ∧ O ∩ G.dodecad = H

/-- The weight argument forces an octad through five points of D to meet D
in six points. This is the manuscript's `20 - 2j` calculation without
truncated subtraction. -/
theorem octad_inter_dodecad_card (A O : Support) (hA : A.card = 5)
    (hAD : A ⊆ G.dodecad) (hO : G.IsOctad O) (hAO : A ⊆ O) :
    (O ∩ G.dodecad).card = 6 := by
  have hlo : 5 ≤ (O ∩ G.dodecad).card := by
    rw [← hA]
    exact Finset.card_le_card (Finset.subset_inter hAO hAD)
  have hhi : (O ∩ G.dodecad).card ≤ 8 := by
    rw [← hO.2]
    exact Finset.card_le_card Finset.inter_subset_left
  have hc := binarySum_card O G.dodecad
  rw [hO.2, G.dodecad_card] at hc
  have hw := G.allowed_weights _ (G.sum_closed O hO.1 G.dodecad G.dodecad_mem)
  rcases hw with hw | hw | hw | hw | hw <;> omega

theorem residual_subset_dodecad {H : Support} (hH : G.IsResidualHexad H) :
    H ⊆ G.dodecad := by
  obtain ⟨O, _, h⟩ := hH.2
  rw [← h]
  exact Finset.inter_subset_right

/-- The residual is a genuine S(5,6,12): every five-subset of D is contained
in exactly one produced residual hexad. -/
theorem residual_steiner_5_6_12 (A : Support) (hA : A.card = 5)
    (hAD : A ⊆ G.dodecad) :
    ∃! H : Support, G.IsResidualHexad H ∧ A ⊆ H := by
  obtain ⟨O, ⟨hOc, hO8, hAO⟩, hOu⟩ := G.steiner_5_8_24 A hA
  have hO : G.IsOctad O := ⟨hOc, hO8⟩
  refine ⟨O ∩ G.dodecad, ?_, ?_⟩
  · exact ⟨⟨G.octad_inter_dodecad_card A O hA hAD hO hAO, O, hO, rfl⟩,
      Finset.subset_inter hAO hAD⟩
  · intro H hH
    obtain ⟨O', hO', hres⟩ := hH.1.2
    have hAO' : A ⊆ O' := by
      have := hH.2
      rw [← hres] at this
      exact this.trans Finset.inter_subset_left
    have heq := hOu O' ⟨hO'.1, hO'.2, hAO'⟩
    simpa only [heq] using hres.symm

/-- A residual hexad has one and only one octad lying above it. -/
theorem residual_unique_lift (H : Support) (hH : G.IsResidualHexad H) :
    ∃! O : Support, G.IsOctad O ∧ O ∩ G.dodecad = H := by
  obtain ⟨O, hO, hres⟩ := hH.2
  obtain ⟨A, hAH, hA⟩ := Finset.exists_subset_card_eq (s := H)
    (n := 5) (by rw [hH.1]; omega)
  obtain ⟨O₀, hO₀, huniq⟩ := G.steiner_5_8_24 A hA
  have hAO : A ⊆ O := by
    rw [← hres] at hAH
    exact hAH.trans Finset.inter_subset_left
  have hOO₀ : O = O₀ := huniq O ⟨hO.1, hO.2, hAO⟩
  refine ⟨O, ⟨hO, hres⟩, ?_⟩
  intro O' hO'
  have hAO' : A ⊆ O' := by
    rw [← hO'.2] at hAH
    exact hAH.trans Finset.inter_subset_left
  exact (huniq O' ⟨hO'.1.1, hO'.1.2, hAO'⟩).trans hOO₀.symm

abbrev ResidualHexad := {H : Support // G.IsResidualHexad H}
abbrev Octad := {O : Support // G.IsOctad O}

noncomputable def lift (H : G.ResidualHexad) : G.Octad :=
  ⟨(G.residual_unique_lift H.val H.property).choose,
    (G.residual_unique_lift H.val H.property).choose_spec.1.1⟩

theorem lift_inter_dodecad (H : G.ResidualHexad) :
    (G.lift H).val ∩ G.dodecad = H.val :=
  (G.residual_unique_lift H.val H.property).choose_spec.1.2

theorem lift_unique (H : G.ResidualHexad) (O : G.Octad)
    (h : O.val ∩ G.dodecad = H.val) : O = G.lift H := by
  apply Subtype.ext
  exact (G.residual_unique_lift H.val H.property).choose_spec.2 O.val ⟨O.property, h⟩

theorem lift_injective : Function.Injective G.lift := by
  intro H H' h
  apply Subtype.ext
  calc
    H.val = (G.lift H).val ∩ G.dodecad := (G.lift_inter_dodecad H).symm
    _ = (G.lift H').val ∩ G.dodecad := congrArg (fun O : G.Octad => O.val ∩ G.dodecad) h
    _ = H'.val := G.lift_inter_dodecad H'

/-- Transport along the declared twelve-position chart. The chart and its
incidence compatibility remain inputs; no HMT selection is claimed for them. -/
structure IncidenceChart where
  sourceHexads : Set (Finset (Fin 12))
  positions : Fin 12 ↪ Fin 24
  image_dodecad : Finset.univ.image positions = G.dodecad
  preserves : ∀ H ∈ sourceHexads, G.IsResidualHexad (H.image positions)

noncomputable def liftAlong (L : G.IncidenceChart)
    (H : {H : Finset (Fin 12) // H ∈ L.sourceHexads}) : G.Octad :=
  G.lift ⟨H.val.image L.positions, L.preserves H.val H.property⟩

theorem liftAlong_inter_dodecad (L : G.IncidenceChart)
    (H : {H : Finset (Fin 12) // H ∈ L.sourceHexads}) :
    (G.liftAlong L H).val ∩ G.dodecad = H.val.image L.positions :=
  G.lift_inter_dodecad _

theorem liftAlong_injective (L : G.IncidenceChart) : Function.Injective (G.liftAlong L) := by
  intro H H' h
  apply Subtype.ext
  have he := congrArg (fun O : G.Octad => O.val ∩ G.dodecad) h
  dsimp only at he
  rw [G.liftAlong_inter_dodecad, G.liftAlong_inter_dodecad] at he
  exact Finset.image_injective L.positions.injective he

#print axioms _root_.HMT.I.HexadOctadResidual.binarySum_card
#print axioms octad_inter_dodecad_card
#print axioms residual_steiner_5_6_12
#print axioms residual_unique_lift
#print axioms lift_inter_dodecad
#print axioms lift_unique
#print axioms lift_injective
#print axioms liftAlong_inter_dodecad
#print axioms liftAlong_injective

end BinaryGolayData

end HMT.I.HexadOctadResidual
