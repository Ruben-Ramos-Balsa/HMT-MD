import DiagonalReturn

/-!
The mass congruence on a finite complex route fiber. The basal operator may
be any positive operator; diagonality is used only for the scalar restriction.
The reference section/calibration is retained as a separate basal factor.
-/
namespace HMT.VI.MassOperator
noncomputable section

variable {Route : Type*} [Fintype Route] [DecidableEq Route]

def corrected (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) (M₀ : End Route) : End Route :=
  (scale Ract κ r).comp (M₀.comp (scale Ract κ r))

theorem corrected_positive (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader)
    (M₀ : End Route) (hM : M₀.IsPositive) : (corrected Ract κ r M₀).IsPositive := by
  have h := hM.adjoint_conj (scale Ract κ r)
  simpa only [(scale_selfAdjoint Ract κ r).adjoint_eq, corrected,
    ContinuousLinearMap.comp_assoc] using h

theorem corrected_selfAdjoint (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader)
    (M₀ : End Route) (hM : M₀.IsPositive) : IsSelfAdjoint (corrected Ract κ r M₀) :=
  (corrected_positive Ract κ r M₀ hM).isSelfAdjoint

theorem corrected_inner (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader)
    (M₀ : End Route) (v : Fiber Route) :
    inner ℂ v (corrected Ract κ r M₀ v) =
      inner ℂ (scale Ract κ r v) (M₀ (scale Ract κ r v)) := by
  change inner ℂ v (scale Ract κ r (M₀ (scale Ract κ r v))) = _
  rw [← ContinuousLinearMap.adjoint_inner_left, (scale_selfAdjoint Ract κ r).adjoint_eq]

theorem corrected_diagonal {Ract : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) (m₀ : Route → ℝ) :
    corrected Ract κ r (diagonal m₀) = diagonal (fun γ => m₀ γ * Ract ^ (κ r γ)) := by
  rw [corrected, scale, diagonal_comp, diagonal_comp]
  congr 1
  funext γ
  calc
    scaleCoefficient Ract (κ r γ) * (m₀ γ * scaleCoefficient Ract (κ r γ)) =
      m₀ γ * scaleCoefficient Ract (κ r γ) ^ 2 := by ring
    _ = m₀ γ * Ract ^ (κ r γ) := by rw [scaleCoefficient_sq hR]

theorem corrected_diagonal_basis {Ract : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) (m₀ : Route → ℝ) (γ : Route) :
    corrected Ract κ r (diagonal m₀) (routeBasis γ) =
      (m₀ γ * Ract ^ (κ r γ) : ℝ) • routeBasis γ := by
  rw [corrected_diagonal hR]
  simpa only [Complex.coe_smul] using diagonal_basis (fun δ => m₀ δ * Ract ^ (κ r δ)) γ

omit [Fintype Route] [DecidableEq Route] in
theorem corrected_scalar_pos {Ract : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) (m₀ : Route → ℝ)
    (hm : ∀ γ, 0 < m₀ γ) (γ : Route) : 0 < m₀ γ * Ract ^ (κ r γ) :=
  mul_pos (hm γ) (Real.rpow_pos_of_pos hR _)

/-- An explicit positive-character interface; a concrete character theorem instantiates it. -/
def calibratedBasal (mRef : ℝ) (χrelative : Route → ℝ) : End Route :=
  diagonal (fun γ => mRef * χrelative γ)

theorem calibratedBasal_positive {mRef : ℝ} (hmRef : 0 < mRef)
    (χrelative : Route → ℝ) (hχ : ∀ γ, 0 < χrelative γ) :
    (calibratedBasal mRef χrelative).IsPositive :=
  diagonal_positive _ (fun γ => (mul_pos hmRef (hχ γ)).le)

theorem calibrated_corrected_basis {Ract mRef : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) (χrelative : Route → ℝ) (γ : Route) :
    corrected Ract κ r (calibratedBasal mRef χrelative) (routeBasis γ) =
      (mRef * χrelative γ * Ract ^ (κ r γ) : ℝ) • routeBasis γ :=
  corrected_diagonal_basis hR κ r (fun δ => mRef * χrelative δ) γ

/-- This separate zero operator is not obtained by making a positive character vanish. -/
def nullOperator : End Route := 0

theorem nullOperator_corrected (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) :
    corrected Ract κ r (nullOperator : End Route) = nullOperator := by
  simp [corrected, nullOperator]

#print axioms corrected_positive
#print axioms corrected_inner
#print axioms corrected_diagonal
#print axioms corrected_diagonal_basis
#print axioms corrected_scalar_pos
#print axioms calibratedBasal_positive
#print axioms calibrated_corrected_basis
#print axioms nullOperator_corrected

end
end HMT.VI.MassOperator
