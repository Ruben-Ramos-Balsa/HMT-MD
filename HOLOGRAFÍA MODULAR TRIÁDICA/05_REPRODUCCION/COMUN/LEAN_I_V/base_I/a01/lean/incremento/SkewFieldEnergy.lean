import SkewFieldTransform

/-! Weight covariance of the coefficientwise finite skew transform. The
translation contribution cancels the shifted Laurent exponent. -/

noncomputable section
namespace HMT.IV.SkewFieldEnergy
open SkewFieldTransform
variable {E T : Type*} [AddCommGroup E] [Module ℂ E]
  [AddCommGroup T] [Module ℂ T]

theorem raising_power_weight (H D : Module.End ℂ T)
    (hD : ∀ t, H (D t) = D (H t) + D t)
    (v : T) (c : ℂ) (hv : H v = c • v) (n : ℕ) :
    H ((D^n) v) = (c+(n:ℂ)) • ((D^n) v) := by
  induction n with
  | zero => simpa using hv
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply, hD, ih, map_smul]
    push_cast
    module

theorem skewTerm_weight (W : E →ₗ[ℂ] VertexOperator ℂ T) (H D : Module.End ℂ T)
    (hD : ∀ t, H (D t) = D (H t) + D t) (v : T) (u : E) (c : ℂ)
    (hW : ∀ r : ℤ, H (HVertexOperator.coeff (W u) r v) =
      (c+(r:ℂ)) • HVertexOperator.coeff (W u) r v) (k : ℤ) (n : ℕ) :
    H (skewTerm W D k n v u) = (c+(k:ℂ)) • skewTerm W D k n v u := by
  simp only [skewTerm, map_smul]
  rw [raising_power_weight H D hD _ _ (hW _) n]
  have hc : c+((k-(n:ℤ):ℤ):ℂ)+(n:ℂ) = c+(k:ℂ) := by push_cast; ring
  rw [hc]
  simp only [smul_smul]
  congr 1
  ring

theorem skewAssignment_weight (W : E →ₗ[ℂ] VertexOperator ℂ T) (H D : Module.End ℂ T)
    (hD : ∀ t, H (D t) = D (H t) + D t) (v : T) (u : E) (c : ℂ)
    (hW : ∀ r : ℤ, H (HVertexOperator.coeff (W u) r v) =
      (c+(r:ℂ)) • HVertexOperator.coeff (W u) r v) (k : ℤ) :
    H (HVertexOperator.coeff (skewAssignment W D v) k u) =
      (c+(k:ℂ)) • HVertexOperator.coeff (skewAssignment W D v) k u := by
  change H (∑ᶠ n, skewTerm W D k n v u) = (c+(k:ℂ)) • ∑ᶠ n, skewTerm W D k n v u
  have hm := H.toAddMonoidHom.map_finsum (skewTerm_finite W D k v u)
  change H (∑ᶠ n, skewTerm W D k n v u) = ∑ᶠ n, H (skewTerm W D k n v u) at hm
  rw [hm]
  simp_rw [skewTerm_weight W H D hD v u c hW k]
  exact (smul_finsum _ _).symm

end HMT.IV.SkewFieldEnergy
end
