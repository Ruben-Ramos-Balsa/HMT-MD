import MemorySeries
import Mathlib.Analysis.Normed.Lp.PiLp
import Mathlib.Logic.Equiv.Fin.Rotate

/-! Concrete twelve-coordinate register in the manuscript's ℓ¹ norm.
The sign/count event coefficients are supplied as integers bounded by nine;
the event's vector norm and the contractive transport hypothesis are proved.
-/

noncomputable section

namespace HMT.II.Memory.Cycle12

variable (𝕜 : Type*) [RCLike 𝕜]

abbrev Register := PiLp 1 (fun _ : Fin 12 => 𝕜)

def coordinate (j : Fin 12) : Register 𝕜 := WithLp.toLp 1 (Pi.single j 1)

def forward : Register 𝕜 ≃ₗᵢ[𝕜] Register 𝕜 :=
  LinearIsometryEquiv.piLpCongrLeft 1 𝕜 𝕜 (finRotate 12)

def backward : Register 𝕜 →L[𝕜] Register 𝕜 :=
  (forward 𝕜).symm.toLinearIsometry.toContinuousLinearMap

theorem norm_coordinate (j : Fin 12) : ‖coordinate 𝕜 j‖ = 1 := by
  simp [coordinate, PiLp.norm_eq_of_L1, Pi.single_apply]

theorem norm_backward_apply (y : Register 𝕜) : ‖backward 𝕜 y‖ = ‖y‖ :=
  (forward 𝕜).symm.norm_map y

theorem norm_backward_le : ‖backward 𝕜‖ ≤ 1 :=
  (forward 𝕜).symm.toLinearIsometry.norm_toContinuousLinearMap_le

/-- `S e_j = e_(j+1)` and `R = S⁻¹`, with indices modulo twelve. -/
theorem backward_coordinate (j : Fin 12) :
    backward 𝕜 (coordinate 𝕜 j) = coordinate 𝕜 (j - 1) := by
  change (LinearIsometryEquiv.piLpCongrLeft 1 𝕜 𝕜 (finRotate 12)).symm
    (WithLp.toLp 1 (Pi.single j 1)) = _
  rw [LinearIsometryEquiv.piLpCongrLeft_symm,
    LinearIsometryEquiv.piLpCongrLeft_single, finRotate_succ_symm_apply]
  rfl

def event (a : ℕ → ℤ) (m : ℕ) : Register 𝕜 :=
  (a m : 𝕜) • backward 𝕜 (coordinate 𝕜 0)

theorem norm_event_le (a : ℕ → ℤ) (ha : ∀ m, |(a m : ℝ)| ≤ 9) (m : ℕ) :
    ‖event 𝕜 a m‖ ≤ 9 := by
  rw [event, norm_smul, norm_backward_apply, norm_coordinate, mul_one,
    ← RCLike.ofReal_intCast (a m), RCLike.norm_ofReal]
  exact ha m

/-- No unproved norm-change from ℓ¹ to the usual product supremum norm occurs. -/
theorem series_eq_resolvent (a : ℕ → ℤ) (ha : ∀ m, |(a m : ℝ)| ≤ 9)
    (y₀ : Register 𝕜) (u : 𝕜) (hu : ‖u‖ < 1) :
    memorySeries (backward 𝕜) (event 𝕜 a) y₀ u =
      resolvent (backward 𝕜) u (y₀ + u • forcingSeries (event 𝕜 a) u) :=
  memorySeries_eq_resolvent _ (norm_backward_le 𝕜) _ 9 (norm_event_le 𝕜 a ha) y₀ u hu

theorem tail_bound (a : ℕ → ℤ) (ha : ∀ m, |(a m : ℝ)| ≤ 9)
    (y₀ : Register 𝕜) (ℓ : Register 𝕜 →L[𝕜] 𝕜)
    (r : ℝ) (hr₀ : 0 < r) (hr : r < 1) (u : 𝕜) (hu : ‖u‖ ≤ r) (N : ℕ) :
    ‖∑' n : ℕ, u ^ (n + (N + 1)) •
      ℓ (record (backward 𝕜) (event 𝕜 a) y₀ (n + (N + 1)))‖ ≤
      ‖ℓ‖ * r ^ (N + 1) *
        ((‖y₀‖ + 9 * (N + 1 : ℕ)) / (1 - r) + 9 * r / (1 - r) ^ 2) :=
  reader_tail_bound _ (norm_backward_le 𝕜) _ (norm_event_le 𝕜 a ha)
    y₀ ℓ r hr₀ hr u hu N

#print axioms backward_coordinate
#print axioms series_eq_resolvent
#print axioms tail_bound

end HMT.II.Memory.Cycle12
