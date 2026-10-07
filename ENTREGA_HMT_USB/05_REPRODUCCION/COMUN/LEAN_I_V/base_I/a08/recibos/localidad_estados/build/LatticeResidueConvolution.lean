import LatticeTripleConvolution
import LatticeTripleLocality

/-!
The residue of the actual ordered triple convolutions is the commutator
of the previously constructed residueCoefficient. Integer-to-natural
reindexing uses the exact supports of the two scalar kernel regions.
Every linear-map/sum interchange is justified on the fixed input vector.
-/

noncomputable section
namespace HMT.IV.LatticeResidueConvolution

open LatticeFactorConvolution LatticeOrderedConvolution LatticeResidueProducts
open LatticeTripleConvolution LatticeTripleLocality LatticeDongBinomial

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

omit [Module ℂ V] in
private theorem finsum_of_nonnegative_support (f : ℤ → V)
    (hf : ∀ j < 0, f j = 0) : (∑ᶠ j : ℤ, f j) = ∑ᶠ a : ℕ, f (a : ℤ) := by
  have hinj : Function.Injective (fun a : ℕ => (a : ℤ)) := by
    intro a b h
    change (a : ℤ) = (b : ℤ) at h
    exact_mod_cast h
  rw [← finsum_mem_range hinj]
  apply finsum_congr
  intro j
  by_cases hj : 0 ≤ j
  · have hr : j ∈ Set.range (fun a : ℕ => (a : ℤ)) :=
      ⟨j.toNat, by change (j.toNat : ℤ) = j; omega⟩
    simp only [hr, finsum_true]
  · have hr : j ∉ Set.range (fun a : ℕ => (a : ℤ)) := by
      rintro ⟨a, ha⟩
      change (a : ℤ) = j at ha
      omega
    simp only [hr, finsum_false, hf j (by omega)]

omit [Module ℂ V] in
private theorem finsum_of_upper_support (p : ℤ) (f : ℤ → V)
    (hf : ∀ j, p < j → f j = 0) :
    (∑ᶠ j : ℤ, f j) = ∑ᶠ a : ℕ, f (p-(a : ℤ)) := by
  have hinj : Function.Injective (fun a : ℕ => p-(a : ℤ)) := by
    intro a b h
    change p-(a : ℤ) = p-(b : ℤ) at h
    have he : (a : ℤ) = (b : ℤ) := by omega
    exact_mod_cast he
  rw [← finsum_mem_range hinj]
  apply finsum_congr
  intro j
  by_cases hj : j ≤ p
  · have hr : j ∈ Set.range (fun a : ℕ => p-(a : ℤ)) :=
      ⟨(p-j).toNat, by change p-((p-j).toNat : ℤ) = j; omega⟩
    simp only [hr, finsum_true]
  · have hr : j ∉ Set.range (fun a : ℕ => p-(a : ℤ)) := by
      rintro ⟨a, ha⟩
      change p-(a : ℤ) = j at ha
      omega
    simp only [hr, finsum_false, hf j (by omega)]

/-- Exact reindexing of the left kernel support; no cutoff is imposed. -/
theorem leftProduct_residue_nat (p : ℤ) (h : BiStates V) (k : ℤ) :
    leftProduct p h (-1) k = ∑ᶠ a : ℕ,
      LatticeTwoRegionFactor.leftExpansion p (p-a) a • h (a-p-1) (k-a) := by
  unfold leftProduct convolution
  rw [finsum_of_nonnegative_support _ (by
    intro j hj
    rw [leftKernel_support p j hj, zero_smul])]
  apply finsum_congr
  intro a
  rw [show (-1 : ℤ)-p+(a : ℤ) = (a : ℤ)-p-1 by omega]
  rfl

/-- The opposite kernel is reindexed by `j=p-a`, preserving its order. -/
theorem rightProduct_residue_nat (p : ℤ) (h : BiStates V) (k : ℤ) :
    rightProduct p h (-1) k = ∑ᶠ a : ℕ,
      LatticeTwoRegionFactor.rightExpansion p a (p-a) • h (-a-1) (k-p+a) := by
  unfold rightProduct convolution
  rw [finsum_of_upper_support p _ (by
    intro j hj
    rw [rightKernel_support p j hj, zero_smul])]
  apply finsum_congr
  intro a
  simp only [rightKernel]
  rw [show p-(p-(a : ℤ)) = (a : ℤ) by omega,
    show (-1 : ℤ)-p+(p-(a : ℤ)) = -(a : ℤ)-1 by omega,
    show k-(p-(a : ℤ)) = k-p+(a : ℤ) by omega]

theorem leftProduct_forward_residue (p : ℤ) (A B : VertexOperator ℂ V)
    (k : ℤ) (v : V) :
    leftProduct p (forwardState A B v) (-1) k =
      ∑ᶠ a : ℕ, leftTerm p A B k a v := by
  rw [leftProduct_residue_nat]
  rfl

