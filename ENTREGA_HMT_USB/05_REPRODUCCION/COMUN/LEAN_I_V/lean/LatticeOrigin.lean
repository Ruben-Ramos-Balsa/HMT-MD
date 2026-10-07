import LatticeShells

/-! Uniform origin control from the proved cardinalities of actual ℤ³ shells.
The hypotheses only bound the scalar observable by C₀/r; the lattice estimate
and its constant 26 are conclusions. -/
namespace HMT.V.ThermodynamicLimit
noncomputable section
open Finset

theorem shell_sum_bound (s : Finset Lattice) (N : ℕ) (g : Lattice → ℝ) (b : ℕ → ℝ)
    (hs : ∀ ν ∈ s, ν ≠ 0 ∧ supRadius ν ≤ N)
    (hb : ∀ m ∈ Finset.Icc 1 N, 0 ≤ b m)
    (hg : ∀ ν ∈ s, g ν ≤ b (supRadius ν)) :
    ∑ ν ∈ s, g ν ≤ ∑ m ∈ Finset.Icc 1 N, (24 * (m : ℝ) ^ 2 + 2) * b m := by
  have hm : ∀ ν ∈ s, supRadius ν ∈ Finset.Icc 1 N := by
    intro ν hν
    have h := hs ν hν
    exact Finset.mem_Icc.2 ⟨Nat.pos_of_ne_zero (fun hz => h.1 ((supRadius_zero_iff ν).1 hz)), h.2⟩
  rw [← Finset.sum_fiberwise_of_maps_to hm g]
  apply Finset.sum_le_sum
  intro m hm
  have hsub : {ν ∈ s | supRadius ν = m} ⊆ shell m := by
    intro ν hν
    exact mem_shell.2 (Finset.mem_filter.1 hν).2
  calc
    ∑ ν ∈ s with supRadius ν = m, g ν ≤ ∑ _ν ∈ s with supRadius _ν = m, b m := by
      apply Finset.sum_le_sum
      intro ν hν
      simpa only [(Finset.mem_filter.1 hν).2] using hg ν (Finset.mem_filter.1 hν).1
    _ = ({ν ∈ s | supRadius ν = m}.card : ℝ) * b m := by simp
    _ ≤ ((shell m).card : ℝ) * b m :=
      mul_le_mul_of_nonneg_right (by exact_mod_cast Finset.card_le_card hsub) (hb m hm)
    _ = (24 * (m : ℝ) ^ 2 + 2) * b m := by
      rw [card_shell (Finset.mem_Icc.1 hm).1]
      push_cast
      rfl

def originPoints (Δ δ : ℝ) : Finset Lattice :=
  (cube ⌊δ / Δ⌋₊).filter (fun ν => 0 < Δ * radius ν ∧ Δ * radius ν ≤ δ)

theorem mem_originPoints {Δ δ : ℝ} (hΔ : 0 < Δ) {ν : Lattice} :
    ν ∈ originPoints Δ δ ↔ 0 < Δ * radius ν ∧ Δ * radius ν ≤ δ := by
  simp only [originPoints, Finset.mem_filter]
  constructor
  · exact fun h => h.2
  · intro h
    refine ⟨mem_cube.2 (Nat.le_floor ?_), h⟩
    apply (le_div_iff₀ hΔ).2
    calc
      (supRadius ν : ℝ) * Δ ≤ radius ν * Δ := mul_le_mul_of_nonneg_right (supRadius_le_radius ν) hΔ.le
      _ ≤ δ := by simpa only [mul_comm] using h.2

theorem originPoints_empty {Δ δ : ℝ} (hΔ : 0 < Δ) (hδΔ : δ < Δ) :
    originPoints Δ δ = ∅ := by
  apply Finset.eq_empty_iff_forall_notMem.2
  intro ν hν
  have h := (mem_originPoints hΔ).1 hν
  have hp : 0 < radius ν := (mul_pos_iff_of_pos_left hΔ).1 h.1
  have hz := (radius_pos_iff ν).1 hp
  have hs : 1 ≤ supRadius ν := Nat.pos_of_ne_zero (fun he => hz ((supRadius_zero_iff ν).1 he))
  have hs' : (1 : ℝ) ≤ supRadius ν := by exact_mod_cast hs
  have hr := hs'.trans (supRadius_le_radius ν)
  nlinarith

