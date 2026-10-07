import LatticeTwistedCarrier
import LatticeModeWeights

/-! Half-integer oscillator weights are computed on the existing monomial
basis. They are not a grading imposed independently of the conformal modes. -/

noncomputable section
namespace HMT.IV.LatticeHalfWeightBasis
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity LatticeModeWeights
open LatticeHalfIntegerHeisenberg LatticeHalfConformalModes LatticeHalfConformalHeisenberg
open LatticeHalfConformalVacuum LatticeHalfConformalCentralizer

def twiceWeight (o : Fin 12) (a : Occupation o) : ℕ :=
  a.sum fun p k => (2*p.1+1)*k

@[simp] theorem twiceWeight_zero (o : Fin 12) : twiceWeight o 0 = 0 := by
  simp [twiceWeight]

theorem twiceWeight_add (o : Fin 12) (a b : Occupation o) :
    twiceWeight o (a+b) = twiceWeight o a + twiceWeight o b := by
  unfold twiceWeight
  exact Finsupp.sum_add_index' (by intros; simp) (by intros; simp [mul_add])

@[simp] theorem twiceWeight_single (o : Fin 12) (p : Mode o) (k : ℕ) :
    twiceWeight o (Finsupp.single p k) = (2*p.1+1)*k := by
  simp [twiceWeight]

theorem quadratic_zero_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (v : HalfFock o) :
    quadraticMode o 0 (create o n i v) =
      create o n i (quadraticMode o 0 v) + ((n:ℂ)+1/2) • create o n i v := by
  have h := quadraticMode_half_commutator_apply o i 0 (Int.negSucc n) v
  simp only [zero_add, halfMode_negSucc] at h
  have hc : (-(Int.negSucc n : ℤ) : ℂ)-1/2 = (n:ℂ)+1/2 := by
    push_cast
    ring
  rw [hc] at h
  rw [sub_eq_iff_eq_add] at h
  exact h.trans (add_comm _ _)

theorem quadratic_zero_monomial (o : Fin 12) (a : Occupation o) :
    quadraticMode o 0 (monomialBasis o a) =
      ((twiceWeight o a : ℂ)/2) • monomialBasis o a := by
  classical
  induction a using Finsupp.induction with
  | zero =>
    rw [monomialBasis_product, Finsupp.prod_zero_index, twiceWeight_zero]
    simpa using quadraticMode_nonnegative_vacuum o 0 (by omega)
  | @single_add p k a _ hk0 ih =>
    clear hk0
    induction k with
    | zero => simpa using ih
    | succ k hk =>
      have heq : Finsupp.single p (k+1) + a =
          Finsupp.single p 1 + (Finsupp.single p k + a) := by
        rw [← add_assoc, ← Finsupp.single_add]
        congr 2
        omega
      rw [heq, ← create_monomial o p.1 p.2 (Finsupp.single p k+a)]
      rw [quadratic_zero_create, hk, map_smul]
      simp only [twiceWeight_add, twiceWeight_single, Nat.cast_add, Nat.cast_mul,
        Nat.cast_one, Nat.cast_ofNat, mul_one]
      module

theorem shifted_zero_monomial (o : Fin 12) (a : Occupation o) :
    shiftedModes o 0 (monomialBasis o a) =
      (((twiceWeight o a : ℂ)+3)/2) • monomialBasis o a := by
  change quadraticMode o 0 (monomialBasis o a) +
    ((BasisSize o : ℂ)/16) • monomialBasis o a = _
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  rw [quadratic_zero_monomial, hr]
  norm_num
  module

end HMT.IV.LatticeHalfWeightBasis
end
