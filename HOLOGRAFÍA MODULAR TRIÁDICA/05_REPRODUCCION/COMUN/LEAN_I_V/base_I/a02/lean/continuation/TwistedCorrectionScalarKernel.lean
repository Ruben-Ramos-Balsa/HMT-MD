import LatticeTwistedCorrection
import Mathlib.RingTheory.PowerSeries.Derivative

/-! The bivariate scalar kernel of the descendant correction. Its coefficients
are exactly those used by the correction operator. The Euler identity is proved
in the full formal series ring, not on a numerical truncation. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.TwistedCorrectionScalarKernel
open PowerSeries LatticeTwistedCorrection

abbrev Uni := PowerSeries ℂ
abbrev Bi := PowerSeries Uni

def bicoeff (m n : ℕ) (f : Bi) : ℂ := coeff ℂ n (coeff Uni m f)

def xEmbed : Uni →+* Bi := PowerSeries.map (C ℂ)
def yEmbed : Uni →+* Bi := C Uni

def euler (f : Bi) : Bi := PowerSeries.mk fun m =>
  PowerSeries.mk fun n => (m+n : ℂ) * bicoeff m n f

theorem euler_coefficient (m n : ℕ) (f : Bi) :
    bicoeff m n (euler f) = (m+n : ℂ) * bicoeff m n f := by
  simp only [bicoeff, euler, coeff_mk]

def kernel : Bi := PowerSeries.mk fun m => PowerSeries.mk (correctionScalar m)

theorem kernel_coefficient (m n : ℕ) : bicoeff m n kernel = correctionScalar m n := by
  simp only [bicoeff, kernel, coeff_mk]

theorem kernel_constant : bicoeff 0 0 kernel = 0 := by
  rw [kernel_coefficient, correctionScalar_zero_zero]

def inverseRoot : Uni := binomialSeries ℂ (-1/2 : ℚ)
def root : Uni := binomialSeries ℂ (1/2 : ℚ)

theorem inverseRoot_coefficient (n : ℕ) :
    coeff ℂ n inverseRoot = ((Ring.choose (-1/2 : ℚ) n : ℚ) : ℂ) := by
  simp [inverseRoot, Algebra.smul_def]

theorem root_coefficient (n : ℕ) :
    coeff ℂ n root = ((Ring.choose (1/2 : ℚ) n : ℚ) : ℂ) := by
  simp [root, Algebra.smul_def]

theorem separated_coefficient (m n : ℕ) (f g : Uni) :
    bicoeff m n (xEmbed f * yEmbed g) = coeff ℂ m f * coeff ℂ n g := by
  change coeff ℂ n (coeff Uni m ((PowerSeries.map (C ℂ) f) * C Uni g)) = _
  rw [coeff_mul_C, coeff_map, coeff_C_mul]

theorem euler_kernel :
    (2:ℂ) • euler kernel = xEmbed inverseRoot * yEmbed inverseRoot - 1 := by
  ext m n
  change coeff ℂ n (coeff Uni m ((2:ℂ) • euler kernel)) = _
  simp only [map_smul, smul_eq_mul, map_sub]
  change (2:ℂ) * bicoeff m n (euler kernel) =
    bicoeff m n (xEmbed inverseRoot * yEmbed inverseRoot) - bicoeff m n 1
  rw [euler_coefficient, kernel_coefficient, separated_coefficient,
    inverseRoot_coefficient, inverseRoot_coefficient]
  by_cases hz : m+n=0
  · have hm : m=0 := by omega
    have hn : n=0 := by omega
    subst m
    subst n
    norm_num [bicoeff, correctionScalar]
  · have hmn : (m+n : ℂ) ≠ 0 := by exact_mod_cast hz
    have hc : bicoeff m n (1:Bi)=0 := by
      by_cases hm : m=0
      · subst m
        simp [bicoeff, show n≠0 by omega]
      · simp [bicoeff, hm]
    rw [hc, sub_zero]
    simp only [correctionScalar, Rat.cast_div, Rat.cast_mul, Rat.cast_ofNat,
      Rat.cast_add, Rat.cast_natCast]
    field_simp
    ring

