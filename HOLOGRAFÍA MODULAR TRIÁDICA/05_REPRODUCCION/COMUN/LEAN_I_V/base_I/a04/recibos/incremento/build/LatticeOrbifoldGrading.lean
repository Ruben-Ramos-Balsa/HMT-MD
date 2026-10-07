import LatticeOrbifoldCarrier
import LatticeTwistedPositiveGrading

/-! The conformal grading of the direct sum of the two constructed positive
sectors. Each eigenspace is finite, and the integral eigenspaces span the
carrier. This concerns the space and its conformal action, not the cross-sector
vertex products. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeOrbifoldGrading
open LatticeEvenVertexFields LatticeEvenConformal LatticeEvenGrading
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading
open LatticeOrbifoldCarrier

abbrev weightSpace (o : Fin 12) (d : ℕ) : Submodule ℂ (Space o) :=
  Module.End.eigenspace (modes o 0) (d:ℂ)

def weightEquiv (o : Fin 12) (d : ℕ) :
    weightSpace o d ≃ₗ[ℂ] evenWeightSpace o d × positiveWeightSpace o d where
  toFun v := (⟨v.val.1, ((eigenspace_components o (d:ℂ) v.val).mp v.property).1⟩,
    ⟨v.val.2, ((eigenspace_components o (d:ℂ) v.val).mp v.property).2⟩)
  invFun v := ⟨(v.1.val,v.2.val),
    (eigenspace_components o (d:ℂ) (v.1.val,v.2.val)).mpr ⟨v.1.property,v.2.property⟩⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

instance weight_finite (o : Fin 12) (d : ℕ) : FiniteDimensional ℂ (weightSpace o d) := by
  haveI : FiniteDimensional ℂ (evenWeightSpace o d) := even_weight_finite o d
  exact FiniteDimensional.of_injective
    (V₂ := (evenWeightSpace o d) × (positiveWeightSpace o d))
    (weightEquiv o d).toLinearMap (weightEquiv o d).injective

theorem weight_dimension (o : Fin 12) (d : ℕ) :
    Module.finrank ℂ (weightSpace o d) =
      Module.finrank ℂ (evenWeightSpace o d) + Module.finrank ℂ (positiveWeightSpace o d) := by
  haveI : FiniteDimensional ℂ (evenWeightSpace o d) := even_weight_finite o d
  haveI : Module.Free ℂ (evenWeightSpace o d) := Module.Free.of_divisionRing ℂ (evenWeightSpace o d)
  haveI : Module.Free ℂ (positiveWeightSpace o d) := Module.Free.of_divisionRing ℂ (positiveWeightSpace o d)
  rw [(weightEquiv o d).finrank_eq]
  exact Module.finrank_prod (R := ℂ) (M := evenWeightSpace o d)
    (M' := positiveWeightSpace o d)

def untwistedInclusion (o : Fin 12) : evenSpace o →ₗ[ℂ] Space o :=
  LinearMap.inl ℂ (evenSpace o) (positiveSector o)

def twistedInclusion (o : Fin 12) : positiveSector o →ₗ[ℂ] Space o :=
  LinearMap.inr ℂ (evenSpace o) (positiveSector o)

theorem untwisted_mem_weight (o : Fin 12) (d : ℕ) (v : evenSpace o)
    (hv : v ∈ evenWeightSpace o d) : untwistedInclusion o v ∈ weightSpace o d := by
  apply (eigenspace_components o (d:ℂ) _).mpr
  exact ⟨hv, Submodule.zero_mem _⟩

theorem twisted_mem_weight (o : Fin 12) (d : ℕ) (v : positiveSector o)
    (hv : v ∈ positiveWeightSpace o d) : twistedInclusion o v ∈ weightSpace o d := by
  apply (eigenspace_components o (d:ℂ) _).mpr
  exact ⟨Submodule.zero_mem _, hv⟩

theorem weights_span (o : Fin 12) : (⨆ d : ℕ, weightSpace o d) = ⊤ := by
  have he : (⨆ d : ℕ, evenWeightSpace o d) ≤
      (⨆ d : ℕ, weightSpace o d).comap (untwistedInclusion o) := by
    apply iSup_le
    intro d v hv
    exact Submodule.mem_iSup_of_mem d (untwisted_mem_weight o d v hv)
  have ht : (⨆ d : ℕ, positiveWeightSpace o d) ≤
      (⨆ d : ℕ, weightSpace o d).comap (twistedInclusion o) := by
    apply iSup_le
    intro d v hv
    exact Submodule.mem_iSup_of_mem d (twisted_mem_weight o d v hv)
  rw [even_weights_span] at he
  rw [positive_weights_span] at ht
  apply top_unique
  intro v _
  have h1 := he (show v.1 ∈ (⊤ : Submodule ℂ (evenSpace o)) from trivial)
  have h2 := ht (show v.2 ∈ (⊤ : Submodule ℂ (positiveSector o)) from trivial)
  have h := Submodule.add_mem (⨆ d : ℕ, weightSpace o d) h1 h2
  simpa [untwistedInclusion, twistedInclusion] using h

theorem assembled_graded_carrier (o : Fin 12) :
    (∀ d : ℕ, FiniteDimensional ℂ (weightSpace o d)) ∧
    (⨆ d : ℕ, weightSpace o d) = ⊤ ∧
    weightSpace o 0 = Submodule.span ℂ {vacuum o} ∧
    weightSpace o 1 = ⊥ := by
  exact ⟨fun d => weight_finite o d, weights_span o,
    by simpa only [weightSpace, Nat.cast_zero] using weight_zero_vacuum_line o,
    by simpa only [weightSpace, Nat.cast_one] using weight_one_zero o⟩

end HMT.IV.LatticeOrbifoldGrading
end
