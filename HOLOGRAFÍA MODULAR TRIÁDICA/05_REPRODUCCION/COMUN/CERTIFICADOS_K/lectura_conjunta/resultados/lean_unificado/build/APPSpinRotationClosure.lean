import APPSpinBridge
import ElectronSpinRotation

/-!
# APP principal-plane spinorial transport

This file composes the actual APP-plane embedding with the already proved
spinorial rotation. The complexified APP plane is represented by its real and
imaginary ambient vectors; hence the return statements below are statements
about produced APP vectors, not only about independent 2-by-2 matrices.

The ambient basis is constructed by APPSpinBridge from the additive and
multiplicative projections and the selected TRIT eigenmode. The trigonometric
angle is the downstream spinorial chart; it is not an input to APP generation.
-/

noncomputable section
open Matrix

namespace HMT.I.APPSpinRotationClosure

open APPSpinBridge

abbrev Spinor := Fin 2 → ℂ
abbrev ComplexAPPPlane := Ambient × Ambient

def realCoordinates (v : Spinor) : LocalPlane :=
  WithLp.toLp 2 (fun i => (v i).re)

def imagCoordinates (v : Spinor) : LocalPlane :=
  WithLp.toLp 2 (fun i => (v i).im)

def complexEmbedding (v : Spinor) : ComplexAPPPlane :=
  (planeEmbedding (realCoordinates v), planeEmbedding (imagCoordinates v))

theorem realCoordinates_neg (v : Spinor) : realCoordinates (-v) = -realCoordinates v := by
  ext i
  simp [realCoordinates]

theorem imagCoordinates_neg (v : Spinor) : imagCoordinates (-v) = -imagCoordinates v := by
  ext i
  simp [imagCoordinates]

theorem complexEmbedding_neg (v : Spinor) : complexEmbedding (-v) = -complexEmbedding v := by
  simp only [complexEmbedding, realCoordinates_neg, imagCoordinates_neg, map_neg,
    Prod.neg_mk]

theorem complexEmbedding_injective : Function.Injective complexEmbedding := by
  intro v w h
  have hr := planeEmbedding.injective (congrArg Prod.fst h)
  have hi := planeEmbedding.injective (congrArg Prod.snd h)
  funext i
  apply Complex.ext
  · exact congrArg (fun z : LocalPlane => z i) hr
  · exact congrArg (fun z : LocalPlane => z i) hi

/-- Transport of a spinor in the complexification of the produced APP plane. -/
def transportedAPPState (n : Fin 3 → ℝ) (theta : ℝ) (v : Spinor) : ComplexAPPPlane :=
  complexEmbedding (ElectronSpinRotation.rotation n theta *ᵥ v)

theorem APP_two_pi_return (n : Fin 3 → ℝ) (v : Spinor) :
    transportedAPPState n (2 * Real.pi) v = -complexEmbedding v := by
  rw [transportedAPPState, ElectronSpinRotation.two_pi_vector, complexEmbedding_neg]

theorem APP_four_pi_return (n : Fin 3 → ℝ) (v : Spinor) :
    transportedAPPState n (4 * Real.pi) v = complexEmbedding v := by
  rw [transportedAPPState, ElectronSpinRotation.four_pi_vector]

theorem APP_rotation_composition (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (a b : ℝ) (v : Spinor) :
    transportedAPPState n (a + b) v =
      transportedAPPState n a (ElectronSpinRotation.rotation n b *ᵥ v) := by
  unfold transportedAPPState
  rw [ElectronSpinRotation.composition n hn, Matrix.mulVec_mulVec]

/-- Both components reside in the same actual APP principal plane. -/
theorem transported_state_residence (n : Fin 3 → ℝ) (theta : ℝ) (v : Spinor) :
    (transportedAPPState n theta v).1 ∈ principalPlane ∧
      (transportedAPPState n theta v).2 ∈ principalPlane := by
  exact ⟨⟨_, rfl⟩, ⟨_, rfl⟩⟩

/-- Assembly theorem: the real APP block and its faithful spinorial returns. -/
theorem actual_APP_spin_rotation (n : Fin 3 → ℝ) (u : LocalPlane) (v : Spinor) :
    ‖planeEmbedding u‖ = ‖u‖ ∧
    APPGlobalCommutator.sigmaProjection (planeEmbedding u) =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.P u) ∧
    APPGlobalCommutator.piProjection (planeEmbedding u) =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.Q u) ∧
    transportedAPPState n (2 * Real.pi) v = -complexEmbedding v ∧
    transportedAPPState n (4 * Real.pi) v = complexEmbedding v := by
  exact ⟨planeEmbedding.norm_map u, sigma_intertwining u, pi_intertwining u,
    APP_two_pi_return n v, APP_four_pi_return n v⟩

end HMT.I.APPSpinRotationClosure

#print axioms HMT.I.APPSpinRotationClosure.complexEmbedding_injective
#print axioms HMT.I.APPSpinRotationClosure.APP_two_pi_return
#print axioms HMT.I.APPSpinRotationClosure.APP_four_pi_return
#print axioms HMT.I.APPSpinRotationClosure.APP_rotation_composition
#print axioms HMT.I.APPSpinRotationClosure.transported_state_residence
#print axioms HMT.I.APPSpinRotationClosure.actual_APP_spin_rotation
