import WeightedOscillatorTrace
import OscillatorEulerProduct

/-!
The finite monomial parity trace is the corresponding coefficient of the
unbounded formal oscillator product. The cutoff disappears for N >= d.
This composes the finite trace theorem with coefficientwise stabilization;
no analytic convergence or FLM premise is used.
-/

noncomputable section
namespace HMT.IV.WeightedEulerBridge

open scoped BigOperators
open HMT.IV.WeightedOscillatorTrace HMT.IV.OscillatorEulerProduct

theorem geometricFactor_coefficient (d n k : ℕ) (hk : k ≤ d) :
    (geometricFactor d (n+1)).coeff k =
      if (n+1) ∣ k then (-1 : ℂ) ^ (k/(n+1)) else 0 := by
  classical
  simp only [geometricFactor, Polynomial.finset_sum_coeff, Polynomial.coeff_monomial]
  by_cases hd : (n+1) ∣ k
  · rw [if_pos hd]
    let a : Fin (d+1) := ⟨k/(n+1), lt_of_le_of_lt (Nat.div_le_self _ _) (by omega)⟩
    have ha : (n+1)*a.val = k := Nat.mul_div_cancel' hd
    rw [Finset.sum_eq_single a]
    · simp [ha, a]
    · intro b _ hba
      have hb : (n+1)*b.val ≠ k := by
        intro hb
        apply hba
        apply Fin.ext
        have hmul : (n+1)*b.val = (n+1)*a.val := hb.trans ha.symm
        exact Nat.eq_of_mul_eq_mul_left (by omega) hmul
      simp [hb]
    · simp
  · rw [if_neg hd]
    apply Finset.sum_eq_zero
    intro a _
    have ha : (n+1)*a.val ≠ k := by
      intro ha
      exact hd ⟨a.val, ha.symm⟩
    simp [ha]

theorem geometricFactor_agrees_mode (d n : ℕ) :
    AgreeThrough d (geometricFactor d (n+1)) (modeFactor n) := by
  intro k hk
  rw [Polynomial.coeff_coe, geometricFactor_coefficient d n k hk,
    modeFactor_coefficient]

theorem polynomial_product_agrees {ι : Type*} [DecidableEq ι]
    (s : Finset ι) {d : ℕ} (p : ι → Polynomial ℂ) (f : ι → PowerSeries ℂ)
    (h : ∀ i ∈ s, AgreeThrough d (p i) (f i)) :
    AgreeThrough d (↑(∏ i ∈ s, p i)) (∏ i ∈ s, f i) := by
  induction s using Finset.induction_on with
  | empty => simpa using agreeThrough_refl d 1
  | @insert i s hi ih =>
    simp only [Finset.prod_insert hi, Polynomial.coe_mul]
    exact agreeThrough_mul (h i (Finset.mem_insert_self _ _))
      (ih (fun j hj => h j (Finset.mem_insert_of_mem hj)))

theorem finiteProduct_agrees (d N r : ℕ) :
    AgreeThrough d (WeightedOscillatorTrace.finiteProduct d N r)
      (OscillatorEulerProduct.finiteProduct r N) := by
  have h := polynomial_product_agrees (Finset.univ : Finset (Mode N r))
    (fun p => geometricFactor d (p.1.val+1)) (fun p => modeFactor p.1.val)
    (fun p _ => geometricFactor_agrees_mode d p.1.val)
  change AgreeThrough d (WeightedOscillatorTrace.finiteProduct d N r)
    (∏ p : Mode N r, modeFactor p.1.val) at h
  simp only [Fintype.prod_prod_type, Finset.prod_const, Finset.card_univ,
    Fintype.card_fin] at h
  rw [Fin.prod_univ_eq_prod_range (fun n => modeFactor n ^ r) N] at h
  exact h

theorem trace_eq_oscillator_coefficient (d N r : ℕ) (hN : d ≤ N) :
    LinearMap.trace ℂ (PieceSpace d N r) (parityOperator d N r) =
      PowerSeries.coeff ℂ d (oscillatorProduct r) := by
  rw [trace_eq_product_coefficient]
  have h := finiteProduct_agrees d N r d le_rfl
  rw [Polynomial.coeff_coe] at h
  exact h.trans (oscillatorProduct_coefficient r d N hN).symm

end HMT.IV.WeightedEulerBridge
end

#print axioms HMT.IV.WeightedEulerBridge.geometricFactor_coefficient
#print axioms HMT.IV.WeightedEulerBridge.geometricFactor_agrees_mode
#print axioms HMT.IV.WeightedEulerBridge.polynomial_product_agrees
#print axioms HMT.IV.WeightedEulerBridge.finiteProduct_agrees
#print axioms HMT.IV.WeightedEulerBridge.trace_eq_oscillator_coefficient
