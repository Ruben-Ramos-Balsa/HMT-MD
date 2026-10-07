import TowerMoments
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Topology.Algebra.InfiniteSum.Module

noncomputable section

namespace HMTMassCharacter

open Filter
open scoped Topology
attribute [local instance] Classical.propDecidable

abbrev TowerCoefficients := Height → ℤ

/-- Extend by zero only for summation; the coefficient domain remains Height. -/
def liftedTerms (η : TowerCoefficients) (s : ℕ → ℝ) (n : ℕ) : ℝ :=
  if hn : IsHeight n then (η ⟨n, hn⟩ : ℝ) * s n else 0

theorem liftedTerms_add (η ζ : TowerCoefficients) (s : ℕ → ℝ) (n : ℕ) :
    liftedTerms (η + ζ) s n = liftedTerms η s n + liftedTerms ζ s n := by
  unfold liftedTerms
  split_ifs <;> simp [Int.cast_add, add_mul]

theorem liftedTerms_sub (η ζ : TowerCoefficients) (s : ℕ → ℝ) (n : ℕ) :
    liftedTerms (η - ζ) s n = liftedTerms η s n - liftedTerms ζ s n := by
  unfold liftedTerms
  split_ifs <;> simp [Int.cast_sub, sub_mul]

/-- This is the absolute convergence hypothesis printed in Article VI. -/
structure Refinement (s : ℕ → ℝ) where
  coefficients : TowerCoefficients
  absolute : Summable (fun n => ‖liftedTerms coefficients s n‖)

namespace Refinement

variable {s : ℕ → ℝ}

theorem summable (η : Refinement s) : Summable (liftedTerms η.coefficients s) :=
  η.absolute.of_norm

def zero (s : ℕ → ℝ) : Refinement s where
  coefficients := 0
  absolute := by simpa [liftedTerms] using (summable_zero : Summable fun _ : ℕ => (0 : ℝ))

def add (η ζ : Refinement s) : Refinement s where
  coefficients := η.coefficients + ζ.coefficients
  absolute := summable_norm_iff.mpr (by
    change Summable (fun n => liftedTerms (η.coefficients + ζ.coefficients) s n)
    simp_rw [liftedTerms_add]
    exact η.summable.add ζ.summable)

def sub (η ζ : Refinement s) : Refinement s where
  coefficients := η.coefficients - ζ.coefficients
  absolute := summable_norm_iff.mpr (by
    change Summable (fun n => liftedTerms (η.coefficients - ζ.coefficients) s n)
    simp_rw [liftedTerms_sub]
    exact η.summable.sub ζ.summable)

def value (η : Refinement s) : ℝ := ∑' n, liftedTerms η.coefficients s n

@[simp] theorem value_zero : (zero s).value = 0 := by simp [value, zero, liftedTerms]

theorem value_add (η ζ : Refinement s) : (add η ζ).value = η.value + ζ.value := by
  simp only [value, add, liftedTerms_add]
  exact η.summable.tsum_add ζ.summable

theorem value_sub (η ζ : Refinement s) : (sub η ζ).value = η.value - ζ.value := by
  simp only [value, sub, liftedTerms_sub]
  exact η.summable.tsum_sub ζ.summable

theorem value_tendsto (η : Refinement s) :
    Tendsto (fun N => ∑ n ∈ Finset.range N, liftedTerms η.coefficients s n)
      atTop (𝓝 η.value) := η.summable.hasSum.tendsto_sum_nat

end Refinement

def refinedExponent {s : ℕ → ℝ} (X : Coordinates) (σ : Signature) (η : Refinement s) : ℝ :=
  exponent X σ + η.value

def refinedCharacter {s : ℕ → ℝ} (X : Coordinates) (σ : Signature) (η : Refinement s) : ℝ :=
  Real.exp (refinedExponent X σ η)

theorem refinedCharacter_pos {s : ℕ → ℝ} (X : Coordinates) (σ : Signature)
    (η : Refinement s) : 0 < refinedCharacter X σ η := Real.exp_pos _

theorem refinedCharacter_add {s : ℕ → ℝ} (X : Coordinates) (σ τ : Signature)
    (η ζ : Refinement s) :
    refinedCharacter X (σ + τ) (η.add ζ) =
      refinedCharacter X σ η * refinedCharacter X τ ζ := by
  unfold refinedCharacter refinedExponent
  rw [exponent_add, Refinement.value_add, ← Real.exp_add]
  congr 1
  ring

theorem refinedCharacter_sub {s : ℕ → ℝ} (X : Coordinates) (σ τ : Signature)
    (η ζ : Refinement s) :
    refinedCharacter X (σ - τ) (η.sub ζ) =
      refinedCharacter X σ η / refinedCharacter X τ ζ := by
  unfold refinedCharacter refinedExponent
  rw [exponent_sub, Refinement.value_sub, ← Real.exp_sub]
  congr 1
  ring

theorem refinedCharacter_truncations {s : ℕ → ℝ} (X : Coordinates) (σ : Signature)
    (η : Refinement s) :
    Tendsto (fun N => Real.exp (exponent X σ +
      ∑ n ∈ Finset.range N, liftedTerms η.coefficients s n))
      atTop (𝓝 (refinedCharacter X σ η)) :=
  Real.continuous_exp.continuousAt.tendsto.comp
    (tendsto_const_nhds.add η.value_tendsto)

