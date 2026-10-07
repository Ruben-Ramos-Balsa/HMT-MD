import MarkedNeighborGroup

/-!
Rational full span and coordinate denominator bound for the constructed
marked neighbour.  Rank is computed in its rational span, not postulated as
a property of a named lattice.  No determinant or Leech classification is
asserted by this file.
-/
namespace HMT.IV.NeighborSpan

open HMT.IV.CoxeterNeighbor

theorem integer_coordinates_mem_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (a b : Fin n → ℤ) :
    (fun i => ((a i : ℚ), (b i : ℚ))) ∈ glue C := by
  refine ⟨a, b, 0, by simpa using C.zero_mem, ?_⟩
  intro i
  simp

theorem radial_mem_glue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) : radial t ∈ glue C := by
  have h := integer_coordinates_mem_glue C
    (fun i => 1 + 3 * t i) (fun i => 1 + 3 * t i)
  simpa only [radial, Int.cast_add, Int.cast_one, Int.cast_mul, Int.cast_ofNat] using h

def simpleRoot {n : ℕ} (i : Fin n) (second : Bool) : Space n :=
  fun j => if j = i then (if second then (0, 1) else (1, 0)) else (0, 0)

theorem simpleRoot_mem_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (i : Fin n) (second : Bool) :
    simpleRoot i second ∈ glue C := by
  convert integer_coordinates_mem_glue C
    (fun j => if j = i then (if second then 0 else 1) else 0)
    (fun j => if j = i then (if second then 1 else 0) else 0) using 1
  funext j
  cases second <;> by_cases h : j = i <;> simp [simpleRoot, h]

theorem triple_glue_mem_kernel {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n)
    (hC : IntegralGlue C) (hv : v ∈ glue C) {x : Space n}
    (hx : x ∈ glue C) : (3 : ℚ) • x ∈ kernel C v := by
  obtain ⟨k, hk⟩ := hC x hx v hv
  refine ⟨?_, k, ?_⟩
  · simpa using (glue C).nsmul_mem hx 3
  · rw [pairing_smul_left, hk]

theorem kernel_mem_neighbor {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n) {x : Space n}
    (hx : x ∈ kernel C v) : x ∈ neighbor C v := by
  exact ⟨x, hx, 0, by simp⟩

theorem simpleRoot_mem_neighbor_span {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n)
    (hC : IntegralGlue C) (hv : v ∈ glue C) (i : Fin n) (second : Bool) :
    simpleRoot i second ∈ Submodule.span ℚ (neighbor C v) := by
  have h : (3 : ℚ) • simpleRoot i second ∈ Submodule.span ℚ (neighbor C v) :=
    Submodule.subset_span (kernel_mem_neighbor C v
    (triple_glue_mem_kernel C v hC hv (simpleRoot_mem_glue C i second)))
  have hs := (Submodule.span ℚ (neighbor C v)).smul_mem (1 / 3 : ℚ) h
  simpa only [smul_smul, one_div_mul_cancel (by norm_num : (3 : ℚ) ≠ 0),
    one_smul] using hs

theorem simpleRoot_decomposition {n : ℕ} (x : Space n) :
    x = ∑ i, ((x i).1 • simpleRoot i false + (x i).2 • simpleRoot i true) := by
  funext j
  rw [Finset.sum_apply, Finset.sum_eq_single j]
  · simp [simpleRoot]
  · intro i _ hij
    simp [simpleRoot, Ne.symm hij]
  · simp

theorem neighbor_rational_span_eq_top {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n)
    (hC : IntegralGlue C) (hv : v ∈ glue C) :
    Submodule.span ℚ (neighbor C v) = ⊤ := by
  apply top_unique
  intro x _
  rw [simpleRoot_decomposition x]
  apply Submodule.sum_mem
  intro i _
  exact Submodule.add_mem _
    (Submodule.smul_mem _ _ (simpleRoot_mem_neighbor_span C v hC hv i false))
    (Submodule.smul_mem _ _ (simpleRoot_mem_neighbor_span C v hC hv i true))

theorem witt_marked_rational_span (o : Fin 12) :
    Submodule.span ℚ (neighbor wittCode (radial (marked o))) = ⊤ :=
  neighbor_rational_span_eq_top _ _
    (integralGlue_of_selfOrthogonal _ wittCode_selfOrthogonal)
    (radial_mem_glue _ _)

theorem witt_marked_rational_dimension (o : Fin 12) :
    Module.finrank ℚ (Submodule.span ℚ (neighbor wittCode (radial (marked o)))) = 24 := by
  rw [witt_marked_rational_span]
  simp [Space, Module.finrank_pi_fintype, Module.finrank_prod]

theorem neighbor_coordinates_thirds {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) {x : Space n}
    (hx : x ∈ neighbor C (radial t)) :
    ∃ a b : Fin n → ℤ, ∀ i, x i = ((a i : ℚ) / 3, (b i : ℚ) / 3) := by
  obtain ⟨y, hy, k, rfl⟩ := hx
  obtain ⟨a, b, c, hc, hcoord⟩ := hy.1
  refine ⟨(fun i => 3 * a i + 2 * c i + k * (1 + 3 * t i)),
    (fun i => 3 * b i + c i + k * (1 + 3 * t i)), ?_⟩
  intro i
  simp only [Pi.add_apply, Pi.smul_apply, hcoord, radial]
  ext <;> simp <;> ring

#print axioms integer_coordinates_mem_glue
#print axioms radial_mem_glue
#print axioms simpleRoot_mem_glue
#print axioms triple_glue_mem_kernel
#print axioms kernel_mem_neighbor
#print axioms simpleRoot_mem_neighbor_span
#print axioms simpleRoot_decomposition
#print axioms neighbor_rational_span_eq_top
#print axioms witt_marked_rational_span
#print axioms witt_marked_rational_dimension
#print axioms neighbor_coordinates_thirds

end HMT.IV.NeighborSpan
