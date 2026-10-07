import PeriodicAnnulus
import LatticeOrigin
import LatticeSummabilityTail

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.ThermodynamicLimit

def meshLatticeSum (F : ℝ → ℝ) (Δ : ℝ) : ℝ :=
  Δ^3 * ∑' ν : Lattice, excitationValue F Δ ν

def meshAnnularSum (F : ℝ → ℝ) (Δ δ R : ℝ) : ℝ :=
  Δ^3 * ∑' ν : Lattice, annularValue F Δ δ R ν

theorem annular_remainder_pointwise {F : ℝ → ℝ} {Δ δ R : ℝ}
    (hΔ : 0 < Δ) (hF : ∀ r, 0 < r → 0 ≤ F r) (ν : Lattice) :
    0 ≤ excitationValue F Δ ν - annularValue F Δ δ R ν ∧
      excitationValue F Δ ν - annularValue F Δ δ R ν ≤
        originSummand F Δ (Real.sqrt 3 * δ) ν + latticeTailValue F Δ R ν := by
  have he := excitationValue_nonneg hΔ hF ν
  have ho : 0 ≤ originSummand F Δ (Real.sqrt 3 * δ) ν := by
    unfold originSummand
    split_ifs with h
    · exact hF _ h.1
    · rfl
  have ht := latticeTailValue_nonneg hΔ hF R ν
  by_cases hν : ν = 0
  · have hezero : excitationValue F Δ ν = 0 := by simp [hν, excitationValue]
    have hazero : annularValue F Δ δ R ν = 0 := by
      rw [annularValue_apply]
      split_ifs <;> simp only [hezero]
    rw [hezero, hazero, sub_self]
    exact ⟨le_rfl, add_nonneg ho ht⟩
  have hp : 0 < Δ * radius ν := mul_pos hΔ ((radius_pos_iff ν).2 hν)
  by_cases ha : δ ≤ Δ * (supRadius ν : ℝ) ∧ Δ * (supRadius ν : ℝ) ≤ R
  · simp only [annularValue_apply, if_pos ha, sub_self, le_refl, true_and]
    exact add_nonneg ho ht
  have hzero : annularValue F Δ δ R ν = 0 := by simp [annularValue_apply, ha]
  rw [hzero, sub_zero]
  refine ⟨he, ?_⟩
  by_cases hlo : δ ≤ Δ * (supRadius ν : ℝ)
  · have hout : R < Δ * (supRadius ν : ℝ) := lt_of_not_ge (fun h => ha ⟨hlo, h⟩)
    have hr : R < Δ * radius ν := hout.trans_le
      (mul_le_mul_of_nonneg_left (supRadius_le_radius ν) hΔ.le)
    rw [latticeTailValue, if_pos hr]
    linarith
  · have hsmall : Δ * radius ν ≤ Real.sqrt 3 * δ := by
      have hb := mul_le_mul_of_nonneg_left (radius_le_sqrt_three_supRadius ν) hΔ.le
      have hs := mul_le_mul_of_nonneg_left (le_of_lt (lt_of_not_ge hlo)) (Real.sqrt_nonneg 3)
      nlinarith
    rw [originSummand, if_pos ⟨hp, hsmall⟩, excitationValue, if_neg hν]
    linarith

theorem annular_remainder_bound {F : ℝ → ℝ} {Δ δ R C₀ C₁ d : ℝ}
    (hΔ : 0 < Δ) (hΔ1 : Δ ≤ 1) (hδ : 0 < δ)
    (hδ1 : Real.sqrt 3 * δ ≤ 1) (hR : 1 ≤ R)
    (hC₀ : 0 ≤ C₀) (hC₁ : 0 ≤ C₁) (hd : 0 < d)
    (hF : ∀ r, 0 < r → 0 ≤ F r)
    (horigin : ∀ r, 0 < r → r ≤ 1 → F r ≤ C₀ / r)
    (htail : ∀ r, 1 ≤ r → F r ≤ C₁ * Real.exp (-(d*r)))
    (hsum : Summable (excitationValue F Δ)) :
    |meshLatticeSum F Δ - meshAnnularSum F Δ δ R| ≤
      78 * C₀ * δ^2 + C₁ * shellUniformConstant (d/2) *
        Real.exp (-d*R/(2*Real.sqrt 3)) := by
  have hsA : Summable (annularValue F Δ δ R) := annularValue_summable hsum δ R
  have hsO := (origin_hasSum F (δ := Real.sqrt 3 * δ) hΔ).summable
  have hsT := lattice_tail_summable hC₁ hd hΔ hR hF htail
  have hsG := hsum.sub hsA
  have hge : (0 : ℝ) ≤ ∑' ν, (excitationValue F Δ ν - annularValue F Δ δ R ν) :=
    tsum_nonneg (fun ν => (annular_remainder_pointwise hΔ hF ν).1)
  have hle := hsG.tsum_le_tsum (fun ν => (annular_remainder_pointwise hΔ hF ν).2)
    (hsO.add hsT)
  rw [hsO.tsum_add hsT] at hle
  have heq : meshLatticeSum F Δ - meshAnnularSum F Δ δ R =
      Δ^3 * ∑' ν, (excitationValue F Δ ν - annularValue F Δ δ R ν) := by
    rw [hsum.tsum_sub hsA]
    unfold meshLatticeSum meshAnnularSum
    ring
  rw [heq, abs_of_nonneg (mul_nonneg (pow_nonneg hΔ.le _) hge)]
  have hO := origin_tsum_bound F hΔ
    (mul_pos (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 3)) hδ) hδ1 hC₀ horigin
  have hT := lattice_tail_uniform hC₁ hd hΔ hΔ1 hR hF htail
  have hsqrt : Real.sqrt 3 ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  have hO' : Δ^3 * ∑' ν, originSummand F Δ (Real.sqrt 3 * δ) ν ≤ 78*C₀*δ^2 := by
    calc
      _ ≤ 26 * C₀ * (Real.sqrt 3 * δ)^2 := hO
      _ = _ := by rw [mul_pow, hsqrt]; ring
  calc
    _ ≤ Δ^3 * ((∑' ν, originSummand F Δ (Real.sqrt 3 * δ) ν) +
        ∑' ν, latticeTailValue F Δ R ν) := mul_le_mul_of_nonneg_left hle (pow_nonneg hΔ.le _)
    _ ≤ _ := by rw [mul_add]; exact add_le_add hO' hT

#print axioms annular_remainder_pointwise
#print axioms annular_remainder_bound

end HMT.V.ThermodynamicLimit