theorem euler_ext (f g : Bi) (hc : bicoeff 0 0 f = bicoeff 0 0 g)
    (he : euler f = euler g) : f=g := by
  ext m n
  change bicoeff m n f = bicoeff m n g
  by_cases hz : m+n=0
  · have hm : m=0 := by omega
    have hn : n=0 := by omega
    simpa [hm,hn] using hc
  · have hmn : (m+n:ℂ) ≠ 0 := by exact_mod_cast hz
    have h := congrArg (bicoeff m n) he
    rw [euler_coefficient, euler_coefficient] at h
    exact mul_left_cancel₀ hmn h

theorem kernel_euler_unique (f : Bi) (hc : bicoeff 0 0 f = 0)
    (he : (2:ℂ) • euler f = xEmbed inverseRoot * yEmbed inverseRoot - 1) :
    f=kernel := by
  apply euler_ext f kernel (hc.trans kernel_constant.symm)
  have h : (2:ℂ) • euler f = (2:ℂ) • euler kernel := he.trans euler_kernel.symm
  exact (smul_right_injective _ (by norm_num : (2:ℂ) ≠ 0)) h

theorem binomial_zero : binomialSeries ℂ (0:ℚ) = 1 := by
  ext n
  simp [binomialSeries_coeff, Ring.choose_zero_ite]

theorem binomial_one : binomialSeries ℂ (1:ℚ) = 1+X := by
  ext n
  cases n with
  | zero => simp
  | succ n =>
    cases n with
    | zero => simp
    | succ n =>
      have h : Ring.choose (1:ℚ) (n+1+1)=0 := by
        rw [show (1:ℚ) = (1:ℕ) by norm_num, Ring.choose_natCast,
          Nat.choose_eq_zero_of_lt (by omega), Nat.cast_zero]
      simp [h, coeff_X, show n+1+1≠1 by omega]

theorem root_inverse : root * inverseRoot = 1 := by
  rw [root, inverseRoot, ← binomialSeries_add, show (1/2:ℚ)+(-1/2)=0 by norm_num,
    binomial_zero]

theorem root_square : root * root = 1+X := by
  rw [root, ← binomialSeries_add, show (1/2:ℚ)+(1/2)=1 by norm_num, binomial_one]

theorem twice_root_derivative : (2:ℂ) • derivative ℂ root = inverseRoot := by
  have h := congrArg (derivative ℂ) root_square
  simp only [Derivation.leibniz, map_add, Derivation.map_one_eq_zero,
    derivative_X, zero_add, smul_eq_mul] at h
  have h2 : (2:ℂ) • (root * derivative ℂ root) = 1 := by
    rw [show (2:ℂ)=1+1 by norm_num, add_smul, one_smul]
    exact h
  have h3 := congrArg (fun f : Uni => inverseRoot*f) h2
  dsimp only at h3
  rw [mul_smul_comm, ← mul_assoc,
    show inverseRoot*root=1 by rw [mul_comm,root_inverse], one_mul, mul_one] at h3
  exact h3

def uniEuler (f : Uni) : Uni := X * derivative ℂ f

theorem uniEuler_coefficient (f : Uni) (n : ℕ) :
    coeff ℂ n (uniEuler f) = (n:ℂ) * coeff ℂ n f := by
  cases n with
  | zero => simp [uniEuler]
  | succ n =>
    rw [uniEuler, ← pow_one (X:Uni), coeff_X_pow_mul, coeff_derivative]
    push_cast
    ring

theorem twice_uniEuler_root : (2:ℂ) • uniEuler root = root-inverseRoot := by
  rw [uniEuler, ← mul_smul_comm, twice_root_derivative,
    show (X:Uni)=root*root-1 by rw [root_square]; ring,
    sub_mul, mul_assoc, root_inverse, mul_one, one_mul]

theorem euler_add (f g : Bi) : euler (f+g)=euler f+euler g := by
  ext m n
  simp [euler, bicoeff, mul_add]

theorem euler_smul (c : ℂ) (f : Bi) : euler (c•f)=c•euler f := by
  ext m n
  simp only [euler, coeff_mk, bicoeff, coeff_smul, smul_eq_mul]
  ring

theorem euler_xEmbed (f : Uni) : euler (xEmbed f)=xEmbed (uniEuler f) := by
  ext m n
  simp only [euler, coeff_mk, bicoeff, xEmbed, coeff_map, coeff_C,
    uniEuler_coefficient]
  split_ifs with hn
  · subst n
    simp
  · simp

theorem euler_yEmbed (f : Uni) : euler (yEmbed f)=yEmbed (uniEuler f) := by
  ext m n
  simp only [euler, coeff_mk, bicoeff, yEmbed, coeff_C]
  split_ifs with hm
  · subst m
    simp [uniEuler_coefficient]
  · simp

