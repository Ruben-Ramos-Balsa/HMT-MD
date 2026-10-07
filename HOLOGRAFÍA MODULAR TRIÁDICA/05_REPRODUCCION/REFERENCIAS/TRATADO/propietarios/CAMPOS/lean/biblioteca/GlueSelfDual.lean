import PaleyWittDuality

/-! Integral autoduality of the actual ternary glue, derived from the
simple-root pairings and the autoduality of the explicit Paley–Witt code. -/
namespace HMT.IV.GlueDuality

open HMT.IV.CoxeterNeighbor

set_option maxHeartbeats 1200000

def integralDual {n : ℕ} (L : AddSubgroup (Space n)) : Set (Space n) :=
  {x | ∀ y ∈ L, ∃ m : ℤ, pairing x y = (m:ℚ)}

def coordinateRootA {n : ℕ} (i : Fin n) : Space n :=
  fun j => if j=i then (1,0) else (0,0)

def coordinateRootB {n : ℕ} (i : Fin n) : Space n :=
  fun j => if j=i then (0,1) else (0,0)

theorem coordinateRootA_mem_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (i : Fin n) :
    coordinateRootA i ∈ glue C := by
  refine ⟨(fun j => if j=i then 1 else 0), 0, 0, ?_, ?_⟩
  · simpa using C.zero_mem
  · intro j
    by_cases h : j=i <;> simp [coordinateRootA, h]

theorem coordinateRootB_mem_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (i : Fin n) :
    coordinateRootB i ∈ glue C := by
  refine ⟨0, (fun j => if j=i then 1 else 0), 0, ?_, ?_⟩
  · simpa using C.zero_mem
  · intro j
    by_cases h : j=i <;> simp [coordinateRootB, h]

theorem pairing_coordinateRootA {n : ℕ} (x : Space n) (i : Fin n) :
    pairing x (coordinateRootA i) = 2*(x i).1 - (x i).2 := by
  calc
    _ = ∑ j, if j=i then 2*(x j).1 - (x j).2 else 0 := by
      apply Finset.sum_congr rfl
      intro j _
      by_cases h : j=i <;> simp [coordinateRootA, localPair, h]
    _ = _ := by simp

theorem pairing_coordinateRootB {n : ℕ} (x : Space n) (i : Fin n) :
    pairing x (coordinateRootB i) = -(x i).1 + 2*(x i).2 := by
  calc
    _ = ∑ j, if j=i then -(x j).1 + 2*(x j).2 else 0 := by
      apply Finset.sum_congr rfl
      intro j _
      by_cases h : j=i <;> simp [coordinateRootB, localPair, h]
    _ = _ := by simp

/-- Pairings with the two roots recover a denominator-three presentation.
No code membership is assumed for the recovered word here. -/
theorem dual_coordinate_decomposition {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) {x : Space n}
    (hx : x ∈ integralDual (glue C)) :
    ∃ b c : Fin n → ℤ, ∀ i,
      x i = (-(b i:ℚ) + 2*(c i:ℚ)/3, (c i:ℚ)/3) := by
  have hA : ∀ i, ∃ a : ℤ, 2*(x i).1 - (x i).2 = (a:ℚ) := by
    intro i
    simpa only [pairing_coordinateRootA] using
      hx _ (coordinateRootA_mem_glue C i)
  have hB : ∀ i, ∃ b : ℤ, -(x i).1 + 2*(x i).2 = (b:ℚ) := by
    intro i
    simpa only [pairing_coordinateRootB] using
      hx _ (coordinateRootB_mem_glue C i)
  choose a ha using hA
  choose b hb using hB
  refine ⟨b, (fun i => a i+2*b i), ?_⟩
  intro i
  apply Prod.ext <;> dsimp only
  · push_cast
    linarith [ha i, hb i]
  · push_cast
    linarith [ha i, hb i]

def codeLift {n : ℕ} (d : Fin n → ℤ) : Space n :=
  fun i => (2*(d i:ℚ)/3, (d i:ℚ)/3)

theorem codeLift_mem_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (d : Fin n → ℤ)
    (hd : (fun i => (d i : ZMod 3)) ∈ C) : codeLift d ∈ glue C := by
  exact ⟨0, 0, d, hd, fun i => by simp [codeLift]⟩

