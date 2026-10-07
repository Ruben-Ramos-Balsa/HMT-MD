import LatticeAnnulusBridge
import LatticeSummabilityTail

/-! The same periodic annular truncation in full-lattice indicator form and
in the subtype form used by the proved Riemann-sum theorem. -/
namespace HMT.V.ThermodynamicLimit
noncomputable section
open Set

def latticeAnnulusDomain (Δ δ R : ℝ) : Set Lattice :=
  {ν | δ ≤ Δ * (supRadius ν : ℝ) ∧ Δ * (supRadius ν : ℝ) ≤ R}

def annularValue (F : ℝ → ℝ) (Δ δ R : ℝ) : Lattice → ℝ :=
  (latticeAnnulusDomain Δ δ R).indicator (excitationValue F Δ)

theorem annularValue_apply (F : ℝ → ℝ) (Δ δ R : ℝ) (ν : Lattice) :
    annularValue F Δ δ R ν =
      if δ ≤ Δ * (supRadius ν : ℝ) ∧ Δ * (supRadius ν : ℝ) ≤ R
      then excitationValue F Δ ν else 0 := by
  simp only [annularValue, Set.indicator_apply, latticeAnnulusDomain, Set.mem_setOf_eq]

theorem annularValue_nonneg {F : ℝ → ℝ} {Δ : ℝ} (hΔ : 0 < Δ)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r) (δ R : ℝ) (ν : Lattice) :
    0 ≤ annularValue F Δ δ R ν := by
  rw [annularValue_apply]
  split_ifs
  · exact excitationValue_nonneg hΔ hF ν
  · exact le_rfl

theorem annularValue_le_excitation {F : ℝ → ℝ} {Δ : ℝ} (hΔ : 0 < Δ)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r) (δ R : ℝ) (ν : Lattice) :
    annularValue F Δ δ R ν ≤ excitationValue F Δ ν := by
  rw [annularValue_apply]
  split_ifs
  · exact le_rfl
  · exact excitationValue_nonneg hΔ hF ν

theorem annularValue_summable {F : ℝ → ℝ} {Δ : ℝ}
    (h : Summable (excitationValue F Δ)) (δ R : ℝ) :
    Summable (annularValue F Δ δ R) := h.indicator _

theorem excitationValue_eq_on_annulus (F : ℝ → ℝ) {Δ δ R : ℝ} (hδ : 0 < δ)
    {ν : Lattice} (hν : ν ∈ latticeAnnulusDomain Δ δ R) :
    excitationValue F Δ ν = F (Δ * radius ν) := by
  have hn : ν ≠ 0 := by
    intro hz
    have hs : supRadius ν = 0 := (supRadius_zero_iff ν).2 hz
    have hle := hν.1
    rw [hs, Nat.cast_zero, mul_zero] at hle
    exact (not_le_of_gt hδ) hle
  simp only [excitationValue, if_neg hn]

theorem annular_domain_reciprocal (n : ℕ) (ν : Lattice) (δ R : ℝ) :
    ν ∈ latticeAnnulusDomain (1 / (n : ℝ)) δ R ↔
      scaledLatticePoint n ν ∈ cubicAnnulus δ R := by
  rw [scaledLatticePoint_mem_annulus]
  simp only [latticeAnnulusDomain, Set.mem_setOf_eq, one_div, div_eq_mul_inv, mul_comm, mul_one, one_mul]

theorem scaled_annularValue_tsum (F : ℝ → ℝ) {n : ℕ} (hn : 0 < n)
    {δ : ℝ} (hδ : 0 < δ) (R : ℝ) :
    (1 / (n : ℝ)) ^ 3 * (∑' ν : Lattice, annularValue F (1 / (n : ℝ)) δ R ν) =
      annularDiscreteSum F δ R n := by
  have hsub : (∑' ν : latticeAnnulusDomain (1 / (n : ℝ)) δ R,
      excitationValue F (1 / (n : ℝ)) ν) =
      ∑' ν : {ν : Lattice // scaledLatticePoint n ν ∈ cubicAnnulus δ R},
        F (radius ν / n) := by
    calc
      _ = ∑' ν : latticeAnnulusDomain (1 / (n : ℝ)) δ R, F (radius ν / n) := by
        apply tsum_congr
        intro ν
        rw [excitationValue_eq_on_annulus F hδ ν.property]
        congr 1
        ring
      _ = _ := tsum_congr_subtype (fun ν : Lattice => F (radius ν / n))
        (fun ν => annular_domain_reciprocal n ν δ R)
  change (1 / (n : ℝ)) ^ 3 *
    (∑' ν : Lattice, (latticeAnnulusDomain (1 / (n : ℝ)) δ R).indicator
      (excitationValue F (1 / (n : ℝ))) ν) = _
  rw [← tsum_subtype, hsub, annularDiscreteSum]
  have hn' : (n : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hn)
  field_simp

#print axioms annularValue_nonneg
#print axioms annularValue_le_excitation
#print axioms annularValue_summable
#print axioms excitationValue_eq_on_annulus
#print axioms scaled_annularValue_tsum

end
end HMT.V.ThermodynamicLimit
