import LatticeDongLocality

/-!
Dong locality for every integer residue index. Negative indices reuse the
proved pole-clearing argument. At a nonnegative index the two expansions are
the same finite polynomial; locality of A and B annihilates their difference.
All statements concern the already defined residueField, not a substitute.
-/

noncomputable section
namespace HMT.IV.LatticeDongAllIndices

open LatticeFieldLocality LatticeFactorConvolution LatticeOrderedConvolution
open LatticeDongBinomial LatticeResidueProducts LatticeDongIntegrand
open LatticeResidueConvolution LatticeTripleConvolution LatticeTripleLocality

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem integrand_second_annihilator_nonnegative {A B C : VertexOperator ℂ V}
    {s : ℕ} (hAB : LocalAt s A B) (r : ℕ) (v : V) :
    (firstSecond^s) (integrand (r : ℤ) A B C v) = 0 := by
  have hl := rawLeft_secondAdmissible A B C v
  have hr := rawRight_firstAdmissible A B C v
  rw [integrand, leftConv_nonnegative r hl, rightConv_nonnegative r hr,
    ← map_sub, ← map_sub, ← Module.End.mul_apply, ← pow_add]
  exact pow_apply_zero_of_le (firstSecond : Module.End ℂ (TriCoefficients V))
    (evaluate v (rawLeft A B C - rawRight A B C)) (Nat.le_add_right s r)
    (rawDifference_annihilated_on_vector hAB v)

theorem integrand_second_nonnegative_with_factor {A B C : VertexOperator ℂ V}
    {s : ℕ} (hAB : LocalAt s A B) (q r : ℕ) (v : V) :
    (firstSecond^(s+1)) ((secondThird^q) (integrand (r : ℤ) A B C v)) = 0 := by
  have hz : (firstSecond^(s+1)) (integrand (r : ℤ) A B C v) = 0 :=
    pow_apply_zero_of_le (firstSecond : Module.End ℂ (TriCoefficients V))
      (integrand (r : ℤ) A B C v) (Nat.le_succ s)
      (integrand_second_annihilator_nonnegative hAB r v)
  rw [← Module.End.mul_apply,
    (firstSecond_secondThird_commute.pow_pow (s+1) q).eq,
    Module.End.mul_apply, hz, map_zero]

theorem integrand_residue_locality_nonnegative {A B C : VertexOperator ℂ V}
    {p q s : ℕ} (hAC : LocalAt p A C) (hBC : LocalAt q B C)
    (hAB : LocalAt s A B) (r : ℕ) (v : V) :
    (crossing^(p+q+s)) (residue (integrand (r : ℤ) A B C v)) = 0 := by
  simpa only [Nat.add_zero] using
    dong_residue_bound (integrand (r : ℤ) A B C v) p q s 0
      (integrand_first_annihilator _ hAC hBC v)
      (integrand_second_nonnegative_with_factor hAB q r v)

theorem residueField_localAt_nonnegative {A B C : VertexOperator ℂ V} {p q s : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) (hAB : LocalAt s A B) (r : ℕ) :
    LocalAt (p+q+s) (residueField (r : ℤ) A B) C := by
  let D := residueField (r : ℤ) A B
  change (crossing^(p+q+s)) (forward D C) = (crossing^(p+q+s)) (backward D C)
  apply sub_eq_zero.mp
  rw [← map_sub]
  funext k l
  apply LinearMap.ext
  intro v
  have hi : residue (integrand (r : ℤ) A B C v) =
      (fun a b => (forward D C a b - backward D C a b) v) := by
    funext a b
    exact residue_convolution_commutator (r : ℤ) A B C v a b
  have he := congrFun (congrFun
    (crossing_pow_evaluate (forward D C-backward D C) (p+q+s) v) k) l
  change ((crossing^(p+q+s)) (forward D C-backward D C) k l) v = 0
  rw [he]
  change (crossing^(p+q+s)) (fun a b => (forward D C a b-backward D C a b) v) k l = 0
  rw [← hi, integrand_residue_locality_nonnegative hAC hBC hAB r v]
  rfl

/-- One sufficient bound for every integer index; it agrees with the
previous bound at r=-n-1 and is p+q+s at every nonnegative index. -/
theorem residueField_localAt_all_indices {A B C : VertexOperator ℂ V} {p q s : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) (hAB : LocalAt s A B) (r : ℤ) :
    LocalAt (p+q+s+(-r-1).toNat) (residueField r A B) C := by
  cases r with
  | ofNat r =>
    have hz : (-(Int.ofNat r)-1).toNat = 0 := by
      change (-(r : ℤ)-1).toNat = 0
      omega
    rw [hz, Nat.add_zero]
    exact residueField_localAt_nonnegative hAC hBC hAB r
  | negSucc n =>
    have hn : (-Int.negSucc n-1).toNat = n := by omega
    rw [hn]
    simpa only [show Int.negSucc n = -(n : ℤ)-1 by omega] using
      LatticeDongLocality.residueField_localAt hAC hBC hAB n

theorem residueField_local_all_indices {A B C : VertexOperator ℂ V}
    (hAC : Local A C) (hBC : Local B C) (hAB : Local A B) (r : ℤ) :
    Local (residueField r A B) C := by
  obtain ⟨p,hp⟩ := hAC
  obtain ⟨q,hq⟩ := hBC
  obtain ⟨s,hs⟩ := hAB
  exact ⟨p+q+s+(-r-1).toNat, residueField_localAt_all_indices hp hq hs r⟩

end HMT.IV.LatticeDongAllIndices
end

#print axioms HMT.IV.LatticeDongAllIndices.integrand_second_annihilator_nonnegative
#print axioms HMT.IV.LatticeDongAllIndices.integrand_second_nonnegative_with_factor
#print axioms HMT.IV.LatticeDongAllIndices.integrand_residue_locality_nonnegative
#print axioms HMT.IV.LatticeDongAllIndices.residueField_localAt_nonnegative
#print axioms HMT.IV.LatticeDongAllIndices.residueField_localAt_all_indices
#print axioms HMT.IV.LatticeDongAllIndices.residueField_local_all_indices
