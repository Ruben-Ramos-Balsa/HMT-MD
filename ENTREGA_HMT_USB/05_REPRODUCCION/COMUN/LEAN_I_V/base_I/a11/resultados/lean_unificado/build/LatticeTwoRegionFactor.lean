import LatticeContractionPascal

/-!
Two expansion regions of the contraction factor. Multiplication by z-w is
the coefficient difference operator, defined before proving its recurrence.
The finite power clearing the two expansions is proved for every integral
pairing. The theorem concerns the scalar factor of the previously constructed
operators, not yet the whole two-field product.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwoRegionFactor
open HMT.IV.LatticeExponentialContraction HMT.IV.LatticeContractionPascal

abbrev BiCoefficients := ℤ → ℤ → ℂ

def crossing : Module.End ℂ BiCoefficients where
  toFun f := fun a b => f (a-1) b - f a (b-1)
  map_add' f g := by funext a b; simp; ring
  map_smul' c f := by funext a b; simp [smul_sub]; ring

def leftExpansion (p : ℤ) : BiCoefficients := fun a b =>
  if 0 ≤ b ∧ a+b=p then scalarContraction p b.toNat else 0

def rightExpansion (p : ℤ) : BiCoefficients := fun a b =>
  (-1 : ℂ)^p * leftExpansion p b a

theorem crossing_left (p : ℤ) : crossing (leftExpansion p) = leftExpansion (p+1) := by
  funext a b
  change leftExpansion p (a-1) b - leftExpansion p a (b-1) = leftExpansion (p+1) a b
  by_cases hs : a+b=p+1
  · have hs1 : a-1+b=p := by omega
    have hs2 : a+(b-1)=p := by omega
    by_cases hb : 0 ≤ b
    · by_cases hz : b=0
      · subst b
        simp [leftExpansion, hs1, hs2, hs]
      · have hb1 : 0 ≤ b-1 := by omega
        have hnat : b.toNat = (b-1).toNat+1 := by omega
        simp only [leftExpansion, hb, hb1, hs1, hs2, hs, and_self, if_true]
        rw [hnat, contraction_pascal]
    · have hb1 : ¬0 ≤ b-1 := by omega
      simp only [leftExpansion,hb,hb1,false_and,if_false,sub_self]
  · have hs1 : a-1+b≠p := by omega
    have hs2 : a+(b-1)≠p := by omega
    simp [leftExpansion,hs,hs1,hs2]

theorem crossing_right (p : ℤ) : crossing (rightExpansion p) = rightExpansion (p+1) := by
  funext a b
  have h := congrFun (congrFun (crossing_left p) b) a
  change leftExpansion p (b-1) a - leftExpansion p b (a-1) = leftExpansion (p+1) b a at h
  change (-1:ℂ)^p * leftExpansion p b (a-1) -
    (-1:ℂ)^p * leftExpansion p (b-1) a = (-1:ℂ)^(p+1) * leftExpansion (p+1) b a
  rw [zpow_add₀ (by norm_num : (-1:ℂ) ≠ 0), zpow_one, ← h]
  ring

theorem crossing_left_iterate (p : ℤ) (n : ℕ) :
    (crossing^n) (leftExpansion p) = leftExpansion (p+n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply, ih, crossing_left]
    push_cast
    ring

theorem crossing_right_iterate (p : ℤ) (n : ℕ) :
    (crossing^n) (rightExpansion p) = rightExpansion (p+n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply, ih, crossing_right]
    push_cast
    ring

theorem zero_expansions_equal : leftExpansion 0 = rightExpansion 0 := by
  funext a b
  simp only [rightExpansion,zpow_zero,one_mul,leftExpansion,contraction_zero_pairing]
  by_cases ha : a=0
  · subst a
    by_cases hb : b=0
    · subst b; simp
    · have hba : ¬(0 ≤ b ∧ b.toNat=0) := by omega
      simp [hb]
  · by_cases hb : b=0
    · subst b; simp [ha]
    · split_ifs <;> simp_all <;> omega

theorem nonnegative_expansions_equal (n : ℕ) : leftExpansion (n:ℤ) = rightExpansion (n:ℤ) := by
  have h := congrArg (fun f : BiCoefficients => (crossing^n) f) zero_expansions_equal
  simpa only [crossing_left_iterate,crossing_right_iterate,zero_add] using h

theorem two_region_polynomial_cancellation (p : ℤ) :
    ∃ n : ℕ, (crossing^n) (leftExpansion p) = (crossing^n) (rightExpansion p) := by
  by_cases hp : 0 ≤ p
  · refine ⟨0, ?_⟩
    have h := nonnegative_expansions_equal p.toNat
    simpa only [Int.toNat_of_nonneg hp, pow_zero, Module.End.one_apply] using h
  · refine ⟨(-p).toNat, ?_⟩
    rw [crossing_left_iterate,crossing_right_iterate]
    have hz : p+((-p).toNat : ℤ)=0 := by omega
    rw [hz]
    exact zero_expansions_equal

end HMT.IV.LatticeTwoRegionFactor
end

#print axioms HMT.IV.LatticeTwoRegionFactor.crossing_left
#print axioms HMT.IV.LatticeTwoRegionFactor.crossing_right
#print axioms HMT.IV.LatticeTwoRegionFactor.crossing_left_iterate
#print axioms HMT.IV.LatticeTwoRegionFactor.crossing_right_iterate
#print axioms HMT.IV.LatticeTwoRegionFactor.zero_expansions_equal
#print axioms HMT.IV.LatticeTwoRegionFactor.nonnegative_expansions_equal
#print axioms HMT.IV.LatticeTwoRegionFactor.two_region_polynomial_cancellation
