import APPArithmetic
import Mathlib.Tactic

/-!
# Arithmetic part of the oriented APP--Fock comparison (U030)

Source: integral, `capitulo_21_c20_lineas_1_2612.tex`, lines 2274--2612.
The histogram below is computed from the two APP evaluations on 1,...,9.
No target 54, 196884, K or coefficient of J enters that computation.

This module formalizes the generated aggregate, the exact polynomial
rigidity and the source's orientation falsifier. `orientedIndexFormula`
is the arithmetic right hand side of the source trace theorem. The
identification with the trace on symmetric powers is NOT asserted here;
it belongs to the operator-level APP--Fock construction.
-/

namespace HMT.I.APPFockRigidity

open APPArithmetic

abbrev Aggregate := Digit → ℤ

/-- The histogram is computed on the common two-dimensional APP support. -/
def histogram (leaf : Digit → Digit → ℕ) (r : Digit) : ℕ :=
  totalOverSupport (fun i j => if leaf i j = value r then 1 else 0)

/-- Oriented difference product minus sum, retaining every residual class. -/
def generatedAggregate : Aggregate := fun r =>
  (histogram productResidue r : ℤ) - (histogram sumResidue r : ℤ)

theorem generated_aggregate_values :
    ∀ r : Digit, generatedAggregate r =
      ![-3, -3, 3, -3, -3, 3, -3, -3, 12] r := by
  decide

/-- Common coefficient of the six unit classes, when balanced. -/
def coefficient (ν : Aggregate) : ℤ := ν ⟨0, by decide⟩

def Balanced (ν : Aggregate) : Prop :=
  ∀ r : Digit, value r % 3 ≠ 0 → ν r = coefficient ν

theorem generated_aggregate_balanced : Balanced generatedAggregate := by
  unfold Balanced
  decide

theorem generated_unit_coefficient : coefficient generatedAggregate = -3 := by
  decide

/-- Positive representatives: the zero residue has digital weight nine. -/
def digitalWeight (ν : Aggregate) : ℤ :=
  ((List.finRange 9).map (fun r => (value r : ℤ) * ν r)).foldl Int.add 0

theorem generated_digital_weight : digitalWeight generatedAggregate = 54 := by
  decide

def zeroResidueUnit : Aggregate := fun r => if value r = 9 then 1 else 0

def perturbZero (ν : Aggregate) (k : ℤ) : Aggregate :=
  fun r => ν r + k * zeroResidueUnit r

theorem perturbZero_coefficient (ν : Aggregate) (k : ℤ) :
    coefficient (perturbZero ν k) = coefficient ν := by
  simp [coefficient, perturbZero, zeroResidueUnit, value]

theorem perturbZero_balanced (ν : Aggregate) (k : ℤ) (h : Balanced ν) :
    Balanced (perturbZero ν k) := by
  intro r hr
  have hne : value r ≠ 9 := by omega
  simp only [perturbZero_coefficient]
  simp [perturbZero, zeroResidueUnit, hne, h r hr]

/-- Arithmetic value of the trace formula after the operator-level theorem. -/
def orientedIndexFormula (m : ℤ) (ν : Aggregate) : ℚ :=
  -3 * (m : ℚ) * (coefficient ν : ℚ) / 2

theorem generated_oriented_index : orientedIndexFormula 12 generatedAggregate = 54 := by
  norm_num [orientedIndexFormula, generated_unit_coefficient]

theorem index_perturbation_invariant (m : ℤ) (ν : Aggregate) (k : ℤ) :
    orientedIndexFormula m (perturbZero ν k) = orientedIndexFormula m ν := by
  simp [orientedIndexFormula, perturbZero_coefficient]

/-- A concrete source falsifier distinguishes the index from digital weight. -/
theorem oriented_index_not_digital_weight :
    orientedIndexFormula 12 (perturbZero generatedAggregate 1) = 54 ∧
    digitalWeight (perturbZero generatedAggregate 1) = 63 := by
  constructor
  · rw [index_perturbation_invariant, generated_oriented_index]
  · decide

