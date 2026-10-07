import LatticeTwistedNormalParity

/-! Scalar-general argument parity for the existing derivative normal product.
It is valid also for c=0 and does not divide by the intertwining scalar. -/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalArgumentScalar
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedNormalDerivative LatticeTwistedNormalParity LatticeTwistedKernelParity

theorem negArgument_creationTerm_scalar (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (c : ℂ)
    (hBC : ∀ k, HVertexOperator.coeff C k = (c*paritySign k) • HVertexOperator.coeff B k)
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    creationTerm o i n C k a v = ((-c)*paritySign k) • creationTerm o i n B k a v := by
  have hp : paritySign (k+2*(n:ℤ)-2*(a:ℤ)+1) = -paritySign k := by
    rw [show k+2*(n:ℤ)-2*(a:ℤ)+1=k+2*((n:ℤ)-a)+1 by omega,
      paritySign_odd_translate]
  simp only [creationTerm, LatticeTwistedNormalProduct.creationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, hBC, map_smul, hp]
  module

theorem negArgument_annihilationTerm_scalar (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (c : ℂ)
    (hBC : ∀ k, HVertexOperator.coeff C k = (c*paritySign k) • HVertexOperator.coeff B k)
    (k : ℤ) (a : ℕ) (v : Carrier o) :
    annihilationTerm o i n C k a v = ((-c)*paritySign k) • annihilationTerm o i n B k a v := by
  have hp : paritySign (k+2*(n:ℤ)+2*(a:ℤ)+3) = -paritySign k := by
    rw [show k+2*(n:ℤ)+2*(a:ℤ)+3=k+2*((n:ℤ)+a+1)+1 by omega,
      paritySign_odd_translate]
  simp only [annihilationTerm, LatticeTwistedNormalProduct.annihilationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, hBC, map_smul, hp]
  module

theorem negArgument_derivativeNormalField_scalar (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (c : ℂ)
    (hBC : ∀ k, HVertexOperator.coeff C k = (c*paritySign k) • HVertexOperator.coeff B k)
    (k : ℤ) (v : Carrier o) :
    HVertexOperator.coeff (derivativeNormalField o i n C) k v =
      ((-c)*paritySign k) • HVertexOperator.coeff (derivativeNormalField o i n B) k v := by
  simp only [derivativeNormalField_coefficient, normalCoefficient_apply,
    negArgument_creationTerm_scalar o i n B C c hBC,
    negArgument_annihilationTerm_scalar o i n B C c hBC]
  rw [← smul_finsum' ((-c)*paritySign k) (creationTerm_finite o i n B k v),
    ← smul_finsum' ((-c)*paritySign k) (annihilationTerm_finite o i n B k v), smul_add]

end HMT.IV.LatticeTwistedNormalArgumentScalar
end

#print axioms HMT.IV.LatticeTwistedNormalArgumentScalar.negArgument_creationTerm_scalar
#print axioms HMT.IV.LatticeTwistedNormalArgumentScalar.negArgument_annihilationTerm_scalar
#print axioms HMT.IV.LatticeTwistedNormalArgumentScalar.negArgument_derivativeNormalField_scalar
