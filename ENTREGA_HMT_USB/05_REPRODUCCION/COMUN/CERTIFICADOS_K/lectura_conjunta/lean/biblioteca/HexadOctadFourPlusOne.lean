import HexadOctadResidual

/-!
Article I, excepcional.tex, residual construction and the four-plus-one
incidence through a tetrad. The counts are derived from the two Steiner
properties; neither four nor five is an extra hypothesis.
The binary Golay data and dodecad are those of HexadOctadResidual.
-/

namespace HMT.I.HexadOctadFourPlusOne

open HMT.I.HexadOctadResidual
open HMT.I.HexadOctadResidual.BinaryGolayData
open scoped BigOperators

private theorem pencil_count {α : Type*} [DecidableEq α]
    (S T : Finset α) (F : Finset (Finset α)) (k : ℕ)
    (hTS : T ⊆ S)
    (hB : ∀ B ∈ F, T ⊆ B ∧ B ⊆ S ∧ B.card = k)
    (hcover : ∀ x ∈ S \ T, ∃! B : Finset α, B ∈ F ∧ x ∈ B) :
    F.card * (k - T.card) = S.card - T.card := by
  classical
  have hd : F.toSet.PairwiseDisjoint (fun B => B \ T) := by
    intro B hBF C hCF hBC
    apply Finset.disjoint_left.mpr
    intro x hx hy
    have hxm := Finset.mem_sdiff.mp hx
    have hym := Finset.mem_sdiff.mp hy
    have hxST : x ∈ S \ T :=
      Finset.mem_sdiff.mpr ⟨(hB B hBF).2.1 hxm.1, hxm.2⟩
    obtain ⟨D, _, hu⟩ := hcover x hxST
    exact hBC ((hu B ⟨hBF, hxm.1⟩).trans (hu C ⟨hCF, hym.1⟩).symm)
  have hUnion : F.biUnion (fun B => B \ T) = S \ T := by
    ext x
    constructor
    · intro hx
      obtain ⟨B, hBF, hxB⟩ := Finset.mem_biUnion.mp hx
      have hxm := Finset.mem_sdiff.mp hxB
      exact Finset.mem_sdiff.mpr ⟨(hB B hBF).2.1 hxm.1, hxm.2⟩
    · intro hx
      obtain ⟨B, ⟨hBF, hxB⟩, _⟩ := hcover x hx
      exact Finset.mem_biUnion.mpr ⟨B, hBF,
        Finset.mem_sdiff.mpr ⟨hxB, (Finset.mem_sdiff.mp hx).2⟩⟩
  have hc := Finset.card_biUnion hd
  rw [hUnion, Finset.card_sdiff hTS] at hc
  have hs : (∑ B ∈ F, (B \ T).card) = F.card * (k - T.card) := by
    apply Finset.sum_const_nat
    intro B hBF
    rw [Finset.card_sdiff (hB B hBF).1, (hB B hBF).2.2]
  exact hs.symm.trans hc.symm

variable (G : BinaryGolayData)

noncomputable def octadStar (T : Support) : Finset Support := by
  classical
  exact Finset.univ.filter (fun O => G.IsOctad O ∧ T ⊆ O)

noncomputable def hexadStar (T : Support) : Finset Support := by
  classical
  exact Finset.univ.filter (fun H => G.IsResidualHexad H ∧ T ⊆ H)

theorem mem_octadStar (T O : Support) :
    O ∈ octadStar G T ↔ G.IsOctad O ∧ T ⊆ O := by
  classical
  simp [octadStar]

theorem mem_hexadStar (T H : Support) :
    H ∈ hexadStar G T ↔ G.IsResidualHexad H ∧ T ⊆ H := by
  classical
  simp [hexadStar]

