import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.Projection
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.Tactic

/-! The two real screens of Article IV.  The arithmetic construction of the
direction is supplied by the separate concrete K module, not postulated here. -/
noncomputable section
namespace HMT.IV.OrthogonalKScreen

open scoped InnerProductSpace
open Module

abbrev E := EuclideanSpace ℝ (Fin 12)
def ones : E := WithLp.toLp 2 (fun _ => 1)
def V11 : Submodule ℝ E := (ℝ ∙ ones)ᗮ
def V10 (u : E) : Submodule ℝ E := (ℝ ∙ u)ᗮ ⊓ V11

theorem ones_ne_zero : ones ≠ 0 := by
  intro h
  have := congrArg (fun x : E => x 0) h
  norm_num [ones] at this

theorem ones_norm_sq : ‖ones‖ ^ 2 = 12 := by
  rw [← real_inner_self_eq_norm_sq]
  simp [EuclideanSpace.inner_eq_star_dotProduct, dotProduct, ones]

def P11 : E →ₗ[ℝ] E :=
  V11.subtype.comp V11.orthogonalProjection.toLinearMap

def rankOne (u : E) : E →ₗ[ℝ] E :=
  (ℝ ∙ u).subtype.comp (ℝ ∙ u).orthogonalProjection.toLinearMap

def P10 (u : E) : E →ₗ[ℝ] E := P11 - rankOne u

theorem P11_formula (v : E) :
    P11 v = v - (⟪ones, v⟫_ℝ / 12) • ones := by
  change (V11.orthogonalProjection v : E) = _
  rw [V11, Submodule.orthogonalProjection_orthogonal_val,
    Submodule.orthogonalProjection_singleton, ones_norm_sq]
  norm_num

theorem P11_coordinates (v : E) (i : Fin 12) :
    P11 v i = v i - (∑ j, v j) / 12 := by
  rw [P11_formula]
  simp [EuclideanSpace.inner_eq_star_dotProduct, dotProduct, ones]

theorem rankOne_formula (u v : E) :
    rankOne u v = (⟪u, v⟫_ℝ / ‖u‖ ^ 2) • u := by
  exact Submodule.orthogonalProjection_singleton ℝ v

theorem P10_formula (u v : E) :
    P10 u v = P11 v - (⟪u, v⟫_ℝ / ‖u‖ ^ 2) • u := by
  simp only [P10, LinearMap.sub_apply, rankOne_formula]

theorem P10_coordinates (u v : E) (i : Fin 12) :
    P10 u v i = v i - (∑ j, v j) / 12 -
      ((∑ j, u j * v j) / ‖u‖ ^ 2) * u i := by
  rw [P10_formula]
  simp [P11_coordinates, EuclideanSpace.inner_eq_star_dotProduct, dotProduct, mul_comm]

theorem P11_mem (v : E) : P11 v ∈ V11 :=
  (V11.orthogonalProjection v).property

theorem P11_self {v : E} (h : v ∈ V11) : P11 v = v :=
  Submodule.orthogonalProjection_eq_self_iff.mpr h

theorem P11_idempotent (v : E) : P11 (P11 v) = P11 v :=
  P11_self (P11_mem v)

theorem rankOne_mem (u v : E) : rankOne u v ∈ ℝ ∙ u :=
  ((ℝ ∙ u).orthogonalProjection v).property

theorem rankOne_self (u : E) : rankOne u u = u :=
  Submodule.orthogonalProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self u)

theorem rankOne_idempotent (u v : E) : rankOne u (rankOne u v) = rankOne u v :=
  Submodule.orthogonalProjection_eq_self_iff.mpr (rankOne_mem u v)

theorem P11_rankOne {u : E} (hu : u ∈ V11) (v : E) :
    P11 (rankOne u v) = rankOne u v := by
  apply P11_self
  exact ((Submodule.span_singleton_le_iff_mem u V11).mpr hu) (rankOne_mem u v)

theorem rankOne_P11 {u : E} (hu : u ∈ V11) (v : E) :
    rankOne u (P11 v) = rankOne u v := by
  have h : ⟪u, ones⟫_ℝ = 0 :=
    Submodule.mem_orthogonal_singleton_iff_inner_left.mp hu
  simp only [rankOne_formula, P11_formula, inner_sub_right, inner_smul_right, h,
    mul_zero, sub_zero]

theorem P10_P11 {u : E} (hu : u ∈ V11) (v : E) :
    P10 u (P11 v) = P10 u v := by
  simp only [P10, LinearMap.sub_apply, P11_idempotent, rankOne_P11 hu]

