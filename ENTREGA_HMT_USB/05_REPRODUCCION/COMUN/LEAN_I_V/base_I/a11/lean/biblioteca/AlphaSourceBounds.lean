import AlphaPublications

/-!
# Source enclosures for the correlated alpha publications

The regional values below are the limits already defined from their emitted
readers.  The register is supplied by its upstream producer, which must prove
the displayed digit equality.  That equality is a downstream interface, not a
definition of the producer or a selection using an alpha value.

Source: article I, registro_k.tex (natural-order register) and
alpha_carta_analitica_completa.tex, rational enclosure propagation.
-/

noncomputable section

namespace AlphaSourceBounds

theorem closure_enclosure :
    (314159 : ℝ) / 100000 < ClosureAnalytic.value ∧
      ClosureAnalytic.value < (314160 : ℝ) / 100000 := by
  have h := ClosureAnalytic.rational_brackets 2
  norm_num [ClosureAnalytic.lowerQ, ClosureAnalytic.upperQ,
    ClosureAnalytic.quarterCount, ClosureAnalytic.companionCount,
    ClosureAnalytic.primitive_slope_value, ClosureAnalytic.compensator_slope_value,
    ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ,
    Finset.sum_range_succ] at h
  constructor <;> linarith

theorem propagation_enclosure :
    (271827 : ℝ) / 100000 < PropagationLimit.value ∧
      PropagationLimit.value < (271829 : ℝ) / 100000 := by
  have h := PropagationLimit.rational_bracket 8
  norm_num [PropagationLimit.partialQ, PropagationLimit.upperQ,
    PropagationLimit.tailQ, PropagationLimit.coefficient, Finset.sum_range_succ] at h
  constructor <;> linarith

theorem autoscale_enclosure :
    (161802 : ℝ) / 100000 < AlphaCarryLimit.autoscaleValue ∧
      AlphaCarryLimit.autoscaleValue < (161804 : ℝ) / 100000 := by
  have h := AutoscaleBrackets.rational_bracket 12
  norm_num [AutoscaleBrackets.lowerQ, AutoscaleBrackets.upperQ,
    AutoscaleBrackets.ratioQ, AutoscaleBrackets.cursorPair,
    ModalIncidence.sequence_recurrence, ModalIncidence.sequence_zero,
    ModalIncidence.sequence_one] at h
  rw [← AlphaCarryLimit.autoscale_recognition] at h
  constructor <;> linarith

theorem periodic_enclosure (register : RadixRecovery.K12)
    (hdigits : register.digits =
      [234,543,140,729,659,824,621,58,914,794,146,601]) :
    (23454 : ℝ) / 100000 < AlphaCarryLimit.Periodic.periodicValue register ∧
      AlphaCarryLimit.Periodic.periodicValue register < (23455 : ℝ) / 100000 := by
  unfold AlphaCarryLimit.Periodic.periodicValue RadixRecovery.Register.publish
  rw [hdigits]
  norm_num [AlphaCarryLimit.Periodic.blockBase, RadixRecovery.encode,
    RadixRecovery.encodeLE, RadixRecovery.appendDigit]

theorem periodic_in_unit (register : RadixRecovery.K12)
    (hdigits : register.digits =
      [234,543,140,729,659,824,621,58,914,794,146,601]) :
    AlphaCanonicalSection.InUnit (AlphaCarryLimit.Periodic.periodicValue register) := by
  have h := periodic_enclosure register hdigits
  constructor <;> linarith

theorem precoordinate_enclosure (register : RadixRecovery.K12)
    (hdigits : register.digits =
      [234,543,140,729,659,824,621,58,914,794,146,601]) :
    (727 : ℝ) / 100000 < AlphaAnalyticChart.precoordinate register ∧
      AlphaAnalyticChart.precoordinate register < (733 : ℝ) / 100000 := by
  have hp := closure_enclosure
  have he := propagation_enclosure
  have hf := autoscale_enclosure
  have hk := periodic_enclosure register hdigits
  unfold AlphaAnalyticChart.precoordinate
  constructor <;> linarith

theorem precoordinate_bounds (register : RadixRecovery.K12)
    (hdigits : register.digits =
      [234,543,140,729,659,824,621,58,914,794,146,601]) :
    0 < AlphaAnalyticChart.precoordinate register ∧
      AlphaAnalyticChart.precoordinate register < AlphaAnalyticChart.radius := by
  have h := precoordinate_enclosure register hdigits
  unfold AlphaAnalyticChart.radius
  constructor <;> linarith

end AlphaSourceBounds

#print axioms AlphaSourceBounds.closure_enclosure
#print axioms AlphaSourceBounds.propagation_enclosure
#print axioms AlphaSourceBounds.autoscale_enclosure
#print axioms AlphaSourceBounds.periodic_enclosure
#print axioms AlphaSourceBounds.periodic_in_unit
#print axioms AlphaSourceBounds.precoordinate_enclosure
#print axioms AlphaSourceBounds.precoordinate_bounds
