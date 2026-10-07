import LatticeHalfConformalModes
import LatticeConformalHeisenberg

/-! The quadratic half-integer modes act on all oscillators by their
actual frequency. The two finite-on-vectors normal sums give complementary
integer deltas. No Virasoro relation or shifted energy is assumed. -/

noncomputable section
namespace HMT.IV.LatticeHalfConformalHeisenberg

open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfConformalModes LatticeGramDual LatticeGramSymmetry
open LatticeConformalHeisenberg
open scoped BigOperators

theorem product_half_commutator (o : Fin 12) (i j t : Fin (BasisSize o))
    (a b n : ℤ) (v : HalfFock o) :
    halfMode o i a (halfMode o j b (halfMode o t n v)) -
      halfMode o t n (halfMode o i a (halfMode o j b v)) =
    (if b+n+1=0 then ((b:ℂ)+1/2)*gram o j t else 0) • halfMode o i a v +
      (if a+n+1=0 then ((a:ℂ)+1/2)*gram o i t else 0) • halfMode o j b v := by
  have h1 := congrArg (halfMode o i a) (half_heisenberg_relation_apply o j t b n v)
  simp only [map_sub, map_smul] at h1
  have h2 := half_heisenberg_relation_apply o i t a n (halfMode o j b v)
  rw [← h1, ← h2]
  abel

theorem creation_half_delta (o : Fin 12) (i j t : Fin (BasisSize o))
    (m n : ℤ) (a : ℕ) (v : HalfFock o) :
    creationHalfTerm o i j m a (halfMode o t n v) -
      halfMode o t n (creationHalfTerm o i j m a v) =
    (if (a:ℤ)=-m-n-1 then ((-(n:ℂ)-1/2)*gram o j t) • halfMode o i (m+n) v else 0) +
    (if (a:ℤ)=n then ((-(n:ℂ)-1/2)*gram o i t) • halfMode o j (m+n) v else 0) := by
  have hc : create o a i = halfMode o i (-(a:ℤ)-1) := by
    rw [show -(a:ℤ)-1=Int.negSucc a by omega, halfMode_negSucc]
  simp only [creationHalfTerm, LinearMap.comp_apply, hc]
  rw [product_half_commutator]
  apply congrArg₂ (fun u w : HalfFock o => u+w)
  · by_cases h : m+(a:ℤ)+n+1=0
    · have ha : (a:ℤ)=-m-n-1 := by omega
      rw [if_pos h, if_pos ha, show m+(a:ℤ) = -n-1 by omega,
        show -(a:ℤ)-1=m+n by omega]
      congr 2
      push_cast
      ring
    · have ha : ¬(a:ℤ)=-m-n-1 := by omega
      simp only [if_neg h, if_neg ha, zero_smul]
  · by_cases h : -(a:ℤ)-1+n+1=0
    · have ha : (a:ℤ)=n := by omega
      rw [if_pos h, if_pos ha, ha]
      congr 2
      push_cast
      ring
    · have ha : ¬(a:ℤ)=n := by omega
      simp only [if_neg h, if_neg ha, zero_smul]

theorem annihilation_half_delta (o : Fin 12) (i j t : Fin (BasisSize o))
    (m n : ℤ) (a : ℕ) (v : HalfFock o) :
    annihilationHalfTerm o i j m a (halfMode o t n v) -
      halfMode o t n (annihilationHalfTerm o i j m a v) =
    (if (a:ℤ)=-n-1 then ((-(n:ℂ)-1/2)*gram o i t) • halfMode o j (m+n) v else 0) +
    (if (a:ℤ)=m+n then ((-(n:ℂ)-1/2)*gram o j t) • halfMode o i (m+n) v else 0) := by
  change halfMode o j (m-a-1) (halfMode o i (a:ℤ) (halfMode o t n v)) -
    halfMode o t n (halfMode o j (m-a-1) (halfMode o i (a:ℤ) v)) = _
  rw [product_half_commutator]
  apply congrArg₂ (fun u w : HalfFock o => u+w)
  · by_cases h : (a:ℤ)+n+1=0
    · have ha : (a:ℤ)=-n-1 := by omega
      rw [if_pos h, if_pos ha, ha, show m-(-n-1)-1=m+n by omega]
      congr 2
      push_cast
      ring
    · have ha : ¬(a:ℤ)=-n-1 := by omega
      simp only [if_neg h, if_neg ha, zero_smul]
  · by_cases h : m-(a:ℤ)-1+n+1=0
    · have ha : (a:ℤ)=m+n := by omega
      rw [if_pos h, if_pos ha, show m-(a:ℤ)-1=-n-1 by omega, ha]
      congr 2
      push_cast
      ring
    · have ha : ¬(a:ℤ)=m+n := by omega
      simp only [if_neg h, if_neg ha, zero_smul]

