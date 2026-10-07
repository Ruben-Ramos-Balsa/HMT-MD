import LatticeTwistedNormalTerms

/-! Pointwise rectangular support for the four contributions to iterated
divided half-normal products. The bounds follow from the Laurent condition
and positive-mode annihilation on the actual twisted carrier. -/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalBounds

open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedNormalTerms
open LatticeTwistedNormalProduct (field_has_bound)

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
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, cc o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, cc o i j n m B k v a b = 0) := by
  obtain ⟨c, hc⟩ := field_has_bound o B v
  refine ⟨(k+2*n+2*m+2-c).toNat+1, (k+2*n+2*m+2-c).toNat+1, ?_, ?_⟩
  · intro a ha b
    have hz : HVertexOperator.coeff B
        (k+2*n-2*(a:ℤ)+1+2*m-2*b+1) v = 0 := hc _ (by omega)
    simp only [cc, creationTerm_apply, hz, map_zero]
  · intro b hb a
    have hz : HVertexOperator.coeff B
        (k+2*n-2*(a:ℤ)+1+2*m-2*b+1) v = 0 := hc _ (by omega)
    simp only [cc, creationTerm_apply, hz, map_zero]

theorem ca_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, ca o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, ca o i j n m B k v a b = 0) := by
  obtain ⟨M, hM⟩ := annihilators_bounded o j m v
  have hb : ∀ b ≥ M, ∀ a, ca o i j n m B k v a b = 0 := by
    intro b hb a
    simp only [ca, annihilationTerm_apply, hM b hb, map_zero]
  have hfirst : ∀ b, ∃ N : ℕ, ∀ a ≥ N, ca o i j n m B k v a b = 0 := by
    intro b
    obtain ⟨c, hc⟩ := field_has_bound o B (annihilator o j m b v)
    refine ⟨(k+2*n+2*m+2*b+4-c).toNat+1, ?_⟩
    intro a ha
    have hz : HVertexOperator.coeff B
        (k+2*n-2*(a:ℤ)+1+2*m+2*b+3) (annihilator o j m b v) = 0 :=
      hc _ (by omega)
    simp only [ca, annihilationTerm_apply, hz, map_zero]
  obtain ⟨N, hN⟩ := uniform_first_bound (ca o i j n m B k v) M hb hfirst
  exact ⟨N, M, hN, hb⟩

theorem ac_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, ac o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, ac o i j n m B k v a b = 0) := by
  obtain ⟨M, N, hM, hN⟩ := ca_rectangle o j i m n B k v
  refine ⟨N, M, ?_, ?_⟩
  · intro a ha b
    rw [ac_swap]
    exact hN a ha b
  · intro b hb a
    rw [ac_swap]
    exact hM b hb a

theorem aa_rectangle (o : Fin 12) (i j : Fin (BasisSize o)) (n m : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    ∃ N M : ℕ,
      (∀ a ≥ N, ∀ b, aa o i j n m B k v a b = 0) ∧
      (∀ b ≥ M, ∀ a, aa o i j n m B k v a b = 0) := by
  obtain ⟨N, hN⟩ := annihilators_bounded o i n v
  obtain ⟨M, hM⟩ := annihilators_bounded o j m v
  refine ⟨N, M, ?_, ?_⟩
  · intro a ha b
    simp only [aa, hN a ha, map_zero]
  · intro b hb a
    have hz : annihilator o j m b (annihilator o i n a v) = 0 := by
      rw [annihilators_commute, hM b hb, map_zero]
    simp only [aa, annihilationTerm_apply, hz, map_zero]

end HMT.IV.LatticeTwistedNormalBounds
end

#print axioms HMT.IV.LatticeTwistedNormalBounds.cc_rectangle
#print axioms HMT.IV.LatticeTwistedNormalBounds.ca_rectangle
#print axioms HMT.IV.LatticeTwistedNormalBounds.ac_rectangle
#print axioms HMT.IV.LatticeTwistedNormalBounds.aa_rectangle
