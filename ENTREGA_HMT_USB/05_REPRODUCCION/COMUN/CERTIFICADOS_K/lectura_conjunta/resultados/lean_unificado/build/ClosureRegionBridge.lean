import TPKRegions
import ClosureAnalytic
import RadixCellSelection

/-!
The analytic closure reader receives the arities of the selected emitted
fibre.  Its slope is defined from that produced cardinal, not from a real
constant or a decimal prefix.  The quarter-turn count belongs to the elliptic
chart; it is not identified with a seed multiplicity.
-/

noncomputable section
namespace ClosureRegionBridge

def regionArity : Nat := TPKRegions.closureFibre.length
def companionArity : Nat := TPKRegions.companions.length
def slope : ℚ := 1 / (regionArity : ℚ)

def accumulated : Nat → ℚ
  | 0 => 0
  | n + 1 => ClosureAnalytic.tanAdd (accumulated n) slope

def companionSlope : ℚ := accumulated companionArity
def compensator : ℚ := (1 + companionSlope) / (companionSlope - 1)
def angle : ℝ := (companionArity : ℝ) * Real.arctan (slope : ℝ) -
  Real.arctan ((1 / compensator : ℚ) : ℝ)
def value : ℝ := (ClosureAnalytic.quarterCount : ℝ) * angle

theorem region_arity : regionArity = ClosureAnalytic.regionCount :=
  TPKRegions.closure_five_regions

theorem companion_arity : companionArity = ClosureAnalytic.companionCount :=
  TPKRegions.closure_four_companions

theorem arities_partition : companionArity + TPKRegions.anchors.length = regionArity := by
  rw [region_arity, companion_arity, TPKRegions.closure_one_anchor]
  exact ClosureAnalytic.companion_count

theorem slope_eq_reader : slope = ClosureAnalytic.primitiveSlope := by
  unfold slope ClosureAnalytic.primitiveSlope
  rw [region_arity]

theorem accumulated_eq_reader (n : Nat) :
    accumulated n = ClosureAnalytic.accumulated n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [accumulated, ClosureAnalytic.accumulated, ih, slope_eq_reader]

theorem companion_slope_eq_reader : companionSlope = ClosureAnalytic.companionSlope := by
  rw [companionSlope, companion_arity, accumulated_eq_reader]
  rfl

theorem compensator_eq_reader : compensator = ClosureAnalytic.compensator := by
  unfold compensator ClosureAnalytic.compensator
  rw [companion_slope_eq_reader]

theorem generated_compensator : compensator = 239 :=
  compensator_eq_reader.trans ClosureAnalytic.compensator_value

theorem angle_eq_reader : angle = ClosureAnalytic.closureAngle := by
  simp only [angle, companion_arity, slope_eq_reader, compensator_eq_reader,
    ClosureAnalytic.closureAngle, ClosureAnalytic.companionAngle,
    ClosureAnalytic.compensatorSlope]

theorem value_eq_reader : value = ClosureAnalytic.value := by
  rw [value, angle_eq_reader]
  rfl

theorem posterior_recognition : value = Real.pi :=
  value_eq_reader.trans ClosureAnalytic.value_eq_pi

theorem elliptic_four_turns (v : ℚ × ℚ) :
    ClosureAnalytic.ellipticJ (ClosureAnalytic.ellipticJ
      (ClosureAnalytic.ellipticJ (ClosureAnalytic.ellipticJ v))) = v := by
  simp [ClosureAnalytic.ellipticJ]

theorem generated_reader_enclosure (n : Nat) :
    (ClosureAnalytic.lowerQ n : ℝ) ≤ value ∧
      value ≤ (ClosureAnalytic.upperQ n : ℝ) := by
  rw [value_eq_reader]
  exact ClosureAnalytic.rational_brackets n

theorem arbitrary_precision (scale : Nat) :
    ∃ n : Nat, 1 ≤ n ∧
      (ClosureAnalytic.upperQ n - ClosureAnalytic.lowerQ n) * scale < 1 :=
  ClosureAnalytic.exists_precision_index scale

theorem eventual_cell_publication (scale : Nat) (hs : 0 < scale) :
    ∃ N : Nat, ∀ n, N ≤ n →
      RadixCellSelection.first (ClosureAnalytic.lowerQ n) scale =
        RadixCellSelection.cell value scale ∧
      RadixCellSelection.last (ClosureAnalytic.upperQ n) scale =
        RadixCellSelection.cell value scale := by
  rw [value_eq_reader]
  exact RadixCellSelection.closure_eventual_cell scale hs

end ClosureRegionBridge
end

#print axioms ClosureRegionBridge.region_arity
#print axioms ClosureRegionBridge.companion_arity
#print axioms ClosureRegionBridge.arities_partition
#print axioms ClosureRegionBridge.slope_eq_reader
#print axioms ClosureRegionBridge.accumulated_eq_reader
#print axioms ClosureRegionBridge.companion_slope_eq_reader
#print axioms ClosureRegionBridge.compensator_eq_reader
#print axioms ClosureRegionBridge.generated_compensator
#print axioms ClosureRegionBridge.angle_eq_reader
#print axioms ClosureRegionBridge.value_eq_reader
#print axioms ClosureRegionBridge.posterior_recognition
#print axioms ClosureRegionBridge.elliptic_four_turns
#print axioms ClosureRegionBridge.generated_reader_enclosure
#print axioms ClosureRegionBridge.arbitrary_precision
#print axioms ClosureRegionBridge.eventual_cell_publication