theorem octad_star_card (T : Support) (hT : T.card = 4) :
    (octadStar G T).card = 5 := by
  classical
  have hc := pencil_count (Finset.univ : Support) T (octadStar G T) 8
    (Finset.subset_univ T) (by
      intro O hO
      obtain ⟨hOct, hTO⟩ := (mem_octadStar G T O).mp hO
      exact ⟨hTO, Finset.subset_univ O, hOct.2⟩) (by
      intro x hx
      have hxT := (Finset.mem_sdiff.mp hx).2
      have hA : (insert x T).card = 5 := by
        rw [Finset.card_insert_of_notMem hxT, hT]
      obtain ⟨O, ⟨hOc, hO8, hAO⟩, hu⟩ := G.steiner_5_8_24 (insert x T) hA
      have hTO : x ∈ O ∧ T ⊆ O :=
        ⟨hAO (Finset.mem_insert_self x T), fun y hy => hAO (Finset.mem_insert_of_mem hy)⟩
      refine ⟨O, ⟨(mem_octadStar G T O).mpr ⟨⟨hOc, hO8⟩, hTO.2⟩, hTO.1⟩, ?_⟩
      intro B hB
      obtain ⟨hBo, hTB⟩ := (mem_octadStar G T B).mp hB.1
      exact hu B ⟨hBo.1, hBo.2, Finset.insert_subset hB.2 hTB⟩)
  simp only [Finset.card_univ, Fintype.card_fin, hT] at hc
  omega

theorem hexad_star_card (T : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) : (hexadStar G T).card = 4 := by
  classical
  have hc := pencil_count G.dodecad T (hexadStar G T) 6 hTD (by
      intro H hH
      obtain ⟨hHex, hTH⟩ := (mem_hexadStar G T H).mp hH
      exact ⟨hTH, G.residual_subset_dodecad hHex, hHex.1⟩) (by
      intro x hx
      have hxD := (Finset.mem_sdiff.mp hx).1
      have hxT := (Finset.mem_sdiff.mp hx).2
      have hA : (insert x T).card = 5 := by
        rw [Finset.card_insert_of_notMem hxT, hT]
      obtain ⟨H, ⟨hHex, hAH⟩, hu⟩ :=
        G.residual_steiner_5_6_12 (insert x T) hA (Finset.insert_subset hxD hTD)
      have hTH : x ∈ H ∧ T ⊆ H :=
        ⟨hAH (Finset.mem_insert_self x T), fun y hy => hAH (Finset.mem_insert_of_mem hy)⟩
      refine ⟨H, ⟨(mem_hexadStar G T H).mpr ⟨hHex, hTH.2⟩, hTH.1⟩, ?_⟩
      intro B hB
      obtain ⟨hBh, hTB⟩ := (mem_hexadStar G T B).mp hB.1
      exact hu B ⟨hBh, Finset.insert_subset hB.2 hTB⟩)
  rw [G.dodecad_card, hT] at hc
  omega

noncomputable def liftSupport (H : Support) : Support := by
  classical
  exact if h : G.IsResidualHexad H then (G.lift ⟨H, h⟩).val else ∅

theorem liftSupport_octad (H : Support) (hH : G.IsResidualHexad H) :
    G.IsOctad (liftSupport G H) := by
  classical
  simpa only [liftSupport, dif_pos hH] using (G.lift ⟨H, hH⟩).property

theorem liftSupport_inter (H : Support) (hH : G.IsResidualHexad H) :
    liftSupport G H ∩ G.dodecad = H := by
  classical
  simpa only [liftSupport, dif_pos hH] using G.lift_inter_dodecad ⟨H, hH⟩

theorem liftSupport_eq (H O : Support) (hH : G.IsResidualHexad H)
    (hO : G.IsOctad O) (hOH : O ∩ G.dodecad = H) : liftSupport G H = O := by
  classical
  have he := G.lift_unique ⟨H, hH⟩ ⟨O, hO⟩ hOH
  have he' := congrArg Subtype.val he
  simpa only [liftSupport, dif_pos hH] using he'.symm

noncomputable def liftedStar (T : Support) : Finset Support := by
  classical
  exact (hexadStar G T).image (liftSupport G)

theorem lifted_star_card (T : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) : (liftedStar G T).card = 4 := by
  classical
  rw [liftedStar, Finset.card_image_of_injOn]
  · exact hexad_star_card G T hT hTD
  · intro H hH H' hH' he
    have hr := congrArg (fun O => O ∩ G.dodecad) he
    dsimp only at hr
    rw [liftSupport_inter G H ((mem_hexadStar G T H).mp hH).1,
      liftSupport_inter G H' ((mem_hexadStar G T H').mp hH').1] at hr
    exact hr

