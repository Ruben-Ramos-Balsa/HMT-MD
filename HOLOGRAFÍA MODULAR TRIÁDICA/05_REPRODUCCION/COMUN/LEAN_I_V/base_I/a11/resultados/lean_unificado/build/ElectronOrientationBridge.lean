import PropagationSemigroup
import AlphaSourceBounds

/-!
# Regional orientation and the declared electronic character

Source: Article I, electron.tex, eq:el-bisagra and its following paragraph.
The involution exchanges the two coordinates of a regional pair. The reader
R(x,y) = x / y^2 is not itself called an involution. Its two orientations are
evaluated on the already constructed closure and autoscale publications.

The electronic application declares the normalized propagation character.
We reuse its generated coefficients before recognizing its evaluation as exp.
The swap identity does not select that character, a regional state, or an
electronic correction coefficient. No measured values enter these definitions.
-/

noncomputable section

namespace HMT.I.ElectronOrientationBridge

def orientationSwap (p : ℝ × ℝ) : ℝ × ℝ := (p.2, p.1)

def PositivePair (p : ℝ × ℝ) : Prop := 0 < p.1 ∧ 0 < p.2

def regionalReader (p : ℝ × ℝ) : ℝ := p.1 / p.2 ^ 2

theorem orientationSwap_involutive : Function.Involutive orientationSwap := by
  intro p
  rfl

theorem orientationSwap_preserves_positive {p : ℝ × ℝ} (hp : PositivePair p) :
    PositivePair (orientationSwap p) := ⟨hp.2, hp.1⟩

theorem regionalReader_positive {p : ℝ × ℝ} (hp : PositivePair p) :
    0 < regionalReader p := div_pos hp.1 (sq_pos_of_pos hp.2)

theorem orientation_identity (x y : ℝ) (hx : 0 < x) (hy : 0 < y) :
    regionalReader (orientationSwap (x, y)) =
      1 / (y ^ 3 * regionalReader (x, y) ^ 2) := by
  dsimp [regionalReader, orientationSwap]
  field_simp [ne_of_gt hx, ne_of_gt hy]
  ring

/-- Evaluation of the normalized coefficients generated in PropagationLimit.
The exponential is used only in the following recognition theorem. -/
def normalizedCharacter (t : ℝ) : ℝ :=
  ∑' n : ℕ, (PropagationLimit.coefficient n : ℝ) * t ^ n

theorem character_hasSum (t : ℝ) :
    HasSum (fun n : ℕ => (PropagationLimit.coefficient n : ℝ) * t ^ n)
      (Real.exp t) := by
  have h := NormedSpace.expSeries_div_hasSum_exp ℝ t
  simpa only [← Real.exp_eq_exp_ℝ, PropagationLimit.coefficient_real_factorial,
    div_eq_mul_inv, one_mul, mul_comm, mul_one] using h

theorem character_recognition (t : ℝ) : normalizedCharacter t = Real.exp t :=
  (character_hasSum t).tsum_eq

theorem character_unit : normalizedCharacter 0 = 1 := by
  rw [character_recognition, Real.exp_zero]

theorem character_semigroup (s t : ℝ) :
    normalizedCharacter (s + t) = normalizedCharacter s * normalizedCharacter t := by
  simp only [character_recognition, Real.exp_add]

theorem character_positive (t : ℝ) : 0 < normalizedCharacter t := by
  rw [character_recognition]
  exact Real.exp_pos t

/-- These two values retain their source-reader definitions. -/
def regionalPair : ℝ × ℝ :=
  (ClosureAnalytic.value, AlphaCarryLimit.autoscaleValue)

theorem regionalPair_positive : PositivePair regionalPair := by
  constructor
  · change 0 < ClosureAnalytic.value
    linarith [AlphaSourceBounds.closure_enclosure.1]
  · change 0 < AlphaCarryLimit.autoscaleValue
    linarith [AlphaSourceBounds.autoscale_enclosure.1]

def markedReturnReading : ℝ := regionalReader regionalPair

def electronicReading : ℝ := regionalReader (orientationSwap regionalPair)

theorem marked_return_reading :
    markedReturnReading = ClosureAnalytic.value / AlphaCarryLimit.autoscaleValue ^ 2 := rfl

theorem electronic_orientation :
    electronicReading = AlphaCarryLimit.autoscaleValue / ClosureAnalytic.value ^ 2 := rfl

theorem electronic_orientation_from_marked_return :
    electronicReading =
      1 / (AlphaCarryLimit.autoscaleValue ^ 3 * markedReturnReading ^ 2) :=
  orientation_identity _ _ regionalPair_positive.1 regionalPair_positive.2

theorem electronic_reading_positive : 0 < electronicReading :=
  regionalReader_positive (orientationSwap_preserves_positive regionalPair_positive)

/-- The choice of this character is the declared electronic reading rule. -/
def electronicCharacter : ℝ := normalizedCharacter electronicReading

theorem electronic_character_recognition :
    electronicCharacter =
      Real.exp (AlphaCarryLimit.autoscaleValue / ClosureAnalytic.value ^ 2) := by
  exact character_recognition electronicReading

theorem electronic_character_from_marked_return :
    electronicCharacter =
      normalizedCharacter
        (1 / (AlphaCarryLimit.autoscaleValue ^ 3 * markedReturnReading ^ 2)) := by
  unfold electronicCharacter
  rw [electronic_orientation_from_marked_return]

theorem electronic_character_positive : 0 < electronicCharacter :=
  character_positive electronicReading

end HMT.I.ElectronOrientationBridge
end

#print axioms HMT.I.ElectronOrientationBridge.orientationSwap_involutive
#print axioms HMT.I.ElectronOrientationBridge.orientationSwap_preserves_positive
#print axioms HMT.I.ElectronOrientationBridge.regionalReader_positive
#print axioms HMT.I.ElectronOrientationBridge.orientation_identity
#print axioms HMT.I.ElectronOrientationBridge.character_hasSum
#print axioms HMT.I.ElectronOrientationBridge.character_recognition
#print axioms HMT.I.ElectronOrientationBridge.character_unit
#print axioms HMT.I.ElectronOrientationBridge.character_semigroup
#print axioms HMT.I.ElectronOrientationBridge.character_positive
#print axioms HMT.I.ElectronOrientationBridge.regionalPair_positive
#print axioms HMT.I.ElectronOrientationBridge.marked_return_reading
#print axioms HMT.I.ElectronOrientationBridge.electronic_orientation
#print axioms HMT.I.ElectronOrientationBridge.electronic_orientation_from_marked_return
#print axioms HMT.I.ElectronOrientationBridge.electronic_reading_positive
#print axioms HMT.I.ElectronOrientationBridge.electronic_character_recognition
#print axioms HMT.I.ElectronOrientationBridge.electronic_character_from_marked_return
#print axioms HMT.I.ElectronOrientationBridge.electronic_character_positive