theorem P10_idempotent {u : E} (hu : u ∈ V11) (v : E) :
    P10 u (P10 u v) = P10 u v := by
  simp only [P10, LinearMap.sub_apply, map_sub, P11_idempotent,
    P11_rankOne hu, rankOne_P11 hu, rankOne_idempotent, sub_self, sub_zero]

theorem P10_kills_u {u : E} (hu : u ∈ V11) : P10 u u = 0 := by
  simp only [P10, LinearMap.sub_apply, P11_self hu, rankOne_self, sub_self]

theorem P11_kills_ones : P11 ones = 0 := by
  rw [P11_formula, real_inner_self_eq_norm_sq, ones_norm_sq]
  norm_num

theorem P10_kills_ones {u : E} (hu : u ∈ V11) : P10 u ones = 0 := by
  have h : ⟪u, ones⟫_ℝ = 0 :=
    Submodule.mem_orthogonal_singleton_iff_inner_left.mp hu
  simp [P10, P11_kills_ones, rankOne_formula, h]

theorem finrank_V11 : finrank ℝ V11 = 11 := by
  have h := Submodule.finrank_add_finrank_orthogonal (ℝ ∙ ones)
  simp only [finrank_span_singleton ones_ne_zero, finrank_euclideanSpace,
    Fintype.card_fin] at h
  change 1 + finrank ℝ V11 = 12 at h
  omega

theorem finrank_V10 {u : E} (hu : u ∈ V11) (hne : u ≠ 0) :
    finrank ℝ (V10 u) = 10 := by
  have h := Submodule.finrank_add_inf_finrank_orthogonal
    ((Submodule.span_singleton_le_iff_mem u V11).mpr hu)
  rw [finrank_span_singleton hne, finrank_V11] at h
  change 1 + finrank ℝ (V10 u) = 11 at h
  omega

theorem P10_mem {u : E} (hu : u ∈ V11) (v : E) : P10 u v ∈ V10 u := by
  constructor
  · apply Submodule.orthogonalProjection_eq_zero_iff.mp
    apply Subtype.ext
    change rankOne u (P10 u v) = 0
    simp only [P10, LinearMap.sub_apply, map_sub, rankOne_P11 hu,
      rankOne_idempotent, sub_self]
  · exact V11.sub_mem (P11_mem v)
      (((Submodule.span_singleton_le_iff_mem u V11).mpr hu) (rankOne_mem u v))

theorem P10_self {u v : E} (hv : v ∈ V10 u) : P10 u v = v := by
  have h : rankOne u v = 0 := by
    have hz := Submodule.orthogonalProjection_eq_zero_iff.mpr hv.1
    exact congrArg (fun x : ℝ ∙ u => (x : E)) hz
  simp only [P10, LinearMap.sub_apply, P11_self hv.2, h, sub_zero]

theorem P10_range {u : E} (hu : u ∈ V11) : LinearMap.range (P10 u) = V10 u := by
  ext v
  constructor
  · rintro ⟨x, rfl⟩
    exact P10_mem hu x
  · intro hv
    exact ⟨v, P10_self hv⟩

theorem P10_rank {u : E} (hu : u ∈ V11) (hne : u ≠ 0) :
    finrank ℝ (LinearMap.range (P10 u)) = 10 := by
  rw [P10_range hu]
  exact finrank_V10 hu hne

theorem P10_symmetric (u v w : E) : ⟪P10 u v, w⟫_ℝ = ⟪v, P10 u w⟫_ℝ := by
  simp only [P10, LinearMap.sub_apply, inner_sub_left, inner_sub_right]
  rw [show ⟪P11 v, w⟫_ℝ = ⟪v, P11 w⟫_ℝ from
    Submodule.inner_orthogonalProjection_left_eq_right V11 v w]
  rw [show ⟪rankOne u v, w⟫_ℝ = ⟪v, rankOne u w⟫_ℝ from
    Submodule.inner_orthogonalProjection_left_eq_right (ℝ ∙ u) v w]

theorem P10_orthogonal_projection {u : E} (hu : u ∈ V11) (v : E) :
    ((V10 u).orthogonalProjection v : E) = P10 u v := by
  apply Submodule.eq_orthogonalProjection_of_mem_of_inner_eq_zero (P10_mem hu v)
  intro w hw
  rw [inner_sub_left, P10_symmetric, P10_self hw, sub_self]

theorem orthogonal_reductions {u : E} (hu : u ∈ V11) :
    IsCompl (ℝ ∙ ones) V11 ∧
    Disjoint (ℝ ∙ u) (V10 u) ∧ (ℝ ∙ u) ⊔ V10 u = V11 := by
  refine ⟨Submodule.isCompl_orthogonal_of_completeSpace, ?_, ?_⟩
  · exact (Submodule.orthogonal_disjoint (ℝ ∙ u)).mono_right inf_le_left
  · exact Submodule.sup_orthogonal_inf_of_completeSpace
      ((Submodule.span_singleton_le_iff_mem u V11).mpr hu)

