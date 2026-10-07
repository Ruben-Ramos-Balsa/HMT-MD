import NormalizedCoordinates

/-!
# Electric charge and quanta from a positive constitutive response

Owner: Article III REV03, `07_carga_y_cuantos.tex`, in full.
This is a scalar realization in one common normalized constitutive chart.
`alpha` and the positive full-turn action `h` are already published upstream;
`W` is the previously constructed labelled positive response. No measured
charge, electrical quantum, or target value selects those inputs. The formulas
below do not claim to regenerate alpha, action, or the underlying TPK history.

The construction starts with the positive square root, proves its defining
equation and uniqueness, and then composes all four electric quanta. Both
action sections remain distinct and their return covariance is proved.
-/

noncomputable section
namespace HMT.III.ElectricQuanta

open HMT.III.Constitutive

def charge (alpha h : ℝ) (W : PositiveResponse) : ℝ :=
  Real.sqrt (2 * alpha * h / W.impedance)

def resistance (alpha h : ℝ) (W : PositiveResponse) : ℝ :=
  h / charge alpha h W ^ 2

def conductance (alpha h : ℝ) (W : PositiveResponse) : ℝ :=
  2 * charge alpha h W ^ 2 / h

def flux (alpha h : ℝ) (W : PositiveResponse) : ℝ :=
  h / (2 * charge alpha h W)

def josephson (alpha h : ℝ) (W : PositiveResponse) : ℝ :=
  2 * charge alpha h W / h

def reducedAction (h : ℝ) : ℝ := h / (2 * Real.pi)