theorem lifted_star_subset (T : Support) : liftedStar G T ⊆ octadStar G T := by
  classical
  intro O hO
  obtain ⟨H, hH, rfl⟩ := Finset.mem_image.mp hO
  obtain ⟨hHex, hTH⟩ := (mem_hexadStar G T H).mp hH
  apply (mem_octadStar G T _).mpr
  refine ⟨liftSupport_octad G H hHex, ?_⟩
  have hHO : H ⊆ liftSupport G H := by
    intro x hx
    have hxI : x ∈ liftSupport G H ∩ G.dodecad := by
      rw [liftSupport_inter G H hHex]
      exact hx
    exact (Finset.mem_inter.mp hxI).1
  exact hTH.trans hHO

theorem lifted_star_inter_card (T O : Support) (hO : O ∈ liftedStar G T) :
    (O ∩ G.dodecad).card = 6 := by
  classical
  obtain ⟨H, hH, rfl⟩ := Finset.mem_image.mp hO
  have hHex := ((mem_hexadStar G T H).mp hH).1
  rw [liftSupport_inter G H hHex]
  exact hHex.1

theorem transverse_card (T : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) :
    (octadStar G T \ liftedStar G T).card = 1 := by
  rw [Finset.card_sdiff (lifted_star_subset G T),
    octad_star_card G T hT, lifted_star_card G T hT hTD]

theorem transverse_inter (T O : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) (hO : O ∈ octadStar G T \ liftedStar G T) :
    O ∩ G.dodecad = T := by
  classical
  obtain ⟨hOS, hOL⟩ := Finset.mem_sdiff.mp hO
  obtain ⟨hOct, hTO⟩ := (mem_octadStar G T O).mp hOS
  have hTI : T ⊆ O ∩ G.dodecad := Finset.subset_inter hTO hTD
  have hlo : 4 ≤ (O ∩ G.dodecad).card := by
    rw [← hT]
    exact Finset.card_le_card hTI
  have hhi : (O ∩ G.dodecad).card ≤ 8 := by
    rw [← hOct.2]
    exact Finset.card_le_card Finset.inter_subset_left
  have hc := binarySum_card O G.dodecad
  rw [hOct.2, G.dodecad_card] at hc
  have hw := G.allowed_weights _ (G.sum_closed O hOct.1 G.dodecad G.dodecad_mem)
  have hcases : (O ∩ G.dodecad).card = 4 ∨ (O ∩ G.dodecad).card = 6 := by
    rcases hw with hw | hw | hw | hw | hw <;> omega
  rcases hcases with h4 | h6
  · exact (Finset.eq_of_subset_of_card_le hTI (by omega)).symm
  · have hHex : G.IsResidualHexad (O ∩ G.dodecad) := ⟨h6, O, hOct, rfl⟩
    have hHS : O ∩ G.dodecad ∈ hexadStar G T :=
      (mem_hexadStar G T _).mpr ⟨hHex, hTI⟩
    exact False.elim (hOL (Finset.mem_image.mpr
      ⟨O ∩ G.dodecad, hHS, liftSupport_eq G _ O hHex hOct rfl⟩))

theorem transverse_iff (T O : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) :
    O ∈ octadStar G T \ liftedStar G T ↔ G.IsOctad O ∧ O ∩ G.dodecad = T := by
  classical
  constructor
  · intro hO
    exact ⟨((mem_octadStar G T O).mp (Finset.mem_sdiff.mp hO).1).1,
      transverse_inter G T O hT hTD hO⟩
  · rintro ⟨hO, hOT⟩
    apply Finset.mem_sdiff.mpr
    constructor
    · apply (mem_octadStar G T O).mpr
      exact ⟨hO, by rw [← hOT]; exact Finset.inter_subset_left⟩
    · intro hL
      have h6 := lifted_star_inter_card G T O hL
      rw [hOT, hT] at h6
      omega

