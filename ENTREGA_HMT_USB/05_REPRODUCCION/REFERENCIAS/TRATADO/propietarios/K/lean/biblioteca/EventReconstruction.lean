import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-! Integral reconstruction of twelve events, Article VI `vi:prop:eventos`.
The codomain is an explicitly characterized sublattice, not all of ℤ¹². -/

namespace HMT.VI.EventReconstruction

open scoped BigOperators

abbrev Events := Fin 12 → ℤ

def first (i : Fin 6) : Fin 12 := ⟨i.val, by omega⟩
def second (i : Fin 6) : Fin 12 := ⟨i.val + 6, by omega⟩

def paired (e : Events) (i : Fin 6) : ℤ := e (first i) + e (second i)
def oriented (e : Events) (i : Fin 6) : ℤ := e (first i) - e (second i)

@[ext] structure Coordinates where
  total : ℤ
  differences : Fin 5 → ℤ
  antisymmetric : Fin 6 → ℤ
  deriving DecidableEq

def extract (e : Events) : Coordinates where
  total := ∑ i : Fin 6, paired e i
  differences i := paired e i.castSucc - paired e (Fin.last 5)
  antisymmetric := oriented e

/-- The single division by six in the inverse coordinate transform. -/
def referencePair (q : Coordinates) : ℤ :=
  (q.total - ∑ i : Fin 5, q.differences i) / 6

def recoverPairs (q : Coordinates) (i : Fin 6) : ℤ :=
  if h : i.val < 5 then referencePair q + q.differences ⟨i.val, h⟩ else referencePair q

/-- Congruence `p_i ≡ a_i mod 2` is represented by divisibility of `p_i-a_i`. -/
def IntegralImage (q : Coordinates) : Prop :=
  6 ∣ q.total - ∑ i : Fin 5, q.differences i ∧
    ∀ i : Fin 6, 2 ∣ recoverPairs q i - q.antisymmetric i

/-- Explicit integral inverse. It is a two-sided inverse exactly on `IntegralImage`. -/
def reconstruct (q : Coordinates) (j : Fin 12) : ℤ :=
  if h : j.val < 6 then
    (recoverPairs q ⟨j.val, h⟩ + q.antisymmetric ⟨j.val, h⟩) / 2
  else
    (recoverPairs q ⟨j.val - 6, by omega⟩ - q.antisymmetric ⟨j.val - 6, by omega⟩) / 2

