import RegionalPublicationComposition

/-!
Finite evaluation of the existing generated regional readers at base 3,
depth 600. The displayed integers are conclusions checked by the kernel,
not inputs to the rational readers. The modal auto-scale uses the already
proved ModalIncidence-to-Fibonacci equality, not a new bisection reader.
This module neither imports nor computes a terminal dodecaphase register.
-/

noncomputable section
namespace HMT.I.RegionalSixHundred

open HMT.I.RegionalPublicationComposition

set_option maxHeartbeats 30000000
set_option maxRecDepth 30000

def scale : Nat := 3 ^ 600

def index : Channel → Nat
  | .closure => 104
  | .propagation => 160
  | .autoscale => 700

def generatedPrefix (c : Channel) : Int :=
  RadixCellSelection.first (lower c (index c)) scale

def expectedPrefix : Channel → Int
  | .closure => 58871175078828582423602861784915247708935515546555106316035256695887729126437412843995626239311410634754654366838309942471935119906958980617248194957427434479381281283100208979121705879879452308865804958280022621974596599299586901072331835467338092495788056065771135131450066637595112365
  | .propagation => 50938636253160180888179413689343899880058096680583139319351969406550618361183491660978173715064929803522463101705965620207820892484968737588803861713662448187098712731515259457451744290391479777457307498688328575564785514917030398659922548502000937467496477613565943535501702691974540942
  | .autoscale => 30320787173456450411059450570937628826773068695035242722820185835779727568438782363522556661749215466090147910298426733894837726975541809544014582262291135933678209524801375812678326344720015103636602750945244918166793903058044540395633023346705455026563404740487452508931290332655453238

theorem closure_cell_computation :
    RadixCellSelection.first (lower .closure 104) scale = expectedPrefix .closure ∧
    RadixCellSelection.last (upper .closure 104) scale = expectedPrefix .closure := by
  norm_num [lower, upper, scale, expectedPrefix,
    RadixCellSelection.first, RadixCellSelection.last,
    ClosureAnalytic.lowerQ, ClosureAnalytic.upperQ,
    ClosureAnalytic.quarterCount, ClosureAnalytic.companionCount,
    ClosureAnalytic.primitive_slope_value, ClosureAnalytic.compensator_slope_value,
    ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ, Finset.sum_range_succ]

theorem propagation_cell_computation :
    RadixCellSelection.first (lower .propagation 160) scale = expectedPrefix .propagation ∧
    RadixCellSelection.last (upper .propagation 160) scale = expectedPrefix .propagation := by
  norm_num [lower, upper, scale, expectedPrefix,
    RadixCellSelection.first, RadixCellSelection.last,
    PropagationLimit.partialQ, PropagationLimit.upperQ, PropagationLimit.tailQ,
    PropagationLimit.coefficient, Finset.sum_range_succ]

theorem autoscale_cell_computation :
    RadixCellSelection.first (lower .autoscale 700) scale = expectedPrefix .autoscale ∧
    RadixCellSelection.last (upper .autoscale 700) scale = expectedPrefix .autoscale := by
  norm_num [lower, upper, scale, expectedPrefix,
    RadixCellSelection.first, RadixCellSelection.last,
    AutoscaleBrackets.lowerQ, AutoscaleBrackets.upperQ,
    AutoscaleBrackets.ratioQ, AutoscaleBrackets.cursorPair,
    AutoscaleLimit.sequence_eq_fib]

theorem generated_cell_computation (c : Channel) :
    RadixCellSelection.first (lower c (index c)) scale = expectedPrefix c ∧
    RadixCellSelection.last (upper c (index c)) scale = expectedPrefix c := by
  cases c with
  | closure => exact closure_cell_computation
  | propagation => exact propagation_cell_computation
  | autoscale => exact autoscale_cell_computation

theorem selected_depth_stops (c : Channel) : Stops c scale (index c) :=
  (generated_cell_computation c).1.trans (generated_cell_computation c).2.symm

theorem generatedPrefix_is_cell (c : Channel) :
    generatedPrefix c = RadixCellSelection.cell (value c) (3 ^ 600) := by
  exact stopped_cell_correct c scale (index c) (by norm_num [scale])
    (selected_depth_stops c)

theorem generatedPrefix_evaluates (c : Channel) :
    generatedPrefix c = expectedPrefix c := (generated_cell_computation c).1

theorem generatedPrefix_is_publication (c : Channel) :
    (generatedPrefix c).toNat = publish c 3 (by decide) 600 := by
  rw [publish_eq_prefix, generatedPrefix_is_cell]
  rw [← RadixCellSelection.prefix_as_cell _ (value_nonnegative c)]
  exact Int.toNat_natCast _

end HMT.I.RegionalSixHundred
end

#print axioms HMT.I.RegionalSixHundred.closure_cell_computation
#print axioms HMT.I.RegionalSixHundred.propagation_cell_computation
#print axioms HMT.I.RegionalSixHundred.autoscale_cell_computation
#print axioms HMT.I.RegionalSixHundred.generated_cell_computation
#print axioms HMT.I.RegionalSixHundred.selected_depth_stops
#print axioms HMT.I.RegionalSixHundred.generatedPrefix_is_cell
#print axioms HMT.I.RegionalSixHundred.generatedPrefix_evaluates
#print axioms HMT.I.RegionalSixHundred.generatedPrefix_is_publication
