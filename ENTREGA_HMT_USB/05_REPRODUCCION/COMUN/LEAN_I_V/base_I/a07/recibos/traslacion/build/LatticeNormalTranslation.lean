import LatticeHeisenbergTranslation
import LatticeNormalOrderedField
import LatticeFiniteDoubleSums
import Mathlib.Data.Nat.Choose.Basic

/-! Translation of normal products by pointwise finite telescoping sums. -/
noncomputable section
set_option maxHeartbeats 1200000
namespace HMT.IV.LatticeNormalTranslation

open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeNormalOrderedField LatticeFiniteDoubleSums LatticeHeisenbergTranslation
open scoped BigOperators

local notation "T" => LatticeTranslationOperator.translation

private theorem support_bound {V : Type*} [Zero V] (f : ℕ → V)
    (hf : (Function.support f).Finite) : ∃ N, ∀ a ≥ N, f a = 0 := by
  classical
  refine ⟨hf.toFinset.sup id + 1, ?_⟩
  intro a ha
  by_contra hn
  have hmem : a ∈ hf.toFinset := hf.mem_toFinset.mpr hn
  have hs : a ≤ hf.toFinset.sup id := Finset.le_sup (f := id) hmem
  omega

private theorem telescoping_sum {V : Type*} [AddCommGroup V] (f : ℕ → V) (N : ℕ) :
    (∑ a ∈ Finset.range N, (f (a+1)-f a)) = f N-f 0 := by
  induction N with
  | zero => simp
  | succ N ih => rw [Finset.sum_range_succ, ih]; abel

theorem commutator_mul {V : Type*} [AddCommGroup V] [Module ℂ V]
    (S A B : Module.End ℂ V) :
    S*(A*B)-(A*B)*S = (S*A-A*S)*B + A*(S*B-B*S) := by
  noncomm_ring

theorem commutator_smul {V : Type*} [AddCommGroup V] [Module ℂ V]
    (S A : Module.End ℂ V) (c : ℂ) :
    S*(c • A)-(c • A)*S = c • (S*A-A*S) := by
  simp only [mul_smul_comm, smul_mul_assoc, smul_sub]

/-- A pointwise finite discrete derivative contributes only its endpoints.
Both endpoints vanish here; no operator-wide frequency cutoff is required. -/
theorem locallyFiniteSum_commutator_of_telescoping
    {V : Type*} [AddCommGroup V] [Module ℂ V]
    (S : Module.End ℂ V) (P Q : ℕ → Module.End ℂ V)
    (hP : ∀ v, (Function.support (fun a => P a v)).Finite)
    (hQ : ∀ v, (Function.support (fun a => Q a v)).Finite)
    (c : ℂ) (v : V) (F : ℕ → V)
    (hF : (Function.support F).Finite) (hzero : F 0 = 0)
    (hcomm : ∀ a, S (P a v)-P a (S v) = c • Q a v + (F (a+1)-F a)) :
    S (locallyFiniteSum P hP v)-locallyFiniteSum P hP (S v) =
      c • locallyFiniteSum Q hQ v := by
  classical
  obtain ⟨NP, hNP⟩ := support_bound _ (hP v)
  obtain ⟨NS, hNS⟩ := support_bound _ (hP (S v))
  obtain ⟨NQ, hNQ⟩ := support_bound _ (hQ v)
  obtain ⟨NF, hNF⟩ := support_bound F hF
  let N := max (max NP NS) (max NQ NF)
  have hp : ∀ a ≥ N, P a v = 0 := by intro a ha; apply hNP; dsimp [N] at ha; omega
  have hs : ∀ a ≥ N, P a (S v) = 0 := by intro a ha; apply hNS; dsimp [N] at ha; omega
  have hq : ∀ a ≥ N, Q a v = 0 := by intro a ha; apply hNQ; dsimp [N] at ha; omega
  have hn : F N = 0 := by apply hNF; dsimp [N]; omega
  change S (∑ᶠ a, P a v) - (∑ᶠ a, P a (S v)) = c • (∑ᶠ a, Q a v)
  rw [finsum_eq_range _ N hp, finsum_eq_range _ N hs, finsum_eq_range _ N hq,
    map_sum, ← Finset.sum_sub_distrib]
  simp_rw [hcomm]
  rw [Finset.sum_add_distrib, telescoping_sum, hn, hzero, sub_self, add_zero,
    Finset.smul_sum]

theorem choose_step (a n : ℕ) :
    ((a+n).choose n : ℂ) * (a+n+1 : ℂ) =
      (a+1 : ℂ) * ((a+1+n).choose n : ℂ) := by
  have h := Nat.choose_mul_succ_eq (a+n) n
  have he : a+n+1-n = a+1 := by omega
  rw [he, show a+n+1=a+1+n by omega] at h
  have hc := congrArg (fun z : ℕ => (z : ℂ)) h
  push_cast at hc
  convert hc using 1 <;> ring

