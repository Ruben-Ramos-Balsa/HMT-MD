import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Data.Int.Interval
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic

/-! Exact shells of the actual lattice ℤ³. No cardinality is supplied as data.
This is the periodic realization used downstream in Article V, section 71. -/
namespace HMT.V.ThermodynamicLimit
noncomputable section
open Finset

abbrev Lattice := Fin 3 → ℤ
abbrev Space := EuclideanSpace ℝ (Fin 3)

def latticePoint (ν : Lattice) : Space := WithLp.toLp 2 (fun i => (ν i : ℝ))
def radius (ν : Lattice) : ℝ := ‖latticePoint ν‖
def supRadius (ν : Lattice) : ℕ := max (ν 0).natAbs (max (ν 1).natAbs (ν 2).natAbs)

def cube (m : ℕ) : Finset Lattice :=
  Fintype.piFinset (fun _ : Fin 3 => Finset.Icc (-(m : ℤ)) (m : ℤ))

def shell (m : ℕ) : Finset Lattice := (cube m).filter (fun ν => supRadius ν = m)

theorem supRadius_le_iff (ν : Lattice) (m : ℕ) :
    supRadius ν ≤ m ↔ ∀ i, (ν i).natAbs ≤ m := by
  simp only [supRadius, max_le_iff]
  constructor
  · rintro ⟨h0, h1, h2⟩ i
    fin_cases i <;> assumption
  · intro h
    exact ⟨h 0, h 1, h 2⟩

theorem natAbs_le_iff_interval (z : ℤ) (m : ℕ) :
    z.natAbs ≤ m ↔ -(m : ℤ) ≤ z ∧ z ≤ m := by
  rw [← Nat.cast_le (α := ℤ), Int.natCast_natAbs, abs_le]

theorem mem_cube {ν : Lattice} {m : ℕ} : ν ∈ cube m ↔ supRadius ν ≤ m := by
  simp only [cube, Fintype.mem_piFinset, Finset.mem_Icc, supRadius_le_iff,
    natAbs_le_iff_interval]

theorem mem_shell {ν : Lattice} {m : ℕ} : ν ∈ shell m ↔ supRadius ν = m := by
  simp only [shell, Finset.mem_filter, mem_cube]
  exact ⟨fun h => h.2, fun h => ⟨h.le, h⟩⟩

theorem cube_mono {m n : ℕ} (h : m ≤ n) : cube m ⊆ cube n :=
  fun _ hν => mem_cube.2 ((mem_cube.1 hν).trans h)

theorem card_cube (m : ℕ) : (cube m).card = (2 * m + 1) ^ 3 := by
  simp only [cube, Fintype.card_piFinset, Int.card_Icc]
  have h : ((m : ℤ) + 1 - -(m : ℤ)).toNat = 2 * m + 1 := by omega
  rw [h]
  simp

theorem shell_succ (m : ℕ) : shell (m + 1) = cube (m + 1) \ cube m := by
  ext ν
  simp only [mem_shell, mem_sdiff, mem_cube]
  omega

theorem card_shell_succ (m : ℕ) : (shell (m + 1)).card = 24 * (m + 1) ^ 2 + 2 := by
  rw [shell_succ, Finset.card_sdiff (cube_mono (Nat.le_succ m)), card_cube, card_cube]
  have h : (2 * (m + 1) + 1) ^ 3 = (2 * m + 1) ^ 3 + (24 * (m + 1) ^ 2 + 2) := by ring
  rw [h, Nat.add_sub_cancel_left]

theorem card_shell {m : ℕ} (hm : 1 ≤ m) : (shell m).card = 24 * m ^ 2 + 2 := by
  obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : m ≠ 0)
  exact card_shell_succ n

theorem supRadius_zero_iff (ν : Lattice) : supRadius ν = 0 ↔ ν = 0 := by
  constructor
  · intro h
    have hi := (supRadius_le_iff ν 0).1 h.le
    funext i
    have hz : (ν i).natAbs = 0 := Nat.eq_zero_of_le_zero (hi i)
    exact Int.natAbs_eq_zero.1 hz
  · rintro rfl
    simp [supRadius]

