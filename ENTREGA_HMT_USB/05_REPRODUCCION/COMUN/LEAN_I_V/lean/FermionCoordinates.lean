import Moments

/-! Every mode, not only the first mode, in the joint fermionic distribution. -/

namespace HMT.FockBridge

open scoped BigOperators

def stateCoordinateValue : (n : ℕ) → Fin n → Occupation n → ℝ
  | 0, i, _ => Fin.elim0 i
  | n + 1, i, s => Fin.cases (if s.1 then 1 else 0)
      (fun j => stateCoordinateValue n j s.2) i

noncomputable def coordinateMean (us : List ℝ) (i : Fin us.length) : ℝ :=
  ∑ s : Occupation us.length, stateCoordinateValue us.length i s * probability us s

theorem coordinateMean_zero (u : ℝ) (us : List ℝ) :
    coordinateMean (u :: us) (0 : Fin (us.length + 1)) = headMean u us := by
  unfold coordinateMean headMean
  apply Finset.sum_congr rfl
  intro s _
  cases h : s.1 <;> simp [stateCoordinateValue, h]

theorem coordinateMean_succ (u : ℝ) (us : List ℝ) (hu : 0 ≤ u)
    (i : Fin us.length) : coordinateMean (u :: us) i.succ = coordinateMean us i := by
  unfold coordinateMean
  change (∑ s : Bool × Occupation us.length,
    stateCoordinateValue us.length i s.2 * probability (u :: us) s) = _
  rw [Fintype.sum_prod_type_right]
  apply Finset.sum_congr rfl
  intro s _
  change (∑ b : Bool, stateCoordinateValue us.length i s *
    probability (u :: us) (b, s)) = _
  rw [← Finset.mul_sum, tail_marginal u us hu s]

/-- The FD marginal at every mode is derived from the complete joint distribution. -/
theorem coordinateMean_eq (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u)
    (i : Fin us.length) : coordinateMean us i = QuantumOccupations.fermionMean (us.get i) := by
  induction us with
  | nil => exact Fin.elim0 i
  | cons u us ih =>
    have ht : ∀ v ∈ us, 0 ≤ v := fun v hv => h v (by simp [hv])
    refine Fin.cases ?_ (fun j => ?_) i
    · rw [coordinateMean_zero, headMean_eq_single_mode u us ht]
      rfl
    · rw [coordinateMean_succ u us (h u (by simp)) j, ih ht j]
      rfl

theorem coordinateMean_fermi_dirac (us : List ℝ) (h : ∀ u ∈ us, 0 ≤ u)
    (i : Fin us.length) : coordinateMean us i = us.get i / (1 + us.get i) := by
  rw [coordinateMean_eq us h i, QuantumOccupations.fermion_mean_eq]

#print axioms coordinateMean_eq
#print axioms coordinateMean_fermi_dirac

end HMT.FockBridge