theorem creationTerm_commutator (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o))
    (hB : ∀ k : ℤ, T o * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)) (k : ℤ) (a : ℕ) :
    T o * creationTerm o i n B k a - creationTerm o i n B k a * T o =
      ((k : ℂ)+1) • creationTerm o i n B (k+1) a +
        ((a+1 : ℂ) • creationTerm o i n B (k+1) (a+1) -
          (a : ℂ) • creationTerm o i n B (k+1) a) := by
  have ht := translation_create o i (a+n)
  change T o * onCarrier o (create o (a+n) i) -
    onCarrier o (create o (a+n) i) * T o =
      (((a+n : ℕ) : ℂ)+1) • onCarrier o (create o (a+n+1) i) at ht
  change T o * (((a+n).choose n : ℂ) •
      (onCarrier o (create o (a+n) i) * HVertexOperator.coeff B (k-a))) -
    (((a+n).choose n : ℂ) •
      (onCarrier o (create o (a+n) i) * HVertexOperator.coeff B (k-a))) * T o = _
  rw [commutator_smul, commutator_mul, ht, hB]
  simp only [creationTerm, smul_add, smul_mul_assoc, mul_smul_comm, smul_smul]
  have hidx : k-(a : ℤ)+1 = k+1-(a : ℤ) := by omega
  have hidx' : k+1-((a+1 : ℕ) : ℤ) = k-(a : ℤ) := by omega
  rw [hidx, hidx', show a+n+1 = a+1+n by omega]
  have hs := choose_step a n
  push_cast at hs ⊢
  match_scalars
  all_goals first | (solve | ring) | linear_combination hs

theorem annihilationTerm_commutator_zero (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o))
    (hB : ∀ k : ℤ, T o * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)) (k : ℤ) :
    T o * annihilationTerm o i n B k 0 - annihilationTerm o i n B k 0 * T o =
      ((k : ℂ)+1) • annihilationTerm o i n B (k+1) 0 +
        (n+1 : ℂ) • annihilationTerm o i n B (k+1) 0 := by
  have ht := translation_hmode o i 0
  simp only [Int.cast_zero, neg_zero, zero_smul] at ht
  change T o * hmode o i 0 - hmode o i 0 * T o = 0 at ht
  change T o * (((-1 : ℂ)^n * ((0+n).choose n : ℂ)) •
      (HVertexOperator.coeff B (k+0+n+1) * hmode o i 0)) -
    (((-1 : ℂ)^n * ((0+n).choose n : ℂ)) •
      (HVertexOperator.coeff B (k+0+n+1) * hmode o i 0)) * T o = _
  rw [commutator_smul, commutator_mul, hB, ht]
  simp only [annihilationTerm, mul_zero, add_zero, smul_mul_assoc, smul_smul,
    Nat.cast_zero, zero_add]
  rw [show k+(n : ℤ)+1+1 = k+1+n+1 by omega]
  push_cast
  module

theorem annihilationTerm_commutator_succ (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o))
    (hB : ∀ k : ℤ, T o * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)) (k : ℤ) (a : ℕ) :
    T o * annihilationTerm o i n B k (a+1) -
      annihilationTerm o i n B k (a+1) * T o =
      ((k : ℂ)+1) • annihilationTerm o i n B (k+1) (a+1) +
        ((a+1+n+1 : ℂ) • annihilationTerm o i n B (k+1) (a+1) -
          (a+n+1 : ℂ) • annihilationTerm o i n B (k+1) a) := by
  have ht := translation_hmode o i ((a+1 : ℕ) : ℤ)
  rw [show ((a+1 : ℕ) : ℤ)-1 = (a : ℤ) by omega] at ht
  change T o * hmode o i ((a+1 : ℕ) : ℤ) -
    hmode o i ((a+1 : ℕ) : ℤ) * T o =
      (-(((a+1 : ℕ) : ℤ) : ℂ)) • hmode o i (a : ℤ) at ht
  change T o * (((-1 : ℂ)^n * ((a+1+n).choose n : ℂ)) •
      (HVertexOperator.coeff B (k+(a+1 : ℕ)+n+1) * hmode o i ((a+1 : ℕ) : ℤ))) -
    (((-1 : ℂ)^n * ((a+1+n).choose n : ℂ)) •
      (HVertexOperator.coeff B (k+(a+1 : ℕ)+n+1) * hmode o i ((a+1 : ℕ) : ℤ))) * T o = _
  rw [commutator_smul, commutator_mul, hB, ht]
  simp only [annihilationTerm, smul_add, smul_mul_assoc, mul_smul_comm, smul_smul]
  have hidx : k+((a+1 : ℕ) : ℤ)+n+1+1 = k+1+((a+1 : ℕ) : ℤ)+n+1 := by omega
  have hidx' : k+((a+1 : ℕ) : ℤ)+n+1 = k+1+(a : ℤ)+n+1 := by omega
  rw [hidx, hidx']
  have hs := choose_step a n
  push_cast at hs ⊢
  match_scalars
  all_goals first | (solve | ring) | linear_combination ((-1 : ℂ)^n) * hs

theorem creation_sum_translation (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o))
    (hB : ∀ k : ℤ, T o * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)) (k : ℤ) (v : LatticeCarrier o) :
    T o (∑ᶠ a, creationTerm o i n B k a v) -
      (∑ᶠ a, creationTerm o i n B k a (T o v)) =
      ((k : ℂ)+1) • (∑ᶠ a, creationTerm o i n B (k+1) a v) := by
  let F : ℕ → LatticeCarrier o := fun a => (a : ℂ) • creationTerm o i n B (k+1) a v
  have hf : (Function.support F).Finite := by
    apply (creationTerm_finite o i n B (k+1) v).subset
    intro a ha hz
    exact ha (by simp [F, hz])
  apply locallyFiniteSum_commutator_of_telescoping (T o)
    (creationTerm o i n B k) (creationTerm o i n B (k+1))
    (creationTerm_finite o i n B k) (creationTerm_finite o i n B (k+1))
    ((k : ℂ)+1) v F hf (by simp [F])
  intro a
  have h := LinearMap.congr_fun (creationTerm_commutator o i n B hB k a) v
  simpa [F, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    LinearMap.add_apply] using h