theorem sum_layer_indices_le_square (N : ℕ) :
    ∑ m ∈ Finset.Icc 1 N, (m : ℝ) ≤ (N : ℝ) ^ 2 := by
  calc
    _ ≤ ∑ _m ∈ Finset.Icc 1 N, (N : ℝ) := by
      apply Finset.sum_le_sum
      intro m hm
      exact_mod_cast (Finset.mem_Icc.1 hm).2
    _ = (N : ℝ) ^ 2 := by simp [pow_two]

theorem shell_reciprocal_bound {m : ℕ} (hm : 1 ≤ m) {Δ C₀ : ℝ}
    (hΔ : 0 < Δ) (hC : 0 ≤ C₀) :
    (24 * (m : ℝ) ^ 2 + 2) * (C₀ / (Δ * m)) ≤ (26 * C₀ / Δ) * m := by
  have hm' : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hmp : (0 : ℝ) < m := lt_of_lt_of_le zero_lt_one hm'
  calc
    (24 * (m : ℝ) ^ 2 + 2) * (C₀ / (Δ * m)) =
        ((24 * (m : ℝ) ^ 2 + 2) * C₀) / (Δ * m) := by ring
    _ ≤ (26 * (m : ℝ) ^ 2 * C₀) / (Δ * m) := by
      apply div_le_div_of_nonneg_right _ (mul_pos hΔ hmp).le
      apply mul_le_mul_of_nonneg_right _ hC
      nlinarith
    _ = (26 * C₀ / Δ) * m := by field_simp; ring

theorem origin_sum_bound (F : ℝ → ℝ) {Δ δ C₀ : ℝ}
    (hΔ : 0 < Δ) (hδ : 0 < δ) (hδ1 : δ ≤ 1) (hC : 0 ≤ C₀)
    (hF : ∀ r : ℝ, 0 < r → r ≤ 1 → F r ≤ C₀ / r) :
    Δ ^ 3 * ∑ ν ∈ originPoints Δ δ, F (Δ * radius ν) ≤ 26 * C₀ * δ ^ 2 := by
  let N := ⌊δ / Δ⌋₊
  have hs : ∀ ν ∈ originPoints Δ δ, ν ≠ 0 ∧ supRadius ν ≤ N := by
    intro ν hν
    have hr := (mem_originPoints hΔ).1 hν
    refine ⟨(radius_pos_iff ν).1 ((mul_pos_iff_of_pos_left hΔ).1 hr.1), ?_⟩
    exact mem_cube.1 (Finset.mem_filter.1 hν).1
  have hb : ∀ m ∈ Finset.Icc 1 N, 0 ≤ C₀ / (Δ * m) := by
    intro m _
    exact div_nonneg hC (mul_nonneg hΔ.le (Nat.cast_nonneg _))
  have hg : ∀ ν ∈ originPoints Δ δ, F (Δ * radius ν) ≤ C₀ / (Δ * supRadius ν) := by
    intro ν hν
    have hr := (mem_originPoints hΔ).1 hν
    have hm : 0 < supRadius ν := Nat.pos_of_ne_zero (fun hz => (hs ν hν).1 ((supRadius_zero_iff ν).1 hz))
    have hmp : (0 : ℝ) < supRadius ν := by exact_mod_cast hm
    calc
      F (Δ * radius ν) ≤ C₀ / (Δ * radius ν) := hF _ hr.1 (hr.2.trans hδ1)
      _ ≤ C₀ / (Δ * supRadius ν) :=
        div_le_div_of_nonneg_left hC (mul_pos hΔ hmp)
          (mul_le_mul_of_nonneg_left (supRadius_le_radius ν) hΔ.le)
  have hsum := shell_sum_bound (originPoints Δ δ) N (fun ν => F (Δ * radius ν))
    (fun m => C₀ / (Δ * m)) hs hb hg
  have hsum' : ∑ ν ∈ originPoints Δ δ, F (Δ * radius ν) ≤ (26 * C₀ / Δ) * (N : ℝ) ^ 2 := by
    calc
      _ ≤ ∑ m ∈ Finset.Icc 1 N, (24 * (m : ℝ) ^ 2 + 2) * (C₀ / (Δ * m)) := hsum
      _ ≤ ∑ m ∈ Finset.Icc 1 N, (26 * C₀ / Δ) * m := by
        apply Finset.sum_le_sum
        intro m hm
        exact shell_reciprocal_bound (Finset.mem_Icc.1 hm).1 hΔ hC
      _ = (26 * C₀ / Δ) * ∑ m ∈ Finset.Icc 1 N, (m : ℝ) := by rw [Finset.mul_sum]
      _ ≤ (26 * C₀ / Δ) * (N : ℝ) ^ 2 :=
        mul_le_mul_of_nonneg_left (sum_layer_indices_le_square N) (by positivity)
  have hN : Δ * (N : ℝ) ≤ δ := by
    have hfloor : (N : ℝ) ≤ δ / Δ := Nat.floor_le (div_nonneg hδ.le hΔ.le)
    simpa only [mul_comm] using (le_div_iff₀ hΔ).1 hfloor
  calc
    _ ≤ Δ ^ 3 * ((26 * C₀ / Δ) * (N : ℝ) ^ 2) := mul_le_mul_of_nonneg_left hsum' (by positivity)
    _ = 26 * C₀ * (Δ * (N : ℝ)) ^ 2 := by field_simp; ring
    _ ≤ 26 * C₀ * δ ^ 2 :=
      mul_le_mul_of_nonneg_left (sq_le_sq₀ (by positivity) hδ.le |>.2 hN) (by positivity)

