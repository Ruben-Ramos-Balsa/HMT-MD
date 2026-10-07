import LatticeOscillatorFock

/-!
Pointwise truncation for the constructed algebraic oscillator carrier.
The set of modes is unbounded; for each particular algebraic state, finite
support supplies a bound above which every annihilation mode vanishes.
This is a theorem of the existing construction, not a field axiom.
-/

noncomputable section
namespace HMT.IV.LatticeFieldTruncation

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.FockTransport.Symmetric
open scoped TensorProduct

/-- A bound on the mode numbers occurring in an oscillator vector. -/
def oscillatorModeBound (o : Fin 12) (x : Oscillators o) : ℕ :=
  x.support.sup (fun p => p.1) + 1

theorem modeCovector_vanishes_above_support (o : Fin 12) (x : Oscillators o)
    (n : ℕ) (hn : oscillatorModeBound o x ≤ n) (i : Fin (BasisSize o)) :
    modeCovector o n i x = 0 := by
  classical
  unfold modeCovector
  rw [Finsupp.linearCombination_apply]
  unfold Finsupp.sum
  apply Finset.sum_eq_zero
  intro p hp
  have hpbound : p.1 ≤ x.support.sup (fun q => q.1) := Finset.le_sup hp
  have hne : n ≠ p.1 := by
    unfold oscillatorModeBound at hn
    omega
  simp [hne]

/-- For every algebraic Fock state, all sufficiently high annihilation
modes vanish, with a single bound valid for every lattice-basis index. -/
theorem exists_annihilation_bound (o : Fin 12) (v : Fock o) :
    ∃ N : ℕ, ∀ n ≥ N, ∀ i : Fin (BasisSize o), annihilate o n i v = 0 := by
  induction v using SymmetricAlgebra.induction with
  | algebraMap r =>
      refine ⟨0, ?_⟩
      intro n hn i
      simp [annihilate]
  | ι x =>
      refine ⟨oscillatorModeBound o x, ?_⟩
      intro n hn i
      change annihilation (modeCovector o n i) (SymmetricAlgebra.ι ℂ (Oscillators o) x) = 0
      rw [annihilation_generator, modeCovector_vanishes_above_support o x n hn i]
      simp
  | mul x y hx hy =>
      obtain ⟨N, hN⟩ := hx
      obtain ⟨M, hM⟩ := hy
      refine ⟨max N M, ?_⟩
      intro n hn i
      have hx0 := hN n (le_trans (le_max_left N M) hn) i
      have hy0 := hM n (le_trans (le_max_right N M) hn) i
      change annihilation (modeCovector o n i) (x * y) = 0
      rw [annihilation_product]
      change x * annihilate o n i y + y * annihilate o n i x = 0
      rw [hx0, hy0]
      simp
  | add x y hx hy =>
      obtain ⟨N, hN⟩ := hx
      obtain ⟨M, hM⟩ := hy
      refine ⟨max N M, ?_⟩
      intro n hn i
      rw [map_add, hN n (le_trans (le_max_left N M) hn) i,
        hM n (le_trans (le_max_right N M) hn) i]
      simp

/-- Tensoring with the twisted lattice algebra preserves pointwise
truncation; the finite bound may depend on the state, not on the basis index. -/
theorem exists_carrier_annihilation_bound (o : Fin 12) (v : LatticeCarrier o) :
    ∃ N : ℕ, ∀ n ≥ N, ∀ i : Fin (BasisSize o),
      onCarrier o (annihilate o n i) v = 0 := by
  induction v using TensorProduct.induction_on with
  | zero =>
      refine ⟨0, ?_⟩
      intro n hn i
      exact map_zero _
  | tmul v a =>
      obtain ⟨N, hN⟩ := exists_annihilation_bound o v
      refine ⟨N, ?_⟩
      intro n hn i
      rw [onCarrier_pure, hN n hn i]
      simp
  | add x y hx hy =>
      obtain ⟨N, hN⟩ := hx
      obtain ⟨M, hM⟩ := hy
      refine ⟨max N M, ?_⟩
      intro n hn i
      rw [map_add, hN n (le_trans (le_max_left N M) hn) i,
        hM n (le_trans (le_max_right N M) hn) i]
      simp

end HMT.IV.LatticeFieldTruncation
end

#print axioms HMT.IV.LatticeFieldTruncation.modeCovector_vanishes_above_support
#print axioms HMT.IV.LatticeFieldTruncation.exists_annihilation_bound
#print axioms HMT.IV.LatticeFieldTruncation.exists_carrier_annihilation_bound
