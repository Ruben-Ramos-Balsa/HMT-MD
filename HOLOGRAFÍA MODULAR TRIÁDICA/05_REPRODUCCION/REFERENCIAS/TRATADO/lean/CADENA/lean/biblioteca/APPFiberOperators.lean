import APPFiberCensus
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul

/-! The actual normalized fibre indicators on all 729 APP triples.
The incidence census is the generator of the compressed Gram matrix. -/
noncomputable section

namespace HMT.I.APPFiberOperators

open Matrix
open APPFiberCensus

def indicatorMatrix (f : Triple → ℕ) : Matrix Triple Digit ℝ :=
  fun x a => if f x = APPArithmetic.value a then 1 else 0

def sigmaIndicator : Matrix Triple Digit ℝ := indicatorMatrix sumDigit
def piIndicator : Matrix Triple Digit ℝ := indicatorMatrix productDigit

def sigmaScale : Matrix Digit Digit ℝ := diagonal (fun _ => (1 / 9 : ℝ))
def piScale : Matrix Digit Digit ℝ := diagonal (fun b => (Real.sqrt (columnTotal b : ℝ))⁻¹)

def VSigma : Matrix Triple Digit ℝ := sigmaIndicator * sigmaScale
def VPi : Matrix Triple Digit ℝ := piIndicator * piScale

def realIncidence : Matrix Digit Digit ℝ := fun a b => (N a b : ℝ)

def generatedGramReal : Matrix Digit Digit ℝ := fun a c =>
  ∑ b, (N a b : ℝ) * (N c b : ℝ) / (81 * (columnTotal b : ℝ))

def PSigma : Matrix Triple Triple ℝ := VSigma * VSigmaᵀ
def PPi : Matrix Triple Triple ℝ := VPi * VPiᵀ

theorem value_injective : Function.Injective APPArithmetic.value := by
  intro a b h
  apply Fin.ext
  exact Nat.succ.inj h

theorem sum_indicator (p : Triple → Prop) [DecidablePred p] :
    (∑ x : Triple, if p x then (1 : ℝ) else 0) =
      ((Finset.univ.filter p).card : ℝ) := by
  rw [← Finset.sum_filter]
  simp

theorem indicator_cross (f g : Triple → ℕ) (a b : Digit) :
    ((indicatorMatrix f)ᵀ * indicatorMatrix g) a b =
      ((Finset.univ.filter (fun x => f x = APPArithmetic.value a ∧
        g x = APPArithmetic.value b)).card : ℝ) := by
  rw [Matrix.mul_apply]
  calc
    _ = ∑ x : Triple, if f x = APPArithmetic.value a ∧
        g x = APPArithmetic.value b then (1 : ℝ) else 0 := by
      apply Finset.sum_congr rfl
      intro x _
      simp only [transpose_apply, indicatorMatrix]
      split_ifs <;> simp_all
    _ = _ := sum_indicator _

theorem sigma_cross_pi : sigmaIndicatorᵀ * piIndicator = realIncidence := by
  ext a b
  exact indicator_cross sumDigit productDigit a b

theorem indicator_self (f : Triple → ℕ) :
    (indicatorMatrix f)ᵀ * indicatorMatrix f =
      diagonal (fun a => ((Finset.univ.filter
        (fun x => f x = APPArithmetic.value a)).card : ℝ)) := by
  ext a b
  rw [indicator_cross]
  by_cases hab : a = b
  · subst b
    simp
  · have hv : APPArithmetic.value a ≠ APPArithmetic.value b :=
      fun h => hab (value_injective h)
    have hempty : Finset.univ.filter (fun x : Triple =>
        f x = APPArithmetic.value a ∧ f x = APPArithmetic.value b) = ∅ := by
      ext x
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.notMem_empty,
        iff_false, not_and]
      intro ha hb
      exact hv (ha.symm.trans hb)
    rw [hempty]
    simp [diagonal_apply, hab]

theorem sigma_indicator_gram : sigmaIndicatorᵀ * sigmaIndicator =
    diagonal (fun _ => (81 : ℝ)) := by
  rw [sigmaIndicator, indicator_self]
  apply congrArg (Matrix.diagonal : (Digit → ℝ) → Matrix Digit Digit ℝ)
  funext a
  exact_mod_cast sum_fiber_card a

theorem pi_indicator_gram : piIndicatorᵀ * piIndicator =
    diagonal (fun b => (columnTotal b : ℝ)) := by
  rw [piIndicator, indicator_self]
  apply congrArg (Matrix.diagonal : (Digit → ℝ) → Matrix Digit Digit ℝ)
  funext b
  exact_mod_cast (columnTotal_eq_fiber_card b).symm

theorem VSigma_entry (x : Triple) (a : Digit) :
    VSigma x a = sigmaIndicator x a / 9 := by
  simp [VSigma, sigmaScale, Matrix.mul_diagonal, div_eq_mul_inv]

