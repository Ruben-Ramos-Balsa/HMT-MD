import LatticeDongBinomial
import LatticeFieldLocality

/-!
The first actual triple annihilation in Dong's argument. Only the original
A--C and B--C localities are used. These are endomorphism-valued coefficient
arrays (no infinite sums); their evaluation on a fixed vector intertwines
all three crossing operators, for later locally finite kernel convolution.
-/

noncomputable section
namespace HMT.IV.LatticeTripleLocality

open LatticeDongBinomial LatticeFactorConvolution LatticeFieldLocality

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

private theorem pow_intertwines {W W' : Type*}
    [AddCommGroup W] [Module ℂ W] [AddCommGroup W'] [Module ℂ W']
    (X : Module.End ℂ W) (Y : Module.End ℂ W') (e : W →ₗ[ℂ] W')
    (h : ∀ f, Y (e f) = e (X f)) (N : ℕ) (f : W) :
    (Y^N) (e f) = e ((X^N) f) := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [pow_succ', Module.End.mul_apply, ih, h,
      pow_succ', Module.End.mul_apply]

def pairCommutator (A C : VertexOperator ℂ V) : BiStates (Module.End ℂ V) :=
  forward A C - backward A C

theorem locality_annihilates_pair {A C : VertexOperator ℂ V} {p : ℕ}
    (h : LocalAt p A C) : (crossing^p) (pairCommutator A C) = 0 := by
  unfold LocalAt at h
  rw [pairCommutator, map_sub, h, sub_self]

def leftOfBC (A : VertexOperator ℂ V) :
    BiStates (Module.End ℂ V) →ₗ[ℂ] TriCoefficients (Module.End ℂ V) where
  toFun f a b c := HVertexOperator.coeff A a * f b c
  map_add' f g := by funext a b c; simp [mul_add]
  map_smul' q f := by funext a b c; simp [mul_smul_comm]

def rightOfBC (A : VertexOperator ℂ V) :
    BiStates (Module.End ℂ V) →ₗ[ℂ] TriCoefficients (Module.End ℂ V) where
  toFun f a b c := f b c * HVertexOperator.coeff A a
  map_add' f g := by funext a b c; simp [add_mul]
  map_smul' q f := by funext a b c; simp [smul_mul_assoc]

def leftOfAC (B : VertexOperator ℂ V) :
    BiStates (Module.End ℂ V) →ₗ[ℂ] TriCoefficients (Module.End ℂ V) where
  toFun f a b c := HVertexOperator.coeff B b * f a c
  map_add' f g := by funext a b c; simp [mul_add]
  map_smul' q f := by funext a b c; simp [mul_smul_comm]

def rightOfAC (B : VertexOperator ℂ V) :
    BiStates (Module.End ℂ V) →ₗ[ℂ] TriCoefficients (Module.End ℂ V) where
  toFun f a b c := f a c * HVertexOperator.coeff B b
  map_add' f g := by funext a b c; simp [add_mul]
  map_smul' q f := by funext a b c; simp [smul_mul_assoc]

theorem secondThird_leftOfBC (A : VertexOperator ℂ V) (f : BiStates (Module.End ℂ V)) :
    secondThird (leftOfBC A f) = leftOfBC A (crossing f) := by
  funext a b c
  simp [secondThird, leftOfBC, crossing, mul_sub]

theorem secondThird_rightOfBC (A : VertexOperator ℂ V) (f : BiStates (Module.End ℂ V)) :
    secondThird (rightOfBC A f) = rightOfBC A (crossing f) := by
  funext a b c
  simp [secondThird, rightOfBC, crossing, sub_mul]

theorem firstThird_leftOfAC (B : VertexOperator ℂ V) (f : BiStates (Module.End ℂ V)) :
    firstThird (leftOfAC B f) = leftOfAC B (crossing f) := by
  funext a b c
  simp [firstThird, leftOfAC, crossing, mul_sub]

theorem firstThird_rightOfAC (B : VertexOperator ℂ V) (f : BiStates (Module.End ℂ V)) :
    firstThird (rightOfAC B f) = rightOfAC B (crossing f) := by
  funext a b c
  simp [firstThird, rightOfAC, crossing, sub_mul]

theorem firstThird_secondThird_commute :
    Commute (firstThird : Module.End ℂ (TriCoefficients V)) secondThird := by
  rw [← triple_crossings_sub]
  exact (Commute.refl _).sub_right triple_crossings_commute

theorem firstSecond_secondThird_commute :
    Commute (firstSecond : Module.End ℂ (TriCoefficients V)) secondThird := by
  rw [← triple_crossings_sub]
  exact triple_crossings_commute.symm.sub_right (Commute.refl _)

private theorem annihilate_sum (F G : TriCoefficients V) (p q : ℕ)
    (hF : (secondThird^q) F = 0) (hG : (firstThird^p) G = 0) :
    (firstThird^p) ((secondThird^q) (F+G)) = 0 := by
  rw [map_add, hF, zero_add, ← Module.End.mul_apply,
    (firstThird_secondThird_commute.pow_pow p q).eq,
    Module.End.mul_apply, hG, map_zero]

/-- The raw coefficient of `A(t)B(z)C(w)-C(w)A(t)B(z)`. -/
def rawLeft (A B C : VertexOperator ℂ V) : TriCoefficients (Module.End ℂ V) :=
  fun a b c => HVertexOperator.coeff A a * HVertexOperator.coeff B b *
      HVertexOperator.coeff C c -
    HVertexOperator.coeff C c * HVertexOperator.coeff A a * HVertexOperator.coeff B b

/-- The raw coefficient of `B(z)A(t)C(w)-C(w)B(z)A(t)`. -/
def rawRight (A B C : VertexOperator ℂ V) : TriCoefficients (Module.End ℂ V) :=
  fun a b c => HVertexOperator.coeff B b * HVertexOperator.coeff A a *
      HVertexOperator.coeff C c -
    HVertexOperator.coeff C c * HVertexOperator.coeff B b * HVertexOperator.coeff A a

theorem rawLeft_decomposition (A B C : VertexOperator ℂ V) :
    rawLeft A B C = leftOfBC A (pairCommutator B C) +
      rightOfAC B (pairCommutator A C) := by
  funext a b c
  simp only [rawLeft, leftOfBC, rightOfAC, pairCommutator, forward, backward,
    LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply, Pi.sub_apply]
  noncomm_ring

theorem rawRight_decomposition (A B C : VertexOperator ℂ V) :
    rawRight A B C = rightOfBC A (pairCommutator B C) +
      leftOfAC B (pairCommutator A C) := by
  funext a b c
  simp only [rawRight, rightOfBC, leftOfAC, pairCommutator, forward, backward,
    LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply, Pi.sub_apply]
  noncomm_ring

theorem rawLeft_annihilated {A B C : VertexOperator ℂ V} {p q : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) :
    (firstThird^p) ((secondThird^q) (rawLeft A B C)) = 0 := by
  rw [rawLeft_decomposition]
  apply annihilate_sum
  · rw [pow_intertwines crossing secondThird (leftOfBC A)
      (secondThird_leftOfBC A), locality_annihilates_pair hBC, map_zero]
  · rw [pow_intertwines crossing firstThird (rightOfAC B)
      (firstThird_rightOfAC B), locality_annihilates_pair hAC, map_zero]

theorem rawRight_annihilated {A B C : VertexOperator ℂ V} {p q : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) :
    (firstThird^p) ((secondThird^q) (rawRight A B C)) = 0 := by
  rw [rawRight_decomposition]
  apply annihilate_sum
  · rw [pow_intertwines crossing secondThird (rightOfBC A)
      (secondThird_rightOfBC A), locality_annihilates_pair hBC, map_zero]
  · rw [pow_intertwines crossing firstThird (leftOfAC B)
      (firstThird_leftOfAC B), locality_annihilates_pair hAC, map_zero]

def commutatorWithC (C : VertexOperator ℂ V) :
    BiStates (Module.End ℂ V) →ₗ[ℂ] TriCoefficients (Module.End ℂ V) where
  toFun f a b c := f a b * HVertexOperator.coeff C c -
    HVertexOperator.coeff C c * f a b
  map_add' f g := by funext a b c; simp [add_mul, mul_add]; abel
  map_smul' q f := by
    funext a b c
    simp [smul_mul_assoc, mul_smul_comm, smul_sub]

theorem firstSecond_commutatorWithC (C : VertexOperator ℂ V)
    (f : BiStates (Module.End ℂ V)) :
    firstSecond (commutatorWithC C f) = commutatorWithC C (crossing f) := by
  funext a b c
  simp [firstSecond, commutatorWithC, crossing, sub_mul, mul_sub]
  abel

theorem raw_difference_decomposition (A B C : VertexOperator ℂ V) :
    rawLeft A B C - rawRight A B C = commutatorWithC C (pairCommutator A B) := by
  funext a b c
  simp only [rawLeft, rawRight, commutatorWithC, pairCommutator, forward, backward,
    LinearMap.coe_mk, AddHom.coe_mk, Pi.sub_apply]
  noncomm_ring

/-- After the two scalar kernels have become the same polynomial, the
remaining raw expression is exactly `[[A(t),B(z)],C(w)]`. -/
theorem rawDifference_annihilated {A B C : VertexOperator ℂ V} {s : ℕ}
    (hAB : LocalAt s A B) :
    (firstSecond^s) (rawLeft A B C - rawRight A B C) = 0 := by
  rw [raw_difference_decomposition,
    pow_intertwines crossing firstSecond (commutatorWithC C)
      (firstSecond_commutatorWithC C), locality_annihilates_pair hAB, map_zero]

theorem rawDifference_annihilated_after_secondThird {A B C : VertexOperator ℂ V}
    {s : ℕ} (hAB : LocalAt s A B) (q : ℕ) :
    (firstSecond^s) ((secondThird^q) (rawLeft A B C - rawRight A B C)) = 0 := by
  rw [← Module.End.mul_apply, (firstSecond_secondThird_commute.pow_pow s q).eq,
    Module.End.mul_apply, rawDifference_annihilated hAB, map_zero]

/-- Evaluation is made before any infinite convolution; no uniform
finite support of endomorphism-valued coefficients is asserted. -/
def evaluate (v : V) :
    TriCoefficients (Module.End ℂ V) →ₗ[ℂ] TriCoefficients V where
  toFun F a b c := F a b c v
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem evaluate_firstThird_pow (v : V) (F : TriCoefficients (Module.End ℂ V)) (N : ℕ) :
    evaluate v ((firstThird^N) F) = (firstThird^N) (evaluate v F) := by
  symm
  apply pow_intertwines firstThird firstThird (evaluate v)
  intro G
  rfl

theorem evaluate_firstSecond_pow (v : V) (F : TriCoefficients (Module.End ℂ V)) (N : ℕ) :
    evaluate v ((firstSecond^N) F) = (firstSecond^N) (evaluate v F) := by
  symm
  apply pow_intertwines firstSecond firstSecond (evaluate v)
  intro G
  rfl

theorem evaluate_secondThird_pow (v : V) (F : TriCoefficients (Module.End ℂ V)) (N : ℕ) :
    evaluate v ((secondThird^N) F) = (secondThird^N) (evaluate v F) := by
  symm
  apply pow_intertwines secondThird secondThird (evaluate v)
  intro G
  rfl

theorem rawLeft_annihilated_on_vector {A B C : VertexOperator ℂ V} {p q : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) (v : V) :
    (firstThird^p) ((secondThird^q) (evaluate v (rawLeft A B C))) = 0 := by
  rw [← evaluate_secondThird_pow, ← evaluate_firstThird_pow,
    rawLeft_annihilated hAC hBC, map_zero]

theorem rawRight_annihilated_on_vector {A B C : VertexOperator ℂ V} {p q : ℕ}
    (hAC : LocalAt p A C) (hBC : LocalAt q B C) (v : V) :
    (firstThird^p) ((secondThird^q) (evaluate v (rawRight A B C))) = 0 := by
  rw [← evaluate_secondThird_pow, ← evaluate_firstThird_pow,
    rawRight_annihilated hAC hBC, map_zero]

theorem rawDifference_annihilated_on_vector {A B C : VertexOperator ℂ V} {s : ℕ}
    (hAB : LocalAt s A B) (v : V) :
    (firstSecond^s) (evaluate v (rawLeft A B C - rawRight A B C)) = 0 := by
  rw [← evaluate_firstSecond_pow, rawDifference_annihilated hAB, map_zero]

end HMT.IV.LatticeTripleLocality
end

#print axioms HMT.IV.LatticeTripleLocality.locality_annihilates_pair
#print axioms HMT.IV.LatticeTripleLocality.firstThird_secondThird_commute
#print axioms HMT.IV.LatticeTripleLocality.rawLeft_decomposition
#print axioms HMT.IV.LatticeTripleLocality.rawRight_decomposition
#print axioms HMT.IV.LatticeTripleLocality.rawLeft_annihilated
#print axioms HMT.IV.LatticeTripleLocality.rawRight_annihilated
#print axioms HMT.IV.LatticeTripleLocality.evaluate_firstThird_pow
#print axioms HMT.IV.LatticeTripleLocality.evaluate_firstSecond_pow
#print axioms HMT.IV.LatticeTripleLocality.evaluate_secondThird_pow
#print axioms HMT.IV.LatticeTripleLocality.rawLeft_annihilated_on_vector
#print axioms HMT.IV.LatticeTripleLocality.rawRight_annihilated_on_vector
#print axioms HMT.IV.LatticeTripleLocality.firstSecond_secondThird_commute
#print axioms HMT.IV.LatticeTripleLocality.raw_difference_decomposition
#print axioms HMT.IV.LatticeTripleLocality.rawDifference_annihilated
#print axioms HMT.IV.LatticeTripleLocality.rawDifference_annihilated_after_secondThird
#print axioms HMT.IV.LatticeTripleLocality.rawDifference_annihilated_on_vector
