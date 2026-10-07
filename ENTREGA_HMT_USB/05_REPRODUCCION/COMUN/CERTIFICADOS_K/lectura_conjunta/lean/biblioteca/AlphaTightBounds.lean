import AlphaStateLinkBound
import AlphaSourceBounds

/-!
# Fine source enclosure required by the state-link estimate

This specializes already proved regional brackets and combines them with the
periodic reading of the upstream register.  The displayed alpha endpoints are
proved inequalities, not definitions of the generated limit.  The producer
must provide the natural-order digit equality, as in AlphaSourceBounds.
-/

noncomputable section

namespace AlphaTightBounds

set_option maxRecDepth 10000 in
theorem precoordinate_tight_enclosure (register : RadixRecovery.K12)
    (hdigits : register.digits =
      [234,543,140,729,659,824,621,58,914,794,146,601]) :
    AlphaStateLinkBound.aLower < AlphaAnalyticChart.precoordinate register ∧
      AlphaAnalyticChart.precoordinate register < AlphaStateLinkBound.aUpper := by
  have hp := ClosureAnalytic.rational_brackets 16
  norm_num [ClosureAnalytic.lowerQ, ClosureAnalytic.upperQ,
    ClosureAnalytic.quarterCount, ClosureAnalytic.companionCount,
    ClosureAnalytic.primitive_slope_value, ClosureAnalytic.compensator_slope_value,
    ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ,
    Finset.sum_range_succ] at hp
  have he := PropagationLimit.rational_bracket 40
  norm_num [PropagationLimit.partialQ, PropagationLimit.upperQ,
    PropagationLimit.tailQ, PropagationLimit.coefficient_eq_factorial,
    Finset.sum_range_succ] at he
  have hf := AutoscaleBrackets.rational_bracket 100
  norm_num [AutoscaleBrackets.lowerQ, AutoscaleBrackets.upperQ,
    AutoscaleBrackets.ratioQ, AutoscaleBrackets.cursorPair,
    AutoscaleLimit.sequence_eq_fib] at hf
  rw [← AlphaCarryLimit.autoscale_recognition] at hf
  have hk : AlphaCarryLimit.Periodic.periodicValue register =
      (234543140729659824621058914794146601 : ℝ) / ((10 : ℝ)^36 - 1) := by
    unfold AlphaCarryLimit.Periodic.periodicValue RadixRecovery.Register.publish
    rw [hdigits]
    norm_num [AlphaCarryLimit.Periodic.blockBase, RadixRecovery.encode,
      RadixRecovery.encodeLE, RadixRecovery.appendDigit]
  unfold AlphaAnalyticChart.precoordinate
  rw [hk]
  norm_num [AlphaStateLinkBound.aLower, AlphaStateLinkBound.aUpper]
  constructor <;> linarith

theorem stateLink_bound_of_vacancy_enclosure (register : RadixRecovery.K12)
    (hdigits : register.digits =
      [234,543,140,729,659,824,621,58,914,794,146,601])
    (delta : ℝ)
    (hdL : AlphaStateLinkBound.deltaLower < delta)
    (hdU : delta < AlphaStateLinkBound.deltaUpper) :
    |AlphaAnalyticChart.stateLink register delta| ≤ AlphaAnalyticChart.lambdaBound := by
  have ha := precoordinate_tight_enclosure register hdigits
  exact AlphaStateLinkBound.stateLink_abs_le register delta ha.1 ha.2 hdL hdU

end AlphaTightBounds

#print axioms AlphaTightBounds.precoordinate_tight_enclosure
#print axioms AlphaTightBounds.stateLink_bound_of_vacancy_enclosure
