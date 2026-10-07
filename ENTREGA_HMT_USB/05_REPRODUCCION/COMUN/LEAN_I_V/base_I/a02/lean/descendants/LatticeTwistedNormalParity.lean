import LatticeTwistedNormalDerivative
import LatticeTwistedKernelParity

/-! Parity covariance of the actual divided-derivative normal products.
The proof transports the two pointwise finite sums through the inherited
involution. It applies to arbitrary Laurent fields on the twisted carrier;
no state-field or twisted Jacobi property is assumed. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedNormalParity
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedParity LatticeTwistedTensorField LatticeTwistedKernelParity
open LatticeTwistedNormalDerivative
open scoped BigOperators

theorem theta_derivativeCoefficient (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) (v : Carrier o) :
    liftedTheta o (derivativeCoefficient o i n k v) =
      -derivativeCoefficient o i n k (liftedTheta o v) := by
  simp only [derivativeCoefficient, LinearMap.smul_apply, map_smul,
    theta_fieldCoefficient, smul_neg]

theorem derivativeCoefficient_even (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) : derivativeCoefficient o i n (2*k)=0 := by
  unfold derivativeCoefficient
  rw [show 2*k+2*(n:ℤ)=2*(k+n) by omega, tensorHalfFieldCoefficient_even, smul_zero]

theorem derivativeField_even (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) : HVertexOperator.coeff (derivativeField o i n) (2*k)=0 := by
  rw [derivativeField_coefficient, derivativeCoefficient_even]

theorem theta_creationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (c : ℂ)
    (hBC : ∀ k v, liftedTheta o (HVertexOperator.coeff B k v) =
      c • HVertexOperator.coeff C k (liftedTheta o v))
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    liftedTheta o (creationTerm o i n B k a v) =
      (-c) • creationTerm o i n C k a (liftedTheta o v) := by
  simp only [creationTerm, LatticeTwistedNormalProduct.creationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, map_smul,
    liftedTheta_halfMode, hBC, smul_neg, neg_smul, smul_smul]
  module

theorem theta_annihilationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (c : ℂ)
    (hBC : ∀ k v, liftedTheta o (HVertexOperator.coeff B k v) =
      c • HVertexOperator.coeff C k (liftedTheta o v))
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    liftedTheta o (annihilationTerm o i n B k a v) =
      (-c) • annihilationTerm o i n C k a (liftedTheta o v) := by
  simp only [annihilationTerm, LatticeTwistedNormalProduct.annihilationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, map_smul,
    hBC, liftedTheta_halfMode, map_neg, smul_neg, neg_smul, smul_smul]
  module

theorem theta_derivativeNormalField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (c : ℂ)
    (hBC : ∀ k v, liftedTheta o (HVertexOperator.coeff B k v) =
      c • HVertexOperator.coeff C k (liftedTheta o v))
    (k : ℤ) (v : Carrier o) :
    liftedTheta o (HVertexOperator.coeff (derivativeNormalField o i n B) k v) =
      (-c) • HVertexOperator.coeff (derivativeNormalField o i n C) k (liftedTheta o v) := by
  simp only [derivativeNormalField_coefficient, normalCoefficient_apply, map_add]
  have hc : liftedTheta o (∑ᶠ a, creationTerm o i n B k a v) =
      ∑ᶠ a, liftedTheta o (creationTerm o i n B k a v) :=
    (liftedTheta o).toAddMonoidHom.map_finsum (creationTerm_finite o i n B k v)
  have ha : liftedTheta o (∑ᶠ a, annihilationTerm o i n B k a v) =
      ∑ᶠ a, liftedTheta o (annihilationTerm o i n B k a v) :=
    (liftedTheta o).toAddMonoidHom.map_finsum (annihilationTerm_finite o i n B k v)
  rw [hc,ha]
  simp_rw [theta_creationTerm o i n B C c hBC, theta_annihilationTerm o i n B C c hBC]
  rw [← smul_finsum' (-c) (creationTerm_finite o i n C k (liftedTheta o v)),
    ← smul_finsum' (-c) (annihilationTerm_finite o i n C k (liftedTheta o v)), smul_add]

theorem theta_derivativeNormalField_comp (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o))
    (hBC : ∀ k, (liftedTheta o).comp (HVertexOperator.coeff B k) =
      (HVertexOperator.coeff C k).comp (liftedTheta o)) (k : ℤ) :
    (liftedTheta o).comp (HVertexOperator.coeff (derivativeNormalField o i n B) k) =
      -((HVertexOperator.coeff (derivativeNormalField o i n C) k).comp (liftedTheta o)) := by
  apply LinearMap.ext
  intro v
  have h := theta_derivativeNormalField o i n B C 1
    (fun k v => by simpa using LinearMap.congr_fun (hBC k) v) k v
  simpa only [neg_one_smul, LinearMap.comp_apply, LinearMap.neg_apply] using h

theorem paritySign_odd_translate (k a : ℤ) :
    paritySign (k+2*a+1) = -paritySign k := by
  have hk : k%2=0 ∨ k%2=1 := by omega
  rcases hk with hk | hk
  · have he : (k+2*a+1)%2=1 := by omega
    simp [paritySign,hk,he]
  · have he : (k+2*a+1)%2=0 := by omega
    simp [paritySign,hk,he]

theorem negArgument_creationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o))
    (hBC : ∀ k, HVertexOperator.coeff C k = paritySign k • HVertexOperator.coeff B k)
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    creationTerm o i n C k a v = (-paritySign k) • creationTerm o i n B k a v := by
  have hp : paritySign (k+2*(n:ℤ)-2*(a:ℤ)+1) = -paritySign k := by
    rw [show k+2*(n:ℤ)-2*(a:ℤ)+1=k+2*((n:ℤ)-a)+1 by omega,
      paritySign_odd_translate]
  simp only [creationTerm, LatticeTwistedNormalProduct.creationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, hBC, map_smul, hp]
  exact smul_comm _ _ _

theorem negArgument_annihilationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o))
    (hBC : ∀ k, HVertexOperator.coeff C k = paritySign k • HVertexOperator.coeff B k)
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    annihilationTerm o i n C k a v = (-paritySign k) • annihilationTerm o i n B k a v := by
  have hp : paritySign (k+2*(n:ℤ)+2*(a:ℤ)+3) = -paritySign k := by
    rw [show k+2*(n:ℤ)+2*(a:ℤ)+3=k+2*((n:ℤ)+a+1)+1 by omega,
      paritySign_odd_translate]
  simp only [annihilationTerm, LatticeTwistedNormalProduct.annihilationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, hBC, map_smul, hp]
  exact smul_comm _ _ _

theorem negArgument_derivativeNormalField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o))
    (hBC : ∀ k, HVertexOperator.coeff C k = paritySign k • HVertexOperator.coeff B k)
    (k : ℤ) (v : Carrier o) :
    HVertexOperator.coeff (derivativeNormalField o i n C) k v =
      (-paritySign k) • HVertexOperator.coeff (derivativeNormalField o i n B) k v := by
  simp only [derivativeNormalField_coefficient, normalCoefficient_apply,
    negArgument_creationTerm o i n B C hBC, negArgument_annihilationTerm o i n B C hBC]
  rw [← smul_finsum' (-paritySign k) (creationTerm_finite o i n B k v),
    ← smul_finsum' (-paritySign k) (annihilationTerm_finite o i n B k v), smul_add]

end HMT.IV.LatticeTwistedNormalParity
end
