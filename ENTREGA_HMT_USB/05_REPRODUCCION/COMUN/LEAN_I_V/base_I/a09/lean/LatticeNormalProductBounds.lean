import LatticeNormalProductTerms
import LatticeSameSignModes

/-!
# Rectangular support bounds for double normal products

Each bound is pointwise on the actual input vector and on the fixed Laurent
coefficient. The finite rectangle is deduced from Laurent truncation and
the existing Heisenberg-mode action, not supplied as an extra hypothesis.
-/

noncomputable section
namespace HMT.IV.LatticeNormalProductBounds

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeNormalOrderedField
open HMT.IV.LatticeNormalProductTerms HMT.IV.LatticeSameSignModes

private theorem uniform_first_bound {V : Type*} [Zero V]
    (f : ℕ → ℕ → V) (M : ℕ)
    (hM : ∀ b ≥ M, ∀ a, f a b = 0)
    (hfirst : ∀ b, ∃ N : ℕ, ∀ a ≥ N, f a b = 0) :
    ∃ N : ℕ, ∀ a ≥ N, ∀ b, f a b = 0 := by
  classical
  choose bounds hbounds using hfirst
  let N : ℕ := (Finset.range M).sup bounds
  refine ⟨N, ?_⟩
  intro a ha b
  by_cases hb : b < M
  · have hle : bounds b ≤ N := Finset.le_sup (f := bounds) (Finset.mem_range.mpr hb)
    exact hbounds b a (hle.trans ha)
  · exact hM b (by omega) a

theorem cc_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, cc o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, cc o i j n m B k v a b = 0) := by
  obtain ⟨c, hc⟩ := field_has_bound o B v
  refine ⟨(k-c).toNat+1, (k-c).toNat+1, ?_, ?_⟩
  · intro a ha b
    have hz : HVertexOperator.coeff B ((k-(a : ℤ))-(b : ℤ)) v = 0 :=
      hc _ (by omega)
    simp only [cc, creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hz, map_zero, smul_zero]
  · intro b hb a
    have hz : HVertexOperator.coeff B ((k-(a : ℤ))-(b : ℤ)) v = 0 :=
      hc _ (by omega)
    simp only [cc, creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hz, map_zero, smul_zero]

theorem ca_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, ca o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, ca o i j n m B k v a b = 0) := by
  obtain ⟨M, hM⟩ := nonnegative_modes_bounded o v
  have hb : ∀ b ≥ M, ∀ a, ca o i j n m B k v a b = 0 := by
    intro b hb a
    simp only [ca, annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hM b hb j, map_zero, smul_zero]
  have hfirst : ∀ b, ∃ N : ℕ, ∀ a ≥ N, ca o i j n m B k v a b = 0 := by
    intro b
    obtain ⟨c, hc⟩ := field_has_bound o B (hmode o j (b : ℤ) v)
    refine ⟨(k+(b : ℤ)+m+1-c).toNat+1, ?_⟩
    intro a ha
    have hz : HVertexOperator.coeff B (k-(a : ℤ)+(b : ℤ)+m+1)
        (hmode o j (b : ℤ) v) = 0 := hc _ (by omega)
    simp only [ca, annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hz, map_zero, smul_zero]
  obtain ⟨N, hN⟩ := uniform_first_bound (ca o i j n m B k v) M hb hfirst
  exact ⟨N, M, hN, hb⟩

theorem ac_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, ac o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, ac o i j n m B k v a b = 0) := by
  obtain ⟨N, hN⟩ := nonnegative_modes_bounded o v
  have ha : ∀ a ≥ N, ∀ b, ac o i j n m B k v a b = 0 := by
    intro a ha b
    simp only [ac, hN a ha i, map_zero, smul_zero]
  have hsecond : ∀ a, ∃ M : ℕ, ∀ b ≥ M, ac o i j n m B k v a b = 0 := by
    intro a
    obtain ⟨c, hc⟩ := field_has_bound o B (hmode o i (a : ℤ) v)
    refine ⟨(k+(a : ℤ)+n+1-c).toNat+1, ?_⟩
    intro b hb
    have hz : HVertexOperator.coeff B ((k+(a : ℤ)+n+1)-(b : ℤ))
        (hmode o i (a : ℤ) v) = 0 := hc _ (by omega)
    simp only [ac, creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hz, map_zero, smul_zero]
  obtain ⟨M, hM⟩ := uniform_first_bound (fun b a => ac o i j n m B k v a b)
    N ha hsecond
  exact ⟨N, M, ha, hM⟩

theorem aa_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, aa o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, aa o i j n m B k v a b = 0) := by
  obtain ⟨N, hN⟩ := nonnegative_modes_bounded o v
  refine ⟨N, N, ?_, ?_⟩
  · intro a ha b
    simp only [aa, hN a ha i, map_zero, smul_zero]
  · intro b hb a
    have hswap : hmode o j (b : ℤ) (hmode o i (a : ℤ) v) =
        hmode o i (a : ℤ) (hmode o j (b : ℤ) v) :=
      LinearMap.congr_fun (nonnegative_hmodes_commute o j i b a) v
    have hz : hmode o j (b : ℤ) (hmode o i (a : ℤ) v) = 0 := by
      rw [hswap, hN b hb j, map_zero]
    simp only [aa, annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hz, map_zero, smul_zero]

end HMT.IV.LatticeNormalProductBounds
end

#print axioms HMT.IV.LatticeNormalProductBounds.cc_rectangle
#print axioms HMT.IV.LatticeNormalProductBounds.ca_rectangle
#print axioms HMT.IV.LatticeNormalProductBounds.ac_rectangle
#print axioms HMT.IV.LatticeNormalProductBounds.aa_rectangle