theorem xEmbed_smul (c : ℂ) (f : Uni) : xEmbed (c•f)=c•xEmbed f := by
  ext m n
  simp only [xEmbed, coeff_map, coeff_smul, smul_eq_mul, map_mul, coeff_C,
    coeff_C_mul]

theorem yEmbed_smul (c : ℂ) (f : Uni) : yEmbed (c•f)=c•yEmbed f := by
  ext m n
  simp only [yEmbed, coeff_C, coeff_smul]
  split_ifs <;> simp

def rootAverage : Bi := (2:ℂ)⁻¹ • (xEmbed root+yEmbed root)

theorem rootAverage_constant : bicoeff 0 0 rootAverage = 1 := by
  simp only [rootAverage, bicoeff, coeff_smul, map_add, xEmbed, yEmbed,
    coeff_map, coeff_C, if_pos rfl, root, binomialSeries_coeff, Ring.choose_zero_right,
    one_smul, map_one]
  norm_num

theorem rootAverage_ne_zero : rootAverage ≠ 0 := by
  intro h
  have hh := congrArg (bicoeff 0 0) h
  rw [rootAverage_constant] at hh
  simp [bicoeff] at hh

theorem four_euler_rootAverage :
    (4:ℂ) • euler rootAverage =
      xEmbed root+yEmbed root-xEmbed inverseRoot-yEmbed inverseRoot := by
  have hx := congrArg xEmbed twice_uniEuler_root
  have hy := congrArg yEmbed twice_uniEuler_root
  rw [xEmbed_smul, map_sub] at hx
  rw [yEmbed_smul, map_sub] at hy
  rw [rootAverage, euler_smul, euler_add, euler_xEmbed, euler_yEmbed]
  calc
    (4:ℂ) • (2:ℂ)⁻¹ • (xEmbed (uniEuler root)+yEmbed (uniEuler root)) =
        (2:ℂ) • xEmbed (uniEuler root)+(2:ℂ) • yEmbed (uniEuler root) := by module
    _ = _ := by rw [hx,hy]; abel

/-- The complete formal logarithmic differential identity for the actual
average of the two normalized square roots. -/
theorem kernel_logarithmic_identity :
    rootAverage * euler kernel = -euler rootAverage := by
  have hx : xEmbed root*xEmbed inverseRoot=1 := by
    rw [← map_mul, root_inverse, map_one]
  have hy : yEmbed root*yEmbed inverseRoot=1 := by
    rw [← map_mul, root_inverse, map_one]
  have hp : (xEmbed root+yEmbed root)*(xEmbed inverseRoot*yEmbed inverseRoot-1) =
      -(xEmbed root+yEmbed root-xEmbed inverseRoot-yEmbed inverseRoot) := by
    calc
      _ = (xEmbed root*xEmbed inverseRoot)*yEmbed inverseRoot +
          (yEmbed root*yEmbed inverseRoot)*xEmbed inverseRoot-xEmbed root-yEmbed root := by ring
      _ = _ := by rw [hx,hy]; ring
  apply (smul_right_injective _ (by norm_num : (4:ℂ) ≠ 0))
  calc
    (4:ℂ) • (rootAverage*euler kernel) =
        (xEmbed root+yEmbed root)*((2:ℂ) • euler kernel) := by
      simp only [rootAverage, smul_mul_assoc, mul_smul_comm, smul_smul]
      congr 1
      norm_num
    _ = -(xEmbed root+yEmbed root-xEmbed inverseRoot-yEmbed inverseRoot) := by
      rw [euler_kernel, hp]
    _ = (4:ℂ) • (-euler rootAverage) := by rw [smul_neg, four_euler_rootAverage]

/-- Zero constant term and the logarithmic Euler equation uniquely determine
the kernel in all bidegrees. No finite coefficient table is used. -/
theorem kernel_logarithmic_unique (f : Bi) (hc : bicoeff 0 0 f=0)
    (hd : rootAverage*euler f = -euler rootAverage) : f=kernel := by
  apply euler_ext f kernel (hc.trans kernel_constant.symm)
  exact mul_left_cancel₀ rootAverage_ne_zero (hd.trans kernel_logarithmic_identity.symm)

end HMT.IV.TwistedCorrectionScalarKernel
end
