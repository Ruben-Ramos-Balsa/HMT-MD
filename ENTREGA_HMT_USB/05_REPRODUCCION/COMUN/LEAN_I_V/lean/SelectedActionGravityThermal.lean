import SelectedActionDomain

/-!
Article II: circular gravitation and the thermal transducer on the very same
regional register already selected in Article I. This is the selected
specialization of the existing GeneratedCircularGravity / GeneratedThermalClosure
proofs, not a new register or a reconstruction of a Ledger from its answer.
The positive dimensional bases U, c, t0 and Theta remain explicit as in
10_gravedad.tex and 10c_boltzmann_desarrollo.tex. The radius is G m / c^2.
-/
noncomputable section
namespace HMT.II.SelectedActionGravityThermal

open HMT.I.SelectedAction HMT.II.ActionReturn

inductive ActionChart where
  | pre
  | ret
  deriving DecidableEq

def sectionAction (U : ℝ) : ActionChart → ℝ
  | .pre => hbarPre alpha phi U
  | .ret => hbarRet alpha phi pi U

def frequency (t0 : ℝ) : ℝ := 2 * pi / (108 * t0)
def radius (c t0 : ℝ) : ℝ := c / frequency t0
def cycleEnergy (U t0 : ℝ) (a : ActionChart) : ℝ :=
  sectionAction U a * frequency t0
def cycleMass (U c t0 : ℝ) (a : ActionChart) : ℝ :=
  cycleEnergy U t0 a / c ^ 2
def gravityFamily (U c t0 : ℝ) (a : ActionChart) (theta : ℝ) : ℝ :=
  theta * c ^ 5 * t0 ^ 2 / sectionAction U a
def circularSelector : ℝ := (54 / pi) ^ 2
def circularGravity (U c t0 : ℝ) (a : ActionChart) : ℝ :=
  gravityFamily U c t0 a circularSelector
def thermalCoefficient (U t0 Theta : ℝ) (a : ActionChart) : ℝ :=
  cycleEnergy U t0 a / (Theta * Real.log 3)
def returnTemperature (U Theta : ℝ) : ℝ :=
  Theta * sectionAction U .ret / sectionAction U .pre
def sectionTemperature (U Theta : ℝ) : ActionChart → ℝ
  | .pre => Theta
  | .ret => returnTemperature U Theta

theorem sectionAction_pos {U : ℝ} (hU : 0 < U) (a : ActionChart) :
    0 < sectionAction U a := by
  cases a
  · exact action_domain.hbarPre_pos hU
  · exact action_domain.hbarRet_pos hU

theorem sectionAction_return_lt {U : ℝ} (hU : 0 < U) :
    sectionAction U .ret < sectionAction U .pre :=
  (action_sections U hU).2.1

theorem frequency_pos {t0 : ℝ} (ht0 : 0 < t0) : 0 < frequency t0 :=
  div_pos (mul_pos (by norm_num) action_domain.pi_pos) (mul_pos (by norm_num) ht0)

theorem radius_eq (c t0 : ℝ) : radius c t0 = (54 / pi) * (c * t0) := by
  unfold radius frequency
  field_simp
  ring

theorem circularSelector_pos : 0 < circularSelector :=
  pow_pos (div_pos (by norm_num) action_domain.pi_pos) 2

theorem gravitational_radius_eq {U c t0 : ℝ}
    (hU : 0 < U) (hc : 0 < c) (ht0 : 0 < t0)
    (a : ActionChart) (theta : ℝ) :
    gravityFamily U c t0 a theta * cycleMass U c t0 a / c ^ 2 =
      theta * (pi / 54) * (c * t0) := by
  have ha := ne_of_gt (sectionAction_pos hU a)
  have hc0 := ne_of_gt hc
  have ht0' := ne_of_gt ht0
  unfold gravityFamily cycleMass cycleEnergy frequency
  field_simp
  ring

theorem circular_selector_iff {U c t0 : ℝ}
    (hU : 0 < U) (hc : 0 < c) (ht0 : 0 < t0)
    (a : ActionChart) (theta : ℝ) :
    gravityFamily U c t0 a theta * cycleMass U c t0 a / c ^ 2 = radius c t0 ↔
      theta = circularSelector := by
  rw [gravitational_radius_eq hU hc ht0 a theta, radius_eq]
  have hp0 := ne_of_gt action_domain.pi_pos
  have hp54 : pi / 54 ≠ 0 := div_ne_zero hp0 (by norm_num)
  have hct : c * t0 ≠ 0 := mul_ne_zero (ne_of_gt hc) (ne_of_gt ht0)
  constructor
  · intro h
    have he : theta * (pi / 54) = 54 / pi := mul_right_cancel₀ hct h
    calc
      theta = (54 / pi) / (pi / 54) := (eq_div_iff hp54).mpr he
      _ = circularSelector := by unfold circularSelector; field_simp; ring
  · rintro rfl
    unfold circularSelector
    field_simp
    ring

