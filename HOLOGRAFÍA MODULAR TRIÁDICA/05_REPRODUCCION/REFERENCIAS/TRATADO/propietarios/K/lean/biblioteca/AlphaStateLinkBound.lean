import AlphaAnalyticChart

/-!
# Target-free interval certificate for the state-link coefficient

This module closes the analytic inequality required by `AlphaAnalyticChart`.
It receives only enclosures of the upstream state precoordinate and vacancy
coordinate.  The constants in those enclosures are the rational outward
roundings used by the executable certificate; no conventional value of alpha
occurs in the statement or proof.

The production of the terminal register and of the vacancy coordinate belongs
to their upstream owner modules.  This file proves that once those owners
establish the displayed rational enclosures, the resulting state-link has the
required absolute bound.
-/

noncomputable section

namespace AlphaStateLinkBound

open AlphaAnalyticChart

def aLower : ℝ :=
  7297352569283800997285105472380662 / (10 : ℝ)^36

def aUpper : ℝ :=
  7297352569283800997285105472380663 / (10 : ℝ)^36

def pLower : ℝ :=
  3141592653589793238462643383279502884 / (10 : ℝ)^36

def pUpper : ℝ :=
  3141592653589793238462643383279502885 / (10 : ℝ)^36

def deltaLower : ℝ :=
  45757490560675125409944193489769381 / (10 : ℝ)^36

def deltaUpper : ℝ :=
  45757490560675125409944193489769382 / (10 : ℝ)^36

def jetLower : ℝ :=
  2*pLower*aLower - (7/4)*aUpper^2 + aLower^3/(2*pUpper) +
    aLower^4/20 - 2*aUpper^5/21 - aUpper^6/46 - aUpper^7/120 +
    aLower^8/45 + 2*aLower^9/495 - deltaUpper

def jetUpper : ℝ :=
  2*pUpper*aUpper - (7/4)*aLower^2 + aUpper^3/(2*pLower) +
    aUpper^4/20 - 2*aLower^5/21 - aLower^6/46 - aLower^7/120 +
    aUpper^8/45 + 2*aUpper^9/495 - deltaLower

theorem closure_tight_enclosure :
    pLower < ClosureAnalytic.value ∧ ClosureAnalytic.value < pUpper := by
  have h := ClosureAnalytic.rational_brackets 25
  norm_num [pLower, pUpper, ClosureAnalytic.lowerQ, ClosureAnalytic.upperQ,
    ClosureAnalytic.quarterCount, ClosureAnalytic.companionCount,
    ClosureAnalytic.primitive_slope_value, ClosureAnalytic.compensator_slope_value,
    ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ,
    Finset.sum_range_succ] at h ⊢
  constructor <;> linarith

theorem jet_enclosure (register : RadixRecovery.K12) (delta : ℝ)
    (haL : aLower < precoordinate register)
    (haU : precoordinate register < aUpper)
    (hdL : deltaLower < delta)
    (hdU : delta < deltaUpper) :
    jetLower < jet9 ClosureAnalytic.value delta (precoordinate register) ∧
      jet9 ClosureAnalytic.value delta (precoordinate register) < jetUpper := by
  let a := precoordinate register
  let p := ClosureAnalytic.value
  have hp := closure_tight_enclosure
  have haL' : aLower < a := haL
  have haU' : a < aUpper := haU
  have hpL : pLower < p := hp.1
  have hpU : p < pUpper := hp.2
  have ha0 : 0 < a := by
    have : 0 < aLower := by norm_num [aLower]
    linarith
  have hp0 : 0 < p := by
    have : 0 < pLower := by norm_num [pLower]
    linarith
  have haLower0 : 0 ≤ aLower := by norm_num [aLower]
  have haUpper0 : 0 ≤ aUpper := by norm_num [aUpper]
  have hpLower0 : 0 ≤ pLower := by norm_num [pLower]
  have hpUpper0 : 0 ≤ pUpper := by norm_num [pUpper]
  have hpLowerPos : 0 < pLower := by norm_num [pLower]
  have hpUpperPos : 0 < pUpper := by norm_num [pUpper]
  have ha2L : aLower^2 < a^2 := by gcongr
  have ha2U : a^2 < aUpper^2 := by gcongr
  have ha3L : aLower^3 < a^3 := by gcongr
  have ha3U : a^3 < aUpper^3 := by gcongr
  have ha4L : aLower^4 < a^4 := by gcongr
  have ha4U : a^4 < aUpper^4 := by gcongr
  have ha5L : aLower^5 < a^5 := by gcongr
  have ha5U : a^5 < aUpper^5 := by gcongr
  have ha6L : aLower^6 < a^6 := by gcongr
  have ha6U : a^6 < aUpper^6 := by gcongr
  have ha7L : aLower^7 < a^7 := by gcongr
  have ha7U : a^7 < aUpper^7 := by gcongr
  have ha8L : aLower^8 < a^8 := by gcongr
  have ha8U : a^8 < aUpper^8 := by gcongr
  have ha9L : aLower^9 < a^9 := by gcongr
  have ha9U : a^9 < aUpper^9 := by gcongr
  have hpaL : pLower*aLower < p*a := by gcongr
  have hpaU : p*a < pUpper*aUpper := by gcongr
  have hdivL : aLower^3/(2*pUpper) < a^3/(2*p) := by
    apply (div_lt_div_iff₀ (by positivity) (by positivity)).2
    gcongr
  have hdivU : a^3/(2*p) < aUpper^3/(2*pLower) := by
    apply (div_lt_div_iff₀ (by positivity) (by positivity)).2
    gcongr
  dsimp [a, p] at *
  unfold jet9 jetLower jetUpper
  constructor <;> linarith