theorem VPi_entry (x : Triple) (b : Digit) :
    VPi x b = piIndicator x b / Real.sqrt (columnTotal b : ℝ) := by
  simp [VPi, piScale, Matrix.mul_diagonal, div_eq_mul_inv]

theorem sigma_isometry : VSigmaᵀ * VSigma = 1 := by
  simp only [VSigma, transpose_mul, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc sigmaIndicatorᵀ, sigma_indicator_gram]
  norm_num [sigmaScale, diagonal_mul_diagonal]

theorem pi_isometry : VPiᵀ * VPi = 1 := by
  simp only [VPi, transpose_mul, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc piIndicatorᵀ, pi_indicator_gram]
  simp only [piScale, diagonal_transpose, diagonal_mul_diagonal]
  rw [← diagonal_one]
  apply congrArg (Matrix.diagonal : (Digit → ℝ) → Matrix Digit Digit ℝ)
  funext b
  have hm : (0 : ℝ) < columnTotal b := by exact_mod_cast column_total_positive b
  have hs : Real.sqrt (columnTotal b : ℝ) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hm)
  have hsq := Real.sq_sqrt hm.le
  field_simp [hs]

theorem normalized_cross : VSigmaᵀ * VPi = sigmaScale * realIncidence * piScale := by
  simp only [VSigma, VPi, transpose_mul, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc sigmaIndicatorᵀ, sigma_cross_pi]
  simp [sigmaScale, Matrix.mul_assoc]

theorem normalized_cross_entry (a b : Digit) :
    (VSigmaᵀ * VPi) a b = (N a b : ℝ) / (9 * Real.sqrt (columnTotal b : ℝ)) := by
  rw [normalized_cross]
  simp [sigmaScale, piScale, Matrix.mul_diagonal, Matrix.diagonal_mul,
    realIncidence, div_eq_mul_inv]
  ring

theorem normalized_cross_gram :
    (VSigmaᵀ * VPi) * (VSigmaᵀ * VPi)ᵀ = generatedGramReal := by
  ext a c
  change (∑ b, (VSigmaᵀ * VPi) a b * (VSigmaᵀ * VPi) c b) =
    ∑ b, (N a b : ℝ) * (N c b : ℝ) / (81 * (columnTotal b : ℝ))
  apply Finset.sum_congr rfl
  intro b _
  rw [normalized_cross_entry, normalized_cross_entry, div_mul_div_comm]
  congr 1
  have hm : (0 : ℝ) ≤ columnTotal b := Nat.cast_nonneg _
  nlinarith [Real.sq_sqrt hm]

theorem compressed_pi_eq_generated_gram :
    VSigmaᵀ * PPi * VSigma = generatedGramReal := by
  rw [← normalized_cross_gram, PPi, transpose_mul, transpose_transpose]
  simp only [Matrix.mul_assoc]

theorem PSigma_idempotent : PSigma * PSigma = PSigma := by
  simp only [PSigma, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc VSigmaᵀ, sigma_isometry, Matrix.one_mul]

theorem PPi_idempotent : PPi * PPi = PPi := by
  simp only [PPi, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc VPiᵀ, pi_isometry, Matrix.one_mul]

theorem PSigma_symmetric : PSigmaᵀ = PSigma := by
  simp [PSigma]

theorem PPi_symmetric : PPiᵀ = PPi := by
  simp [PPi]

end HMT.I.APPFiberOperators

end

#print axioms HMT.I.APPFiberOperators.value_injective
#print axioms HMT.I.APPFiberOperators.sum_indicator
#print axioms HMT.I.APPFiberOperators.indicator_cross
#print axioms HMT.I.APPFiberOperators.sigma_cross_pi
#print axioms HMT.I.APPFiberOperators.indicator_self
#print axioms HMT.I.APPFiberOperators.sigma_indicator_gram
#print axioms HMT.I.APPFiberOperators.pi_indicator_gram
#print axioms HMT.I.APPFiberOperators.VSigma_entry
#print axioms HMT.I.APPFiberOperators.VPi_entry
#print axioms HMT.I.APPFiberOperators.sigma_isometry
#print axioms HMT.I.APPFiberOperators.pi_isometry
#print axioms HMT.I.APPFiberOperators.normalized_cross
#print axioms HMT.I.APPFiberOperators.normalized_cross_entry
#print axioms HMT.I.APPFiberOperators.normalized_cross_gram
#print axioms HMT.I.APPFiberOperators.compressed_pi_eq_generated_gram
#print axioms HMT.I.APPFiberOperators.PSigma_idempotent
#print axioms HMT.I.APPFiberOperators.PPi_idempotent
#print axioms HMT.I.APPFiberOperators.PSigma_symmetric
#print axioms HMT.I.APPFiberOperators.PPi_symmetric