/-- Polynomial obtained from the degree-two cyclotomic product calculation.
This definition does not claim an infinite-product trace identity. -/
def fockCoefficientPolynomial (m : ℤ) : ℚ := (m : ℚ) * ((m : ℚ) - 3) / 2

/-- Squared norm of the declared radial family 4ρ₁+ρ₂+...+ρₘ. -/
def radialNormPolynomial (m : ℤ) : ℚ := 2 * ((m : ℚ) + 15)

theorem degree_two_formula (m : ℤ) :
    (m : ℚ) * ((m : ℚ) - 1) / 2 - m = fockCoefficientPolynomial m := by
  unfold fockCoefficientPolynomial
  ring

theorem radial_formula (m : ℤ) :
    4 ^ 2 * (2 : ℚ) + ((m : ℚ) - 1) * 2 = radialNormPolynomial m := by
  unfold radialNormPolynomial
  ring

theorem cyclotomic_radial_equation (m : ℤ) :
    fockCoefficientPolynomial m = radialNormPolynomial m ↔
      (m - 12) * (m + 5) = 0 := by
  constructor
  · intro h
    have hp : ((m : ℚ) - 12) * ((m : ℚ) + 5) = 0 := by
      unfold fockCoefficientPolynomial radialNormPolynomial at h
      nlinarith [h]
    exact_mod_cast hp
  · intro h
    have hp : ((m : ℚ) - 12) * ((m : ℚ) + 5) = 0 := by
      exact_mod_cast h
    unfold fockCoefficientPolynomial radialNormPolynomial
    nlinarith [hp]

theorem positive_cyclotomic_radial_rigidity (m : ℤ) (hm : 0 < m) :
    fockCoefficientPolynomial m = radialNormPolynomial m ↔ m = 12 := by
  rw [cyclotomic_radial_equation, mul_eq_zero]
  constructor
  · rintro (h | h)
    · omega
    · omega
  · intro h
    left
    omega

theorem common_index_value :
    fockCoefficientPolynomial 12 = 54 ∧ radialNormPolynomial 12 = 54 := by
  norm_num [fockCoefficientPolynomial, radialNormPolynomial]

/-- The generated aggregate and the two polynomial realizations have the
same value at the unique positive solution, without taking that value as input. -/
theorem generated_aggregate_rigidity (m : ℤ) (hm : 0 < m)
    (h : fockCoefficientPolynomial m = radialNormPolynomial m) :
    m = 12 ∧
    orientedIndexFormula m generatedAggregate = fockCoefficientPolynomial m ∧
    fockCoefficientPolynomial m = 54 := by
  have hm12 := (positive_cyclotomic_radial_rigidity m hm).mp h
  subst m
  exact ⟨rfl, generated_oriented_index.trans common_index_value.1.symm,
    common_index_value.1⟩

end HMT.I.APPFockRigidity

#print axioms HMT.I.APPFockRigidity.generated_aggregate_values
#print axioms HMT.I.APPFockRigidity.generated_aggregate_balanced
#print axioms HMT.I.APPFockRigidity.generated_unit_coefficient
#print axioms HMT.I.APPFockRigidity.generated_digital_weight
#print axioms HMT.I.APPFockRigidity.perturbZero_coefficient
#print axioms HMT.I.APPFockRigidity.perturbZero_balanced
#print axioms HMT.I.APPFockRigidity.generated_oriented_index
#print axioms HMT.I.APPFockRigidity.index_perturbation_invariant
#print axioms HMT.I.APPFockRigidity.oriented_index_not_digital_weight
#print axioms HMT.I.APPFockRigidity.degree_two_formula
#print axioms HMT.I.APPFockRigidity.radial_formula
#print axioms HMT.I.APPFockRigidity.cyclotomic_radial_equation
#print axioms HMT.I.APPFockRigidity.positive_cyclotomic_radial_rigidity
#print axioms HMT.I.APPFockRigidity.common_index_value
#print axioms HMT.I.APPFockRigidity.generated_aggregate_rigidity
