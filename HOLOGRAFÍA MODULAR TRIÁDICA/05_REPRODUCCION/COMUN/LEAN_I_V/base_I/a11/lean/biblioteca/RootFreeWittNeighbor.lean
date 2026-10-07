import NeighborRootCoordinates
import WittMinimumWeight

namespace HMT.IV.CoxeterNeighbor

set_option maxHeartbeats 1200000

def NoNormTwoNeighbor {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (v : Space n) : Prop :=
  ∀ w ∈ neighbor C v, pairing w w ≠ 2

theorem numerator_norm_sum_ge_twelve (a b c t : Fin 12 → ℤ) (k : ℤ)
    (hk : ¬ 3 ∣ k) :
    12 ≤ ∑ i, a2IntNorm (numeratorA (a i) (c i) k (t i))
      (numeratorB (b i) (c i) k (t i)) := by
  calc
    12 = ∑ _i : Fin 12, (1:ℤ) := by norm_num
    _ ≤ _ := Finset.sum_le_sum fun i _ =>
      numerator_norm_ge_one (a i) (b i) (c i) k (t i) hk

theorem numerator_norm_sum_ge_weight (a b c t : Fin 12 → ℤ) (l : ℤ) :
    3 * (hammingWeight (fun i => (c i : ZMod 3)) : ℤ) ≤
      ∑ i, a2IntNorm (numeratorA (a i) (c i) (3*l) (t i))
        (numeratorB (b i) (c i) (3*l) (t i)) := by
  have hw : (hammingWeight (fun i => (c i : ZMod 3)) : ℤ) =
      ∑ i : Fin 12, if (c i : ZMod 3) = 0 then (0:ℤ) else 1 := by
    simp [hammingWeight]
  rw [hw, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  by_cases hi : (c i : ZMod 3) = 0
  · simp only [hi, if_pos, mul_zero]
    exact a2IntNorm_nonneg _ _
  · simp only [hi, if_neg, mul_one]
    apply numerator_norm_ge_three
    intro hd
    exact hi ((ZMod.intCast_zmod_eq_zero_iff_dvd (c i) 3).mpr hd)

/-- Root exclusion for the explicit code and any marked origin.
The proof uses all twelve coordinates and the proved minimum weight six.
-/
theorem witt_marked_neighbor_no_norm_two (o : Fin 12) :
    NoNormTwoNeighbor wittCode (radial (marked o)) := by
  rintro w ⟨x, hx, k, rfl⟩ htwo
  obtain ⟨a, b, c, hc, hcoord⟩ := hx.1
  have hnum :
      (∑ i, a2IntNorm (numeratorA (a i) (c i) k (marked o i))
        (numeratorB (b i) (c i) k (marked o i)) : ℤ) = 9 := by
    have hthird := neighbor_as_thirds a b c (marked o) x k hcoord
    rw [hthird, thirds_norm] at htwo
    have hr :
        ((∑ i, a2IntNorm (numeratorA (a i) (c i) k (marked o i))
          (numeratorB (b i) (c i) k (marked o i)) : ℤ):ℚ) = 9 := by
      linarith
    exact_mod_cast hr
  have hk : 3 ∣ k := by
    by_contra hkn
    have hb := numerator_norm_sum_ge_twelve a b c (marked o) k hkn
    omega
  obtain ⟨l, rfl⟩ := hk
  have hcz : (fun i => (c i : ZMod 3)) = 0 := by
    by_contra hcn
    have hweight := witt_nonzero_weight_ge_six hc hcn
    have hb := numerator_norm_sum_ge_weight a b c (marked o) l
    have hweight' : (6:ℤ) ≤ (hammingWeight (fun i => (c i : ZMod 3)) : ℤ) :=
      by exact_mod_cast hweight
    omega
  have hdiv : ∀ i, ∃ d : ℤ, c i = 3*d := by
    intro i
    have hz : (c i : ZMod 3) = 0 := congrFun hcz i
    exact (ZMod.intCast_zmod_eq_zero_iff_dvd (c i) 3).mp hz
  choose d hd using hdiv
  let aa : Fin 12 → ℤ := fun i => a i + 2*d i + l*(1+3*marked o i)
  let bb : Fin 12 → ℤ := fun i => b i + d i + l*(1+3*marked o i)
  have hcoord' : ∀ i, x i = ((a i:ℚ)+2*((3*d i:ℤ):ℚ)/3,
      (b i:ℚ)+((3*d i:ℤ):ℚ)/3) := by
    intro i
    rw [hcoord i, hd i]
  have hw : x + ((3*l:ℤ):ℚ) • ((1/3:ℚ) • radial (marked o)) =
      integerVector aa bb :=
    neighbor_as_integerVector a b d (marked o) x l hcoord'
  have hone : (∑ i, a2IntNorm (aa i) (bb i) : ℤ) = 1 := by
    rw [hw, integerVector_norm] at htwo
    have hr : ((∑ i, a2IntNorm (aa i) (bb i) : ℤ):ℚ) = 1 := by linarith
    exact_mod_cast hr
  obtain ⟨j, hj⟩ := hx.2
  have hp : pairing (integerVector aa bb) (radial (marked o)) =
      3 * ((j+18*l:ℤ):ℚ) := by
    rw [← hw, pairing_add_left, pairing_smul_left, pairing_smul_left,
      hj, marked_radial_norm]
    push_cast
    ring
  rw [integerVector_radial_pair] at hp
  have hpint : (∑ i, (aa i + bb i)*(1+3*marked o i) : ℤ) = 3*(j+18*l) := by
    exact_mod_cast hp
  exact integer_root_radial_pair_not_divisible aa bb (marked o) hone ⟨_, hpint⟩

#print axioms numerator_norm_sum_ge_twelve
#print axioms numerator_norm_sum_ge_weight
#print axioms witt_marked_neighbor_no_norm_two

end HMT.IV.CoxeterNeighbor
