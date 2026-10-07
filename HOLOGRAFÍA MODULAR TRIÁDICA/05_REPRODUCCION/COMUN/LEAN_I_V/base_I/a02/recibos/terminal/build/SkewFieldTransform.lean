import Mathlib.Algebra.Vertex.VertexOperator
import Mathlib.Algebra.BigOperators.Finprod
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-! The heterogeneous skew field exp(zD) W(e,-z)t.
Finiteness is pointwise and follows from Laurent truncation of W(e)t.
There is no local-nilpotence assumption on D. -/

noncomputable section
namespace HMT.IV.SkewFieldTransform
open scoped BigOperators
variable {E T : Type*} [AddCommGroup E] [Module ℂ E]
  [AddCommGroup T] [Module ℂ T]

def skewTerm (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (n : ℕ) (t : T) (e : E) : T :=
  (n.factorial : ℂ)⁻¹ •
    ((D ^ n) (((-1 : ℂ) ^ (k - (n : ℤ))) •
      (HVertexOperator.coeff (W e) (k - (n : ℤ)) t)))

theorem skewTerm_add_e (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (n : ℕ) (t : T) (e f : E) :
    skewTerm W D k n t (e + f) = skewTerm W D k n t e + skewTerm W D k n t f := by
  simp only [skewTerm, map_add, HVertexOperator.coeff_add, Pi.add_apply,
    LinearMap.add_apply, smul_add]

theorem skewTerm_smul_e (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (n : ℕ) (t : T) (c : ℂ) (e : E) :
    skewTerm W D k n t (c • e) = c • skewTerm W D k n t e := by
  simp only [skewTerm, map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
    LinearMap.smul_apply, smul_smul]
  congr 1
  ring

theorem skewTerm_add_t (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (n : ℕ) (t s : T) (e : E) :
    skewTerm W D k n (t + s) e = skewTerm W D k n t e + skewTerm W D k n s e := by
  simp only [skewTerm, map_add, smul_add]

theorem skewTerm_smul_t (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (n : ℕ) (c : ℂ) (t : T) (e : E) :
    skewTerm W D k n (c • t) e = c • skewTerm W D k n t e := by
  simp only [skewTerm, map_smul, smul_smul]
  congr 1
  ring

theorem field_has_bound (W : E →ₗ[ℂ] VertexOperator ℂ T) (t : T) (e : E) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff (W e) k t = 0 := by
  refine ⟨HahnSeries.order ((HahnModule.of ℂ).symm (W e t)), ?_⟩
  intro k hk
  exact VertexOperator.coeff_eq_zero_of_lt_order (W e) k t hk

theorem skewTerm_finite (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (t : T) (e : E) :
    (Function.support (fun n : ℕ => skewTerm W D k n t e)).Finite := by
  obtain ⟨b,hb⟩ := field_has_bound W t e
  apply (Finset.range ((k - b).toNat + 1)).finite_toSet.subset
  intro n hn
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra h
  have hlt : k - (n : ℤ) < b := by omega
  exact hn (by simp only [skewTerm, hb _ hlt, smul_zero, map_zero])

def skewCoefficient (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) : T →ₗ[ℂ] E →ₗ[ℂ] T where
  toFun t :=
    { toFun := fun e => ∑ᶠ n : ℕ, skewTerm W D k n t e
      map_add' := fun e f => by
        simp only [skewTerm_add_e]
        exact finsum_add_distrib (skewTerm_finite W D k t e) (skewTerm_finite W D k t f)
      map_smul' := fun c e => by
        simp only [skewTerm_smul_e, RingHom.id_apply]
        exact (smul_finsum c (fun n => skewTerm W D k n t e)).symm }
  map_add' t s := by
    ext e
    change (∑ᶠ n : ℕ, skewTerm W D k n (t+s) e) =
      (∑ᶠ n : ℕ, skewTerm W D k n t e) + (∑ᶠ n : ℕ, skewTerm W D k n s e)
    simp only [skewTerm_add_t]
    exact finsum_add_distrib (skewTerm_finite W D k t e) (skewTerm_finite W D k s e)
  map_smul' c t := by
    ext e
    change (∑ᶠ n : ℕ, skewTerm W D k n (c • t) e) =
      c • (∑ᶠ n : ℕ, skewTerm W D k n t e)
    simp only [skewTerm_smul_t]
    exact (smul_finsum c (fun n => skewTerm W D k n t e)).symm

theorem skewCoefficient_apply (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (k : ℤ) (t : T) (e : E) :
    skewCoefficient W D k t e = ∑ᶠ n : ℕ,
      (n.factorial : ℂ)⁻¹ •
        ((D ^ n) (((-1 : ℂ) ^ (k - (n : ℤ))) •
          (HVertexOperator.coeff (W e) (k - (n : ℤ)) t))) := rfl

theorem skewCoefficient_eq_zero_of_lt_bound (W : E →ₗ[ℂ] VertexOperator ℂ T)
    (D : Module.End ℂ T) (t : T) (e : E) (b : ℤ)
    (hb : ∀ j < b, HVertexOperator.coeff (W e) j t = 0)
    (k : ℤ) (hk : k < b) : skewCoefficient W D k t e = 0 := by
  change (∑ᶠ n : ℕ, skewTerm W D k n t e) = 0
  have hz : ∀ n : ℕ, skewTerm W D k n t e = 0 := by
    intro n
    have hlt : k - (n : ℤ) < b := by omega
    simp only [skewTerm, hb _ hlt, smul_zero, map_zero]
  simp only [hz, finsum_zero]

theorem skewCoefficient_bounded (W : E →ₗ[ℂ] VertexOperator ℂ T)
    (D : Module.End ℂ T) (t : T) (e : E) :
    ∃ b : ℤ, ∀ k < b, skewCoefficient W D k t e = 0 := by
  obtain ⟨b,hb⟩ := field_has_bound W t e
  exact ⟨b, skewCoefficient_eq_zero_of_lt_bound W D t e b hb⟩

def skewField (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (t : T) : HVertexOperator ℤ ℂ E T :=
  HVertexOperator.of_coeff (fun k => skewCoefficient W D k t)
    (fun e => HahnSeries.suppBddBelow_supp_PWO (fun k => skewCoefficient W D k t e)
      (HahnSeries.forallLTEqZero_supp_BddBelow (fun k => skewCoefficient W D k t e)
        (Exists.choose (skewCoefficient_bounded W D t e))
        (Exists.choose_spec (skewCoefficient_bounded W D t e))))

theorem skewField_coefficient (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T)
    (t : T) (k : ℤ) :
    HVertexOperator.coeff (skewField W D t) k = skewCoefficient W D k t := rfl

def skewAssignment (W : E →ₗ[ℂ] VertexOperator ℂ T) (D : Module.End ℂ T) :
    T →ₗ[ℂ] HVertexOperator ℤ ℂ E T where
  toFun := skewField W D
  map_add' t s := by
    apply HVertexOperator.coeff_inj
    funext k
    rw [HVertexOperator.coeff_add]
    change skewCoefficient W D k (t+s) = skewCoefficient W D k t + skewCoefficient W D k s
    exact map_add _ _ _
  map_smul' c t := by
    apply HVertexOperator.coeff_inj
    funext k
    rw [HVertexOperator.coeff_smul]
    change skewCoefficient W D k (c • t) = c • skewCoefficient W D k t
    exact map_smul _ _ _

theorem skewAssignment_coefficient (W : E →ₗ[ℂ] VertexOperator ℂ T)
    (D : Module.End ℂ T) (t : T) (k : ℤ) :
    HVertexOperator.coeff (skewAssignment W D t) k = skewCoefficient W D k t := rfl

theorem skewAssignment_coefficient_apply (W : E →ₗ[ℂ] VertexOperator ℂ T)
    (D : Module.End ℂ T) (t : T) (e : E) (k : ℤ) :
    HVertexOperator.coeff (skewAssignment W D t) k e = ∑ᶠ n : ℕ,
      (n.factorial : ℂ)⁻¹ •
        ((D ^ n) (((-1 : ℂ) ^ (k - (n : ℤ))) •
          (HVertexOperator.coeff (W e) (k - (n : ℤ)) t))) := rfl

end HMT.IV.SkewFieldTransform
end

#print axioms HMT.IV.SkewFieldTransform.skewTerm_finite
#print axioms HMT.IV.SkewFieldTransform.skewCoefficient
#print axioms HMT.IV.SkewFieldTransform.skewCoefficient_bounded
#print axioms HMT.IV.SkewFieldTransform.skewAssignment
#print axioms HMT.IV.SkewFieldTransform.skewAssignment_coefficient_apply
