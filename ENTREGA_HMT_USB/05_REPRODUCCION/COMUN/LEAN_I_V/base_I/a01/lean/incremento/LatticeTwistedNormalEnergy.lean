import LatticeTwistedNormalDerivative
import LatticeTwistedKernelEnergy

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedNormalEnergy
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedNormalDerivative LatticeTwistedOscillatorTensor
open LatticeFiniteIrreducible LatticeHalfConformalCentralizer
open scoped BigOperators

theorem conformal_halfMode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    conformalMode o 0 * halfMode o i m - halfMode o i m * conformalMode o 0 =
      (-(m:ℂ)-1/2) • halfMode o i m := by
  have h := congrArg (fun f : Module.End ℂ (LatticeHalfIntegerHeisenberg.HalfFock o) =>
    f.rTensor (FiniteSpace o)) (shifted_comm_half o i 0 m)
  simpa only [LatticeConformalCentralizer.comm, zero_add, LinearMap.rTensor_sub,
    LinearMap.rTensor_mul, LinearMap.rTensor_smul, conformalMode, halfMode,
    conformalModeTensor, halfModeTensor] using h

theorem conformal_halfMode_apply (o : Fin 12) (i : Fin (BasisSize o))
    (m : ℤ) (v : Carrier o) :
    conformalMode o 0 (halfMode o i m v) =
      halfMode o i m (conformalMode o 0 v) + (-(m:ℂ)-1/2) • halfMode o i m v := by
  have h := LinearMap.congr_fun (conformal_halfMode o i m) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at h
  exact (sub_eq_iff_eq_add.mp h).trans (add_comm _ _)

theorem creationTerm_energy (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (h : ℂ)
    (hB : ∀ k v, conformalMode o 0 (HVertexOperator.coeff B k v) =
      HVertexOperator.coeff B k (conformalMode o 0 v) +
        (h+(k:ℂ)/2) • HVertexOperator.coeff B k v)
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    conformalMode o 0 (creationTerm o i n B k a v) =
      creationTerm o i n B k a (conformalMode o 0 v) +
        (h+(n:ℂ)+1+(k:ℂ)/2) • creationTerm o i n B k a v := by
  simp only [creationTerm, LatticeTwistedNormalProduct.creationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, map_smul, conformal_halfMode_apply, hB,
    map_add, map_smul]
  push_cast
  module

theorem annihilationTerm_energy (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (h : ℂ)
    (hB : ∀ k v, conformalMode o 0 (HVertexOperator.coeff B k v) =
      HVertexOperator.coeff B k (conformalMode o 0 v) +
        (h+(k:ℂ)/2) • HVertexOperator.coeff B k v)
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    conformalMode o 0 (annihilationTerm o i n B k a v) =
      annihilationTerm o i n B k a (conformalMode o 0 v) +
        (h+(n:ℂ)+1+(k:ℂ)/2) • annihilationTerm o i n B k a v := by
  simp only [annihilationTerm, LatticeTwistedNormalProduct.annihilationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, map_smul, hB, conformal_halfMode_apply,
    map_add, map_smul]
  push_cast
  module

theorem derivativeNormalField_energy (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (h : ℂ)
    (hB : ∀ k v, conformalMode o 0 (HVertexOperator.coeff B k v) =
      HVertexOperator.coeff B k (conformalMode o 0 v) +
        (h+(k:ℂ)/2) • HVertexOperator.coeff B k v)
    (k : ℤ) (v : Carrier o) :
    conformalMode o 0 (HVertexOperator.coeff (derivativeNormalField o i n B) k v) =
      HVertexOperator.coeff (derivativeNormalField o i n B) k (conformalMode o 0 v) +
        (h+(n:ℂ)+1+(k:ℂ)/2) •
          HVertexOperator.coeff (derivativeNormalField o i n B) k v := by
  simp only [derivativeNormalField_coefficient, normalCoefficient_apply, map_add]
  have hc : conformalMode o 0 (∑ᶠ a, creationTerm o i n B k a v) =
      ∑ᶠ a, conformalMode o 0 (creationTerm o i n B k a v) :=
    (conformalMode o 0).toAddMonoidHom.map_finsum (creationTerm_finite o i n B k v)
  have ha : conformalMode o 0 (∑ᶠ a, annihilationTerm o i n B k a v) =
      ∑ᶠ a, conformalMode o 0 (annihilationTerm o i n B k a v) :=
    (conformalMode o 0).toAddMonoidHom.map_finsum (annihilationTerm_finite o i n B k v)
  rw [hc, ha]
  simp_rw [creationTerm_energy o i n B h hB, annihilationTerm_energy o i n B h hB]
  have hc' : (Function.support (fun a =>
      (h+(n:ℂ)+1+(k:ℂ)/2) • creationTerm o i n B k a v)).Finite := by
    apply (creationTerm_finite o i n B k v).subset
    intro a ha hz
    exact ha (by simp [hz])
  have ha' : (Function.support (fun a =>
      (h+(n:ℂ)+1+(k:ℂ)/2) • annihilationTerm o i n B k a v)).Finite := by
    apply (annihilationTerm_finite o i n B k v).subset
    intro a ha hz
    exact ha (by simp [hz])
  rw [finsum_add_distrib (creationTerm_finite o i n B k (conformalMode o 0 v))
      hc',
    finsum_add_distrib (annihilationTerm_finite o i n B k (conformalMode o 0 v))
      ha',
    ← smul_finsum' _ (creationTerm_finite o i n B k v),
    ← smul_finsum' _ (annihilationTerm_finite o i n B k v)]
  module

end HMT.IV.LatticeTwistedNormalEnergy
end
