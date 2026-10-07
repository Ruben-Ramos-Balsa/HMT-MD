import LatticeTwistedPositiveSector
import LatticeTwistedGrading
import LatticeTwistedBasisParity

/-! The positive sector inherits the actual conformal grading of the twisted
carrier. Finiteness and low-weight vanishing are proved from its existing
eigenspaces, not imposed as axioms or by truncating the carrier. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedPositiveGrading
open LatticeTwistedCarrier LatticeTwistedParity LatticeTwistedPositiveSector
open LatticeTwistedGrading LatticeTwistedLowWeights LatticeHalfWeightBasis
open LatticeTwistedBasisParity

abbrev positiveWeightSpace (o : Fin 12) (d : ℕ) : Submodule ℂ (positiveSector o) :=
  Module.End.eigenspace (positiveConformalMode o 0) (d:ℂ)

theorem positive_eigenspace_eq_comap (o : Fin 12) (c : ℂ) :
    Module.End.eigenspace (positiveConformalMode o 0) c =
      (Module.End.eigenspace (conformalMode o 0) c).comap (positiveSector o).subtype := by
  ext v
  rw [Module.End.mem_eigenspace_iff, Submodule.mem_comap,
    Module.End.mem_eigenspace_iff]
  constructor
  · intro h
    have hc := congrArg Subtype.val h
    simpa only [Submodule.coe_smul, positiveConformalMode_coe] using hc
  · intro h
    apply Subtype.ext
    rw [positiveConformalMode_coe]
    exact h

theorem positive_weight_zero (o : Fin 12) : positiveWeightSpace o 0 = ⊥ := by
  rw [positiveWeightSpace, Nat.cast_zero, positive_eigenspace_eq_comap,
    weight_zero_vanishes, Submodule.comap_bot]
  exact LinearMap.ker_eq_bot.mpr (positiveSector o).subtype_injective

theorem positive_weight_one (o : Fin 12) : positiveWeightSpace o 1 = ⊥ := by
  rw [positiveWeightSpace, Nat.cast_one, positive_eigenspace_eq_comap,
    weight_one_vanishes, Submodule.comap_bot]
  exact LinearMap.ker_eq_bot.mpr (positiveSector o).subtype_injective

theorem integer_eigenspace_finite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (Module.End.eigenspace (conformalMode o 0) (d:ℂ)) := by
  by_cases hd : d ≤ 1
  · interval_cases d
    · rw [Nat.cast_zero, weight_zero_vanishes]
      infer_instance
    · rw [Nat.cast_one, weight_one_vanishes]
      infer_instance
  · have hi : ((2*d-3:ℕ):ℂ)+3 = 2*(d:ℂ) := by
      have h : (2*d-3:ℕ)+3=2*d := by omega
      exact_mod_cast h
    have hc : (((2*d-3:ℕ):ℂ)+3)/2 = (d:ℂ) := by linear_combination hi/2
    rw [← hc]
    exact conformal_eigenspace_finite o (2*d-3)

def positiveWeightInclusion (o : Fin 12) (d : ℕ) :
    positiveWeightSpace o d →ₗ[ℂ]
      Module.End.eigenspace (conformalMode o 0) (d:ℂ) where
  toFun v := ⟨v.val.val, by
    have h := v.property
    change v.val ∈ Module.End.eigenspace (positiveConformalMode o 0) (d:ℂ) at h
    rw [positive_eigenspace_eq_comap] at h
    exact h⟩
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem positiveWeightInclusion_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (positiveWeightInclusion o d) := by
  intro u v h
  apply Subtype.ext
  apply Subtype.ext
  exact congrArg (fun w : Module.End.eigenspace (conformalMode o 0) (d:ℂ) => w.val) h

instance positive_weight_finite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (positiveWeightSpace o d) := by
  haveI := integer_eigenspace_finite o d
  exact FiniteDimensional.of_injective (positiveWeightInclusion o d)
    (positiveWeightInclusion_injective o d)

def positiveProjection (o : Fin 12) : Carrier o →ₗ[ℂ] positiveSector o :=
  (evenProjector o).codRestrict (positiveSector o) (fun v => even_fixed o v)

theorem positiveProjection_of_positive (o : Fin 12) (v : positiveSector o) :
    positiveProjection o v.val = v := by
  apply Subtype.ext
  exact evenProjector_fixed_identity o v.val v.property

theorem positiveProjection_mem_fixed_weight (o : Fin 12) (d : ℕ) (v : Carrier o)
    (hv : liftedTheta o v = v) (hw : conformalMode o 0 v = (d:ℂ) • v) :
    positiveProjection o v ∈ positiveWeightSpace o d := by
  have hmem : (⟨v,hv⟩ : positiveSector o) ∈ positiveWeightSpace o d := by
    apply Module.End.mem_eigenspace_iff.mpr
    apply Subtype.ext
    exact hw
  rw [show positiveProjection o v = (⟨v,hv⟩ : positiveSector o) from
    positiveProjection_of_positive o ⟨v,hv⟩]
  exact hmem

theorem positive_weights_span (o : Fin 12) :
    (⨆ d : ℕ, positiveWeightSpace o d) = ⊤ := by
  classical
  apply top_unique
  intro v _
  rw [← positiveProjection_of_positive o v,
    ← (twistedBasis o).linearCombination_repr v.val,
    Finsupp.linearCombination_apply, Finsupp.sum, map_sum]
  apply Submodule.sum_mem
  intro p hp
  rw [map_smul]
  apply Submodule.smul_mem
  have hp0 : (twistedBasis o).repr v.val p ≠ 0 := Finsupp.mem_support_iff.mp hp
  have hfixed : liftedTheta o (twistedBasis o p) = twistedBasis o p :=
    (positive_basis_iff_odd o p).mpr (positive_support_odd o v.val v.property p hp0)
  obtain ⟨d, _, hd⟩ := positive_basis_integer_weight o p hfixed
  exact Submodule.mem_iSup_of_mem d
    (positiveProjection_mem_fixed_weight o d (twistedBasis o p) hfixed hd)

theorem positive_eigenvalue_integer_ge_two (o : Fin 12) (v : positiveSector o)
    (hv : v ≠ 0) (c : ℂ) (hc : positiveConformalMode o 0 v = c • v) :
    ∃ d : ℕ, 2 ≤ d ∧ c = (d:ℂ) := by
  apply LatticeTwistedBasisParity.positive_eigenvalue_integer_ge_two o v.val
  · intro hz
    exact hv (Subtype.ext hz)
  · exact v.property
  · have h := congrArg Subtype.val hc
    simpa only [positiveConformalMode_coe, Submodule.coe_smul] using h

end HMT.IV.LatticeTwistedPositiveGrading
end
