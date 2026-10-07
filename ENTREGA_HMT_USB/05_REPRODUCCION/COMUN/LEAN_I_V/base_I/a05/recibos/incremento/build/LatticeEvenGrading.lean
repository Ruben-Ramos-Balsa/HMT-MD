import LatticeEvenConformal
import LatticeConformalGrading

/-!
The grading of the actual untwisted fixed subspace. Each weight space embeds
in the already constructed finite full-weight space. The existing parity
projector preserves weights, so projecting the proved spanning decomposition
of the full carrier proves the spanning decomposition of its fixed subspace.
No diagonalizability or grading is supplied as an extra assumption. This is
not a construction of a twisted module or an orbifold product.
-/

noncomputable section
namespace HMT.IV.LatticeEvenGrading

open LatticeOscillatorFock LatticeParityCarrier LatticeEvenVertexFields
open LatticeEvenConformal LatticeConformalGrading LatticeFullGradedTrace
open LatticeEnergyGrading

abbrev evenWeightSpace (o : Fin 12) (d : ℕ) : Submodule ℂ (evenSpace o) :=
  Module.End.eigenspace (evenConformalMode o 0) (d : ℂ)

def evenWeightInclusion (o : Fin 12) (d : ℕ) :
    evenWeightSpace o d →ₗ[ℂ] fullWeightSpace o d where
  toFun v := ⟨v.val.val, by
    have h : v.val ∈ Module.End.eigenspace (evenConformalMode o 0) (d : ℂ) :=
      v.property
    rw [even_weight_space] at h
    exact h⟩
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem evenWeightInclusion_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (evenWeightInclusion o d) := by
  intro u v h
  apply Subtype.ext
  apply Subtype.ext
  exact congrArg (fun w : fullWeightSpace o d => w.val) h

theorem even_weight_finite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (evenWeightSpace o d) :=
  FiniteDimensional.of_injective (evenWeightInclusion o d)
    (evenWeightInclusion_injective o d)

theorem carrierTheta_mem_weight (o : Fin 12) (d : ℕ)
    (v : LatticeCarrier o) (hv : v ∈ fullWeightSpace o d) :
    carrierTheta o v ∈ fullWeightSpace o d := by
  rw [← fullTheta_is_actual_restriction o d ⟨v, hv⟩]
  exact (fullTheta o d ⟨v, hv⟩).property

theorem evenProjector_mem_weight (o : Fin 12) (d : ℕ)
    (v : LatticeCarrier o) (hv : v ∈ fullWeightSpace o d) :
    evenProjector o v ∈ fullWeightSpace o d := by
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply]
  exact Submodule.smul_mem _ _
    (Submodule.add_mem _ hv (carrierTheta_mem_weight o d v hv))

def evenProjection (o : Fin 12) : LatticeCarrier o →ₗ[ℂ] evenSpace o :=
  (evenProjector o).codRestrict (evenSpace o) (evenProjector_mem o)

theorem evenProjection_of_even (o : Fin 12) (v : evenSpace o) :
    evenProjection o v.val = v := by
  apply Subtype.ext
  exact evenProjector_eq_self o v.val v.property

theorem evenProjection_mem_weight (o : Fin 12) (d : ℕ)
    (v : LatticeCarrier o) (hv : v ∈ fullWeightSpace o d) :
    evenProjection o v ∈ evenWeightSpace o d := by
  rw [evenWeightSpace, even_weight_space]
  exact evenProjector_mem_weight o d v hv

theorem even_weights_span (o : Fin 12) :
    (⨆ d : ℕ, evenWeightSpace o d) = ⊤ := by
  have hle : (⨆ d : ℕ, fullWeightSpace o d) ≤
      (⨆ d : ℕ, evenWeightSpace o d).comap (evenProjection o) := by
    apply iSup_le
    intro d v hv
    exact Submodule.mem_iSup_of_mem d (evenProjection_mem_weight o d v hv)
  rw [total_weights_span_carrier] at hle
  apply top_unique
  intro v _
  have h := hle (show v.val ∈ (⊤ : Submodule ℂ (LatticeCarrier o)) from trivial)
  change evenProjection o v.val ∈ (⨆ d : ℕ, evenWeightSpace o d) at h
  rw [evenProjection_of_even] at h
  exact h

theorem evenCoefficient_mem_weight (o : Fin 12) (u v : evenSpace o)
    (d e r : ℕ) (hu : u ∈ evenWeightSpace o d) (hv : v ∈ evenWeightSpace o e)
    (k : ℤ) (hr : (r : ℤ) = d + e + k) :
    evenCoefficient o u k v ∈ evenWeightSpace o r := by
  rw [evenWeightSpace, even_weight_space] at hu hv ⊢
  exact coefficient_mem_weight o u.val v.val d e r hu hv k hr

theorem evenCoefficient_negative_weight_zero (o : Fin 12) (u v : evenSpace o)
    (d e : ℕ) (hu : u ∈ evenWeightSpace o d) (hv : v ∈ evenWeightSpace o e)
    (k : ℤ) (hk : (d : ℤ) + e + k < 0) :
    evenCoefficient o u k v = 0 := by
  apply Subtype.ext
  rw [evenWeightSpace, even_weight_space] at hu hv
  exact coefficient_negative_weight_zero o u.val v.val d e hu hv k hk

end HMT.IV.LatticeEvenGrading
end

#print axioms HMT.IV.LatticeEvenGrading.evenWeightSpace
#print axioms HMT.IV.LatticeEvenGrading.evenWeightInclusion
#print axioms HMT.IV.LatticeEvenGrading.evenWeightInclusion_injective
#print axioms HMT.IV.LatticeEvenGrading.even_weight_finite
#print axioms HMT.IV.LatticeEvenGrading.carrierTheta_mem_weight
#print axioms HMT.IV.LatticeEvenGrading.evenProjector_mem_weight
#print axioms HMT.IV.LatticeEvenGrading.evenProjection
#print axioms HMT.IV.LatticeEvenGrading.evenProjection_of_even
#print axioms HMT.IV.LatticeEvenGrading.evenProjection_mem_weight
#print axioms HMT.IV.LatticeEvenGrading.even_weights_span
#print axioms HMT.IV.LatticeEvenGrading.evenCoefficient_mem_weight
#print axioms HMT.IV.LatticeEvenGrading.evenCoefficient_negative_weight_zero