theorem stateLink_abs_le (register : RadixRecovery.K12) (delta : ℝ)
    (haL : aLower < precoordinate register)
    (haU : precoordinate register < aUpper)
    (hdL : deltaLower < delta)
    (hdU : delta < deltaUpper) :
    |stateLink register delta| ≤ lambdaBound := by
  let a := precoordinate register
  let E := jet9 ClosureAnalytic.value delta a
  have hjet := jet_enclosure register delta haL haU hdL hdU
  have hEL : jetLower < E := hjet.1
  have hEU : E < jetUpper := hjet.2
  have hJL : 0 < jetLower := by norm_num [jetLower, aLower, aUpper,
    pLower, pUpper, deltaUpper]
  have hJU : 0 < jetUpper := by norm_num [jetUpper, aLower, aUpper,
    pLower, pUpper, deltaLower]
  have hE0 : 0 < E := hJL.trans hEL
  have ha0 : 0 < a := by
    have h : 0 < aLower := by norm_num [aLower]
    exact h.trans haL
  have haR : a ≤ radius := by
    have h : aUpper < radius := by norm_num [aUpper, radius]
    exact (haU.trans h).le
  have hden : 0 < 1 - q*a^3 := denominator_pos ha0.le haR
  have haLower0 : 0 ≤ aLower := by norm_num [aLower]
  have hpowL : aLower^3 < a^3 := by gcongr
  have hfactor : 1-q*a^3 < 1-q*aLower^3 := by
    have hq := q_pos
    nlinarith
  have hlink : stateLink register delta ≤ 0 := by
    change -(E * (1-q*a^3)) / a^10 ≤ 0
    exact div_nonpos_of_nonpos_of_nonneg
      (neg_nonpos.mpr (mul_nonneg hE0.le hden.le)) (pow_nonneg ha0.le 10)
  rw [abs_of_nonpos hlink]
  change -(-(E * (1-q*a^3)) / a^10) ≤ lambdaBound
  simp only [neg_div, neg_neg]
  apply (div_le_iff₀ (pow_pos ha0 10)).2
  calc
    E * (1 - q*a^3) ≤ jetUpper * (1 - q*aLower^3) := by
      exact mul_le_mul hEU.le hfactor.le hden.le hJU.le
    _ ≤ lambdaBound * aLower^10 := by
      norm_num [jetUpper, aLower, aUpper, pLower, pUpper, deltaLower,
        lambdaBound, q]
    _ ≤ lambdaBound * a^10 := by
      have hL : aLower ≤ a := haL.le
      have hLambda : 0 ≤ lambdaBound := by norm_num [lambdaBound]
      gcongr

end AlphaStateLinkBound
end

#print axioms AlphaStateLinkBound.closure_tight_enclosure
#print axioms AlphaStateLinkBound.jet_enclosure
#print axioms AlphaStateLinkBound.stateLink_abs_le
