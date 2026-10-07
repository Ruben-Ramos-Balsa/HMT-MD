import ContractiveChannels

/-!
Exact downstream equivalence between the declared angular chamber and ordered
contractive labelled channels. This joins the existing exponential/logarithmic
formulas and scalar constitutive inverse. It does not generate angular data from
TPK, reconstruct an enriched TPK history, or certify all of Article III.

Source: Article III, iii:sec:constitutiva, iii:eq:rchannels and
iii:eq:recover-angular. No physical target value enters this construction.
-/
namespace HMT.III.Constitutive
noncomputable section

structure AngularChamber where
  x : ℝ
  y : ℝ
  y_pos : 0 < y
  y_lt_x : y < x

namespace AngularChamber

theorem ext_pair (A B : AngularChamber) (hx : A.x = B.x) (hy : A.y = B.y) :
    A = B := by
  cases A
  cases B
  cases hx
  cases hy
  rfl

def channels (A : AngularChamber) : OrientedChannels where
  qPlus := Real.exp (-A.x - A.y)
  qMinus := Real.exp (-A.x + A.y)
  plus_pos := Real.exp_pos _
  ordered := Real.exp_lt_exp.mpr (by linarith [A.y_pos])
  minus_lt_one := Real.exp_lt_one_iff.mpr (by linarith [A.y_lt_x])

theorem channels_contractivity (A : AngularChamber) :
    0 < A.channels.qPlus ∧ A.channels.qPlus < A.channels.qMinus ∧
      A.channels.qMinus < 1 :=
  ⟨A.channels.plus_pos, A.channels.ordered, A.channels.minus_lt_one⟩

@[simp] theorem angularX_channels (A : AngularChamber) :
    A.channels.angularX = A.x := by
  dsimp [OrientedChannels.angularX, channels]
  rw [Real.log_mul (ne_of_gt (Real.exp_pos _)) (ne_of_gt (Real.exp_pos _))]
  simp only [Real.log_exp]
  ring

@[simp] theorem angularY_channels (A : AngularChamber) :
    A.channels.angularY = A.y := by
  dsimp [OrientedChannels.angularY, channels]
  rw [Real.log_div (ne_of_gt (Real.exp_pos _)) (ne_of_gt (Real.exp_pos _))]
  simp only [Real.log_exp]
  ring

theorem channels_angular_recovery (A : AngularChamber) :
    A.channels.angularX = A.x ∧ A.channels.angularY = A.y :=
  ⟨A.angularX_channels, A.angularY_channels⟩

theorem recover_plus (A : AngularChamber) :
    recoverChannel (channelResponse A.channels.qPlus)
      (channelResponse_bounds A.channels.plus_mem) = Real.exp (-A.x - A.y) :=
  recoverChannel_response A.channels.plus_mem

theorem recover_minus (A : AngularChamber) :
    recoverChannel (channelResponse A.channels.qMinus)
      (channelResponse_bounds A.channels.minus_mem) = Real.exp (-A.x + A.y) :=
  recoverChannel_response A.channels.minus_mem

end AngularChamber

namespace OrientedChannels

theorem ext_pair (Q R : OrientedChannels)
    (hp : Q.qPlus = R.qPlus) (hm : Q.qMinus = R.qMinus) : Q = R := by
  cases Q
  cases R
  cases hp
  cases hm
  rfl

def chamber (Q : OrientedChannels) : AngularChamber where
  x := Q.angularX
  y := Q.angularY
  y_pos := Q.angular_chamber.1
  y_lt_x := Q.angular_chamber.2

@[simp] theorem channels_chamber (Q : OrientedChannels) :
    Q.chamber.channels = Q := by
  apply ext_pair
  · exact Q.angular_channels.1
  · exact Q.angular_channels.2

theorem labelled_responses_determine_channels (Q R : OrientedChannels)
    (hp : Q.vacuum.rPlus = R.vacuum.rPlus)
    (hm : Q.vacuum.rMinus = R.vacuum.rMinus) : Q = R := by
  apply ext_pair
  · exact channelResponse_strictAntiOn.injOn Q.plus_mem R.plus_mem hp
  · exact channelResponse_strictAntiOn.injOn Q.minus_mem R.minus_mem hm

theorem labelled_responses_determine_angles (Q R : OrientedChannels)
    (hp : Q.vacuum.rPlus = R.vacuum.rPlus)
    (hm : Q.vacuum.rMinus = R.vacuum.rMinus) :
    Q.angularX = R.angularX ∧ Q.angularY = R.angularY := by
  have h := labelled_responses_determine_channels Q R hp hm
  exact ⟨congrArg angularX h, congrArg angularY h⟩

end OrientedChannels

namespace AngularChamber

@[simp] theorem chamber_channels (A : AngularChamber) :
    A.channels.chamber = A := by
  apply ext_pair
  · exact A.angularX_channels
  · exact A.angularY_channels

theorem labelled_responses_determine_pair (A B : AngularChamber)
    (hp : A.channels.vacuum.rPlus = B.channels.vacuum.rPlus)
    (hm : A.channels.vacuum.rMinus = B.channels.vacuum.rMinus) :
    A.x = B.x ∧ A.y = B.y := by
  simpa only [angularX_channels, angularY_channels] using
    OrientedChannels.labelled_responses_determine_angles A.channels B.channels hp hm

theorem labelled_responses_injective (A B : AngularChamber)
    (hp : A.channels.vacuum.rPlus = B.channels.vacuum.rPlus)
    (hm : A.channels.vacuum.rMinus = B.channels.vacuum.rMinus) : A = B := by
  have h := labelled_responses_determine_pair A B hp hm
  exact ext_pair A B h.1 h.2

theorem normalized_readings_injective (A B : AngularChamber)
    (hZ : A.channels.vacuum.impedance = B.channels.vacuum.impedance)
    (hc : A.channels.vacuum.speed = B.channels.vacuum.speed) : A = B := by
  have h := PositiveResponse.readings_determine_response
    A.channels.vacuum B.channels.vacuum hZ hc
  exact labelled_responses_injective A B h.1 h.2

end AngularChamber

def angularChannelsEquiv : AngularChamber ≃ OrientedChannels where
  toFun := AngularChamber.channels
  invFun := OrientedChannels.chamber
  left_inv := AngularChamber.chamber_channels
  right_inv := OrientedChannels.channels_chamber

#print axioms AngularChamber.ext_pair
#print axioms AngularChamber.channels_contractivity
#print axioms AngularChamber.angularX_channels
#print axioms AngularChamber.angularY_channels
#print axioms AngularChamber.channels_angular_recovery
#print axioms AngularChamber.recover_plus
#print axioms AngularChamber.recover_minus
#print axioms OrientedChannels.ext_pair
#print axioms OrientedChannels.channels_chamber
#print axioms OrientedChannels.labelled_responses_determine_channels
#print axioms OrientedChannels.labelled_responses_determine_angles
#print axioms AngularChamber.chamber_channels
#print axioms AngularChamber.labelled_responses_determine_pair
#print axioms AngularChamber.labelled_responses_injective
#print axioms AngularChamber.normalized_readings_injective
#print axioms angularChannelsEquiv

end
end HMT.III.Constitutive