def originSummand (F : ℝ → ℝ) (Δ δ : ℝ) (ν : Lattice) : ℝ :=
  if 0 < Δ * radius ν ∧ Δ * radius ν ≤ δ then F (Δ * radius ν) else 0

theorem origin_hasSum (F : ℝ → ℝ) {Δ δ : ℝ} (hΔ : 0 < Δ) :
    HasSum (originSummand F Δ δ) (∑ ν ∈ originPoints Δ δ, F (Δ * radius ν)) := by
  have h : HasSum (originSummand F Δ δ)
      (∑ ν ∈ originPoints Δ δ, originSummand F Δ δ ν) :=
    hasSum_sum_of_ne_finset_zero (fun ν hν => by
      have hn : ¬(0 < Δ * radius ν ∧ Δ * radius ν ≤ δ) :=
        fun hp => hν ((mem_originPoints hΔ).2 hp)
      simp [originSummand, hn])
  convert h using 1
  apply Finset.sum_congr rfl
  intro ν hν
  simp [originSummand, (mem_originPoints hΔ).1 hν]

theorem origin_tsum_bound (F : ℝ → ℝ) {Δ δ C₀ : ℝ}
    (hΔ : 0 < Δ) (hδ : 0 < δ) (hδ1 : δ ≤ 1) (hC : 0 ≤ C₀)
    (hF : ∀ r : ℝ, 0 < r → r ≤ 1 → F r ≤ C₀ / r) :
    Δ ^ 3 * ∑' ν : Lattice, originSummand F Δ δ ν ≤ 26 * C₀ * δ ^ 2 := by
  rw [(origin_hasSum F hΔ).tsum_eq]
  exact origin_sum_bound F hΔ hδ hδ1 hC hF

def originDomain (Δ δ : ℝ) : Set Lattice := {ν | ν ≠ 0 ∧ Δ * radius ν ≤ δ}

theorem originDomain_indicator (F : ℝ → ℝ) {Δ δ : ℝ} (hΔ : 0 < Δ) :
    (originDomain Δ δ).indicator (fun ν => F (Δ * radius ν)) = originSummand F Δ δ := by
  funext ν
  have hp : ν ≠ 0 ↔ 0 < Δ * radius ν := by
    rw [mul_pos_iff_of_pos_left hΔ, radius_pos_iff]
  simp only [originDomain, Set.indicator, Set.mem_setOf_eq, originSummand, hp]

theorem origin_subtype_hasSum (F : ℝ → ℝ) {Δ δ : ℝ} (hΔ : 0 < Δ) :
    HasSum (fun ν : originDomain Δ δ => F (Δ * radius ν))
      (∑ ν ∈ originPoints Δ δ, F (Δ * radius ν)) := by
  apply (hasSum_subtype_iff_indicator (s := originDomain Δ δ)
    (f := fun ν : Lattice => F (Δ * radius ν))).2
  rw [originDomain_indicator F hΔ]
  exact origin_hasSum F hΔ

