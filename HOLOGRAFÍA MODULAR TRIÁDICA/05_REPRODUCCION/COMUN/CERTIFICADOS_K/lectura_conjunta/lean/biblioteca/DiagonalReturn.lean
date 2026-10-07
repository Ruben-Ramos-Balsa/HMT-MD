import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
Finite complex Hilbert fibers with the orthonormal route basis of Article VI.
Real return exponents are received with a retained reader label. No mass table
or electron calibration is used to construct the return operator.
-/
namespace HMT.VI.MassOperator
noncomputable section

inductive Reader where
  | D
  | Omega
  deriving DecidableEq, Repr

abbrev Fiber (Route : Type*) := EuclideanSpace ℂ Route
abbrev End (Route : Type*) [Fintype Route] := Fiber Route →L[ℂ] Fiber Route

variable {Route : Type*} [Fintype Route] [DecidableEq Route]

def routeBasis : OrthonormalBasis Route ℂ (Fiber Route) :=
  EuclideanSpace.basisFun Route ℂ

def diagonal (d : Route → ℝ) : End Route :=
  (Matrix.toEuclideanLin (Matrix.diagonal (fun γ => (d γ : ℂ)))).toContinuousLinearMap

@[simp] theorem diagonal_apply (d : Route → ℝ) (v : Fiber Route) (γ : Route) :
    diagonal d v γ = (d γ : ℂ) * v γ := by
  simp [diagonal, Matrix.toEuclideanLin_apply, Matrix.mulVec_diagonal]

theorem diagonal_basis (d : Route → ℝ) (γ : Route) :
    diagonal d (routeBasis γ) = (d γ : ℂ) • routeBasis γ := by
  ext δ
  simp [diagonal_apply, routeBasis, EuclideanSpace.basisFun_apply,
    Pi.single_apply]
  split_ifs <;> simp_all

theorem diagonal_comp (d e : Route → ℝ) :
    (diagonal d).comp (diagonal e) = diagonal (fun γ => d γ * e γ) := by
  ext v γ
  simp [diagonal_apply, mul_assoc]

@[simp] theorem diagonal_one : diagonal (fun _ : Route => 1) = 1 := by
  ext v γ
  simp

@[simp] theorem diagonal_zero : diagonal (fun _ : Route => 0) = 0 := by
  ext v γ
  simp

theorem diagonal_selfAdjoint (d : Route → ℝ) : IsSelfAdjoint (diagonal d) := by
  apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
  apply Matrix.isHermitian_iff_isSymmetric.mp
  apply Matrix.isHermitian_diagonal_iff.mpr
  intro γ
  change star (d γ : ℂ) = (d γ : ℂ)
  simp

theorem diagonal_positive (d : Route → ℝ) (hd : ∀ γ, 0 ≤ d γ) :
    (diagonal d).IsPositive := by
  have h := (ContinuousLinearMap.isPositive_one (𝕜 := ℂ) (E := Fiber Route)).adjoint_conj
    (diagonal (fun γ => Real.sqrt (d γ)))
  rw [(diagonal_selfAdjoint _).adjoint_eq] at h
  simpa only [ContinuousLinearMap.one_def, ContinuousLinearMap.id_comp, diagonal_comp, ← sq,
    Real.sq_sqrt (hd _)] using h

def returnOperator (κ : Reader → Route → ℝ) (r : Reader) : End Route := diagonal (κ r)

theorem returnOperator_basis (κ : Reader → Route → ℝ) (r : Reader) (γ : Route) :
    returnOperator κ r (routeBasis γ) = (κ r γ : ℂ) • routeBasis γ :=
  diagonal_basis (κ r) γ

theorem returnOperator_selfAdjoint (κ : Reader → Route → ℝ) (r : Reader) :
    IsSelfAdjoint (returnOperator κ r) := diagonal_selfAdjoint (κ r)

def scaleCoefficient (Ract k : ℝ) : ℝ := Ract ^ (k / 2)

theorem scaleCoefficient_pos {Ract : ℝ} (hR : 0 < Ract) (k : ℝ) :
    0 < scaleCoefficient Ract k := Real.rpow_pos_of_pos hR _

theorem scaleCoefficient_sq {Ract : ℝ} (hR : 0 < Ract) (k : ℝ) :
    scaleCoefficient Ract k ^ 2 = Ract ^ k := by
  rw [scaleCoefficient, sq, ← Real.rpow_add hR]
  congr 1
  ring

def scale (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) : End Route :=
  diagonal (fun γ => scaleCoefficient Ract (κ r γ))

def inverseScale (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) : End Route :=
  diagonal (fun γ => 1 / scaleCoefficient Ract (κ r γ))

theorem scale_basis (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) (γ : Route) :
    scale Ract κ r (routeBasis γ) =
      (scaleCoefficient Ract (κ r γ) : ℂ) • routeBasis γ := diagonal_basis _ γ

theorem scale_selfAdjoint (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) :
    IsSelfAdjoint (scale Ract κ r) := diagonal_selfAdjoint _

theorem scale_positive {Ract : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) : (scale Ract κ r).IsPositive :=
  diagonal_positive _ (fun γ => (scaleCoefficient_pos hR (κ r γ)).le)

theorem inverseScale_selfAdjoint (Ract : ℝ) (κ : Reader → Route → ℝ) (r : Reader) :
    IsSelfAdjoint (inverseScale Ract κ r) := diagonal_selfAdjoint _

theorem inverseScale_scale {Ract : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) :
    (inverseScale Ract κ r).comp (scale Ract κ r) = 1 := by
  rw [inverseScale, scale, diagonal_comp]
  have hc : (fun γ => 1 / scaleCoefficient Ract (κ r γ) * scaleCoefficient Ract (κ r γ)) =
      (fun _ : Route => (1 : ℝ)) := by
    funext γ
    exact one_div_mul_cancel (ne_of_gt (scaleCoefficient_pos hR (κ r γ)))
  rw [hc, diagonal_one]

theorem scale_inverseScale {Ract : ℝ} (hR : 0 < Ract)
    (κ : Reader → Route → ℝ) (r : Reader) :
    (scale Ract κ r).comp (inverseScale Ract κ r) = 1 := by
  rw [inverseScale, scale, diagonal_comp]
  have hc : (fun γ => scaleCoefficient Ract (κ r γ) * (1 / scaleCoefficient Ract (κ r γ))) =
      (fun _ : Route => (1 : ℝ)) := by
    funext γ
    exact mul_one_div_cancel (ne_of_gt (scaleCoefficient_pos hR (κ r γ)))
  rw [hc, diagonal_one]

/-- Invertibility is packaged only after both inverse laws have been proved. -/
def scaleUnit {Ract : ℝ} (hR : 0 < Ract) (κ : Reader → Route → ℝ) (r : Reader) :
    (End Route)ˣ where
  val := scale Ract κ r
  inv := inverseScale Ract κ r
  val_inv := scale_inverseScale hR κ r
  inv_val := inverseScale_scale hR κ r

#print axioms returnOperator_basis
#print axioms returnOperator_selfAdjoint
#print axioms scale_basis
#print axioms scaleCoefficient_sq
#print axioms scale_positive
#print axioms scale_selfAdjoint
#print axioms inverseScale_scale
#print axioms scale_inverseScale
#print axioms scaleUnit

end
end HMT.VI.MassOperator