theorem annihilation_sum_translation (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o))
    (hB : ∀ k : ℤ, T o * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)) (k : ℤ) (v : LatticeCarrier o) :
    T o (∑ᶠ a, annihilationTerm o i n B k a v) -
      (∑ᶠ a, annihilationTerm o i n B k a (T o v)) =
      ((k : ℂ)+1) • (∑ᶠ a, annihilationTerm o i n B (k+1) a v) := by
  let F : ℕ → LatticeCarrier o
    | 0 => 0
    | a+1 => (a+n+1 : ℂ) • annihilationTerm o i n B (k+1) a v
  have hf : (Function.support F).Finite := by
    obtain ⟨N, hN⟩ := support_bound _ (annihilationTerm_finite o i n B (k+1) v)
    apply finite_support_of_bound F (N+1)
    intro a ha
    cases a with
    | zero => rfl
    | succ a => simp only [F, hN a (by omega), smul_zero]
  apply locallyFiniteSum_commutator_of_telescoping (T o)
    (annihilationTerm o i n B k) (annihilationTerm o i n B (k+1))
    (annihilationTerm_finite o i n B k) (annihilationTerm_finite o i n B (k+1))
    ((k : ℂ)+1) v F hf rfl
  intro a
  cases a with
  | zero =>
    have h := LinearMap.congr_fun (annihilationTerm_commutator_zero o i n B hB k) v
    simpa [F, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
      LinearMap.add_apply] using h
  | succ a =>
    have h := LinearMap.congr_fun (annihilationTerm_commutator_succ o i n B hB k a) v
    simpa [F, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
      LinearMap.add_apply, Nat.cast_add, Nat.cast_one] using h

/-- Normal ordering preserves differential translation covariance for each
divided Heisenberg derivative and every already covariant right-hand field. -/
theorem normalField_translation_covariant (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o))
    (hB : ∀ k : ℤ, T o * HVertexOperator.coeff B k - HVertexOperator.coeff B k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)) (k : ℤ) :
    T o * HVertexOperator.coeff (normalField o i n B) k -
      HVertexOperator.coeff (normalField o i n B) k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff (normalField o i n B) (k+1) := by
  apply LinearMap.ext
  intro v
  simp only [normalField_coefficient, Module.End.mul_apply, LinearMap.sub_apply,
    LinearMap.smul_apply, normalCoefficient_apply, map_add]
  have hc := creation_sum_translation o i n B hB k v
  have ha := annihilation_sum_translation o i n B hB k v
  rw [smul_add]
  rw [← hc, ← ha]
  abel

end HMT.IV.LatticeNormalTranslation
end

#print axioms HMT.IV.LatticeNormalTranslation.locallyFiniteSum_commutator_of_telescoping
#print axioms HMT.IV.LatticeNormalTranslation.creationTerm_commutator
#print axioms HMT.IV.LatticeNormalTranslation.annihilationTerm_commutator_zero
#print axioms HMT.IV.LatticeNormalTranslation.annihilationTerm_commutator_succ
#print axioms HMT.IV.LatticeNormalTranslation.creation_sum_translation
#print axioms HMT.IV.LatticeNormalTranslation.annihilation_sum_translation
#print axioms HMT.IV.LatticeNormalTranslation.normalField_translation_covariant