theorem pairing_codeLift {n : ℕ} (x : Space n) (b c d : Fin n → ℤ)
    (hx : ∀ i, x i = (-(b i:ℚ)+2*(c i:ℚ)/3, (c i:ℚ)/3)) :
    pairing x (codeLift d) =
      2*((∑ i, c i*d i : ℤ):ℚ)/3 - ((∑ i, b i*d i : ℤ):ℚ) := by
  simp only [Int.cast_sum, Int.cast_mul]
  rw [Finset.mul_sum, Finset.sum_div, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  simp only [hx i, localPair, codeLift]
  ring

theorem recovered_word_orthogonal_lifts {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) {x : Space n}
    (hx : x ∈ integralDual (glue C)) (b c : Fin n → ℤ)
    (hcoord : ∀ i, x i = (-(b i:ℚ)+2*(c i:ℚ)/3, (c i:ℚ)/3))
    (d : Fin n → ℤ) (hd : (fun i => (d i : ZMod 3)) ∈ C) :
    3 ∣ ∑ i, c i*d i := by
  obtain ⟨m, hm⟩ := hx (codeLift d) (codeLift_mem_glue C d hd)
  rw [pairing_codeLift x b c d hcoord] at hm
  have hq : ((2*(∑ i, c i*d i):ℤ):ℚ) =
      ((3*(m+(∑ i, b i*d i)):ℤ):ℚ) := by
    push_cast at hm ⊢
    linarith [hm]
  have hi : (2*(∑ i, c i*d i):ℤ) = 3*(m+(∑ i, b i*d i)) := by
    exact_mod_cast hq
  refine ⟨2*(m+(∑ i, b i*d i)) - (∑ i, c i*d i), ?_⟩
  omega

theorem recovered_word_mem_wittCode {x : Space 12}
    (hx : x ∈ integralDual (glue wittCode)) (b c : Fin 12 → ℤ)
    (hcoord : ∀ i, x i = (-(b i:ℚ)+2*(c i:ℚ)/3, (c i:ℚ)/3)) :
    (fun i => (c i : ZMod 3)) ∈ wittCode := by
  apply (HMT.PaleyWittDuality.mem_orthogonal_iff _).mp
  intro e he
  let d : Fin 12 → ℤ := fun i => (e i).val
  have hd : (fun i => (d i : ZMod 3)) = e := by
    funext i
    simp [d]
  have hm : (fun i => (d i : ZMod 3)) ∈ wittCode := by rw [hd]; exact he
  have hdiv := recovered_word_orthogonal_lifts wittCode hx b c hcoord d hm
  have hz : ((∑ i, c i*d i : ℤ):ZMod 3) = 0 :=
    (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mpr hdiv
  push_cast at hz
  simpa [d, mul_comm] using hz

theorem witt_glue_dual_subset :
    integralDual (glue wittCode) ⊆ (glue wittCode : Set (Space 12)) := by
  intro x hx
  obtain ⟨b, c, hc⟩ := dual_coordinate_decomposition wittCode hx
  refine ⟨-b, 0, c, recovered_word_mem_wittCode hx b c hc, ?_⟩
  intro i
  simpa only [Pi.neg_apply, Pi.zero_apply, Int.cast_neg, Int.cast_zero,
    zero_add] using hc i

theorem witt_glue_dual_iff (x : Space 12) :
    x ∈ integralDual (glue wittCode) ↔ x ∈ glue wittCode := by
  constructor
  · exact fun hx => witt_glue_dual_subset hx
  · intro hx y hy
    exact witt_glue_integral x hx y hy

theorem witt_glue_selfDual :
    integralDual (glue wittCode) = (glue wittCode : Set (Space 12)) := by
  ext x
  exact witt_glue_dual_iff x

#print axioms coordinateRootA_mem_glue
#print axioms coordinateRootB_mem_glue
#print axioms pairing_coordinateRootA
#print axioms pairing_coordinateRootB
#print axioms dual_coordinate_decomposition
#print axioms codeLift_mem_glue
#print axioms pairing_codeLift
#print axioms recovered_word_orthogonal_lifts
#print axioms recovered_word_mem_wittCode
#print axioms witt_glue_dual_subset
#print axioms witt_glue_dual_iff
#print axioms witt_glue_selfDual

end HMT.IV.GlueDuality
