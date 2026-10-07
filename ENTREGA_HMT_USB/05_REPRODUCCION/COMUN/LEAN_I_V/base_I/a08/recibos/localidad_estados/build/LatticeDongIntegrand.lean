import LatticeTripleConvolution
import LatticeTripleLocality

/-!
The real Dong integrand, built from the existing fields and their ordered
expansion kernels on each input vector. Both annihilators are proved
from the three pairwise field localities. They are not additional inputs
to the final integrand theorem.
-/

noncomputable section
namespace HMT.IV.LatticeDongIntegrand

open HMT.IV.LatticeDongBinomial HMT.IV.LatticeTripleLocality
open HMT.IV.LatticeTripleConvolution HMT.IV.LatticeResidueProducts
open HMT.IV.LatticeFieldLocality HMT.IV.LatticeFactorConvolution

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem rawLeft_secondAdmissible (A B C : VertexOperator ℂ V) (v : V) :
    SecondAdmissible (evaluate v (rawLeft A B C)) := by
  intro c
  obtain ⟨l,hl⟩ := field_lower_bound B (HVertexOperator.coeff C c v)
  obtain ⟨u,hu⟩ := field_lower_bound B v
  refine ⟨min l u, fun a b hb => ?_⟩
  simp only [evaluate, rawLeft, LinearMap.coe_mk, AddHom.coe_mk,
    LinearMap.sub_apply, Module.End.mul_apply,
    hl b (lt_of_lt_of_le hb (min_le_left _ _)),
    hu b (lt_of_lt_of_le hb (min_le_right _ _)), map_zero, sub_self]

theorem rawRight_firstAdmissible (A B C : VertexOperator ℂ V) (v : V) :
    FirstAdmissible (evaluate v (rawRight A B C)) := by
  intro c
  obtain ⟨l,hl⟩ := field_lower_bound A (HVertexOperator.coeff C c v)
  obtain ⟨u,hu⟩ := field_lower_bound A v
  refine ⟨min l u, fun a b ha => ?_⟩
  simp only [evaluate, rawRight, LinearMap.coe_mk, AddHom.coe_mk,
    LinearMap.sub_apply, Module.End.mul_apply,
    hl a (lt_of_lt_of_le ha (min_le_left _ _)),
    hu a (lt_of_lt_of_le ha (min_le_right _ _)), map_zero, sub_self]

def integrand (r : ℤ) (A B C : VertexOperator ℂ V) (v : V) : TriCoefficients V :=
  leftConv r (evaluate v (rawLeft A B C)) -
    rightConv r (evaluate v (rawRight A B C))

/-- The first annihilator follows from A--C and B--C locality after
commuting the finite polynomial with each locally finite convolution. -/
theorem integrand_first_annihilator (r : ℤ) {A B C : VertexOperator ℂ V}
    {p q : ℕ} (hAC : LocalAt p A C) (hBC : LocalAt q B C) (v : V) :
    (firstThird^p) ((secondThird^q) (integrand r A B C v)) = 0 := by
  have hl := rawLeft_secondAdmissible A B C v
  have hr := rawRight_firstAdmissible A B C v
  rw [integrand, map_sub, map_sub,
    ← leftConv_secondThird_pow r q hl, ← rightConv_secondThird_pow r q hr,
    ← leftConv_firstThird_pow r p (secondAdmissible_secondThird_pow q hl),
    ← rightConv_firstThird_pow r p (firstAdmissible_secondThird_pow q hr),
    rawLeft_annihilated_on_vector hAC hBC v,
    rawRight_annihilated_on_vector hAC hBC v,
    leftConv_zero, rightConv_zero, sub_self]

/-- Clearing the two negative kernels gives the same polynomial acting
on the actual double commutator. Locality of A--B then kills it. -/
theorem integrand_second_annihilator {A B C : VertexOperator ℂ V}
    {s : ℕ} (hAB : LocalAt s A B) (n : ℕ) (v : V) :
    (firstSecond^(s+n+1)) (integrand (-(n : ℤ)-1) A B C v) = 0 := by
  have hl := rawLeft_secondAdmissible A B C v
  have hr := rawRight_firstAdmissible A B C v
  rw [integrand, map_sub, firstSecond_pow_leftConv _ _ hl,
    firstSecond_pow_rightConv _ _ hr]
  have hindex : -(n : ℤ)-1+((s+n+1 : ℕ) : ℤ) = (s : ℤ) := by omega
  rw [hindex, leftConv_nonnegative s hl, rightConv_nonnegative s hr, ← map_sub,
    ← map_sub]
  exact rawDifference_annihilated_on_vector hAB v

theorem integrand_second_annihilator_with_factor {A B C : VertexOperator ℂ V}
    {s : ℕ} (hAB : LocalAt s A B) (q n : ℕ) (v : V) :
    (firstSecond^(s+n+1)) ((secondThird^q)
      (integrand (-(n : ℤ)-1) A B C v)) = 0 := by
  rw [← Module.End.mul_apply,
    (firstSecond_secondThird_commute.pow_pow (s+n+1) q).eq,
    Module.End.mul_apply, integrand_second_annihilator hAB n v, map_zero]

/-- Dong's sufficient bound on the residue of the concrete integrand.
Only the three original field localities occur as hypotheses. -/
theorem integrand_residue_locality {A B C : VertexOperator ℂ V}
    {p q s : ℕ} (hAC : LocalAt p A C) (hBC : LocalAt q B C)
    (hAB : LocalAt s A B) (n : ℕ) (v : V) :
    (crossing^(p+q+s+n)) (residue (integrand (-(n : ℤ)-1) A B C v)) = 0 :=
  dong_residue_bound _ p q s n
    (integrand_first_annihilator _ hAC hBC v)
    (integrand_second_annihilator_with_factor hAB q n v)

end HMT.IV.LatticeDongIntegrand
end

#print axioms HMT.IV.LatticeDongIntegrand.rawLeft_secondAdmissible
#print axioms HMT.IV.LatticeDongIntegrand.rawRight_firstAdmissible
#print axioms HMT.IV.LatticeDongIntegrand.integrand_first_annihilator
#print axioms HMT.IV.LatticeDongIntegrand.integrand_second_annihilator
#print axioms HMT.IV.LatticeDongIntegrand.integrand_second_annihilator_with_factor
#print axioms HMT.IV.LatticeDongIntegrand.integrand_residue_locality
