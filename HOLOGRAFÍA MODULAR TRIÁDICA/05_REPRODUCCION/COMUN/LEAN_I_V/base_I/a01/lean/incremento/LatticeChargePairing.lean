import LatticeWeightShells
import LatticeFockMonomialParity
import WittNegationLift
import Mathlib.LinearAlgebra.BilinearForm.Basic

/-!
The charge part of the contragredient pairing on the existing twisted group
algebra. The normalization is the primary-field sign (-1)^halfnorm times the
actual inverse-charge cocycle, not an arbitrary diagonal normalization of that
cocycle. This file constructs and proves the bilinear algebraic properties;
full vertex-operator invariance is a separate statement.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeChargePairing

open LatticeCocycle LatticeWeightShells TwistedGroupAlgebra
open LatticeFockMonomialParity WittNegationLift

def chargeWeight (o : Fin 12) (x : Lattice o) : ℂ :=
  (-1 : ℂ) ^ halfnormNat o x * (wittSign o x (-x) : ℂ)

@[simp] theorem chargeWeight_neg (o : Fin 12) (x : Lattice o) :
    chargeWeight o (-x) = chargeWeight o x := by
  simp only [chargeWeight, halfnormNat_neg, neg_neg]
  congr 1
  unfold wittSign
  rw [← wittCocycle_neg_swap]

@[simp] theorem chargeWeight_zero (o : Fin 12) : chargeWeight o 0 = 1 := by
  simp [chargeWeight, wittSign_zero_left]

theorem chargeWeight_ne_zero (o : Fin 12) (x : Lattice o) :
    chargeWeight o x ≠ 0 := by
  apply mul_ne_zero (pow_ne_zero _ (by norm_num))
  have hs : wittSign o x (-x) ≠ 0 := by
    intro h
    have hh := wittSign_square o x (-x)
    simp [h] at hh
  exact_mod_cast hs

def chargePairing (o : Fin 12) : LinearMap.BilinForm ℂ (TwistedAlgebra o) :=
  (latticeBasisComplex o).constr ℂ
    (fun x => chargeWeight o x • (latticeBasisComplex o).coord (-x))

theorem chargePairing_basis_left (o : Fin 12) (x : Lattice o) (t : TwistedAlgebra o) :
    chargePairing o (basisElement o x) t =
      chargeWeight o x * (latticeBasisComplex o).repr t (-x) := by
  change chargePairing o (latticeBasisComplex o x) t = _
  simp only [chargePairing, Basis.constr_basis, LinearMap.smul_apply,
    Basis.coord_apply, smul_eq_mul]

theorem chargePairing_basis (o : Fin 12) (x y : Lattice o) :
    chargePairing o (basisElement o x) (basisElement o y) =
      if y = -x then chargeWeight o x else 0 := by
  classical
  rw [chargePairing_basis_left]
  change chargeWeight o x * (Finsupp.single y (1 : ℂ)) (-x) = _
  simp only [Finsupp.single_apply]
  split_ifs <;> simp_all

theorem chargePairing_basis_right (o : Fin 12) (t : TwistedAlgebra o) (y : Lattice o) :
    chargePairing o t (basisElement o y) =
      chargeWeight o y * (latticeBasisComplex o).repr t (-y) := by
  classical
  have he : (chargePairing o).flip (basisElement o y) =
      chargeWeight o y • (latticeBasisComplex o).coord (-y) := by
    apply (latticeBasisComplex o).ext
    intro x
    change chargePairing o (basisElement o x) (basisElement o y) = _
    rw [chargePairing_basis]
    change (if y = -x then chargeWeight o x else 0) =
      chargeWeight o y * (Finsupp.single x (1 : ℂ)) (-y)
    by_cases h : y = -x
    · subst y
      simp
    · have hxy : x ≠ -y := by intro he; subst x; simp at h
      simp [h, hxy, Finsupp.single_apply]
  exact LinearMap.congr_fun he t