theorem shell_zero : shell 0 = {0} := by
  ext ν
  simp only [mem_shell, mem_singleton, supRadius_zero_iff]

theorem shell_nonzero {m : ℕ} (hm : 1 ≤ m) {ν : Lattice} (hν : ν ∈ shell m) : ν ≠ 0 := by
  intro h
  have hz := (supRadius_zero_iff ν).2 h
  have he := mem_shell.1 hν
  omega

theorem radius_nonneg (ν : Lattice) : 0 ≤ radius ν := norm_nonneg _

theorem radius_sq (ν : Lattice) :
    radius ν ^ 2 = (ν 0 : ℝ) ^ 2 + (ν 1 : ℝ) ^ 2 + (ν 2 : ℝ) ^ 2 := by
  simp [radius, latticePoint, PiLp.norm_sq_eq_of_L2, Fin.sum_univ_three, Real.norm_eq_abs, sq_abs]

theorem natAbs_real (z : ℤ) : (z.natAbs : ℝ) = |(z : ℝ)| := by
  simpa only [Int.cast_natCast, Int.cast_abs] using
    congrArg (fun n : ℤ => (n : ℝ)) (Int.natCast_natAbs z)

theorem supRadius_le_radius (ν : Lattice) : (supRadius ν : ℝ) ≤ radius ν := by
  simp only [supRadius, Nat.cast_max, max_le_iff, natAbs_real]
  have h (i : Fin 3) : |(ν i : ℝ)| ≤ radius ν := by
    simpa only [latticePoint, radius, Real.norm_eq_abs] using PiLp.norm_apply_le (latticePoint ν) i
  exact ⟨h 0, h 1, h 2⟩

theorem radius_le_sqrt_three_supRadius (ν : Lattice) :
    radius ν ≤ Real.sqrt 3 * (supRadius ν : ℝ) := by
  have hi := (supRadius_le_iff ν (supRadius ν)).1 le_rfl
  have h (i : Fin 3) : (ν i : ℝ) ^ 2 ≤ (supRadius ν : ℝ) ^ 2 := by
    have hn : |(ν i : ℝ)| ≤ (supRadius ν : ℝ) := by
      rw [← natAbs_real]
      exact_mod_cast hi i
    nlinarith [sq_abs (ν i : ℝ), abs_nonneg (ν i : ℝ)]
  have hs : Real.sqrt 3 ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  have hp : 0 ≤ Real.sqrt 3 * (supRadius ν : ℝ) := mul_nonneg (Real.sqrt_nonneg _) (Nat.cast_nonneg _)
  have he := radius_sq ν
  nlinarith [h 0, h 1, h 2, radius_nonneg ν]

theorem radius_pos_iff (ν : Lattice) : 0 < radius ν ↔ ν ≠ 0 := by
  constructor
  · intro h hz
    subst ν
    have hz := radius_sq (0 : Lattice)
    norm_num at hz
    nlinarith
  · intro hν
    have hs : 0 < supRadius ν := Nat.pos_of_ne_zero (fun h => hν ((supRadius_zero_iff ν).1 h))
    exact lt_of_lt_of_le (by exact_mod_cast hs) (supRadius_le_radius ν)

theorem shell_radius_bounds {m : ℕ} {ν : Lattice} (hν : ν ∈ shell m) :
    (m : ℝ) ≤ radius ν ∧ radius ν ≤ Real.sqrt 3 * m := by
  constructor
  · simpa only [mem_shell.1 hν] using supRadius_le_radius ν
  · simpa only [mem_shell.1 hν] using radius_le_sqrt_three_supRadius ν

#print axioms card_cube
#print axioms card_shell
#print axioms shell_zero
#print axioms radius_sq
#print axioms supRadius_le_radius
#print axioms radius_le_sqrt_three_supRadius
#print axioms radius_pos_iff
#print axioms shell_radius_bounds

end
end HMT.V.ThermodynamicLimit