theorem circular_selector_unique {U c t0 : ℝ}
    (hU : 0 < U) (hc : 0 < c) (ht0 : 0 < t0) (a : ActionChart) :
    ∃! theta : ℝ, 0 < theta ∧
      gravityFamily U c t0 a theta * cycleMass U c t0 a / c ^ 2 = radius c t0 := by
  refine ⟨circularSelector, ⟨circularSelector_pos,
    (circular_selector_iff hU hc ht0 a _).mpr rfl⟩, ?_⟩
  intro theta htheta
  exact (circular_selector_iff hU hc ht0 a theta).mp htheta.2

theorem circularGravity_eq (U c t0 : ℝ) (a : ActionChart) :
    circularGravity U c t0 a = c ^ 3 * radius c t0 ^ 2 / sectionAction U a := by
  rw [radius_eq]
  unfold circularGravity gravityFamily circularSelector
  ring

theorem circular_area_invariant {U c : ℝ} (t0 : ℝ)
    (hU : 0 < U) (hc : 0 < c) (a : ActionChart) :
    sectionAction U a * circularGravity U c t0 a / c ^ 3 = radius c t0 ^ 2 := by
  rw [circularGravity_eq]
  have ha := ne_of_gt (sectionAction_pos hU a)
  have hc0 := ne_of_gt hc
  field_simp

theorem gravity_return_ratio {U c t0 : ℝ}
    (hU : 0 < U) (hc : 0 < c) (ht0 : 0 < t0) :
    circularGravity U c t0 .pre / circularGravity U c t0 .ret =
      (actionRatio U)⁻¹ := by
  have ha := ne_of_gt (sectionAction_pos hU .pre)
  have hb := ne_of_gt (sectionAction_pos hU .ret)
  have hn : circularSelector * c ^ 5 * t0 ^ 2 ≠ 0 :=
    ne_of_gt (mul_pos (mul_pos circularSelector_pos (pow_pos hc 5)) (pow_pos ht0 2))
  change circularGravity U c t0 .pre / circularGravity U c t0 .ret =
    (sectionAction U .pre / sectionAction U .ret)⁻¹
  unfold circularGravity gravityFamily
  field_simp
  ring

theorem trit_information_pos : 0 < Real.log (3 : ℝ) := Real.log_pos (by norm_num)

theorem thermalCoefficient_pos {U t0 Theta : ℝ}
    (hU : 0 < U) (ht0 : 0 < t0) (hTheta : 0 < Theta) (a : ActionChart) :
    0 < thermalCoefficient U t0 Theta a :=
  div_pos (mul_pos (sectionAction_pos hU a) (frequency_pos ht0))
    (mul_pos hTheta trit_information_pos)

theorem thermal_coefficient_characterization (U t0 Theta b : ℝ)
    (hTheta : 0 < Theta) (a : ActionChart) :
    b * Theta * Real.log 3 = cycleEnergy U t0 a ↔
      b = thermalCoefficient U t0 Theta a := by
  have hd : Theta * Real.log 3 ≠ 0 := ne_of_gt (mul_pos hTheta trit_information_pos)
  rw [thermalCoefficient, eq_div_iff hd, mul_assoc]

theorem unique_positive_transducer {U t0 Theta : ℝ}
    (hU : 0 < U) (ht0 : 0 < t0) (hTheta : 0 < Theta) (a : ActionChart) :
    ∃! b : ℝ, 0 < b ∧ b * Theta * Real.log 3 = cycleEnergy U t0 a := by
  refine ⟨thermalCoefficient U t0 Theta a, ⟨?_,
    (thermal_coefficient_characterization U t0 Theta _ hTheta a).mpr rfl⟩, ?_⟩
  · exact thermalCoefficient_pos hU ht0 hTheta a
  · intro b hb
    exact (thermal_coefficient_characterization U t0 Theta b hTheta a).mp hb.2

theorem return_temperature_pos {U Theta : ℝ} (hU : 0 < U) (hTheta : 0 < Theta) :
    0 < returnTemperature U Theta :=
  div_pos (mul_pos hTheta (sectionAction_pos hU .ret)) (sectionAction_pos hU .pre)

theorem sectionTemperature_pos {U Theta : ℝ}
    (hU : 0 < U) (hTheta : 0 < Theta) (a : ActionChart) :
    0 < sectionTemperature U Theta a := by
  cases a
  · exact hTheta
  · exact return_temperature_pos hU hTheta

theorem return_preserves_transducer {U Theta : ℝ} (t0 : ℝ)
    (hU : 0 < U) (hTheta : 0 < Theta) :
    thermalCoefficient U t0 Theta .pre =
      thermalCoefficient U t0 (returnTemperature U Theta) .ret := by
  have ha := ne_of_gt (sectionAction_pos hU .pre)
  have hb := ne_of_gt (sectionAction_pos hU .ret)
  have ht := ne_of_gt hTheta
  have hi := ne_of_gt trit_information_pos
  dsimp [thermalCoefficient, returnTemperature, cycleEnergy]
  field_simp
  ring

