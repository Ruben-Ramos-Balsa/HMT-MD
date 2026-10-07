import SelectedGradedTrace
import LatticeWeightShells
import LatticeChargeParityTrace

/-!
Finite total-weight pieces inside the actual untwisted lattice carrier.
Labels include every oscillator occupation and every lattice charge of the
specified total weight. Their finiteness follows from the bounded oscillator
encoding and finite lattice norm shells. The restriction is the existing
carrierTheta. Only zero charge contributes to its trace, leaving the formal
oscillator product in every weight. No twisted module or FLM premise occurs.
-/

noncomputable section
namespace HMT.IV.LatticeFullGradedTrace

open scoped BigOperators TensorProduct
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeCocycle HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeWeightFiniteness HMT.IV.LatticeWeightShells
open HMT.IV.LatticeChargeParityTrace HMT.IV.OscillatorEulerProduct
open HMT.I.SelectedGradedTrace

abbrev FullLabel (o : Fin 12) (d : ℕ) :=
  {p : Occupation o × Lattice o // occupationWeight o p.1 + halfnormNat o p.2 = d}

noncomputable instance fullLabelDecidableEq (o : Fin 12) (d : ℕ) :
    DecidableEq (FullLabel o d) := Classical.decEq _

abbrev ShellLabels (o : Fin 12) (d : ℕ) :=
  Σ k : Fin (d+1), WeightOccupation o (d-k.val) × EnergyShell o k.val

def encodeLabel (o : Fin 12) (d : ℕ) (a : FullLabel o d) : ShellLabels o d :=
  ⟨⟨halfnormNat o a.val.2, by have := a.property; omega⟩,
    ⟨⟨a.val.1, by
      change occupationWeight o a.val.1 = d - halfnormNat o a.val.2
      have := a.property
      omega⟩, ⟨a.val.2, rfl⟩⟩⟩

def decodeLabelPair (o : Fin 12) (d : ℕ) (a : ShellLabels o d) :
    Occupation o × Lattice o := (a.2.1.val, a.2.2.val)

theorem encodeLabel_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (encodeLabel o d) := by
  intro a b h
  apply Subtype.ext
  exact congrArg (decodeLabelPair o d) h

noncomputable instance fullLabelFintype (o : Fin 12) (d : ℕ) :
    Fintype (FullLabel o d) :=
  Fintype.ofInjective (encodeLabel o d) (encodeLabel_injective o d)

def fullWeightSpace (o : Fin 12) (d : ℕ) : Submodule ℂ (LatticeCarrier o) :=
  Submodule.span ℂ (Set.range (fun a : FullLabel o d => carrierBasis o a.val))

theorem fullLabels_independent (o : Fin 12) (d : ℕ) :
    LinearIndependent ℂ (fun a : FullLabel o d => carrierBasis o a.val) :=
  (carrierBasis o).linearIndependent.comp Subtype.val Subtype.val_injective

def fullBasis (o : Fin 12) (d : ℕ) : Basis (FullLabel o d) ℂ (fullWeightSpace o d) :=
  Basis.span (fullLabels_independent o d)

@[simp] theorem fullBasis_coe (o : Fin 12) (d : ℕ) (a : FullLabel o d) :
    (fullBasis o d a : LatticeCarrier o) = carrierBasis o a.val :=
  Basis.span_apply _ a

instance fullWeightFinite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (fullWeightSpace o d) :=
  FiniteDimensional.of_fintype_basis (fullBasis o d)

theorem fullWeight_finrank (o : Fin 12) (d : ℕ) :
    Module.finrank ℂ (fullWeightSpace o d) = Fintype.card (FullLabel o d) :=
  Module.finrank_eq_card_basis (fullBasis o d)

theorem carrierBasis_mem_total_weight (o : Fin 12)
    (a : Occupation o) (x : Lattice o) :
    carrierBasis o (a, x) ∈ fullWeightSpace o (occupationWeight o a + halfnormNat o x) := by
  apply Submodule.subset_span
  exact ⟨⟨(a, x), rfl⟩, rfl⟩

theorem total_weights_span_carrier (o : Fin 12) :
    (⨆ d : ℕ, fullWeightSpace o d) = ⊤ := by
  apply top_unique
  rw [← (carrierBasis o).span_eq]
  apply Submodule.span_le.mpr
  rintro _ ⟨⟨a, x⟩, rfl⟩
  exact Submodule.mem_iSup_of_mem (occupationWeight o a + halfnormNat o x)
    (carrierBasis_mem_total_weight o a x)

def reflectedLabel (o : Fin 12) (d : ℕ) (a : FullLabel o d) : FullLabel o d :=
  ⟨(a.val.1, -a.val.2), by simpa only [halfnormNat_neg] using a.property⟩

theorem reflectedLabel_fixed (o : Fin 12) (d : ℕ) (a : FullLabel o d) :
    reflectedLabel o d a = a ↔ a.val.2 = 0 := by
  constructor
  · intro h
    have hv := congrArg (fun b : FullLabel o d => b.val.2) h
    exact (negation_fixed_iff_zero o a.val.2).mp hv
  · intro h
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · change -a.val.2 = a.val.2
      simp [h]

def fullTheta (o : Fin 12) (d : ℕ) : Module.End ℂ (fullWeightSpace o d) :=
  (fullBasis o d).constr ℂ fun a =>
    (-1 : ℂ) ^ occupationLength o a.val.1 • fullBasis o d (reflectedLabel o d a)

@[simp] theorem fullTheta_basis (o : Fin 12) (d : ℕ) (a : FullLabel o d) :
    fullTheta o d (fullBasis o d a) =
      (-1 : ℂ) ^ occupationLength o a.val.1 • fullBasis o d (reflectedLabel o d a) :=
  Basis.constr_basis _ _ _ _

theorem fullTheta_intertwines (o : Fin 12) (d : ℕ) :
    (fullWeightSpace o d).subtype.comp (fullTheta o d) =
      (carrierTheta o).comp (fullWeightSpace o d).subtype := by
  apply (fullBasis o d).ext
  intro a
  simp only [LinearMap.comp_apply, fullTheta_basis, map_smul,
    Submodule.subtype_apply, fullBasis_coe, carrierTheta_basis]
  exact (carrierTheta_basis o a.val.1 a.val.2).symm

theorem fullTheta_is_actual_restriction (o : Fin 12) (d : ℕ)
    (v : fullWeightSpace o d) :
    (fullTheta o d v : LatticeCarrier o) = carrierTheta o (v : LatticeCarrier o) :=
  LinearMap.congr_fun (fullTheta_intertwines o d) v

theorem fullTheta_diagonal (o : Fin 12) (d : ℕ) (a : FullLabel o d) :
    LinearMap.toMatrix (fullBasis o d) (fullBasis o d) (fullTheta o d) a a =
      if a.val.2 = 0 then (-1 : ℂ) ^ occupationLength o a.val.1 else 0 := by
  classical
  rw [LinearMap.toMatrix_apply, fullTheta_basis, LinearEquiv.map_smul,
    Basis.repr_self]
  simp only [Finsupp.smul_apply, Finsupp.single_apply, smul_eq_mul,
    reflectedLabel_fixed]
  split_ifs <;> simp

abbrev ZeroChargeLabel (o : Fin 12) (d : ℕ) := {a : FullLabel o d // a.val.2 = 0}

def zeroChargeEquiv (o : Fin 12) (d : ℕ) :
    ZeroChargeLabel o d ≃ WeightOccupation o d where
  toFun a := ⟨a.val.val.1, by
    have h := a.val.property
    simpa only [a.property, halfnormNat_zero, add_zero] using h⟩
  invFun a := ⟨⟨(a.val, 0), by simp only [halfnormNat_zero, add_zero]; exact a.property⟩, rfl⟩
  left_inv a := by
    apply Subtype.ext
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · exact a.property.symm
  right_inv a := by apply Subtype.ext; rfl

theorem fullTheta_trace_zero_charge (o : Fin 12) (d : ℕ) :
    LinearMap.trace ℂ (fullWeightSpace o d) (fullTheta o d) =
      ∑ a : WeightOccupation o d, (-1 : ℂ) ^ occupationLength o a.val := by
  classical
  rw [LinearMap.trace_eq_matrix_trace ℂ (fullBasis o d)]
  change (∑ a : FullLabel o d,
    LinearMap.toMatrix (fullBasis o d) (fullBasis o d) (fullTheta o d) a a) = _
  simp_rw [fullTheta_diagonal]
  rw [← Finset.sum_filter]
  rw [Finset.sum_subtype (p := fun a : FullLabel o d => a.val.2 = 0) _ (by simp) (fun a : FullLabel o d =>
    (-1 : ℂ) ^ occupationLength o a.val.1)]
  exact Fintype.sum_equiv (zeroChargeEquiv o d) _ _ (fun _ => rfl)

theorem fullTheta_trace_product (o : Fin 12) (d : ℕ) :
    LinearMap.trace ℂ (fullWeightSpace o d) (fullTheta o d) =
      PowerSeries.coeff ℂ d (oscillatorProduct (BasisSize o)) := by
  rw [fullTheta_trace_zero_charge]
  rw [← weight_trace_product o d]
  exact (HMT.IV.FockFiniteParityPiece.actual_piece_trace o
    (weightLabels o d) Subtype.val_injective).symm

end HMT.IV.LatticeFullGradedTrace
end

#print axioms HMT.IV.LatticeFullGradedTrace.encodeLabel_injective
#print axioms HMT.IV.LatticeFullGradedTrace.fullLabelFintype
#print axioms HMT.IV.LatticeFullGradedTrace.fullWeight_finrank
#print axioms HMT.IV.LatticeFullGradedTrace.carrierBasis_mem_total_weight
#print axioms HMT.IV.LatticeFullGradedTrace.total_weights_span_carrier
#print axioms HMT.IV.LatticeFullGradedTrace.fullTheta_is_actual_restriction
#print axioms HMT.IV.LatticeFullGradedTrace.fullTheta_trace_zero_charge
#print axioms HMT.IV.LatticeFullGradedTrace.fullTheta_trace_product