theorem charge_pos {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : 0 < charge alpha h W := by
  apply Real.sqrt_pos.mpr
  exact div_pos (mul_pos (mul_pos (by norm_num) ha) hh) W.coordinates_pos.2.2.1

theorem charge_sq {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : charge alpha h W ^ 2 = 2 * alpha * h / W.impedance := by
  apply Real.sq_sqrt
  exact (div_pos (mul_pos (mul_pos (by norm_num) ha) hh) W.coordinates_pos.2.2.1).le

theorem charge_equation {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : W.impedance * charge alpha h W ^ 2 = 2 * alpha * h := by
  rw [charge_sq ha hh W]
  field_simp [ne_of_gt W.coordinates_pos.2.2.1]

theorem positive_charge_unique {alpha h e : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) (he : 0 < e)
    (hEq : W.impedance * e ^ 2 = 2 * alpha * h) : e = charge alpha h W := by
  apply (sq_eq_sq₀ he.le (charge_pos ha hh W).le).mp
  apply mul_left_cancel₀ (ne_of_gt W.coordinates_pos.2.2.1)
  rw [hEq, charge_equation ha hh W]

theorem positive_charge_exists_unique {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) :
    ∃! e : ℝ, 0 < e ∧ W.impedance * e ^ 2 = 2 * alpha * h := by
  refine ⟨charge alpha h W, ⟨charge_pos ha hh W, charge_equation ha hh W⟩, ?_⟩
  intro e he
  exact positive_charge_unique ha hh W he.1 he.2

theorem conjugate_charge {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) :
    -charge alpha h W < 0 ∧ W.impedance * (-charge alpha h W) ^ 2 = 2 * alpha * h := by
  constructor
  · exact neg_neg_of_pos (charge_pos ha hh W)
  · simpa only [neg_sq] using charge_equation ha hh W

theorem coupling_from_charge {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : alpha = W.impedance * charge alpha h W ^ 2 / (2 * h) := by
  rw [charge_equation ha hh W]
  field_simp [hh.ne']
  ring

theorem epsilon_speed (W : PositiveResponse) : W.epsilon * W.speed = 1 / W.impedance := by
  have hp := ne_of_gt W.plus_pos
  have hm := ne_of_gt W.minus_pos
  dsimp [PositiveResponse.epsilon, PositiveResponse.speed, PositiveResponse.impedance]
  field_simp
  ring

theorem reducedAction_pos {h : ℝ} (hh : 0 < h) : 0 < reducedAction h :=
  div_pos hh (mul_pos (by norm_num) Real.pi_pos)

theorem full_turn_action (h : ℝ) : 2 * Real.pi * reducedAction h = h := by
  unfold reducedAction
  field_simp [Real.pi_ne_zero]

theorem coupling_electromagnetic {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) :
    alpha = charge alpha h W ^ 2 /
      (4 * Real.pi * W.epsilon * reducedAction h * W.speed) := by
  rw [charge_sq ha hh W]
  have hp := ne_of_gt W.plus_pos
  have hm := ne_of_gt W.minus_pos
  dsimp [PositiveResponse.epsilon, PositiveResponse.speed, PositiveResponse.impedance,
    reducedAction]
  field_simp [Real.pi_ne_zero, hh.ne']
  ring

theorem resistance_pos {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : 0 < resistance alpha h W :=
  div_pos hh (pow_pos (charge_pos ha hh W) 2)

theorem conductance_pos {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : 0 < conductance alpha h W :=
  div_pos (mul_pos (by norm_num) (pow_pos (charge_pos ha hh W) 2)) hh

theorem flux_pos {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : 0 < flux alpha h W :=
  div_pos hh (mul_pos (by norm_num) (charge_pos ha hh W))

theorem josephson_pos {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : 0 < josephson alpha h W :=
  div_pos (mul_pos (by norm_num) (charge_pos ha hh W)) hh

theorem resistance_eq {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : resistance alpha h W = W.impedance / (2 * alpha) := by
  rw [resistance, charge_sq ha hh W]
  field_simp [ha.ne', hh.ne', ne_of_gt W.coordinates_pos.2.2.1]
  ring

theorem conductance_eq {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : conductance alpha h W = 4 * alpha / W.impedance := by
  rw [conductance, charge_sq ha hh W]
  field_simp [hh.ne', ne_of_gt W.coordinates_pos.2.2.1]
  ring

theorem flux_sq {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : flux alpha h W ^ 2 = h * W.impedance / (8 * alpha) := by
  rw [flux, div_pow, mul_pow, charge_sq ha hh W]
  field_simp [ha.ne', hh.ne', ne_of_gt W.coordinates_pos.2.2.1]
  ring

theorem flux_eq_sqrt {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : flux alpha h W = Real.sqrt (h * W.impedance / (8 * alpha)) := by
  calc
    flux alpha h W = Real.sqrt (flux alpha h W ^ 2) :=
      (Real.sqrt_sq (flux_pos ha hh W).le).symm
    _ = Real.sqrt (h * W.impedance / (8 * alpha)) := by rw [flux_sq ha hh W]

theorem josephson_eq_inv_flux (alpha h : ℝ)
    (W : PositiveResponse) : josephson alpha h W = (flux alpha h W)⁻¹ := by
  simp only [josephson, flux, inv_div]

theorem resistance_conductance {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : resistance alpha h W * conductance alpha h W = 2 := by
  unfold resistance conductance
  field_simp [hh.ne', ne_of_gt (charge_pos ha hh W)]
  ring

theorem conductance_impedance {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : conductance alpha h W * W.impedance = 4 * alpha := by
  rw [conductance_eq ha hh W]
  exact div_mul_cancel₀ _ (ne_of_gt W.coordinates_pos.2.2.1)

theorem josephson_flux {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : josephson alpha h W * flux alpha h W = 1 := by
  rw [josephson_eq_inv_flux alpha h W]
  exact inv_mul_cancel₀ (ne_of_gt (flux_pos ha hh W))

theorem josephson_sq_resistance {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) : josephson alpha h W ^ 2 * resistance alpha h W = 4 / h := by
  unfold josephson resistance
  field_simp [hh.ne', ne_of_gt (charge_pos ha hh W)]
  ring

/-- All four cross-identities use the same charge and action section. -/
theorem electric_quanta_identities {alpha h : ℝ} (ha : 0 < alpha) (hh : 0 < h)
    (W : PositiveResponse) :
    resistance alpha h W * conductance alpha h W = 2 ∧
    conductance alpha h W * W.impedance = 4 * alpha ∧
    josephson alpha h W * flux alpha h W = 1 ∧
    josephson alpha h W ^ 2 * resistance alpha h W = 4 / h :=
  ⟨resistance_conductance ha hh W, conductance_impedance ha hh W,
   josephson_flux ha hh W, josephson_sq_resistance ha hh W⟩

theorem charge_return_ratio {alpha hPre hRet : ℝ}
    (ha : 0 < alpha) (hp : 0 < hPre) (hr : 0 < hRet) (W : PositiveResponse) :
    charge alpha hPre W / charge alpha hRet W = Real.sqrt (hPre / hRet) := by
  have hs : (charge alpha hPre W / charge alpha hRet W) ^ 2 = hPre / hRet := by
    rw [div_pow, charge_sq ha hp W, charge_sq ha hr W]
    field_simp [ha.ne', hr.ne', ne_of_gt W.coordinates_pos.2.2.1]
    ring
  calc
    charge alpha hPre W / charge alpha hRet W =
        Real.sqrt ((charge alpha hPre W / charge alpha hRet W) ^ 2) :=
      (Real.sqrt_sq (div_pos (charge_pos ha hp W) (charge_pos ha hr W)).le).symm
    _ = Real.sqrt (hPre / hRet) := by rw [hs]

theorem resistance_return_invariant {alpha hPre hRet : ℝ}
    (ha : 0 < alpha) (hp : 0 < hPre) (hr : 0 < hRet) (W : PositiveResponse) :
    resistance alpha hPre W = resistance alpha hRet W := by
  rw [resistance_eq ha hp W, resistance_eq ha hr W]

theorem conductance_return_invariant {alpha hPre hRet : ℝ}
    (ha : 0 < alpha) (hp : 0 < hPre) (hr : 0 < hRet) (W : PositiveResponse) :
    conductance alpha hPre W = conductance alpha hRet W := by
  rw [conductance_eq ha hp W, conductance_eq ha hr W]

theorem flux_return_ratio {alpha hPre hRet : ℝ}
    (ha : 0 < alpha) (hp : 0 < hPre) (hr : 0 < hRet) (W : PositiveResponse) :
    flux alpha hPre W / flux alpha hRet W = Real.sqrt (hPre / hRet) := by
  have hs : (flux alpha hPre W / flux alpha hRet W) ^ 2 = hPre / hRet := by
    rw [div_pow, flux_sq ha hp W, flux_sq ha hr W]
    field_simp [ha.ne', hr.ne', ne_of_gt W.coordinates_pos.2.2.1]
    ring
  calc
    flux alpha hPre W / flux alpha hRet W =
        Real.sqrt ((flux alpha hPre W / flux alpha hRet W) ^ 2) :=
      (Real.sqrt_sq (div_pos (flux_pos ha hp W) (flux_pos ha hr W)).le).symm
    _ = Real.sqrt (hPre / hRet) := by rw [hs]

theorem josephson_return_ratio {alpha hPre hRet : ℝ}
    (ha : 0 < alpha) (hp : 0 < hPre) (hr : 0 < hRet) (W : PositiveResponse) :
    josephson alpha hPre W / josephson alpha hRet W = (Real.sqrt (hPre / hRet))⁻¹ := by
  rw [josephson_eq_inv_flux alpha hPre W, josephson_eq_inv_flux alpha hRet W]
  have hi : (flux alpha hPre W)⁻¹ / (flux alpha hRet W)⁻¹ =
      (flux alpha hPre W / flux alpha hRet W)⁻¹ := by
    field_simp [ne_of_gt (flux_pos ha hp W), ne_of_gt (flux_pos ha hr W)]
  rw [hi, flux_return_ratio ha hp hr W]

/-- Full algebraic return covariance from the same upstream alpha and response. -/
theorem electric_quanta_return_covariance {alpha hPre hRet : ℝ}
    (ha : 0 < alpha) (hp : 0 < hPre) (hr : 0 < hRet) (W : PositiveResponse) :
    charge alpha hPre W / charge alpha hRet W = Real.sqrt (hPre / hRet) ∧
    resistance alpha hPre W = resistance alpha hRet W ∧
    conductance alpha hPre W = conductance alpha hRet W ∧
    flux alpha hPre W / flux alpha hRet W = Real.sqrt (hPre / hRet) ∧
    josephson alpha hPre W / josephson alpha hRet W = (Real.sqrt (hPre / hRet))⁻¹ :=
  ⟨charge_return_ratio ha hp hr W, resistance_return_invariant ha hp hr W,
   conductance_return_invariant ha hp hr W, flux_return_ratio ha hp hr W,
   josephson_return_ratio ha hp hr W⟩

#print axioms charge_pos
#print axioms charge_sq
#print axioms charge_equation
#print axioms positive_charge_unique
#print axioms positive_charge_exists_unique
#print axioms conjugate_charge
#print axioms coupling_from_charge
#print axioms epsilon_speed
#print axioms reducedAction_pos
#print axioms full_turn_action
#print axioms coupling_electromagnetic
#print axioms resistance_pos
#print axioms conductance_pos
#print axioms flux_pos
#print axioms josephson_pos
#print axioms resistance_eq
#print axioms conductance_eq
#print axioms flux_sq
#print axioms flux_eq_sqrt
#print axioms josephson_eq_inv_flux
#print axioms resistance_conductance
#print axioms conductance_impedance
#print axioms josephson_flux
#print axioms josephson_sq_resistance
#print axioms electric_quanta_identities
#print axioms charge_return_ratio
#print axioms resistance_return_invariant
#print axioms conductance_return_invariant
#print axioms flux_return_ratio
#print axioms josephson_return_ratio
#print axioms electric_quanta_return_covariance

end HMT.III.ElectricQuanta