theorem halfNormalMode_commutator (o : Fin 12) (i j t : Fin (BasisSize o))
    (m n : ℤ) (v : HalfFock o) :
    halfNormalMode o i j m (halfMode o t n v) -
      halfMode o t n (halfNormalMode o i j m v) =
      ((-(n:ℂ)-1/2)*gram o j t) • halfMode o i (m+n) v +
      ((-(n:ℂ)-1/2)*gram o i t) • halfMode o j (m+n) v := by
  rw [halfNormalMode_apply, halfNormalMode_apply, map_add]
  rw [show (∑ᶠ a, creationHalfTerm o i j m a (halfMode o t n v)) +
      (∑ᶠ a, annihilationHalfTerm o i j m a (halfMode o t n v)) -
      (halfMode o t n (∑ᶠ a, creationHalfTerm o i j m a v) +
       halfMode o t n (∑ᶠ a, annihilationHalfTerm o i j m a v)) =
      ((∑ᶠ a, creationHalfTerm o i j m a (halfMode o t n v)) -
       halfMode o t n (∑ᶠ a, creationHalfTerm o i j m a v)) +
      ((∑ᶠ a, annihilationHalfTerm o i j m a (halfMode o t n v)) -
       halfMode o t n (∑ᶠ a, annihilationHalfTerm o i j m a v)) by abel]
  rw [finsum_commutator _ (creationHalfTerm_finite o i j m),
    finsum_commutator _ (annihilationHalfTerm_finite o i j m)]
  simp_rw [creation_half_delta, annihilation_half_delta]
  rw [finsum_add_distrib (integer_delta_finite _ _) (integer_delta_finite _ _),
    finsum_add_distrib (integer_delta_finite _ _) (integer_delta_finite _ _)]
  simp_rw [finsum_integer_delta]
  split_ifs <;> first | omega | abel

theorem gram_contract_half {V : Type*} [AddCommGroup V] [Module ℂ V]
    (o : Fin 12) (t : Fin (BasisSize o)) (c : ℂ) (w : Fin (BasisSize o) → V) :
    (∑ i, ∑ j, gramInv o i j • ((c*gram o j t) • w i)) = c • w t := by
  classical
  simp only [smul_smul]
  have inner (i : Fin (BasisSize o)) :
      (∑ j, (gramInv o i j * (c*gram o j t)) • w i) =
      (c*(if i=t then 1 else 0)) • w i := by
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = c * ∑ j, gramInv o i j * gram o j t := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intros
        ring
      _ = _ := by rw [gramInv_pairing]
  simp_rw [inner]
  simp

theorem gram_contract_half_swapped {V : Type*} [AddCommGroup V] [Module ℂ V]
    (o : Fin 12) (t : Fin (BasisSize o)) (c : ℂ) (w : Fin (BasisSize o) → V) :
    (∑ i, ∑ j, gramInv o i j • ((c*gram o i t) • w j)) = c • w t := by
  rw [Finset.sum_comm]
  have h : (∑ j, ∑ i, gramInv o i j • ((c*gram o i t) • w j)) =
      ∑ j, ∑ i, gramInv o j i • ((c*gram o i t) • w j) := by
    apply Finset.sum_congr rfl
    intro j _
    apply Finset.sum_congr rfl
    intro i _
    rw [gramInv_symmetric o i j]
  rw [h, gram_contract_half]

theorem quadraticMode_half_commutator_apply (o : Fin 12)
    (t : Fin (BasisSize o)) (m n : ℤ) (v : HalfFock o) :
    quadraticMode o m (halfMode o t n v) - halfMode o t n (quadraticMode o m v) =
      (-(n:ℂ)-1/2) • halfMode o t (m+n) v := by
  classical
  rw [quadraticMode_apply, quadraticMode_apply]
  have combine :
      (2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j • halfNormalMode o i j m (halfMode o t n v)) -
      halfMode o t n ((2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j • halfNormalMode o i j m v)) =
      (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j •
        (halfNormalMode o i j m (halfMode o t n v) -
         halfMode o t n (halfNormalMode o i j m v)) := by
    simp only [map_smul, map_sum, smul_sub, Finset.sum_sub_distrib]
  rw [combine]
  simp_rw [halfNormalMode_commutator, smul_add, Finset.sum_add_distrib]
  rw [gram_contract_half, gram_contract_half_swapped]
  module

theorem quadraticMode_half_commutator (o : Fin 12)
    (t : Fin (BasisSize o)) (m n : ℤ) :
    (quadraticMode o m).comp (halfMode o t n) - (halfMode o t n).comp (quadraticMode o m) =
      (-(n:ℂ)-1/2) • halfMode o t (m+n) := by
  apply LinearMap.ext
  intro v
  exact quadraticMode_half_commutator_apply o t m n v

end HMT.IV.LatticeHalfConformalHeisenberg
end

#print axioms HMT.IV.LatticeHalfConformalHeisenberg.product_half_commutator
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.creation_half_delta
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.annihilation_half_delta
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.halfNormalMode_commutator
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.gram_contract_half
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.gram_contract_half_swapped
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.quadraticMode_half_commutator_apply
#print axioms HMT.IV.LatticeHalfConformalHeisenberg.quadraticMode_half_commutator
