import NormalizedCoordinates

/-!
The 90/120 response of labelled contractive channels and its scalar inverse.
These channels are received downstream. No generation of them by TPK, nor
reconstruction of an enriched history from two spectral values, is asserted.
-/
namespace HMT.III.Constitutive
noncomputable section
open Set

def channelResponse (q : ℝ) : ℝ := (1 - q ^ 90) / (1 - q ^ 120)

theorem channel_power_mem {q : ℝ} (hq : q ∈ Ioo 0 1) : q ^ 30 ∈ Ioo 0 1 :=
  ⟨pow_pos hq.1 _, pow_lt_one₀ hq.1.le hq.2 (by decide)⟩

theorem channel_denominator_pos {q : ℝ} (hq : q ∈ Ioo 0 1) :
    0 < 1 - q ^ 120 :=
  sub_pos.mpr (pow_lt_one₀ hq.1.le hq.2 (by decide))

theorem channelResponse_eq {q : ℝ} (hq : q ∈ Ioo 0 1) :
    channelResponse q = response (q ^ 30) := by
  have h90 : q ^ 90 = (q ^ 30) ^ 3 := by rw [← pow_mul]
  have h120 : q ^ 120 = (q ^ 30) ^ 4 := by rw [← pow_mul]
  unfold channelResponse response
  apply (div_eq_div_iff (ne_of_gt (channel_denominator_pos hq))
    (ne_of_gt (denominator_pos (channel_power_mem hq).1.le))).mpr
  rw [h90, h120]
  unfold numerator denominator
  ring

theorem channelResponse_bounds {q : ℝ} (hq : q ∈ Ioo 0 1) :
    channelResponse q ∈ Ioo (3 / 4) 1 := by
  rw [channelResponse_eq hq]
  exact response_bounds (channel_power_mem hq)

theorem channelResponse_strictAntiOn : StrictAntiOn channelResponse (Ioo 0 1) := by
  intro q hq t ht hqt
  rw [channelResponse_eq hq, channelResponse_eq ht]
  exact response_strictAntiOn (channel_power_mem hq).1.le (channel_power_mem ht).1.le
    (pow_lt_pow_left₀ hqt hq.1.le (by decide))

def thirtiethRoot (s : ℝ) : ℝ := s ^ ((30 : ℝ)⁻¹)

theorem thirtiethRoot_mem {s : ℝ} (hs : s ∈ Ioo 0 1) :
    thirtiethRoot s ∈ Ioo 0 1 :=
  ⟨Real.rpow_pos_of_pos hs.1 _, Real.rpow_lt_one hs.1.le hs.2 (by norm_num)⟩

theorem thirtiethRoot_pow {s : ℝ} (hs : 0 ≤ s) :
    thirtiethRoot s ^ 30 = s :=
  Real.rpow_inv_natCast_pow hs (by decide : (30 : ℕ) ≠ 0)

theorem thirtiethRoot_of_pow {q : ℝ} (hq : 0 ≤ q) :
    thirtiethRoot (q ^ 30) = q :=
  Real.pow_rpow_inv_natCast hq (by decide : (30 : ℕ) ≠ 0)

def recoverChannel (r : ℝ) (hr : r ∈ Ioo (3 / 4) 1) : ℝ :=
  thirtiethRoot (recover r hr)

theorem recoverChannel_spec (r : ℝ) (hr : r ∈ Ioo (3 / 4) 1) :
    recoverChannel r hr ∈ Ioo 0 1 ∧ channelResponse (recoverChannel r hr) = r := by
  have hs := recover_spec r hr
  have hq := thirtiethRoot_mem hs.1
  refine ⟨hq, ?_⟩
  rw [recoverChannel, channelResponse_eq hq, thirtiethRoot_pow hs.1.1.le, hs.2]

theorem channelResponse_exists_unique {r : ℝ} (hr : r ∈ Ioo (3 / 4) 1) :
    ∃! q : ℝ, q ∈ Ioo 0 1 ∧ channelResponse q = r := by
  refine ⟨recoverChannel r hr, recoverChannel_spec r hr, ?_⟩
  intro q hq
  exact channelResponse_strictAntiOn.injOn hq.1 (recoverChannel_spec r hr).1
    (hq.2.trans (recoverChannel_spec r hr).2.symm)

