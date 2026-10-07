import MarkedKernelIndex
import RootFreeWittNeighbor

/-! The constructed neighbour has minimum squared norm exactly four.
The lower bound uses proved parity and exclusion of roots; the upper bound
uses the difference of two displayed coordinate roots, in the actual kernel.
-/
namespace HMT.IV.NeighborMinimum

open HMT.IV.CoxeterNeighbor

theorem simpleRoot_pairing {n : ℕ} (i j : Fin n) :
    pairing (simpleRoot i) (simpleRoot j) = if i = j then 2 else 0 := by
  unfold pairing
  have h : ∀ k, localPair (simpleRoot i k) (simpleRoot j k) =
      if k = i then (if i = j then 2 else 0) else 0 := by
    intro k
    by_cases hki : k = i
    · subst k
      by_cases hij : i = j <;> simp [simpleRoot, hij, localPair]
    · simp [simpleRoot, hki, localPair]
  simp_rw [h]
  simp

theorem pairing_sub_left {n : ℕ} (x y z : Space n) :
    pairing (x - y) z = pairing x z - pairing y z := by
  have h : x - y = x + (-1 : ℚ) • y := by simp [sub_eq_add_neg]
  rw [h, pairing_add_left, pairing_smul_left]
  ring

theorem pairing_sub_right {n : ℕ} (x y z : Space n) :
    pairing x (y - z) = pairing x y - pairing x z := by
  rw [pairing_comm, pairing_sub_left, pairing_comm y x, pairing_comm z x]

theorem coordinate_root_difference_in_kernel {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) (i j : Fin n) :
    simpleRoot i - simpleRoot j ∈ kernel C (radial t) := by
  refine ⟨(glue C).sub_mem (simpleRoot_mem_glue C i) (simpleRoot_mem_glue C j),
    t i - t j, ?_⟩
  rw [pairing_sub_left, simpleRoot_pairing_radial, simpleRoot_pairing_radial]
  push_cast
  ring

theorem coordinate_root_difference_norm {n : ℕ} (i j : Fin n) (hij : i ≠ j) :
    pairing (simpleRoot i - simpleRoot j) (simpleRoot i - simpleRoot j) = 4 := by
  rw [pairing_sub_left, pairing_sub_right, pairing_sub_right]
  norm_num [simpleRoot_pairing, hij, Ne.symm hij]

theorem witt_marked_norm_ge_four (o : Fin 12) (x : Space 12)
    (hx : x ∈ neighbor wittCode (radial (marked o))) (hne : x ≠ 0) :
    4 ≤ pairing x x := by
  obtain ⟨k, hk⟩ := witt_marked_neighbor_even o x hx
  have hp : 0 < pairing x x :=
    lt_of_le_of_ne (pairing_self_nonneg x)
      (Ne.symm (fun h => hne ((pairing_self_eq_zero_iff x).mp h)))
  have htwo := witt_marked_neighbor_no_norm_two o x hx
  have hkp : 0 < k := by exact_mod_cast (show (0 : ℚ) < (k : ℚ) by linarith)
  have hk1 : k ≠ 1 := by
    intro he
    apply htwo
    rw [hk, he]
    norm_num
  have hk2 : (2 : ℤ) ≤ k := by omega
  have hk2q : (2 : ℚ) ≤ (k : ℚ) := by exact_mod_cast hk2
  linarith

theorem witt_marked_has_norm_four (o : Fin 12) :
    ∃ x ∈ neighbor wittCode (radial (marked o)), pairing x x = 4 := by
  let x : Space 12 := simpleRoot 0 - simpleRoot 1
  refine ⟨x, ?_, ?_⟩
  · exact ⟨x, coordinate_root_difference_in_kernel _ _ 0 1, 0, by simp⟩
  · exact coordinate_root_difference_norm 0 1 (by decide)

theorem witt_marked_minimum_exactly_four (o : Fin 12) :
    (∀ x ∈ neighbor wittCode (radial (marked o)), x ≠ 0 → 4 ≤ pairing x x) ∧
    (∃ x ∈ neighbor wittCode (radial (marked o)), pairing x x = 4) :=
  ⟨witt_marked_norm_ge_four o, witt_marked_has_norm_four o⟩

#print axioms simpleRoot_pairing
#print axioms pairing_sub_left
#print axioms pairing_sub_right
#print axioms coordinate_root_difference_in_kernel
#print axioms coordinate_root_difference_norm
#print axioms witt_marked_norm_ge_four
#print axioms witt_marked_has_norm_four
#print axioms witt_marked_minimum_exactly_four

end HMT.IV.NeighborMinimum
