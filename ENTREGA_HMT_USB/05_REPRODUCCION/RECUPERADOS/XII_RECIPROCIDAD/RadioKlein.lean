import Mathlib.Tactic

/-! Rational radius charts and reciprocal symmetry. These theorems concern
    real algebra only; no hyperbolic distance or physical realization is asserted. -/

namespace RadioKlein

noncomputable section

def poincare (r : ℝ) : ℝ := (r ^ 2 - 1) / (r ^ 2 + 1)
def angularContrast (r : ℝ) : ℝ := (1 - r ^ 4) / (1 + r ^ 4)
def kleinCoord (r : ℝ) : ℝ := -angularContrast r

/-- `orientation` is an angular orientation label. No identification with a
    radion action sign or physical parameter is assumed. -/
def etaRet (a orientation r : ℝ) : ℝ :=
  a * (500 * orientation * angularContrast r - 1)

theorem denominator_positive (r : ℝ) : 0 < r ^ 2 + 1 := by positivity

theorem poincare_lower {r : ℝ} (hr : 0 < r) : -1 < poincare r := by
  rw [poincare, lt_div_iff₀ (denominator_positive r)]
  nlinarith [sq_pos_of_pos hr]

theorem poincare_upper (r : ℝ) : poincare r < 1 := by
  rw [poincare, div_lt_iff₀ (denominator_positive r)]
  nlinarith

theorem poincare_interval {r : ℝ} (hr : 0 < r) :
    -1 < poincare r ∧ poincare r < 1 :=
  ⟨poincare_lower hr, poincare_upper r⟩

theorem poincare_to_klein (r : ℝ) :
    2 * poincare r / (1 + poincare r ^ 2) = kleinCoord r := by
  have h2 : r ^ 2 + 1 ≠ 0 := ne_of_gt (denominator_positive r)
  have h4 : 1 + r ^ 4 ≠ 0 := by positivity
  have hw : 1 + ((r ^ 2 - 1) / (r ^ 2 + 1)) ^ 2 ≠ 0 := by positivity
  unfold poincare kleinCoord angularContrast
  field_simp
  ring

theorem poincare_reciprocal {r : ℝ} (hr : 0 < r) :
    poincare r⁻¹ = -poincare r := by
  have hn : r ≠ 0 := ne_of_gt hr
  unfold poincare
  field_simp
  ring_nf
  simp

theorem angularContrast_reciprocal {r : ℝ} (hr : 0 < r) :
    angularContrast r⁻¹ = -angularContrast r := by
  have hn : r ≠ 0 := ne_of_gt hr
  unfold angularContrast
  field_simp
  ring_nf
  simp

theorem kleinCoord_reciprocal {r : ℝ} (hr : 0 < r) :
    kleinCoord r⁻¹ = -kleinCoord r := by
  simp [kleinCoord, angularContrast_reciprocal hr]

theorem etaRet_reciprocal (a orientation : ℝ) {r : ℝ} (hr : 0 < r) :
    etaRet a (-orientation) r⁻¹ = etaRet a orientation r := by
  unfold etaRet
  rw [angularContrast_reciprocal hr]
  ring

theorem etaRet_positive_iff_reciprocal (a orientation : ℝ) {r : ℝ} (hr : 0 < r) :
    0 < etaRet a (-orientation) r⁻¹ ↔ 0 < etaRet a orientation r := by
  rw [etaRet_reciprocal a orientation hr]

theorem radius_squared_recovery (r : ℝ) :
    r ^ 2 = (1 + poincare r) / (1 - poincare r) := by
  have h2 : r ^ 2 + 1 ≠ 0 := ne_of_gt (denominator_positive r)
  have hw : 1 - poincare r ≠ 0 := ne_of_gt (sub_pos.mpr (poincare_upper r))
  unfold poincare at *
  field_simp
  ring

#print axioms poincare_interval
#print axioms poincare_to_klein
#print axioms poincare_reciprocal
#print axioms angularContrast_reciprocal
#print axioms kleinCoord_reciprocal
#print axioms etaRet_reciprocal
#print axioms etaRet_positive_iff_reciprocal
#print axioms radius_squared_recovery

end
end RadioKlein
