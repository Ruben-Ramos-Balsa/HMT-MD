import GlueSelfDual
import MarkedKernelIndex

/-!
Integral self-duality of the marked neighbour, obtained from self-duality
of the actual glued code. A simple root pairing to one is explicitly chosen
outside the marked coordinate. No determinant or lattice classification is
introduced as an assumption.
-/
namespace HMT.IV.NeighborDuality

open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality

theorem neighbor_integral_dual_of_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v g : Space n)
    (hC : IntegralGlue C)
    (hself : integralDual (glue C) = (glue C : Set (Space n)))
    (hv : v ∈ glue C) (hvv : pairing v v = 54)
    (hg : g ∈ glue C) (hgv : pairing g v = 1) :
    integralDual (neighborSubgroup C v) = (neighbor C v) := by
  ext x
  constructor
  · intro hx
    have h3g : (3 : ℚ) • g ∈ kernel C v := by
      refine ⟨?_, 1, ?_⟩
      · simpa using (glue C).nsmul_mem hg 3
      · rw [pairing_smul_left, hgv]
        norm_num
    have h3gn : (3 : ℚ) • g ∈ neighborSubgroup C v :=
      ⟨(3 : ℚ) • g, h3g, 0, by simp⟩
    obtain ⟨k, hk⟩ := hx _ h3gn
    rw [pairing_smul_right] at hk
    have hxg : pairing x g = (k : ℚ) / 3 := by linarith
    have hvn : (1 / 3 : ℚ) • v ∈ neighborSubgroup C v := by
      refine ⟨0, (kernelSubgroup C v).zero_mem, 1, ?_⟩
      simp
    obtain ⟨m, hm⟩ := hx _ hvn
    rw [pairing_smul_right] at hm
    have hxv : pairing x v = 3 * (m : ℚ) := by linarith
    let z : Space n := x + (-(k : ℚ) / 3) • v
    have hzdual : z ∈ integralDual (glue C) := by
      intro y hy
      obtain ⟨j, hj⟩ := hC y hy v hv
      have hym : y + (-(j : ℚ)) • g ∈ kernel C v := by
        refine ⟨(glue C).add_mem hy ?_, 0, ?_⟩
        · simpa using (glue C).zsmul_mem hg (-j)
        · rw [pairing_add_left, pairing_smul_left, hj, hgv]
          simp
      have hymn : y + (-(j : ℚ)) • g ∈ neighborSubgroup C v :=
        ⟨_, hym, 0, by simp⟩
      obtain ⟨l, hl⟩ := hx _ hymn
      refine ⟨l, ?_⟩
      calc
        pairing z y = pairing x (y + (-(j : ℚ)) • g) := by
          dsimp [z]
          rw [pairing_add_left, pairing_smul_left, pairing_comm v y,
            hj, pairing_add_right, pairing_smul_right, hxg]
          ring
        _ = (l : ℚ) := hl
    have hz : z ∈ glue C := by rwa [hself] at hzdual
    have hzker : z ∈ kernel C v := by
      refine ⟨hz, m - 6 * k, ?_⟩
      dsimp [z]
      rw [pairing_add_left, pairing_smul_left, hxv, hvv]
      push_cast
      ring
    refine ⟨z, hzker, k, ?_⟩
    dsimp [z]
    module
  · intro hx y hy
    exact integralNeighbor_of_integralGlue C v hC
      ⟨6, by rw [hvv]; norm_num⟩ x hx y hy

theorem marked_pairing_one_root (C : AddSubgroup (Fin 12 → ZMod 3))
    (o : Fin 12) : ∃ g ∈ glue C, pairing g (radial (marked o)) = 1 := by
  let r : Fin 12 := if o = 0 then 1 else 0
  have hr : r ≠ o := by
    dsimp [r]
    split_ifs with h
    · subst o
      decide
    · exact Ne.symm h
  refine ⟨simpleRoot r, simpleRoot_mem_glue C r, ?_⟩
  rw [simpleRoot_pairing_radial]
  simp [marked, hr]

theorem witt_marked_neighbor_selfDual (o : Fin 12) :
    integralDual (neighborSubgroup wittCode (radial (marked o))) =
      neighbor wittCode (radial (marked o)) := by
  obtain ⟨g, hg, hgv⟩ := marked_pairing_one_root wittCode o
  exact neighbor_integral_dual_of_glue wittCode _ g
    witt_glue_integral witt_glue_selfDual (radial_mem_glue _ _)
    (marked_radial_norm o) hg hgv

#print axioms neighbor_integral_dual_of_glue
#print axioms marked_pairing_one_root
#print axioms witt_marked_neighbor_selfDual

end HMT.IV.NeighborDuality