/-- A finite contribution at height 120 does not merge its provenance with η. -/
def totalCoefficient (σ : Signature) (η : TowerCoefficients) : TowerCoefficients :=
  fun h => η h + if h.val = 120 then σ 3 else 0

theorem totalCoefficient_term (σ : Signature) (η : TowerCoefficients)
    (s : ℕ → ℝ) (n : ℕ) :
    liftedTerms (totalCoefficient σ η) s n =
      liftedTerms η s n + if n = 120 then (σ 3 : ℝ) * s 120 else 0 := by
  by_cases hn : IsHeight n
  · simp only [liftedTerms, dif_pos hn, totalCoefficient, Int.cast_add, add_mul]
    by_cases h120 : n = 120
    · subst n; simp
    · simp [h120]
  · have h120 : n ≠ 120 := by
      intro he
      apply hn
      subst n
      exact ⟨0, 1, by omega, by omega⟩
    simp [liftedTerms, hn, h120]

/-- The manuscript's absolute convergence condition for `N_h s_h` is
equivalent to the condition for `η_h s_h`: their difference is supported at 120. -/
theorem totalCoefficient_absolute_iff (σ : Signature) (η : TowerCoefficients)
    (s : ℕ → ℝ) :
    Summable (fun n => ‖liftedTerms (totalCoefficient σ η) s n‖) ↔
      Summable (fun n => ‖liftedTerms η s n‖) := by
  rw [summable_norm_iff, summable_norm_iff]
  change Summable (fun n => liftedTerms (totalCoefficient σ η) s n) ↔
    Summable (fun n => liftedTerms η s n)
  simp_rw [totalCoefficient_term]
  have hfinite : Summable (fun n : ℕ => if n = 120 then (σ 3 : ℝ) * s 120 else 0) :=
    (hasSum_ite_eq (120 : ℕ) ((σ 3 : ℝ) * s 120)).summable
  constructor
  · intro h
    simpa using h.sub hfinite
  · intro h
    exact h.add hfinite

theorem totalCoefficient_hasSum {s : ℕ → ℝ} (σ : Signature) (η : Refinement s) :
    HasSum (liftedTerms (totalCoefficient σ η.coefficients) s)
      (η.value + (σ 3 : ℝ) * s 120) := by
  change HasSum (fun n => liftedTerms (totalCoefficient σ η.coefficients) s n) _
  simp_rw [totalCoefficient_term]
  exact
    η.summable.hasSum.add (hasSum_ite_eq (120 : ℕ) ((σ 3 : ℝ) * s 120))

/-- Literal refined expression in the source, with the 120 correction counted once. -/
theorem literal_refined_exponent {s : ℕ → ℝ} (σ : Signature) (η : Refinement s)
    (x y delta : ℝ) :
    refinedExponent (internalCoordinates x y delta (s 120)) σ η =
      (σ 0 : ℝ) * x + ((σ 1 : ℝ) / 6) * y + (σ 2 : ℝ) * delta +
      (σ 4 : ℝ) * (135 * delta ^ 2) +
      ∑' n, liftedTerms (totalCoefficient σ η.coefficients) s n := by
  rw [(totalCoefficient_hasSum σ η).tsum_eq]
  unfold refinedExponent
  rw [internal_exponent]
  ring

def refinedBasalMass {s : ℕ → ℝ} (mRef : ℝ) (X : Coordinates)
    (σ σRef : Signature) (η ηRef : Refinement s) : ℝ :=
  mRef * refinedCharacter X (σ - σRef) (η.sub ηRef)

theorem refinedBasalMass_pos {s : ℕ → ℝ} {mRef : ℝ} (hm : 0 < mRef)
    (X : Coordinates) (σ σRef : Signature) (η ηRef : Refinement s) :
    0 < refinedBasalMass mRef X σ σRef η ηRef :=
  mul_pos hm (refinedCharacter_pos _ _ _)

theorem refinedBasalMass_ratio {s : ℕ → ℝ} {mRef : ℝ} (hm : 0 < mRef)
    (X : Coordinates) (σ τ σRef : Signature) (η ζ ηRef : Refinement s) :
    refinedBasalMass mRef X σ σRef η ηRef /
      refinedBasalMass mRef X τ σRef ζ ηRef = refinedCharacter X (σ - τ) (η.sub ζ) := by
  simp only [refinedBasalMass, refinedCharacter_sub]
  field_simp [ne_of_gt hm, ne_of_gt (refinedCharacter_pos X σRef ηRef),
    ne_of_gt (refinedCharacter_pos X τ ζ)]
  ring

#print axioms Refinement.value_tendsto
#print axioms refinedCharacter_truncations
#print axioms refinedCharacter_add
#print axioms refinedCharacter_sub
#print axioms totalCoefficient_hasSum
#print axioms totalCoefficient_absolute_iff
#print axioms literal_refined_exponent
#print axioms refinedBasalMass_pos
#print axioms refinedBasalMass_ratio

end HMTMassCharacter
