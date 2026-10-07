import EvenCoxeterNeighbor
import A2NormBounds

namespace HMT.IV.CoxeterNeighbor

def numeratorA (a c k t : ℤ) : ℤ := 3*a + 2*c + k*(1+3*t)
def numeratorB (b c k t : ℤ) : ℤ := 3*b + c + k*(1+3*t)

def thirds {n : ℕ} (p q : Fin n → ℤ) : Space n :=
  fun i => ((p i : ℚ)/3, (q i : ℚ)/3)

def integerVector {n : ℕ} (a b : Fin n → ℤ) : Space n :=
  fun i => ((a i : ℚ), (b i : ℚ))

theorem thirds_norm {n : ℕ} (p q : Fin n → ℤ) :
    pairing (thirds p q) (thirds p q) =
      (2:ℚ)/9 * ((∑ i, a2IntNorm (p i) (q i) : ℤ):ℚ) := by
  simp only [pairing, localPair, thirds, Int.cast_sum]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  simp only [a2IntNorm, Int.cast_add, Int.cast_sub, Int.cast_mul]
  ring

theorem integerVector_norm {n : ℕ} (a b : Fin n → ℤ) :
    pairing (integerVector a b) (integerVector a b) =
      2 * ((∑ i, a2IntNorm (a i) (b i) : ℤ):ℚ) := by
  simp only [pairing, localPair, integerVector, Int.cast_sum]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  simp only [a2IntNorm, Int.cast_add, Int.cast_sub, Int.cast_mul]
  ring

theorem integerVector_radial_pair {n : ℕ} (a b t : Fin n → ℤ) :
    pairing (integerVector a b) (radial t) =
      ((∑ i, (a i+b i)*(1+3*t i) : ℤ):ℚ) := by
  simp only [pairing, localPair, integerVector, radial, Int.cast_sum]
  apply Finset.sum_congr rfl
  intro i _
  push_cast
  ring

theorem numerator_nonzero_of_k_not_divisible (a b c k t : ℤ)
    (hk : ¬ 3 ∣ k) :
    numeratorA a c k t ≠ 0 ∨ numeratorB b c k t ≠ 0 := by
  by_contra h
  push_neg at h
  obtain ⟨ha, hb⟩ := h
  apply hk
  refine ⟨a - 2*b - k*t, ?_⟩
  dsimp [numeratorA, numeratorB] at ha hb
  nlinarith [ha, hb]

theorem numerator_norm_ge_one (a b c k t : ℤ) (hk : ¬ 3 ∣ k) :
    1 ≤ a2IntNorm (numeratorA a c k t) (numeratorB b c k t) :=
  a2IntNorm_ge_one _ _ (numerator_nonzero_of_k_not_divisible a b c k t hk)

theorem numerator_norm_ge_three (a b c l t : ℤ) (hc : ¬ 3 ∣ c) :
    3 ≤ a2IntNorm (numeratorA a c (3*l) t) (numeratorB b c (3*l) t) := by
  apply a2IntNorm_ge_three
  · right
    intro hz
    apply hc
    refine ⟨-b - l*(1+3*t), ?_⟩
    dsimp [numeratorB] at hz
    nlinarith [hz]
  · refine ⟨a+b+c+2*l*(1+3*t), ?_⟩
    dsimp [numeratorA, numeratorB]
    ring

theorem neighbor_as_thirds {n : ℕ} (a b c t : Fin n → ℤ)
    (x : Space n) (k : ℤ)
    (hx : ∀ i, x i = ((a i:ℚ)+2*(c i:ℚ)/3, (b i:ℚ)+(c i:ℚ)/3)) :
    x + (k:ℚ) • ((1/3:ℚ) • radial t) =
      thirds (fun i => numeratorA (a i) (c i) k (t i))
        (fun i => numeratorB (b i) (c i) k (t i)) := by
  ext i <;> simp [hx, thirds, numeratorA, numeratorB, radial] <;> ring

theorem neighbor_as_integerVector {n : ℕ} (a b d t : Fin n → ℤ)
    (x : Space n) (l : ℤ)
    (hx : ∀ i, x i = ((a i:ℚ)+2*(3*(d i):ℤ)/3,
      (b i:ℚ)+((3*(d i):ℤ):ℚ)/3)) :
    x + ((3*l:ℤ):ℚ) • ((1/3:ℚ) • radial t) =
      integerVector (fun i => a i + 2*d i + l*(1+3*t i))
        (fun i => b i+d i+l*(1+3*t i)) := by
  ext i <;> simp [hx, integerVector, radial] <;> ring

#print axioms thirds_norm
#print axioms integerVector_norm
#print axioms integerVector_radial_pair
#print axioms numerator_nonzero_of_k_not_divisible
#print axioms numerator_norm_ge_one
#print axioms numerator_norm_ge_three
#print axioms neighbor_as_thirds
#print axioms neighbor_as_integerVector

end HMT.IV.CoxeterNeighbor
