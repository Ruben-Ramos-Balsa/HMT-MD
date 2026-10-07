import LatticeTwistedLowWeights
import LatticeWeightFiniteness

/-! Finite eigenspaces for every half-integer conformal weight of the actual
twisted carrier. Boundedness is proved by encoding occupations in previously
constructed finite oscillator shells. There is no ambient frequency cutoff. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedGrading
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeWeightFiniteness LatticeFiniteIrreducible LatticeTwistedCarrier
open LatticeHalfWeightBasis LatticeTwistedLowWeights

theorem occupationWeight_le_twiceWeight (o : Fin 12) (a : Occupation o) :
    occupationWeight o a ≤ twiceWeight o a := by
  classical
  unfold occupationWeight twiceWeight Finsupp.sum
  exact Finset.sum_le_sum fun p _ => Nat.mul_le_mul_right (a p) (by omega)

abbrev HalfOccupation (o : Fin 12) (d : ℕ) :=
  {a : Occupation o // twiceWeight o a = d}

def encodeOccupation (o : Fin 12) (d : ℕ) (a : HalfOccupation o d) :
    Σ k : Fin (d+1), WeightOccupation o k.val :=
  ⟨⟨occupationWeight o a.val, by
      have h := occupationWeight_le_twiceWeight o a.val
      rw [a.property] at h
      omega⟩, ⟨a.val, rfl⟩⟩

theorem encodeOccupation_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (encodeOccupation o d) := by
  intro a b h
  apply Subtype.ext
  exact congrArg (fun p : Σ k : Fin (d+1), WeightOccupation o k.val => p.2.val) h

instance halfOccupationFintype (o : Fin 12) (d : ℕ) :
    Fintype (HalfOccupation o d) :=
  Fintype.ofInjective (encodeOccupation o d) (encodeOccupation_injective o d)

abbrev WeightLabel (o : Fin 12) (d : ℕ) :=
  {p : BasisIndex o // twiceWeight o p.1 = d}

def encodeLabel (o : Fin 12) (d : ℕ) (a : WeightLabel o d) :
    HalfOccupation o d × Fin (Module.finrank ℂ (FiniteSpace o)) :=
  (⟨a.val.1, a.property⟩, a.val.2)

theorem encodeLabel_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (encodeLabel o d) := by
  intro a b h
  apply Subtype.ext
  exact congrArg (fun p : HalfOccupation o d × Fin (Module.finrank ℂ (FiniteSpace o)) =>
    (p.1.val, p.2)) h

instance weightLabelFintype (o : Fin 12) (d : ℕ) :
    Fintype (WeightLabel o d) :=
  Fintype.ofInjective (encodeLabel o d) (encodeLabel_injective o d)

def weightSpace (o : Fin 12) (d : ℕ) : Submodule ℂ (Carrier o) :=
  Submodule.span ℂ (Set.range fun a : WeightLabel o d => twistedBasis o a.val)

theorem weightLabels_independent (o : Fin 12) (d : ℕ) :
    LinearIndependent ℂ (fun a : WeightLabel o d => twistedBasis o a.val) :=
  (twistedBasis o).linearIndependent.comp Subtype.val Subtype.val_injective

def weightBasis (o : Fin 12) (d : ℕ) : Basis (WeightLabel o d) ℂ (weightSpace o d) :=
  Basis.span (weightLabels_independent o d)

@[simp] theorem weightBasis_coe (o : Fin 12) (d : ℕ) (a : WeightLabel o d) :
    (weightBasis o d a : Carrier o) = twistedBasis o a.val := Basis.span_apply _ a

instance weightSpaceFinite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (weightSpace o d) :=
  FiniteDimensional.of_fintype_basis (weightBasis o d)

theorem weightSpace_finrank (o : Fin 12) (d : ℕ) :
    Module.finrank ℂ (weightSpace o d) = Fintype.card (WeightLabel o d) :=
  Module.finrank_eq_card_basis (weightBasis o d)

theorem weightSpace_le_eigenspace (o : Fin 12) (d : ℕ) :
    weightSpace o d ≤ Module.End.eigenspace (conformalMode o 0) (((d:ℂ)+3)/2) := by
  apply Submodule.span_le.mpr
  rintro _ ⟨a, rfl⟩
  apply Module.End.mem_eigenspace_iff.mpr
  rw [conformal_basis_weight, a.property]

theorem eigenspace_le_weightSpace (o : Fin 12) (d : ℕ) :
    Module.End.eigenspace (conformalMode o 0) (((d:ℂ)+3)/2) ≤ weightSpace o d := by
  classical
  intro v hv
  have hv' := Module.End.mem_eigenspace_iff.mp hv
  rw [← (twistedBasis o).linearCombination_repr v,
    Finsupp.linearCombination_apply, Finsupp.sum]
  apply Submodule.sum_mem
  intro p hp
  apply Submodule.smul_mem
  apply Submodule.subset_span
  have hn : (twistedBasis o).repr v p ≠ 0 := Finsupp.mem_support_iff.mp hp
  have h := congrArg (fun w => (twistedBasis o).repr w p) hv'
  dsimp only at h
  rw [conformal_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hw : ((twiceWeight o p.1 : ℂ)+3)/2 = ((d:ℂ)+3)/2 := mul_right_cancel₀ hn h
  have hc : (twiceWeight o p.1 : ℂ) = (d:ℂ) := by linear_combination 2*hw
  have hd : twiceWeight o p.1 = d := by exact_mod_cast hc
  exact ⟨⟨p, hd⟩, rfl⟩

theorem weightSpace_eq_eigenspace (o : Fin 12) (d : ℕ) :
    weightSpace o d = Module.End.eigenspace (conformalMode o 0) (((d:ℂ)+3)/2) :=
  le_antisymm (weightSpace_le_eigenspace o d) (eigenspace_le_weightSpace o d)

theorem conformal_eigenspace_finite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (Module.End.eigenspace (conformalMode o 0) (((d:ℂ)+3)/2)) := by
  rw [← weightSpace_eq_eigenspace]
  infer_instance

theorem basis_mem_weight (o : Fin 12) (p : BasisIndex o) :
    twistedBasis o p ∈ weightSpace o (twiceWeight o p.1) :=
  Submodule.subset_span ⟨⟨p, rfl⟩, rfl⟩

theorem weights_span (o : Fin 12) : (⨆ d : ℕ, weightSpace o d) = ⊤ := by
  apply top_unique
  rw [← (twistedBasis o).span_eq]
  apply Submodule.span_le.mpr
  rintro _ ⟨p, rfl⟩
  exact Submodule.mem_iSup_of_mem (twiceWeight o p.1) (basis_mem_weight o p)

end HMT.IV.LatticeTwistedGrading
end
