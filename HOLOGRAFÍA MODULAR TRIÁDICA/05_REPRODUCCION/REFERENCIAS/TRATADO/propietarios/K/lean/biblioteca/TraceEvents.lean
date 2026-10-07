import Cycle12L1

/-! The exact event of `mem:evento`, read from a supplied integer-coded trace.
This module neither generates the trajectory nor identifies direction codes
with the cardinal-direction alphabet. Every window has nine distinct steps. -/

namespace HMT.II.Memory.TraceEvents

open scoped BigOperators

def windowStep (m : ℕ) (i : Fin 9) : ℕ := 9 * m + i.val + 1

theorem windowStep_injective (m : ℕ) : Function.Injective (windowStep m) := by
  intro i j h
  apply Fin.ext
  simp only [windowStep] at h
  omega

theorem windowStep_range (m t : ℕ) :
    (∃ i : Fin 9, windowStep m i = t) ↔ 9 * m + 1 ≤ t ∧ t ≤ 9 * m + 9 := by
  constructor
  · rintro ⟨i, rfl⟩
    have hi := i.isLt
    dsimp [windowStep]
    omega
  · rintro ⟨hl, hu⟩
    refine ⟨⟨t - (9 * m + 1), by omega⟩, ?_⟩
    simp only [windowStep]
    omega

/-- Cardinality of the occurrences with codes in `{2,4,6,8}` in window `m`. -/
def eventCount (d : ℕ → ℤ) (m : ℕ) : ℕ :=
  ∑ i : Fin 9, if d (windowStep m i) ∈ ({2, 4, 6, 8} : Finset ℤ) then 1 else 0

theorem eventCount_le_nine (d : ℕ → ℤ) (m : ℕ) : eventCount d m ≤ 9 := by
  calc
    eventCount d m ≤ ∑ _i : Fin 9, (1 : ℕ) := by
      apply Finset.sum_le_sum
      intro i _
      split <;> omega
    _ = 9 := by simp

/-- Signed coefficient, without a target-value choice of events or directions. -/
def signedCoefficient (d : ℕ → ℤ) (σ : ℕ → ℤ) (m : ℕ) : ℤ :=
  σ m * eventCount d m

theorem signedCoefficient_abs_le_nine (d : ℕ → ℤ) (σ : ℕ → ℤ)
    (hσ : ∀ m, σ m = 1 ∨ σ m = -1) (m : ℕ) :
    |(signedCoefficient d σ m : ℝ)| ≤ 9 := by
  have hc : (eventCount d m : ℝ) ≤ 9 := by exact_mod_cast eventCount_le_nine d m
  rcases hσ m with hs | hs
  · simpa [signedCoefficient, hs] using hc
  · simpa [signedCoefficient, hs] using hc

noncomputable section

variable (𝕜 : Type*) [RCLike 𝕜]

/-- The concrete memory series is now instantiated using the supplied trace;
the nine-event norm bound is proved internally, not a caller hypothesis. -/
theorem trace_series_eq_resolvent (d : ℕ → ℤ) (σ : ℕ → ℤ)
    (hσ : ∀ m, σ m = 1 ∨ σ m = -1)
    (y₀ : Cycle12.Register 𝕜) (u : 𝕜) (hu : ‖u‖ < 1) :
    memorySeries (Cycle12.backward 𝕜)
      (Cycle12.event 𝕜 (signedCoefficient d σ)) y₀ u =
      resolvent (Cycle12.backward 𝕜) u
        (y₀ + u • forcingSeries (Cycle12.event 𝕜 (signedCoefficient d σ)) u) :=
  Cycle12.series_eq_resolvent 𝕜 _ (signedCoefficient_abs_le_nine d σ hσ) y₀ u hu

theorem trace_reader_tail_bound (d : ℕ → ℤ) (σ : ℕ → ℤ)
    (hσ : ∀ m, σ m = 1 ∨ σ m = -1)
    (y₀ : Cycle12.Register 𝕜) (ℓ : Cycle12.Register 𝕜 →L[𝕜] 𝕜)
    (r : ℝ) (hr₀ : 0 < r) (hr : r < 1) (u : 𝕜) (hu : ‖u‖ ≤ r) (N : ℕ) :
    ‖∑' n : ℕ, u ^ (n + (N + 1)) •
      ℓ (record (Cycle12.backward 𝕜) (Cycle12.event 𝕜 (signedCoefficient d σ)) y₀
        (n + (N + 1)))‖ ≤
      ‖ℓ‖ * r ^ (N + 1) *
        ((‖y₀‖ + 9 * (N + 1 : ℕ)) / (1 - r) + 9 * r / (1 - r) ^ 2) :=
  Cycle12.tail_bound 𝕜 _ (signedCoefficient_abs_le_nine d σ hσ)
    y₀ ℓ r hr₀ hr u hu N

#print axioms signedCoefficient_abs_le_nine
#print axioms trace_series_eq_resolvent
#print axioms trace_reader_tail_bound

end

end HMT.II.Memory.TraceEvents
