import LatticeHeisenbergField

/-! Differential covariance is closed under the existing complex-linear
field operations. This is an extension lemma, not an assumed covariance
of any generator or of the constructed state-field map. -/

noncomputable section
namespace HMT.IV.LatticeTranslationLinear

variable {V W ι : Type*} [AddCommGroup V] [Module ℂ V]
  [AddCommGroup W] [Module ℂ W]

def TranslationCovariant (T : Module.End ℂ V) (B : VertexOperator ℂ V) : Prop :=
  ∀ k : ℤ, T * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T =
    ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)

theorem covariant_zero (T : Module.End ℂ V) : TranslationCovariant T 0 := by
  intro k
  have hz (j : ℤ) : HVertexOperator.coeff (0 : VertexOperator ℂ V) j = 0 := by
    apply LinearMap.ext
    intro v
    rfl
  simp only [hz, mul_zero, zero_mul, sub_self, smul_zero]

theorem covariant_add {T : Module.End ℂ V} {A B : VertexOperator ℂ V}
    (hA : TranslationCovariant T A) (hB : TranslationCovariant T B) :
    TranslationCovariant T (A+B) := by
  intro k
  simp only [HVertexOperator.coeff_add, Pi.add_apply]
  calc
    _ = (T * HVertexOperator.coeff A k - HVertexOperator.coeff A k * T) +
      (T * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T) := by
        simp only [mul_add, add_mul]; abel
    _ = _ := by rw [hA k, hB k, smul_add]

theorem covariant_smul {T : Module.End ℂ V} {B : VertexOperator ℂ V}
    (hB : TranslationCovariant T B) (c : ℂ) :
    TranslationCovariant T (c • B) := by
  intro k
  simp only [HVertexOperator.coeff_smul, Pi.smul_apply]
  rw [mul_smul_comm, smul_mul_assoc, ← smul_sub, hB k, smul_comm]

theorem covariance_linear_extension (basis : Basis ι ℂ W)
    (Y : W →ₗ[ℂ] VertexOperator ℂ V) (T : Module.End ℂ V)
    (h : ∀ i, TranslationCovariant T (Y (basis i))) (w : W) :
    TranslationCovariant T (Y w) := by
  let S : Submodule ℂ W :=
    { carrier := {v | TranslationCovariant T (Y v)}
      zero_mem' := by
        change TranslationCovariant T (Y 0)
        simpa only [map_zero] using covariant_zero T
      add_mem' := by
        intro v u hv hu
        change TranslationCovariant T (Y (v+u))
        simpa only [map_add] using covariant_add hv hu
      smul_mem' := by
        intro c v hv
        change TranslationCovariant T (Y (c • v))
        simpa only [map_smul] using covariant_smul hv c }
  have hrange : Set.range basis ⊆ S := by
    rintro _ ⟨i,rfl⟩
    exact h i
  have hspan : Submodule.span ℂ (Set.range basis) ≤ S :=
    Submodule.span_le.mpr hrange
  rw [basis.span_eq] at hspan
  exact hspan Submodule.mem_top

end HMT.IV.LatticeTranslationLinear
end

#print axioms HMT.IV.LatticeTranslationLinear.covariant_zero
#print axioms HMT.IV.LatticeTranslationLinear.covariant_add
#print axioms HMT.IV.LatticeTranslationLinear.covariant_smul
#print axioms HMT.IV.LatticeTranslationLinear.covariance_linear_extension
