import LatticeHalfIntegerField
import LatticeNormalOrderedField
import LatticeGramDual

/-!
Normally ordered quadratic modes on the already constructed half-integer
oscillator Fock space, using the inverse of the same marked Gram matrix.
The two infinite sums are locally finite on every vector. No scalar vacuum
shift, conformal axiom, twisted lattice module or orbifold product is assumed.
-/

noncomputable section
namespace HMT.IV.LatticeHalfConformalModes

open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg LatticeGramDual
open LatticeNormalOrderedField
open scoped BigOperators

def creationHalfTerm (o : Fin 12) (i j : Fin (BasisSize o)) (m : ℤ) (a : ℕ) :
    Module.End ℂ (HalfFock o) :=
  (create o a i).comp (halfMode o j (m+a))

def annihilationHalfTerm (o : Fin 12) (i j : Fin (BasisSize o)) (m : ℤ) (a : ℕ) :
    Module.End ℂ (HalfFock o) :=
  (halfMode o j (m-a-1)).comp (halfAnnihilate o a i)

private theorem finite_support_of_bound {V : Type*} [Zero V]
    (f : ℕ → V) (N : ℕ) (h : ∀ a ≥ N, f a = 0) :
    (Function.support f).Finite := by
  apply (Finset.range N).finite_toSet.subset
  intro a ha
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact ha (h a (by omega))

theorem creationHalfTerm_finite (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (v : HalfFock o) :
    (Function.support (fun a => creationHalfTerm o i j m a v)).Finite := by
  obtain ⟨N, hN⟩ := halfMode_annihilation_bound o v
  apply finite_support_of_bound _ ((-m).toNat+N)
  intro a ha
  have hk : m+(a:ℤ) = (((m+(a:ℤ)).toNat):ℤ) := by omega
  have hz : halfMode o j (m+a) v=0 := by
    rw [hk]
    exact hN _ (by omega) j
  simp only [creationHalfTerm, LinearMap.comp_apply, hz, map_zero]

theorem annihilationHalfTerm_finite (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (v : HalfFock o) :
    (Function.support (fun a => annihilationHalfTerm o i j m a v)).Finite := by
  obtain ⟨N, hN⟩ := halfMode_annihilation_bound o v
  apply finite_support_of_bound _ N
  intro a ha
  have hz : halfAnnihilate o a i v=0 := hN a ha i
  simp only [annihilationHalfTerm, LinearMap.comp_apply, hz, map_zero]

def halfNormalMode (o : Fin 12) (i j : Fin (BasisSize o)) (m : ℤ) :
    Module.End ℂ (HalfFock o) :=
  locallyFiniteSum (creationHalfTerm o i j m) (creationHalfTerm_finite o i j m) +
    locallyFiniteSum (annihilationHalfTerm o i j m) (annihilationHalfTerm_finite o i j m)

theorem halfNormalMode_apply (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (v : HalfFock o) :
    halfNormalMode o i j m v =
      (∑ᶠ a, creationHalfTerm o i j m a v) +
        ∑ᶠ a, annihilationHalfTerm o i j m a v := rfl

/-- The unshifted quadratic modes. Any vacuum shift is a later derived scalar. -/
def quadraticMode (o : Fin 12) (m : ℤ) : Module.End ℂ (HalfFock o) :=
  (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j • halfNormalMode o i j m

theorem quadraticMode_apply (o : Fin 12) (m : ℤ) (v : HalfFock o) :
    quadraticMode o m v =
      (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j • halfNormalMode o i j m v := by
  simp only [quadraticMode, LinearMap.smul_apply, LinearMap.sum_apply]

theorem halfMode_nonnegative_vacuum (o : Fin 12) (i : Fin (BasisSize o))
    (k : ℤ) (hk : 0 ≤ k) : halfMode o i k 1=0 := by
  cases k with
  | ofNat a => exact halfAnnihilate_vacuum o a i
  | negSucc a => omega

theorem halfNormalMode_nonnegative_vacuum (o : Fin 12)
    (i j : Fin (BasisSize o)) (m : ℤ) (hm : 0 ≤ m) :
    halfNormalMode o i j m 1=0 := by
  have hc (a : ℕ) : creationHalfTerm o i j m a 1=0 := by
    simp only [creationHalfTerm, LinearMap.comp_apply,
      halfMode_nonnegative_vacuum o j (m+a) (by omega), map_zero]
  have ha (a : ℕ) : annihilationHalfTerm o i j m a 1=0 := by
    simp only [annihilationHalfTerm, LinearMap.comp_apply,
      halfAnnihilate_vacuum, map_zero]
  simp only [halfNormalMode_apply, hc, ha, finsum_zero, add_zero]

theorem quadraticMode_nonnegative_vacuum (o : Fin 12) (m : ℤ) (hm : 0 ≤ m) :
    quadraticMode o m 1=0 := by
  simp only [quadraticMode_apply, halfNormalMode_nonnegative_vacuum o _ _ m hm,
    smul_zero, Finset.sum_const_zero]

theorem halfNormalMode_neg_one_vacuum (o : Fin 12)
    (i j : Fin (BasisSize o)) :
    halfNormalMode o i j (-1) 1=create o 0 i (create o 0 j 1) := by
  have hc (a : ℕ) (ha : a≠0) : creationHalfTerm o i j (-1) a 1=0 := by
    simp only [creationHalfTerm, LinearMap.comp_apply,
      halfMode_nonnegative_vacuum o j (-1+a) (by omega), map_zero]
  have ha (a : ℕ) : annihilationHalfTerm o i j (-1) a 1=0 := by
    simp only [annihilationHalfTerm, LinearMap.comp_apply,
      halfAnnihilate_vacuum, map_zero]
  rw [halfNormalMode_apply, finsum_eq_single _ 0 hc]
  simp only [ha, finsum_zero, add_zero, creationHalfTerm, LinearMap.comp_apply,
    Nat.cast_zero, add_zero]
  rfl

theorem quadraticMode_neg_one_vacuum (o : Fin 12) :
    quadraticMode o (-1) 1=
      (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j • create o 0 i (create o 0 j 1) := by
  simp only [quadraticMode_apply, halfNormalMode_neg_one_vacuum]

end HMT.IV.LatticeHalfConformalModes
end

#print axioms HMT.IV.LatticeHalfConformalModes.creationHalfTerm
#print axioms HMT.IV.LatticeHalfConformalModes.annihilationHalfTerm
#print axioms HMT.IV.LatticeHalfConformalModes.creationHalfTerm_finite
#print axioms HMT.IV.LatticeHalfConformalModes.annihilationHalfTerm_finite
#print axioms HMT.IV.LatticeHalfConformalModes.halfNormalMode
#print axioms HMT.IV.LatticeHalfConformalModes.halfNormalMode_apply
#print axioms HMT.IV.LatticeHalfConformalModes.quadraticMode
#print axioms HMT.IV.LatticeHalfConformalModes.quadraticMode_apply
#print axioms HMT.IV.LatticeHalfConformalModes.halfMode_nonnegative_vacuum
#print axioms HMT.IV.LatticeHalfConformalModes.halfNormalMode_nonnegative_vacuum
#print axioms HMT.IV.LatticeHalfConformalModes.quadraticMode_nonnegative_vacuum
#print axioms HMT.IV.LatticeHalfConformalModes.halfNormalMode_neg_one_vacuum
#print axioms HMT.IV.LatticeHalfConformalModes.quadraticMode_neg_one_vacuum