theorem recoverChannel_response {q : ℝ} (hq : q ∈ Ioo 0 1) :
    recoverChannel (channelResponse q) (channelResponse_bounds hq) = q :=
  channelResponse_strictAntiOn.injOn (recoverChannel_spec _ _).1 hq
    (recoverChannel_spec _ _).2

structure OrientedChannels where
  qPlus : ℝ
  qMinus : ℝ
  plus_pos : 0 < qPlus
  ordered : qPlus < qMinus
  minus_lt_one : qMinus < 1

namespace OrientedChannels

theorem plus_mem (Q : OrientedChannels) : Q.qPlus ∈ Ioo 0 1 :=
  ⟨Q.plus_pos, Q.ordered.trans Q.minus_lt_one⟩

theorem minus_mem (Q : OrientedChannels) : Q.qMinus ∈ Ioo 0 1 :=
  ⟨Q.plus_pos.trans Q.ordered, Q.minus_lt_one⟩

def vacuum (Q : OrientedChannels) : PositiveResponse where
  rPlus := channelResponse Q.qPlus
  rMinus := channelResponse Q.qMinus
  plus_pos := lt_trans (by norm_num : (0 : ℝ) < 3 / 4) (channelResponse_bounds Q.plus_mem).1
  minus_pos := lt_trans (by norm_num : (0 : ℝ) < 3 / 4) (channelResponse_bounds Q.minus_mem).1

theorem vacuum_order (Q : OrientedChannels) :
    3 / 4 < Q.vacuum.rMinus ∧ Q.vacuum.rMinus < Q.vacuum.rPlus ∧ Q.vacuum.rPlus < 1 :=
  ⟨(channelResponse_bounds Q.minus_mem).1,
   channelResponse_strictAntiOn Q.plus_mem Q.minus_mem Q.ordered,
   (channelResponse_bounds Q.plus_mem).2⟩

def angularX (Q : OrientedChannels) : ℝ := - Real.log (Q.qPlus * Q.qMinus) / 2
def angularY (Q : OrientedChannels) : ℝ := Real.log (Q.qMinus / Q.qPlus) / 2

theorem angular_log_channels (Q : OrientedChannels) :
    Real.log Q.qPlus = -Q.angularX - Q.angularY ∧
    Real.log Q.qMinus = -Q.angularX + Q.angularY := by
  have hp := ne_of_gt Q.plus_pos
  have hm := ne_of_gt Q.minus_mem.1
  dsimp [angularX, angularY]
  rw [Real.log_mul hp hm, Real.log_div hm hp]
  constructor <;> ring

theorem angular_channels (Q : OrientedChannels) :
    Real.exp (-Q.angularX - Q.angularY) = Q.qPlus ∧
    Real.exp (-Q.angularX + Q.angularY) = Q.qMinus := by
  rw [← Q.angular_log_channels.1, ← Q.angular_log_channels.2]
  exact ⟨Real.exp_log Q.plus_pos, Real.exp_log Q.minus_mem.1⟩

theorem angular_chamber (Q : OrientedChannels) :
    0 < Q.angularY ∧ Q.angularY < Q.angularX := by
  have hlog := Real.strictMonoOn_log Q.plus_pos Q.minus_mem.1 Q.ordered
  have hminus := Real.log_neg Q.minus_mem.1 Q.minus_lt_one
  have hchannels := Q.angular_log_channels
  constructor <;> linarith [hchannels.1, hchannels.2]

end OrientedChannels

#print axioms channelResponse_eq
#print axioms channelResponse_strictAntiOn
#print axioms channelResponse_exists_unique
#print axioms recoverChannel_response
#print axioms OrientedChannels.vacuum_order
#print axioms OrientedChannels.angular_channels
#print axioms OrientedChannels.angular_chamber

end
end HMT.III.Constitutive
