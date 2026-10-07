import LatticeDongKernel
import LatticeFactorConvolution
import Mathlib.RingTheory.Nilpotent.Basic

/-!
The finite binomial core of Dong's argument, on a single vector rather
than on globally nilpotent operators. Applied to coefficient arrays, the
two commuting endomorphisms are multiplication by `t-w` and `t-z`.
This is not yet the residue/locality theorem: its two annihilation
hypotheses must be supplied by the three actual field localities and
the two kernel-clearing identities.
-/

noncomputable section
namespace HMT.IV.LatticeDongBinomial

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem pow_apply_zero_of_le (X : Module.End ℂ V) (v : V)
    {p k : ℕ} (h : p ≤ k) (hp : (X^p) v = 0) : (X^k) v = 0 := by
  rw [show k = (k-p)+p by omega, pow_add, Module.End.mul_apply, hp, map_zero]

/-- The sharp binomial bound holds on a fixed vector, without assuming
that either operator is nilpotent on the entire space. -/
theorem commuting_add_pow_apply_zero (X Y : Module.End ℂ V) (v : V)
    (hXY : Commute X Y) {p q N : ℕ}
    (hX : (X^p) v = 0) (hY : (Y^q) v = 0) (hN : p+q ≤ N+1) :
    ((X+Y)^N) v = 0 := by
  rw [hXY.add_pow']
  simp only [LinearMap.sum_apply, LinearMap.smul_apply]
  apply Finset.sum_eq_zero
  rintro ⟨i,j⟩ hij
  have hterm : (X^i * Y^j) v = 0 := by
    by_cases hi : p ≤ i
    · rw [(hXY.pow_pow i j).eq, Module.End.mul_apply,
        pow_apply_zero_of_le X v hi hX, map_zero]
    · rw [Module.End.mul_apply,
        pow_apply_zero_of_le Y v (by have := Finset.mem_antidiagonal.mp hij; omega) hY,
        map_zero]
  simp only [hterm, smul_zero]

theorem neg_pow_apply_zero (Y : Module.End ℂ V) (v : V) {q : ℕ}
    (hY : (Y^q) v = 0) : ((-Y)^q) v = 0 := by
  rw [neg_pow]
  simp only [Module.End.mul_apply]
  rw [hY, map_zero]

theorem commuting_sub_pow_apply_zero (X Y : Module.End ℂ V) (v : V)
    (hXY : Commute X Y) {p q N : ℕ}
    (hX : (X^p) v = 0) (hY : (Y^q) v = 0) (hN : p+q ≤ N+1) :
    ((X-Y)^N) v = 0 := by
  simpa only [sub_eq_add_neg] using
    commuting_add_pow_apply_zero X (-Y) v hXY.neg_right hX
      (neg_pow_apply_zero Y v hY) hN

/-- Exact Dong exponent for a divided derivative of order `n`:
the second annihilator retains the `s` locality factor after clearing
the pole of order `n+1`. -/
theorem dong_binomial_bound (X Y : Module.End ℂ V) (v : V)
    (hXY : Commute X Y) (p s n : ℕ)
    (hX : (X^p) v = 0) (hY : (Y^(s+n+1)) v = 0) :
    ((X-Y)^(p+s+n)) v = 0 :=
  commuting_sub_pow_apply_zero X Y v hXY hX hY (by omega)

abbrev TriCoefficients (V : Type*) := ℤ → ℤ → ℤ → V

/-- Multiplication by `t-w`, with Laurent exponent indices. -/
def firstThird : Module.End ℂ (TriCoefficients V) where
  toFun F a b c := F (a-1) b c - F a b (c-1)
  map_add' F G := by funext a b c; simp; abel
  map_smul' q F := by funext a b c; simp [smul_sub]

/-- Multiplication by `t-z`. -/
def firstSecond : Module.End ℂ (TriCoefficients V) where
  toFun F a b c := F (a-1) b c - F a (b-1) c
  map_add' F G := by funext a b c; simp; abel
  map_smul' q F := by funext a b c; simp [smul_sub]

/-- Multiplication by `z-w`. -/
def secondThird : Module.End ℂ (TriCoefficients V) where
  toFun F a b c := F a (b-1) c - F a b (c-1)
  map_add' F G := by funext a b c; simp; abel
  map_smul' q F := by funext a b c; simp [smul_sub]

theorem triple_crossings_commute :
    Commute (firstThird : Module.End ℂ (TriCoefficients V)) firstSecond := by
  apply LinearMap.ext
  intro F
  funext a b c
  simp only [Module.End.mul_apply, firstThird, firstSecond, LinearMap.coe_mk,
    AddHom.coe_mk]
  abel

theorem triple_crossings_sub :
    (firstThird : Module.End ℂ (TriCoefficients V)) - firstSecond = secondThird := by
  apply LinearMap.ext
  intro F
  funext a b c
  simp only [LinearMap.sub_apply, firstThird, firstSecond, secondThird,
    LinearMap.coe_mk, AddHom.coe_mk, Pi.sub_apply]
  abel

/-- Formal residue is coefficient extraction at exponent `-1`. -/
def residue : TriCoefficients V →ₗ[ℂ] LatticeFactorConvolution.BiStates V where
  toFun F := F (-1)
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem residue_secondThird (F : TriCoefficients V) :
    residue (secondThird F) = LatticeFactorConvolution.crossing (residue F) := rfl

theorem residue_secondThird_pow (F : TriCoefficients V) (N : ℕ) :
    residue ((secondThird^N) F) =
      (LatticeFactorConvolution.crossing^N) (residue F) := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [pow_succ', Module.End.mul_apply, residue_secondThird,
      pow_succ', Module.End.mul_apply, ih]

/-- Coefficient-level Dong binomial and residue step. The two hypotheses
are genuine annihilation identities on the same triple coefficient array;
neither is a locality conclusion hidden as a typeclass or an axiom. -/
theorem dong_residue_core (F : TriCoefficients V) (p s n : ℕ)
    (hX : (firstThird^p) F = 0) (hY : (firstSecond^(s+n+1)) F = 0) :
    (LatticeFactorConvolution.crossing^(p+s+n)) (residue F) = 0 := by
  have h := dong_binomial_bound firstThird firstSecond F
    triple_crossings_commute p s n hX hY
  rw [triple_crossings_sub] at h
  rw [← residue_secondThird_pow, h, map_zero]

/-- The prior factor `(z-w)^q` supplies the B--C locality factor.
After the two independently proved triple annihilations, the resulting
residue has the exact sufficient order `p+q+s+n`. -/
theorem dong_residue_bound (F : TriCoefficients V) (p q s n : ℕ)
    (hX : (firstThird^p) ((secondThird^q) F) = 0)
    (hY : (firstSecond^(s+n+1)) ((secondThird^q) F) = 0) :
    (LatticeFactorConvolution.crossing^(p+q+s+n)) (residue F) = 0 := by
  have h := dong_residue_core ((secondThird^q) F) p s n hX hY
  rw [residue_secondThird_pow, ← Module.End.mul_apply, ← pow_add] at h
  simpa only [show p+s+n+q = p+q+s+n by omega] using h

end HMT.IV.LatticeDongBinomial
end

#print axioms HMT.IV.LatticeDongBinomial.pow_apply_zero_of_le
#print axioms HMT.IV.LatticeDongBinomial.commuting_add_pow_apply_zero
#print axioms HMT.IV.LatticeDongBinomial.neg_pow_apply_zero
#print axioms HMT.IV.LatticeDongBinomial.commuting_sub_pow_apply_zero
#print axioms HMT.IV.LatticeDongBinomial.dong_binomial_bound
#print axioms HMT.IV.LatticeDongBinomial.triple_crossings_commute
#print axioms HMT.IV.LatticeDongBinomial.triple_crossings_sub
#print axioms HMT.IV.LatticeDongBinomial.residue_secondThird_pow
#print axioms HMT.IV.LatticeDongBinomial.dong_residue_core
#print axioms HMT.IV.LatticeDongBinomial.dong_residue_bound