theorem origin_subtype_tsum_bound (F : ℝ → ℝ) {Δ δ C₀ : ℝ}
    (hΔ : 0 < Δ) (hδ : 0 < δ) (hδ1 : δ ≤ 1) (hC : 0 ≤ C₀)
    (hF : ∀ r : ℝ, 0 < r → r ≤ 1 → F r ≤ C₀ / r) :
    Δ ^ 3 * ∑' ν : originDomain Δ δ, F (Δ * radius ν) ≤ 26 * C₀ * δ ^ 2 := by
  rw [(origin_subtype_hasSum F hΔ).tsum_eq]
  exact origin_sum_bound F hΔ hδ hδ1 hC hF

def cubeOriginDomain (Δ δ : ℝ) : Set Lattice :=
  {ν | ν ≠ 0 ∧ Δ * (supRadius ν : ℝ) < δ}

theorem cubeOrigin_subset_origin {Δ δ : ℝ} (hΔ : 0 < Δ) :
    cubeOriginDomain Δ δ ⊆ originDomain Δ (Real.sqrt 3 * δ) := by
  intro ν hν
  refine ⟨hν.1, ?_⟩
  calc
    Δ * radius ν ≤ Δ * (Real.sqrt 3 * (supRadius ν : ℝ)) :=
      mul_le_mul_of_nonneg_left (radius_le_sqrt_three_supRadius ν) hΔ.le
    _ = Real.sqrt 3 * (Δ * (supRadius ν : ℝ)) := by ring
    _ ≤ Real.sqrt 3 * δ := mul_le_mul_of_nonneg_left hν.2.le (Real.sqrt_nonneg _)

theorem cubeOrigin_summable (F : ℝ → ℝ) {Δ δ : ℝ} (hΔ : 0 < Δ) :
    Summable (fun ν : cubeOriginDomain Δ δ => F (Δ * radius ν)) := by
  have hsub := cubeOrigin_subset_origin (δ := δ) hΔ
  have h : Summable (fun ν : originDomain Δ (Real.sqrt 3 * δ) => F (Δ * radius ν)) :=
    (origin_subtype_hasSum F hΔ).summable
  exact h.comp_injective (i := Set.inclusion hsub) (Set.inclusion_injective hsub)

theorem cube_origin_tsum_bound (F : ℝ → ℝ) {Δ δ C₀ : ℝ}
    (hΔ : 0 < Δ) (hδ : 0 < δ) (hδ1 : Real.sqrt 3 * δ ≤ 1) (hC : 0 ≤ C₀)
    (hF0 : ∀ r : ℝ, 0 < r → 0 ≤ F r)
    (hF : ∀ r : ℝ, 0 < r → r ≤ 1 → F r ≤ C₀ / r) :
    Δ ^ 3 * ∑' ν : cubeOriginDomain Δ δ, F (Δ * radius ν) ≤ 78 * C₀ * δ ^ 2 := by
  have hsub := cubeOrigin_subset_origin (δ := δ) hΔ
  have hsum : (∑' ν : cubeOriginDomain Δ δ, F (Δ * radius ν)) ≤
      ∑' ν : originDomain Δ (Real.sqrt 3 * δ), F (Δ * radius ν) := by
    apply Summable.tsum_le_tsum_of_inj (Set.inclusion hsub) (Set.inclusion_injective hsub)
    · intro ν _
      exact hF0 _ (mul_pos hΔ ((radius_pos_iff ν).2 ν.property.1))
    · intro ν
      exact le_rfl
    · exact cubeOrigin_summable F hΔ
    · exact (origin_subtype_hasSum F hΔ).summable
  calc
    _ ≤ Δ ^ 3 * ∑' ν : originDomain Δ (Real.sqrt 3 * δ), F (Δ * radius ν) :=
      mul_le_mul_of_nonneg_left hsum (by positivity)
    _ ≤ 26 * C₀ * (Real.sqrt 3 * δ) ^ 2 :=
      origin_subtype_tsum_bound F hΔ (mul_pos (Real.sqrt_pos.2 (by norm_num)) hδ) hδ1 hC hF
    _ = 78 * C₀ * δ ^ 2 := by rw [mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]; ring

#print axioms shell_sum_bound
#print axioms mem_originPoints
#print axioms originPoints_empty
#print axioms sum_layer_indices_le_square
#print axioms shell_reciprocal_bound
#print axioms origin_sum_bound
#print axioms origin_hasSum
#print axioms origin_tsum_bound
#print axioms origin_subtype_hasSum
#print axioms origin_subtype_tsum_bound
#print axioms cubeOrigin_summable
#print axioms cube_origin_tsum_bound

end
end HMT.V.ThermodynamicLimit