theorem rightProduct_backward_residue (p : ℤ) (A B : VertexOperator ℂ V)
    (k : ℤ) (v : V) :
    rightProduct p (backwardState A B v) (-1) k =
      ∑ᶠ a : ℕ, rightTerm p A B k a v := by
  rw [rightProduct_residue_nat]
  rfl

private theorem finsum_sub_map (f g : ℕ → V) (hf : (Function.support f).Finite)
    (hg : (Function.support g).Finite) (T : Module.End ℂ V) :
    (∑ᶠ a, (f a - T (g a))) = (∑ᶠ a, f a) - T (∑ᶠ a, g a) := by
  have hTg : (Function.support (fun a => T (g a))).Finite := by
    apply hg.subset
    intro a ha
    intro hz
    exact ha (show T (g a) = 0 by rw [hz, map_zero])
  rw [finsum_sub_distrib hf hTg]
  congr 1
  exact (T.toAddMonoidHom.map_finsum hg).symm

theorem leftConv_raw_residue (p : ℤ) (A B C : VertexOperator ℂ V)
    (v : V) (k l : ℤ) :
    leftConv p (evaluate v (rawLeft A B C)) (-1) k l =
      (∑ᶠ a, leftTerm p A B k a (HVertexOperator.coeff C l v)) -
        HVertexOperator.coeff C l (∑ᶠ a, leftTerm p A B k a v) := by
  unfold leftConv
  rw [leftProduct_residue_nat]
  calc
    _ = ∑ᶠ a : ℕ,
        (leftTerm p A B k a (HVertexOperator.coeff C l v) -
          HVertexOperator.coeff C l (leftTerm p A B k a v)) := by
      apply finsum_congr
      intro a
      simp only [evaluate, rawLeft, LinearMap.coe_mk, AddHom.coe_mk,
        LinearMap.sub_apply, Module.End.mul_apply, leftTerm,
        LinearMap.smul_apply, LinearMap.comp_apply, smul_sub, map_smul]
    _ = _ := finsum_sub_map _ _ (leftTerm_finite p A B k _)
      (leftTerm_finite p A B k v) (HVertexOperator.coeff C l)

theorem rightConv_raw_residue (p : ℤ) (A B C : VertexOperator ℂ V)
    (v : V) (k l : ℤ) :
    rightConv p (evaluate v (rawRight A B C)) (-1) k l =
      (∑ᶠ a, rightTerm p A B k a (HVertexOperator.coeff C l v)) -
        HVertexOperator.coeff C l (∑ᶠ a, rightTerm p A B k a v) := by
  unfold rightConv
  rw [rightProduct_residue_nat]
  calc
    _ = ∑ᶠ a : ℕ,
        (rightTerm p A B k a (HVertexOperator.coeff C l v) -
          HVertexOperator.coeff C l (rightTerm p A B k a v)) := by
      apply finsum_congr
      intro a
      simp only [evaluate, rawRight, LinearMap.coe_mk, AddHom.coe_mk,
        LinearMap.sub_apply, Module.End.mul_apply, rightTerm,
        LinearMap.smul_apply, LinearMap.comp_apply, smul_sub, map_smul]
    _ = _ := finsum_sub_map _ _ (rightTerm_finite p A B k _)
      (rightTerm_finite p A B k v) (HVertexOperator.coeff C l)

/-- The final port to the already constructed residue field. This is an
identity on every vector and all Laurent coefficients, not an assumed
Jacobi identity or a finite-mode approximation. -/
theorem residue_convolution_commutator (p : ℤ) (A B C : VertexOperator ℂ V)
    (v : V) (k l : ℤ) :
    residue (leftConv p (evaluate v (rawLeft A B C)) -
      rightConv p (evaluate v (rawRight A B C))) k l =
    residueCoefficient p A B k (HVertexOperator.coeff C l v) -
      HVertexOperator.coeff C l (residueCoefficient p A B k v) := by
  change leftConv p (evaluate v (rawLeft A B C)) (-1) k l -
    rightConv p (evaluate v (rawRight A B C)) (-1) k l = _
  rw [leftConv_raw_residue, rightConv_raw_residue,
    residueCoefficient_apply, residueCoefficient_apply, map_sub]
  abel

end HMT.IV.LatticeResidueConvolution
end

#print axioms HMT.IV.LatticeResidueConvolution.leftProduct_residue_nat
#print axioms HMT.IV.LatticeResidueConvolution.rightProduct_residue_nat
#print axioms HMT.IV.LatticeResidueConvolution.leftProduct_forward_residue
#print axioms HMT.IV.LatticeResidueConvolution.rightProduct_backward_residue
#print axioms HMT.IV.LatticeResidueConvolution.leftConv_raw_residue
#print axioms HMT.IV.LatticeResidueConvolution.rightConv_raw_residue
#print axioms HMT.IV.LatticeResidueConvolution.residue_convolution_commutator
