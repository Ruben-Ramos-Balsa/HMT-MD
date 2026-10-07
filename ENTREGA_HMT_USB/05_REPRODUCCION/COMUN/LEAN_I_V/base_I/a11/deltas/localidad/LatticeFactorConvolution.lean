import LatticeTwoRegionFactor
import Mathlib.Algebra.BigOperators.Finprod
import Mathlib.Data.Int.Interval

/-!
Algebraic convolution of a diagonal contraction factor with a two-variable
series bounded below in each variable. Finiteness is proved before using
finsum; no analytic convergence or summability assumption is introduced.
-/
noncomputable section
namespace HMT.IV.LatticeFactorConvolution

variable {V : Type*} [AddCommGroup V] [Module ℂ V]
abbrev BiStates (V : Type*) := ℤ → ℤ → V

def LowerBounded (h : BiStates V) : Prop :=
  ∃ l u : ℤ, ∀ a b, a < l ∨ b < u → h a b = 0

def convolution (p : ℤ) (k : ℤ → ℂ) (h : BiStates V) : BiStates V :=
  fun a b => ∑ᶠ j : ℤ, k j • h (a-p+j) (b-j)

def crossing : Module.End ℂ (BiStates V) where
  toFun f := fun a b => f (a-1) b - f a (b-1)
  map_add' f g := by funext a b; simp; abel
  map_smul' c f := by funext a b; simp [smul_sub]

def raiseKernel (k : ℤ → ℂ) : ℤ → ℂ := fun j => k j - k (j-1)

theorem convolution_support_finite (p : ℤ) (k : ℤ → ℂ) (h : BiStates V)
    (hh : LowerBounded h) (a b : ℤ) :
    (Function.support (fun j : ℤ => k j • h (a-p+j) (b-j))).Finite := by
  obtain ⟨l,u,hu⟩ := hh
  apply (Set.finite_Icc (l-a+p) (b-u)).subset
  intro j hj
  change k j • h (a-p+j) (b-j) ≠ 0 at hj
  simp only [Set.mem_Icc]
  by_contra hn
  have hz : h (a-p+j) (b-j)=0 := hu _ _ (by omega)
  exact hj (by rw [hz,smul_zero])

theorem convolution_reindex_one (p : ℤ) (k : ℤ → ℂ) (h : BiStates V) (a b : ℤ) :
    (∑ᶠ j : ℤ, k j • h (a-p+j) (b-1-j)) =
      ∑ᶠ j : ℤ, k (j-1) • h (a-(p+1)+j) (b-j) := by
  let e : ℤ ≃ ℤ := Equiv.addRight 1
  have he := finsum_comp_equiv e
    (f := fun j : ℤ => k (j-1) • h (a-(p+1)+j) (b-j))
  simpa only [e, Equiv.coe_addRight, add_sub_cancel_right,
    show ∀ j : ℤ, a-(p+1)+(j+1)=a-p+j by omega,
    show ∀ j : ℤ, b-(j+1)=b-1-j by omega] using he

theorem crossing_convolution (p : ℤ) (k : ℤ → ℂ) (h : BiStates V)
    (hh : LowerBounded h) :
    crossing (convolution p k h) = convolution (p+1) (raiseKernel k) h := by
  funext a b
  change ((∑ᶠ j : ℤ, k j • h (a-1-p+j) (b-j)) -
    ∑ᶠ j : ℤ, k j • h (a-p+j) (b-1-j)) =
      ∑ᶠ j : ℤ, (k j-k (j-1)) • h (a-(p+1)+j) (b-j)
  rw [convolution_reindex_one]
  have harg : ∀ j : ℤ, a-1-p+j=a-(p+1)+j := by omega
  simp only [harg, sub_smul]
  exact (finsum_sub_distrib (convolution_support_finite (p+1) k h hh a b)
    (convolution_support_finite (p+1) (fun j => k (j-1)) h hh a b)).symm

def leftKernel (p : ℤ) : ℤ → ℂ := fun j =>
  LatticeTwoRegionFactor.leftExpansion p (p-j) j

def rightKernel (p : ℤ) : ℤ → ℂ := fun j =>
  LatticeTwoRegionFactor.rightExpansion p (p-j) j

theorem raise_leftKernel (p : ℤ) : raiseKernel (leftKernel p) = leftKernel (p+1) := by
  funext j
  have he := congrFun (congrFun (LatticeTwoRegionFactor.crossing_left p) (p+1-j)) j
  change LatticeTwoRegionFactor.leftExpansion p (p+1-j-1) j -
    LatticeTwoRegionFactor.leftExpansion p (p+1-j) (j-1) =
      LatticeTwoRegionFactor.leftExpansion (p+1) (p+1-j) j at he
  change LatticeTwoRegionFactor.leftExpansion p (p-j) j -
    LatticeTwoRegionFactor.leftExpansion p (p-(j-1)) (j-1) =
      LatticeTwoRegionFactor.leftExpansion (p+1) (p+1-j) j
  rw [show p+1-j-1=p-j by omega] at he
  rw [← show p+1-j=p-(j-1) by omega]
  exact he