/-- The fifth octad is unique and meets the dodecad in exactly the tetrad. -/
theorem unique_transverse_octad (T : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) :
    ∃! O : Support, G.IsOctad O ∧ O ∩ G.dodecad = T := by
  classical
  obtain ⟨O, hSingle⟩ := Finset.card_eq_one.mp (transverse_card G T hT hTD)
  have hO : O ∈ octadStar G T \ liftedStar G T := by rw [hSingle]; simp
  refine ⟨O, (transverse_iff G T O hT hTD).mp hO, ?_⟩
  intro O' hO'
  have hm := (transverse_iff G T O' hT hTD).mpr hO'
  rw [hSingle] at hm
  exact Finset.mem_singleton.mp hm

/-- The exact disjoint four-plus-one decomposition, not a cardinal analogy. -/
theorem four_plus_one (T : Support) (hT : T.card = 4)
    (hTD : T ⊆ G.dodecad) :
    (hexadStar G T).card = 4 ∧ (liftedStar G T).card = 4 ∧
    (octadStar G T).card = 5 ∧
    ∃ O : Support, G.IsOctad O ∧ O ∩ G.dodecad = T ∧
      O ∉ liftedStar G T ∧ octadStar G T = insert O (liftedStar G T) := by
  classical
  refine ⟨hexad_star_card G T hT hTD, lifted_star_card G T hT hTD,
    octad_star_card G T hT, ?_⟩
  obtain ⟨O, hSingle⟩ := Finset.card_eq_one.mp (transverse_card G T hT hTD)
  have hO : O ∈ octadStar G T \ liftedStar G T := by rw [hSingle]; simp
  have hOT := (transverse_iff G T O hT hTD).mp hO
  refine ⟨O, hOT.1, hOT.2, (Finset.mem_sdiff.mp hO).2, ?_⟩
  ext B
  constructor
  · intro hB
    by_cases hBL : B ∈ liftedStar G T
    · exact Finset.mem_insert_of_mem hBL
    · have hm : B ∈ octadStar G T \ liftedStar G T := Finset.mem_sdiff.mpr ⟨hB, hBL⟩
      rw [hSingle] at hm
      rw [Finset.mem_singleton.mp hm]
      exact Finset.mem_insert_self _ _
  · intro hB
    rcases Finset.mem_insert.mp hB with hB | hB
    · rw [hB]
      exact (Finset.mem_sdiff.mp hO).1
    · exact lifted_star_subset G T hB

/-- Composition with the same marked twelve-position chart used by the
hexad lift. No ordering of the three positive petals is asserted. -/
theorem four_plus_one_along_chart (L : G.IncidenceChart)
    (B : Finset (Fin 12)) (hB : B.card = 4) :
    let T := B.image L.positions
    (hexadStar G T).card = 4 ∧ (liftedStar G T).card = 4 ∧
    (octadStar G T).card = 5 ∧
    ∃ O : Support, G.IsOctad O ∧ O ∩ G.dodecad = T ∧
      O ∉ liftedStar G T ∧ octadStar G T = insert O (liftedStar G T) := by
  classical
  have hT : (B.image L.positions).card = 4 := by
    rw [Finset.card_image_of_injective B L.positions.injective, hB]
  have hTD : B.image L.positions ⊆ G.dodecad := by
    rw [← L.image_dodecad]
    exact Finset.image_subset_image (Finset.subset_univ B)
  exact four_plus_one G (B.image L.positions) hT hTD

#print axioms HMT.I.HexadOctadFourPlusOne.octad_star_card
#print axioms HMT.I.HexadOctadFourPlusOne.hexad_star_card
#print axioms HMT.I.HexadOctadFourPlusOne.lifted_star_card
#print axioms HMT.I.HexadOctadFourPlusOne.lifted_star_subset
#print axioms HMT.I.HexadOctadFourPlusOne.transverse_card
#print axioms HMT.I.HexadOctadFourPlusOne.transverse_inter
#print axioms HMT.I.HexadOctadFourPlusOne.transverse_iff
#print axioms HMT.I.HexadOctadFourPlusOne.unique_transverse_octad
#print axioms HMT.I.HexadOctadFourPlusOne.four_plus_one
#print axioms HMT.I.HexadOctadFourPlusOne.four_plus_one_along_chart

end HMT.I.HexadOctadFourPlusOne
