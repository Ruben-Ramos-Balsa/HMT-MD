import LatticeTwistedFiniteQuotient
import MarkedNeighborSelfDual
import Mathlib.GroupTheory.Subgroup.Center

/-! Nondegeneracy modulo two is inherited from integral self-duality of the
same marked neighbour: an even-pairing vector has its half in the integral
dual, hence in the lattice itself. This identifies the centre of the actual
finite quotient, without introducing a representation or its dimension. -/

noncomputable section
namespace HMT.IV.LatticeParityNondegenerate
open CoxeterNeighbor GlueDuality NeighborDuality LatticeCocycle
open LatticeTwistedFiniteQuotient

theorem even_pairings_imply_double (o : Fin 12) (x : Lattice o)
    (hx : ∀ y : Lattice o, (integerPair o x y : ZMod 2)=0) :
    ∃ z : Lattice o, x=(2:ℤ) • z := by
  let half : Space 12 := (1/2:ℚ) • (x : Space 12)
  have hdual : half ∈ integralDual (Lattice o) := by
    intro y hy
    let yL : Lattice o := ⟨y,hy⟩
    have hdiv : (2:ℤ) ∣ integerPair o x yL :=
      (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).mp (hx yL)
    obtain ⟨k,hk⟩ := hdiv
    refine ⟨k, ?_⟩
    change pairing ((1/2:ℚ) • (x : Space 12)) (yL : Space 12) = (k:ℚ)
    rw [pairing_smul_left, ← cast_integerPair, hk]
    push_cast
    ring
  have hhalf : half ∈ Lattice o := by
    rw [witt_marked_neighbor_selfDual o] at hdual
    exact hdual
  refine ⟨⟨half,hhalf⟩, ?_⟩
  apply Subtype.ext
  change (x : Space 12) = (2:ℤ) • half
  rw [← Int.cast_smul_eq_zsmul (R := ℚ)]
  dsimp [half]
  module

theorem parityPair_radical_iff (o : Fin 12) (x : Lattice o) :
    (∀ y : Lattice o, parityBilinear o x y=0) ↔ parityCoordinates o x=0 := by
  constructor
  · intro hx
    apply (parityCoordinates_zero_iff_double o x).mpr
    exact even_pairings_imply_double o x hx
  · intro hx y
    rw [← parityGram_recovers_pairing, hx]
    simp only [TC.bilinear, Pi.zero_apply, zero_mul, Finset.sum_const_zero]

theorem parityGram_nondegenerate (o : Fin 12) (v : ParityVector o)
    (hv : ∀ w : ParityVector o, TC.bilinear (parityGram o) v w=0) : v=0 := by
  obtain ⟨x,rfl⟩ := parityCoordinates_surjective o v
  apply (parityPair_radical_iff o x).mp
  intro y
  rw [← parityGram_recovers_pairing]
  exact hv (parityCoordinates o y)

theorem finite_commute_iff (o : Fin 12) (a b : FiniteExtension o) :
    a*b=b*a ↔ TC.bilinear (parityGram o) a.2 b.2=0 := by
  have ht := TC.tau_commutator (parityGram o) (parityGram_symmetric o)
    (parityGram_diagonal_zero o) a.2 b.2
  constructor
  · intro hab
    have hs := congrArg Prod.fst hab
    change a.1+b.1+TC.tau (parityGram o) a.2 b.2 =
      b.1+a.1+TC.tau (parityGram o) b.2 a.2 at hs
    have heq : TC.tau (parityGram o) a.2 b.2 = TC.tau (parityGram o) b.2 a.2 := by
      linear_combination hs
    rw [← ht, heq]
    simpa only [ZMod.neg_eq_self_mod_two] using
      add_neg_cancel (TC.tau (parityGram o) b.2 a.2)
  · intro h
    have hs : TC.tau (parityGram o) a.2 b.2 = TC.tau (parityGram o) b.2 a.2 := by
      have hz := eq_neg_of_add_eq_zero_left (ht.trans h)
      simpa only [ZMod.neg_eq_self_mod_two] using hz
    apply Prod.ext
    · change a.1+b.1+TC.tau (parityGram o) a.2 b.2 =
        b.1+a.1+TC.tau (parityGram o) b.2 a.2
      rw [hs]
      ring
    · change a.2+b.2=b.2+a.2
      exact add_comm _ _

theorem finite_mem_center_iff (o : Fin 12) (a : FiniteExtension o) :
    a ∈ Subgroup.center (FiniteExtension o) ↔ a.2=0 := by
  rw [Subgroup.mem_center_iff]
  constructor
  · intro ha
    apply parityGram_nondegenerate o a.2
    intro w
    exact (finite_commute_iff o a (0,w)).mp (ha (0,w)).symm
  · intro ha b
    apply (finite_commute_iff o b a).mpr
    rw [ha]
    simp only [TC.bilinear, Pi.zero_apply, mul_zero, Finset.sum_const_zero]

theorem finite_center_exact (o : Fin 12) (a : FiniteExtension o) :
    a ∈ Subgroup.center (FiniteExtension o) ↔ ∃ s : ZMod 2, a=(s,0) := by
  rw [finite_mem_center_iff]
  constructor
  · intro ha
    exact ⟨a.1, Prod.ext rfl ha⟩
  · rintro ⟨s,rfl⟩
    rfl

end HMT.IV.LatticeParityNondegenerate
end

#print axioms HMT.IV.LatticeParityNondegenerate.even_pairings_imply_double
#print axioms HMT.IV.LatticeParityNondegenerate.parityPair_radical_iff
#print axioms HMT.IV.LatticeParityNondegenerate.parityGram_nondegenerate
#print axioms HMT.IV.LatticeParityNondegenerate.finite_commute_iff
#print axioms HMT.IV.LatticeParityNondegenerate.finite_mem_center_iff
#print axioms HMT.IV.LatticeParityNondegenerate.finite_center_exact