theorem raise_rightKernel (p : ℤ) : raiseKernel (rightKernel p) = rightKernel (p+1) := by
  funext j
  have he := congrFun (congrFun (LatticeTwoRegionFactor.crossing_right p) (p+1-j)) j
  change LatticeTwoRegionFactor.rightExpansion p (p+1-j-1) j -
    LatticeTwoRegionFactor.rightExpansion p (p+1-j) (j-1) =
      LatticeTwoRegionFactor.rightExpansion (p+1) (p+1-j) j at he
  change LatticeTwoRegionFactor.rightExpansion p (p-j) j -
    LatticeTwoRegionFactor.rightExpansion p (p-(j-1)) (j-1) =
      LatticeTwoRegionFactor.rightExpansion (p+1) (p+1-j) j
  rw [show p+1-j-1=p-j by omega] at he
  rw [← show p+1-j=p-(j-1) by omega]
  exact he

def leftProduct (p : ℤ) (h : BiStates V) : BiStates V := convolution p (leftKernel p) h
def rightProduct (p : ℤ) (h : BiStates V) : BiStates V := convolution p (rightKernel p) h

theorem crossing_leftProduct (p : ℤ) (h : BiStates V) (hh : LowerBounded h) :
    crossing (leftProduct p h) = leftProduct (p+1) h := by
  rw [leftProduct,crossing_convolution p _ _ hh,raise_leftKernel]
  rfl

theorem crossing_rightProduct (p : ℤ) (h : BiStates V) (hh : LowerBounded h) :
    crossing (rightProduct p h) = rightProduct (p+1) h := by
  rw [rightProduct,crossing_convolution p _ _ hh,raise_rightKernel]
  rfl

theorem crossing_leftProduct_iterate (p : ℤ) (n : ℕ) (h : BiStates V) (hh : LowerBounded h) :
    (crossing^n) (leftProduct p h) = leftProduct (p+n) h := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ',Module.End.mul_apply,ih,crossing_leftProduct _ _ hh]
    push_cast
    ring

theorem crossing_rightProduct_iterate (p : ℤ) (n : ℕ) (h : BiStates V) (hh : LowerBounded h) :
    (crossing^n) (rightProduct p h) = rightProduct (p+n) h := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ',Module.End.mul_apply,ih,crossing_rightProduct _ _ hh]
    push_cast
    ring

theorem zero_products_equal (h : BiStates V) : leftProduct 0 h = rightProduct 0 h := by
  have hk : leftKernel 0 = rightKernel 0 := by
    funext j
    exact congrFun (congrFun LatticeTwoRegionFactor.zero_expansions_equal (0-j)) j
  rw [leftProduct,rightProduct,hk]

theorem nonnegative_products_equal (n : ℕ) (h : BiStates V) (hh : LowerBounded h) :
    leftProduct (n:ℤ) h = rightProduct (n:ℤ) h := by
  have he := congrArg (fun f : BiStates V => (crossing^n) f) (zero_products_equal h)
  simpa only [crossing_leftProduct_iterate _ _ _ hh,
    crossing_rightProduct_iterate _ _ _ hh,zero_add] using he

/-- Cancellation is transported to every lower-bounded common normal product.
The bound depends only on the integral pairing, not on that product. -/
theorem product_polynomial_cancellation (p : ℤ) :
    ∃ n : ℕ, ∀ (h : BiStates V), LowerBounded h →
      (crossing^n) (leftProduct p h) = (crossing^n) (rightProduct p h) := by
  by_cases hp : 0 ≤ p
  · refine ⟨0,fun h hh => ?_⟩
    have he := nonnegative_products_equal p.toNat h hh
    simpa only [Int.toNat_of_nonneg hp,pow_zero,Module.End.one_apply] using he
  · refine ⟨(-p).toNat,fun h hh => ?_⟩
    rw [crossing_leftProduct_iterate _ _ _ hh,crossing_rightProduct_iterate _ _ _ hh]
    have hz : p+((-p).toNat : ℤ)=0 := by omega
    rw [hz]
    exact zero_products_equal h

end HMT.IV.LatticeFactorConvolution
end

#print axioms HMT.IV.LatticeFactorConvolution.convolution_support_finite
#print axioms HMT.IV.LatticeFactorConvolution.convolution_reindex_one
#print axioms HMT.IV.LatticeFactorConvolution.crossing_convolution
#print axioms HMT.IV.LatticeFactorConvolution.raise_leftKernel
#print axioms HMT.IV.LatticeFactorConvolution.raise_rightKernel
#print axioms HMT.IV.LatticeFactorConvolution.crossing_leftProduct_iterate
#print axioms HMT.IV.LatticeFactorConvolution.crossing_rightProduct_iterate
#print axioms HMT.IV.LatticeFactorConvolution.product_polynomial_cancellation