theorem total_minus_differences (e : Events) :
    (extract e).total - ∑ i : Fin 5, (extract e).differences i =
      6 * paired e (Fin.last 5) := by
  simp only [extract, Fin.sum_univ_castSucc, Finset.sum_sub_distrib,
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  ring

theorem referencePair_extract (e : Events) :
    referencePair (extract e) = paired e (Fin.last 5) := by
  rw [referencePair, total_minus_differences]
  omega

@[simp] theorem recoverPairs_castSucc (q : Coordinates) (i : Fin 5) :
    recoverPairs q i.castSucc = referencePair q + q.differences i := by
  simp [recoverPairs, i.isLt]

@[simp] theorem recoverPairs_last (q : Coordinates) :
    recoverPairs q (Fin.last 5) = referencePair q := by simp [recoverPairs]

theorem recoverPairs_extract (e : Events) (i : Fin 6) :
    recoverPairs (extract e) i = paired e i := by
  refine Fin.lastCases ?_ (fun j => ?_) i
  · rw [recoverPairs_last, referencePair_extract]
  · rw [recoverPairs_castSucc, referencePair_extract]
    change paired e (Fin.last 5) + (paired e j.castSucc - paired e (Fin.last 5)) = _
    ring

theorem extract_integral (e : Events) : IntegralImage (extract e) := by
  constructor
  · rw [total_minus_differences]
    exact dvd_mul_right 6 _
  · intro i
    rw [recoverPairs_extract]
    change 2 ∣ paired e i - oriented e i
    refine ⟨e (second i), ?_⟩
    simp [paired, oriented]
    ring

@[simp] theorem reconstruct_first (q : Coordinates) (i : Fin 6) :
    reconstruct q (first i) = (recoverPairs q i + q.antisymmetric i) / 2 := by
  simp [reconstruct, first, i.isLt]

@[simp] theorem reconstruct_second (q : Coordinates) (i : Fin 6) :
    reconstruct q (second i) = (recoverPairs q i - q.antisymmetric i) / 2 := by
  simp [reconstruct, second]

theorem reconstruct_extract (e : Events) : reconstruct (extract e) = e := by
  funext j
  by_cases hj : j.val < 6
  · let i : Fin 6 := ⟨j.val, hj⟩
    have hji : j = first i := Fin.ext rfl
    rw [hji, reconstruct_first, recoverPairs_extract]
    change (paired e i + oriented e i) / 2 = e (first i)
    simp only [paired, oriented]
    omega
  · let i : Fin 6 := ⟨j.val - 6, by omega⟩
    have hji : j = second i := by apply Fin.ext; dsimp [i, second]; omega
    rw [hji, reconstruct_second, recoverPairs_extract]
    change (paired e i - oriented e i) / 2 = e (second i)
    simp only [paired, oriented]
    omega

theorem extract_injective : Function.Injective extract := by
  intro e f h
  rw [← reconstruct_extract e, ← reconstruct_extract f, h]

theorem paired_reconstruct (q : Coordinates) (hq : IntegralImage q) (i : Fin 6) :
    paired (reconstruct q) i = recoverPairs q i := by
  rcases hq.2 i with ⟨k, hk⟩
  simp only [paired, reconstruct_first, reconstruct_second]
  omega

theorem oriented_reconstruct (q : Coordinates) (hq : IntegralImage q) (i : Fin 6) :
    oriented (reconstruct q) i = q.antisymmetric i := by
  rcases hq.2 i with ⟨k, hk⟩
  simp only [oriented, reconstruct_first, reconstruct_second]
  omega

theorem sum_recoverPairs (q : Coordinates) (hq : IntegralImage q) :
    ∑ i : Fin 6, recoverPairs q i = q.total := by
  have hdiv := Int.ediv_mul_cancel hq.1
  change referencePair q * 6 = q.total - ∑ i : Fin 5, q.differences i at hdiv
  rw [Fin.sum_univ_castSucc]
  simp only [recoverPairs_castSucc, recoverPairs_last, Finset.sum_add_distrib,
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  norm_num at hdiv ⊢
  linarith

theorem extract_reconstruct (q : Coordinates) (hq : IntegralImage q) :
    extract (reconstruct q) = q := by
  apply Coordinates.ext
  · change (∑ i : Fin 6, paired (reconstruct q) i) = q.total
    simp_rw [paired_reconstruct q hq]
    exact sum_recoverPairs q hq
  · funext i
    change paired (reconstruct q) i.castSucc - paired (reconstruct q) (Fin.last 5) =
      q.differences i
    rw [paired_reconstruct _ hq, paired_reconstruct _ hq]
    rw [recoverPairs_castSucc, recoverPairs_last]
    ring
  · funext i
    exact oriented_reconstruct q hq i

/-- Necessary and sufficient image conditions, not only a left inverse. -/
theorem image_iff (q : Coordinates) : (∃ e : Events, extract e = q) ↔ IntegralImage q := by
  constructor
  · rintro ⟨e, rfl⟩
    exact extract_integral e
  · intro hq
    exact ⟨reconstruct q, extract_reconstruct q hq⟩

def integralEquiv : Events ≃ {q : Coordinates // IntegralImage q} where
  toFun e := ⟨extract e, extract_integral e⟩
  invFun q := reconstruct q.val
  left_inv := reconstruct_extract
  right_inv q := Subtype.ext (extract_reconstruct q.val q.property)

#print axioms extract_injective
#print axioms image_iff
#print axioms integralEquiv

end HMT.VI.EventReconstruction