abbrev UniformQuotient := E ⧸ (ℝ ∙ ones)

def uniformQuotientEquiv : UniformQuotient ≃ₗ[ℝ] V11 :=
  Submodule.quotientEquivOfIsCompl (ℝ ∙ ones) V11
    Submodule.isCompl_orthogonal_of_completeSpace

theorem uniformQuotientEquiv_apply (v : E) :
    (uniformQuotientEquiv (Submodule.Quotient.mk v) : E) = P11 v := by
  have h : uniformQuotientEquiv (Submodule.Quotient.mk v) =
      V11.orthogonalProjection v := by
    apply uniformQuotientEquiv.symm.injective
    simp only [LinearEquiv.symm_apply_apply]
    change (Submodule.Quotient.mk v : UniformQuotient) =
      Submodule.Quotient.mk (P11 v)
    apply (Submodule.Quotient.eq (ℝ ∙ ones)).mpr
    rw [P11_formula, sub_sub_cancel]
    exact Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self ones)
  exact congrArg (fun x : V11 => (x : E)) h

def graphMap (u : E) : V11 →ₗ[ℝ] E × E :=
  V11.subtype.prod ((P10 u).comp V11.subtype)

def Graph (u : E) : Submodule ℝ (E × E) := LinearMap.range (graphMap u)

theorem graphMap_injective (u : E) : Function.Injective (graphMap u) := by
  intro v w h
  exact Subtype.ext (congrArg Prod.fst h)

def graphEquiv (u : E) : V11 ≃ₗ[ℝ] Graph u :=
  LinearEquiv.ofInjective (graphMap u) (graphMap_injective u)

def realScreenEquiv (u : E) : UniformQuotient ≃ₗ[ℝ] Graph u :=
  uniformQuotientEquiv.trans (graphEquiv u)

theorem realScreenEquiv_formula {u : E} (hu : u ∈ V11) (v : E) :
    (realScreenEquiv u (Submodule.Quotient.mk v) : E × E) = (P11 v, P10 u v) := by
  change (graphMap u (uniformQuotientEquiv (Submodule.Quotient.mk v))) = _
  change ((uniformQuotientEquiv (Submodule.Quotient.mk v) : E),
    P10 u (uniformQuotientEquiv (Submodule.Quotient.mk v) : E)) = _
  rw [uniformQuotientEquiv_apply, P10_P11 hu]

theorem graph_mem_iff (u : E) (p : E × E) :
    p ∈ Graph u ↔ p.1 ∈ V11 ∧ p.2 = P10 u p.1 := by
  constructor
  · rintro ⟨v, rfl⟩
    exact ⟨v.property, rfl⟩
  · rintro ⟨h, hp⟩
    refine ⟨⟨p.1, h⟩, ?_⟩
    exact Prod.ext rfl hp.symm

theorem graph_finrank (u : E) : finrank ℝ (Graph u) = 11 :=
  (graphEquiv u).finrank_eq.symm.trans finrank_V11

theorem P10_scale_invariant (u v : E) {c : ℝ} (hc : c ≠ 0) :
    P10 (c • u) v = P10 u v := by
  have h : rankOne (c • u) v = rankOne u v :=
    Submodule.eq_orthogonalProjection_of_eq_submodule
      (Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr hc) u) v
  simp only [P10, LinearMap.sub_apply, h]

theorem P11_covariant (S : E ≃ₗᵢ[ℝ] E) (hS : S ones = ones) (v : E) :
    P11 (S v) = S (P11 v) := by
  have h : ⟪ones, S v⟫_ℝ = ⟪ones, v⟫_ℝ := by
    calc
      ⟪ones, S v⟫_ℝ = ⟪S ones, S v⟫_ℝ := by rw [hS]
      _ = ⟪ones, v⟫_ℝ := S.inner_map_map ones v
  simp only [P11_formula, map_sub, map_smul, h, hS]

theorem P10_covariant (S : E ≃ₗᵢ[ℝ] E) (hS : S ones = ones) (u v : E) :
    P10 (S u) (S v) = S (P10 u v) := by
  simp only [P10_formula, P11_covariant S hS, S.inner_map_map, S.norm_map,
    map_sub, map_smul]

end HMT.IV.OrthogonalKScreen
end

#print axioms HMT.IV.OrthogonalKScreen.P10_rank
#print axioms HMT.IV.OrthogonalKScreen.P10_orthogonal_projection
#print axioms HMT.IV.OrthogonalKScreen.realScreenEquiv_formula
#print axioms HMT.IV.OrthogonalKScreen.P10_covariant
