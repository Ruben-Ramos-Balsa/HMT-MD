import LatticeTwistedPositiveGrading

/-! The positive conformal weight-two space is exactly the first oscillator
layer of the constructed tensor carrier. Its dimension is counted from the
actual occupation basis and the already proved finite representation dimension.
No dimension or truncation is supplied as a hypothesis. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedWeightTwo
open LatticeOscillatorFock LatticeFockMonomialParity LatticeHalfWeightBasis
open LatticeFiniteIrreducible LatticeFiniteGroundState
open LatticeTwistedCarrier LatticeTwistedLowWeights LatticeTwistedGrading
open LatticeTwistedParity LatticeTwistedBasisParity
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading

theorem twiceWeight_entry_le (o : Fin 12) (a : Occupation o) (p : Mode o) :
    (2*p.1+1)*a p ≤ twiceWeight o a := by
  classical
  by_cases hp : p ∈ a.support
  · change (2*p.1+1)*a p ≤ ∑ q ∈ a.support, (2*q.1+1)*a q
    exact Finset.single_le_sum (f := fun q : Mode o => (2*q.1+1)*a q)
      (fun _ _ => Nat.zero_le _) hp
  · simp [Finsupp.notMem_support_iff.mp hp]

theorem twiceWeight_zero_iff (o : Fin 12) (a : Occupation o) :
    twiceWeight o a = 0 ↔ a = 0 := by
  constructor
  · intro h
    ext p
    have hp := twiceWeight_entry_le o a p
    rw [h] at hp
    change a p = 0
    nlinarith
  · rintro rfl
    exact twiceWeight_zero o

theorem twiceWeight_one_iff (o : Fin 12) (a : Occupation o) :
    twiceWeight o a = 1 ↔
      ∃ i : Fin (LatticeCocycle.BasisSize o), a = Finsupp.single (0,i) 1 := by
  classical
  constructor
  · intro h
    induction a using Finsupp.induction with
    | zero => simp at h
    | @single_add p k a _ hk _ =>
      rw [twiceWeight_add, twiceWeight_single] at h
      have hkpos : 0 < k := Nat.pos_of_ne_zero hk
      have hk1 : k = 1 := by nlinarith
      rw [hk1, mul_one] at h
      have hp0 : p.1 = 0 := by omega
      have ha0 : a = 0 := (twiceWeight_zero_iff o a).mp (by omega)
      refine ⟨p.2, ?_⟩
      rw [hk1, ha0, add_zero]
      congr 1
      exact Prod.ext hp0 rfl
  · rintro ⟨i, rfl⟩
    simp

def firstWeightLabelEquiv (o : Fin 12) :
    (Fin (LatticeCocycle.BasisSize o) × Fin (Module.finrank ℂ (FiniteSpace o))) ≃
      WeightLabel o 1 :=
  Equiv.ofBijective (fun p => ⟨(Finsupp.single (0,p.1) 1,p.2), by simp⟩) (by
    constructor
    · intro p q h
      apply Prod.ext
      · have hs : Finsupp.single (0,p.1) (1:ℕ) = Finsupp.single (0,q.1) 1 :=
          congrArg (fun a : WeightLabel o 1 => a.val.1) h
        exact congrArg Prod.snd (Finsupp.single_left_injective (by omega) hs)
      · exact congrArg (fun a : WeightLabel o 1 => a.val.2) h
    · intro a
      obtain ⟨i, hi⟩ := (twiceWeight_one_iff o a.val.1).mp a.property
      refine ⟨(i,a.val.2), ?_⟩
      apply Subtype.ext
      exact Prod.ext hi.symm rfl)

theorem firstWeightLabel_card (o : Fin 12) :
    Fintype.card (WeightLabel o 1) = LatticeCocycle.BasisSize o *
      Module.finrank ℂ (FiniteSpace o) := by
  rw [← Fintype.card_congr (firstWeightLabelEquiv o), Fintype.card_prod]
  simp

theorem firstWeightSpace_finrank (o : Fin 12) :
    Module.finrank ℂ (weightSpace o 1) = 98304 := by
  have hr : LatticeCocycle.BasisSize o = 24 := NeighborRank.witt_marked_integer_rank o
  rw [weightSpace_finrank, firstWeightLabel_card,
    hr, finiteSpace_dimension]

theorem firstWeightSpace_le_positive (o : Fin 12) :
    weightSpace o 1 ≤ positiveSector o := by
  apply Submodule.span_le.mpr
  rintro _ ⟨a,rfl⟩
  apply (positive_basis_iff_odd o a.val).mpr
  rw [← twiceWeight_mod_two, a.property]

theorem weight_two_eigenspace_eq (o : Fin 12) :
    Module.End.eigenspace (conformalMode o 0) (2:ℂ) = weightSpace o 1 := by
  convert (weightSpace_eq_eigenspace o 1).symm using 1
  norm_num

theorem positive_weight_two_eq_comap (o : Fin 12) :
    positiveWeightSpace o 2 = (weightSpace o 1).comap (positiveSector o).subtype := by
  rw [positiveWeightSpace, positive_eigenspace_eq_comap]
  norm_num only [Nat.cast_ofNat]
  rw [weight_two_eigenspace_eq]

theorem positive_weight_two_finrank (o : Fin 12) :
    Module.finrank ℂ (positiveWeightSpace o 2) = 98304 := by
  rw [positive_weight_two_eq_comap,
    (Submodule.comapSubtypeEquivOfLe (firstWeightSpace_le_positive o)).finrank_eq,
    firstWeightSpace_finrank]

theorem positive_weight_two_dimension_product (o : Fin 12) :
    Module.finrank ℂ (positiveWeightSpace o 2) =
      24 * Module.finrank ℂ (FiniteSpace o) := by
  rw [positive_weight_two_finrank, finiteSpace_dimension]

end HMT.IV.LatticeTwistedWeightTwo
end

#print axioms HMT.IV.LatticeTwistedWeightTwo.twiceWeight_entry_le
#print axioms HMT.IV.LatticeTwistedWeightTwo.twiceWeight_zero_iff
#print axioms HMT.IV.LatticeTwistedWeightTwo.twiceWeight_one_iff
#print axioms HMT.IV.LatticeTwistedWeightTwo.firstWeightLabelEquiv
#print axioms HMT.IV.LatticeTwistedWeightTwo.firstWeightLabel_card
#print axioms HMT.IV.LatticeTwistedWeightTwo.firstWeightSpace_finrank
#print axioms HMT.IV.LatticeTwistedWeightTwo.firstWeightSpace_le_positive
#print axioms HMT.IV.LatticeTwistedWeightTwo.weight_two_eigenspace_eq
#print axioms HMT.IV.LatticeTwistedWeightTwo.positive_weight_two_eq_comap
#print axioms HMT.IV.LatticeTwistedWeightTwo.positive_weight_two_finrank
#print axioms HMT.IV.LatticeTwistedWeightTwo.positive_weight_two_dimension_product
