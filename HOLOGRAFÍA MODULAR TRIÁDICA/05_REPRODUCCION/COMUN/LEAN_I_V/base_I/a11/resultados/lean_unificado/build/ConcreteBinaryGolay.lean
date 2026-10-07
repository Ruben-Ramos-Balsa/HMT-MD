import ConcreteBinaryGolayCode

/-!
Steiner's property is a theorem, not an input: allowed weights force
uniqueness above each five-set, and the exact count of octads makes this
packing cover all five-sets. This realizes the classical branch expressly
chosen in Article I; an incidence chart to the selected ternary branch is
a separate map.
-/

namespace HMT.I.ConcreteBinaryGolay

open HexadOctadResidual

set_option maxRecDepth 20000
set_option maxHeartbeats 2000000

theorem octad_unique_over_five (A O P : Support) (hA : A.card = 5)
    (hO : O ∈ octads) (hP : P ∈ octads) (hAO : A ⊆ O) (hAP : A ⊆ P) : O = P := by
  obtain ⟨hOc, hO8⟩ := (mem_octads O).mp hO
  obtain ⟨hPc, hP8⟩ := (mem_octads P).mp hP
  have hinter : 5 ≤ (O ∩ P).card := by
    rw [← hA]
    exact Finset.card_le_card (Finset.subset_inter hAO hAP)
  have hcard := binarySum_card O P
  have hweights := allowed_weights _ (sum_closed O hOc P hPc)
  have hempty : (binarySum O P).card = 0 := by
    rcases hweights with h | h | h | h | h <;> omega
  have he : binarySum O P = ∅ := Finset.card_eq_zero.mp hempty
  have hd : O \ P = ∅ ∧ P \ O = ∅ := by
    simpa only [binarySum, Finset.union_eq_empty] using he
  exact Finset.Subset.antisymm (Finset.sdiff_eq_empty_iff_subset.mp hd.1)
    (Finset.sdiff_eq_empty_iff_subset.mp hd.2)

abbrev FiveSets := (Finset.univ : Support).powersetCard 5
abbrev Octad := {O : Support // O ∈ octads}
abbrev FiveSet := {A : Support // A ∈ FiveSets}
abbrev Flag := Σ O : Octad, {A : Support // A ∈ O.val.powersetCard 5}

def forgetOctad (f : Flag) : FiveSet :=
  ⟨f.2.val, Finset.mem_powersetCard.mpr
    ⟨Finset.subset_univ _, (Finset.mem_powersetCard.mp f.2.property).2⟩⟩

theorem forgetOctad_injective : Function.Injective forgetOctad := by
  intro f g h
  have hA : f.2.val = g.2.val := congrArg Subtype.val h
  have hO : f.1 = g.1 := by
    apply Subtype.ext
    apply octad_unique_over_five f.2.val
    · exact (Finset.mem_powersetCard.mp f.2.property).2
    · exact f.1.property
    · exact g.1.property
    · exact (Finset.mem_powersetCard.mp f.2.property).1
    · rw [hA]
      exact (Finset.mem_powersetCard.mp g.2.property).1
  cases f with
  | mk O A =>
    cases g with
    | mk P B =>
      dsimp only at hO hA
      subst P
      have : A = B := Subtype.ext hA
      subst B
      rfl

theorem fiveSet_card : Fintype.card FiveSet = 42504 := by
  rw [Fintype.card_coe, Finset.card_powersetCard]
  norm_num only [Finset.card_univ, Fintype.card_fin]
  decide

theorem flag_card_generic (s : Finset Support) (hs : ∀ O ∈ s, O.card = 8) :
    Fintype.card (Σ O : {O : Support // O ∈ s},
      {A : Support // A ∈ O.val.powersetCard 5}) = s.card * 56 := by
  rw [Fintype.card_sigma]
  have h : ∀ O : {O : Support // O ∈ s},
      Fintype.card {A : Support // A ∈ O.val.powersetCard 5} = 56 := by
    intro O
    rw [Fintype.card_coe, Finset.card_powersetCard, hs O.val O.property]
    decide
  simp only [h, Finset.sum_const, Finset.card_univ, smul_eq_mul]
  rw [Fintype.card_coe]

theorem flag_card : Fintype.card Flag = 42504 := by
  have h := flag_card_generic octads (fun O hO => ((mem_octads O).mp hO).2)
  rw [octads_card] at h
  exact h

theorem forgetOctad_surjective : Function.Surjective forgetOctad :=
  ((Fintype.bijective_iff_injective_and_card forgetOctad).mpr
    ⟨forgetOctad_injective, flag_card.trans fiveSet_card.symm⟩).2

theorem steiner_5_8_24 (A : Support) (hA : A.card = 5) :
    ∃! O : Support, O ∈ code ∧ O.card = 8 ∧ A ⊆ O := by
  let a : FiveSet := ⟨A, Finset.mem_powersetCard.mpr ⟨Finset.subset_univ _, hA⟩⟩
  obtain ⟨f, hf⟩ := forgetOctad_surjective a
  have hsub : A ⊆ f.1.val := by
    have hval : f.2.val = A := congrArg Subtype.val hf
    rw [← hval]
    exact (Finset.mem_powersetCard.mp f.2.property).1
  obtain ⟨hc, h8⟩ := (mem_octads f.1.val).mp f.1.property
  refine ⟨f.1.val, ⟨hc, h8, hsub⟩, ?_⟩
  intro P hP
  exact octad_unique_over_five A P f.1.val hA
    ((mem_octads P).mpr ⟨hP.1, hP.2.1⟩) f.1.property hP.2.2 hsub

/-- All fields of the formerly abstract binary interface are discharged. -/
def golay : BinaryGolayData where
  code := code
  sum_closed := sum_closed
  allowed_weights := allowed_weights
  dodecad := dodecad
  dodecad_mem := dodecad_mem
  dodecad_card := dodecad_card
  steiner_5_8_24 := steiner_5_8_24

theorem concrete_residual_steiner (A : Support) (hA : A.card = 5) (hAD : A ⊆ dodecad) :
    ∃! H : Support, golay.IsResidualHexad H ∧ A ⊆ H :=
  golay.residual_steiner_5_6_12 A hA hAD

end HMT.I.ConcreteBinaryGolay

#print axioms HMT.I.ConcreteBinaryGolay.octad_unique_over_five
#print axioms HMT.I.ConcreteBinaryGolay.flag_card
#print axioms HMT.I.ConcreteBinaryGolay.steiner_5_8_24
#print axioms HMT.I.ConcreteBinaryGolay.golay
#print axioms HMT.I.ConcreteBinaryGolay.concrete_residual_steiner
