import ConstitutiveResponse

/-!
The four normalized coordinates of a fixed positive labelled response.
This is the uniqueness within the constitutive rules of `iii:eq:four`;
physical units and production of the channels are not supplied here.
-/
namespace HMT.III.Constitutive
noncomputable section

structure PositiveResponse where
  rPlus : ℝ
  rMinus : ℝ
  plus_pos : 0 < rPlus
  minus_pos : 0 < rMinus

namespace PositiveResponse

def epsilon (W : PositiveResponse) : ℝ := W.rPlus ^ 2
def mu (W : PositiveResponse) : ℝ := W.rMinus ^ 2
def impedance (W : PositiveResponse) : ℝ := W.rMinus / W.rPlus
def speed (W : PositiveResponse) : ℝ := 1 / (W.rPlus * W.rMinus)

theorem coordinates_pos (W : PositiveResponse) :
    0 < W.epsilon ∧ 0 < W.mu ∧ 0 < W.impedance ∧ 0 < W.speed := by
  have hp := W.plus_pos
  have hm := W.minus_pos
  dsimp [epsilon, mu, impedance, speed]
  exact ⟨sq_pos_of_pos hp, sq_pos_of_pos hm, div_pos hm hp,
    div_pos zero_lt_one (mul_pos hp hm)⟩

theorem product_identity (W : PositiveResponse) :
    W.mu * W.epsilon = 1 / W.speed ^ 2 := by
  dsimp [mu, epsilon, speed]
  field_simp
  ring

theorem quotient_identity (W : PositiveResponse) :
    W.mu / W.epsilon = W.impedance ^ 2 := by
  simp only [mu, epsilon, impedance, div_pow]

theorem epsilon_from_readings (W : PositiveResponse) :
    W.epsilon = 1 / (W.impedance * W.speed) := by
  have hp := ne_of_gt W.plus_pos
  have hm := ne_of_gt W.minus_pos
  dsimp [epsilon, impedance, speed]
  field_simp
  ring

theorem mu_from_readings (W : PositiveResponse) :
    W.mu = W.impedance / W.speed := by
  have hp := ne_of_gt W.plus_pos
  have hm := ne_of_gt W.minus_pos
  dsimp [mu, impedance, speed]
  field_simp
  ring

theorem recover_rPlus (W : PositiveResponse) :
    W.rPlus = 1 / Real.sqrt (W.impedance * W.speed) := by
  have hp := ne_of_gt W.plus_pos
  have hm := ne_of_gt W.minus_pos
  have hz : W.impedance * W.speed = (1 / W.rPlus) ^ 2 := by
    dsimp [impedance, speed]
    field_simp
    ring
  rw [hz, Real.sqrt_sq (le_of_lt (div_pos zero_lt_one W.plus_pos))]
  simp

theorem recover_rMinus (W : PositiveResponse) :
    W.rMinus = Real.sqrt (W.impedance / W.speed) := by
  rw [← W.mu_from_readings]
  exact (Real.sqrt_sq W.minus_pos.le).symm

-- Product and oriented quotient determine a positive pair without a sign choice.
theorem positive_pair_unique {a b c d : ℝ}
    (ha : 0 < a) (_hb : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (hp : a * b = c * d) (hq : b / a = d / c) : a = c ∧ b = d := by
  have hcross := (div_eq_div_iff (ne_of_gt ha) (ne_of_gt hc)).mp hq
  have h₁ := congrArg (fun t : ℝ => t * c) hp
  have h₂ := congrArg (fun t : ℝ => t * a) hcross
  have hprod : d * (a ^ 2 - c ^ 2) = 0 := by nlinarith only [h₁, h₂]
  have hs : a ^ 2 = c ^ 2 := by
    rcases mul_eq_zero.mp hprod with hzero | hzero
    · exact (ne_of_gt hd hzero).elim
    · linarith
  have hac := (sq_eq_sq₀ ha.le hc.le).mp hs
  refine ⟨hac, ?_⟩
  rw [hac] at hp
  exact mul_left_cancel₀ (ne_of_gt hc) hp

theorem quadratic_coordinates_unique (W : PositiveResponse) {e m : ℝ}
    (he : 0 < e) (hm : 0 < m)
    (hproduct : m * e = 1 / W.speed ^ 2)
    (hquotient : m / e = W.impedance ^ 2) :
    e = W.epsilon ∧ m = W.mu := by
  apply positive_pair_unique he hm W.coordinates_pos.1 W.coordinates_pos.2.1
  · rw [mul_comm e m, hproduct, ← W.product_identity, mul_comm W.mu W.epsilon]
  · exact hquotient.trans W.quotient_identity.symm

theorem readings_determine_response (W V : PositiveResponse)
    (hZ : W.impedance = V.impedance) (hc : W.speed = V.speed) :
    W.rPlus = V.rPlus ∧ W.rMinus = V.rMinus := by
  constructor
  · rw [W.recover_rPlus, V.recover_rPlus, hZ, hc]
  · rw [W.recover_rMinus, V.recover_rMinus, hZ, hc]

def swap (W : PositiveResponse) : PositiveResponse :=
  ⟨W.rMinus, W.rPlus, W.minus_pos, W.plus_pos⟩

theorem swap_coordinates (W : PositiveResponse) :
    W.swap.epsilon = W.mu ∧ W.swap.mu = W.epsilon ∧
    W.swap.impedance = 1 / W.impedance ∧ W.swap.speed = W.speed := by
  dsimp [swap, epsilon, mu, impedance, speed]
  simp [mul_comm]

end PositiveResponse

#print axioms PositiveResponse.coordinates_pos
#print axioms PositiveResponse.product_identity
#print axioms PositiveResponse.quotient_identity
#print axioms PositiveResponse.recover_rPlus
#print axioms PositiveResponse.recover_rMinus
#print axioms PositiveResponse.quadratic_coordinates_unique
#print axioms PositiveResponse.readings_determine_response
#print axioms PositiveResponse.swap_coordinates

end
end HMT.III.Constitutive