theorem chargePairing_symmetric (o : Fin 12) (s t : TwistedAlgebra o) :
    chargePairing o s t = chargePairing o t s := by
  have he : chargePairing o = (chargePairing o).flip := by
    apply (latticeBasisComplex o).ext
    intro x
    apply LinearMap.ext
    intro t
    change chargePairing o (basisElement o x) t = chargePairing o t (basisElement o x)
    rw [chargePairing_basis_left, chargePairing_basis_right]
  exact LinearMap.congr_fun (LinearMap.congr_fun he s) t

@[simp] theorem chargePairing_vacuum (o : Fin 12) :
    chargePairing o (basisElement o 0) (basisElement o 0) = 1 := by
  simp [chargePairing_basis]

def chargeDual (o : Fin 12) (x : Lattice o) : TwistedAlgebra o :=
  (chargeWeight o x)⁻¹ • basisElement o (-x)

theorem chargeDual_right (o : Fin 12) (t : TwistedAlgebra o) (x : Lattice o) :
    chargePairing o t (chargeDual o x) = (latticeBasisComplex o).repr t x := by
  rw [chargeDual, map_smul, chargePairing_basis_right, chargeWeight_neg, neg_neg]
  simp [smul_eq_mul, ← mul_assoc, chargeWeight_ne_zero]

theorem chargeDual_left (o : Fin 12) (t : TwistedAlgebra o) (x : Lattice o) :
    chargePairing o (chargeDual o x) t = (latticeBasisComplex o).repr t x := by
  rw [chargePairing_symmetric, chargeDual_right]

theorem chargePairing_nondegenerate (o : Fin 12) : (chargePairing o).Nondegenerate := by
  intro t ht
  apply (latticeBasisComplex o).repr.injective
  apply Finsupp.ext
  intro x
  have h := ht (chargeDual o x)
  simpa only [chargeDual_right, map_zero, Finsupp.zero_apply] using h

theorem chargePairing_right_separating (o : Fin 12) (t : TwistedAlgebra o)
    (ht : ∀ s, chargePairing o s t = 0) : t = 0 := by
  apply (latticeBasisComplex o).repr.injective
  apply Finsupp.ext
  intro x
  have h := ht (chargeDual o x)
  simpa only [chargeDual_left, map_zero, Finsupp.zero_apply] using h

theorem chargePairing_theta (o : Fin 12) (s t : TwistedAlgebra o) :
    chargePairing o (thetaLinear o s) t = chargePairing o s (thetaLinear o t) := by
  have he : LinearMap.comp (chargePairing o) (thetaLinear o).toLinearMap =
      LinearMap.compl₂ (chargePairing o) (thetaLinear o).toLinearMap := by
    apply (latticeBasisComplex o).ext
    intro x
    apply (latticeBasisComplex o).ext
    intro y
    change chargePairing o (thetaLinear o (basisElement o x)) (basisElement o y) =
      chargePairing o (basisElement o x) (thetaLinear o (basisElement o y))
    rw [show thetaLinear o (basisElement o x) = basisElement o (-x) from theta_single o x 1,
      show thetaLinear o (basisElement o y) = basisElement o (-y) from theta_single o y 1]
    simp only [chargePairing_basis, chargeWeight_neg, neg_neg, neg_inj]
  exact LinearMap.congr_fun (LinearMap.congr_fun he s) t

theorem chargePairing_theta_isometry (o : Fin 12) (s t : TwistedAlgebra o) :
    chargePairing o (thetaLinear o s) (thetaLinear o t) = chargePairing o s t := by
  rw [chargePairing_theta, theta_square]

end HMT.IV.LatticeChargePairing
end

#print axioms HMT.IV.LatticeChargePairing.chargePairing_nondegenerate
#print axioms HMT.IV.LatticeChargePairing.chargePairing_right_separating
#print axioms HMT.IV.LatticeChargePairing.chargePairing_theta_isometry