theorem temperature_return_ratio {U Theta : ℝ} (hU : 0 < U) (hTheta : 0 < Theta) :
    Theta / returnTemperature U Theta = actionRatio U := by
  have ha := ne_of_gt (sectionAction_pos hU .pre)
  have hb := ne_of_gt (sectionAction_pos hU .ret)
  have ht := ne_of_gt hTheta
  change Theta / returnTemperature U Theta = sectionAction U .pre / sectionAction U .ret
  dsimp [returnTemperature]
  field_simp
  ring

theorem common_transducer_cycle_balance {U Theta : ℝ} (t0 : ℝ)
    (hU : 0 < U) (hTheta : 0 < Theta) (a : ActionChart) :
    thermalCoefficient U t0 Theta .pre * sectionTemperature U Theta a * Real.log 3 =
      cycleEnergy U t0 a := by
  cases a
  · exact (thermal_coefficient_characterization U t0 Theta _ hTheta .pre).mpr rfl
  · change thermalCoefficient U t0 Theta .pre * returnTemperature U Theta * Real.log 3 = _
    rw [return_preserves_transducer t0 hU hTheta]
    exact (thermal_coefficient_characterization U t0 (returnTemperature U Theta) _
      (return_temperature_pos hU hTheta) .ret).mpr rfl

theorem gravitational_thermal_area_identity {U c Theta : ℝ} (t0 : ℝ)
    (hU : 0 < U) (hc : 0 < c) (hTheta : 0 < Theta) (a : ActionChart) :
    circularGravity U c t0 a *
        (thermalCoefficient U t0 Theta .pre * sectionTemperature U Theta a * Real.log 3) =
      c ^ 3 * radius c t0 ^ 2 * frequency t0 := by
  rw [common_transducer_cycle_balance t0 hU hTheta a]
  have ha := (div_eq_iff (pow_ne_zero 3 (ne_of_gt hc))).mp
    (circular_area_invariant t0 hU hc a)
  calc
    circularGravity U c t0 a * cycleEnergy U t0 a =
        (sectionAction U a * circularGravity U c t0 a) * frequency t0 := by
          dsimp [cycleEnergy]; ring
    _ = (radius c t0 ^ 2 * c ^ 3) * frequency t0 := by rw [ha]
    _ = c ^ 3 * radius c t0 ^ 2 * frequency t0 := by ring

theorem reciprocal_joint_return {U c t0 Theta : ℝ}
    (hU : 0 < U) (hc : 0 < c) (ht0 : 0 < t0) (hTheta : 0 < Theta) :
    (circularGravity U c t0 .pre / circularGravity U c t0 .ret) *
      (Theta / returnTemperature U Theta) = 1 := by
  rw [gravity_return_ratio hU hc ht0, temperature_return_ratio hU hTheta]
  exact inv_mul_cancel₀ (ne_of_gt (lt_trans zero_lt_one (action_ratio_gt_one hU)))

/-- Selected HMT action feeds both realizations. Only positive dimensional
charts remain as hypotheses; no register equality or target value is assumed. -/
theorem selected_action_gravity_thermal_chain {U c t0 Theta : ℝ}
    (hU : 0 < U) (hc : 0 < c) (ht0 : 0 < t0) (hTheta : 0 < Theta) :
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (∀ (a : ActionChart) (theta : ℝ),
      gravityFamily U c t0 a theta * cycleMass U c t0 a / c ^ 2 = radius c t0 ↔
        theta = circularSelector) ∧
    (∀ a : ActionChart, ∃! b : ℝ, 0 < b ∧
      b * sectionTemperature U Theta a * Real.log 3 = cycleEnergy U t0 a) ∧
    (∀ a : ActionChart,
      thermalCoefficient U t0 Theta .pre * sectionTemperature U Theta a * Real.log 3 =
        cycleEnergy U t0 a) ∧
    (∀ a : ActionChart,
      sectionAction U a * circularGravity U c t0 a / c ^ 3 = radius c t0 ^ 2) ∧
    (∀ a : ActionChart,
      circularGravity U c t0 a *
          (thermalCoefficient U t0 Theta .pre * sectionTemperature U Theta a * Real.log 3) =
        c ^ 3 * radius c t0 ^ 2 * frequency t0) ∧
    (circularGravity U c t0 .pre / circularGravity U c t0 .ret) *
      (Theta / returnTemperature U Theta) = 1 := by
  exact ⟨action_decimal_order, circular_selector_iff hU hc ht0,
    fun a => unique_positive_transducer hU ht0 (sectionTemperature_pos hU hTheta a) a,
    common_transducer_cycle_balance t0 hU hTheta,
    circular_area_invariant t0 hU hc,
    gravitational_thermal_area_identity t0 hU hc hTheta,
    reciprocal_joint_return hU hc ht0 hTheta⟩

end HMT.II.SelectedActionGravityThermal
end

#print axioms HMT.II.SelectedActionGravityThermal.selected_action_gravity_thermal_chain
#print axioms HMT.II.SelectedActionGravityThermal.thermalCoefficient_pos
