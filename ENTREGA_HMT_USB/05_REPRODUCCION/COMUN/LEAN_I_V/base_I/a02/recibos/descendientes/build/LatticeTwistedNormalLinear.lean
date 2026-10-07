import LatticeTwistedNormalTerms

/-! Complex linearity in the field argument of divided half-normal products.
The finite supports are the established pointwise supports on the actual
twisted carrier; no additional truncation assumption is imposed. -/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalLinear

open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedNormalDerivative LatticeTwistedNormalTerms

set_option synthInstance.maxHeartbeats 200000

private theorem creationTerm_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i n (B+C) k a =
      creationTerm o i n B k a + creationTerm o i n C k a := by
  apply LinearMap.ext
  intro v
  simp only [creationTerm_apply, HVertexOperator.coeff_add, Pi.add_apply,
    LinearMap.add_apply, map_add]

private theorem annihilationTerm_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n (B+C) k a =
      annihilationTerm o i n B k a + annihilationTerm o i n C k a := by
  apply LinearMap.ext
  intro v
  simp only [annihilationTerm_apply, HVertexOperator.coeff_add, Pi.add_apply,
    LinearMap.add_apply]

private theorem creationTerm_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i n (c • B) k a = c • creationTerm o i n B k a := by
  apply LinearMap.ext
  intro v
  simp only [creationTerm_apply, HVertexOperator.coeff_smul, Pi.smul_apply,
    LinearMap.smul_apply, map_smul]

private theorem annihilationTerm_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n (c • B) k a = c • annihilationTerm o i n B k a := by
  apply LinearMap.ext
  intro v
  simp only [annihilationTerm_apply, HVertexOperator.coeff_smul, Pi.smul_apply,
    LinearMap.smul_apply]

theorem normalCoefficient_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) (k : ℤ) :
    normalCoefficient o i n (B+C) k =
      normalCoefficient o i n B k + normalCoefficient o i n C k := by
  apply LinearMap.ext
  intro v
  simp only [normalCoefficient_apply, LinearMap.add_apply, creationTerm_add,
    annihilationTerm_add]
  rw [finsum_add_distrib (creationTerm_finite o i n B k v)
      (creationTerm_finite o i n C k v),
    finsum_add_distrib (annihilationTerm_finite o i n B k v)
      (annihilationTerm_finite o i n C k v)]
  abel

theorem normalCoefficient_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ) :
    normalCoefficient o i n (c • B) k = c • normalCoefficient o i n B k := by
  apply LinearMap.ext
  intro v
  simp only [normalCoefficient_apply, LinearMap.smul_apply,
    creationTerm_smul, annihilationTerm_smul]
  rw [← smul_finsum, ← smul_finsum, smul_add]

theorem derivativeNormalField_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (Carrier o)) :
    derivativeNormalField o i n (B+C) =
      derivativeNormalField o i n B + derivativeNormalField o i n C := by
  apply HVertexOperator.coeff_inj
  funext k
  simp only [derivativeNormalField_coefficient, HVertexOperator.coeff_add,
    Pi.add_apply, normalCoefficient_add]

theorem derivativeNormalField_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (Carrier o)) :
    derivativeNormalField o i n (c • B) = c • derivativeNormalField o i n B := by
  apply HVertexOperator.coeff_inj
  funext k
  simp only [derivativeNormalField_coefficient, HVertexOperator.coeff_smul,
    Pi.smul_apply, normalCoefficient_smul]

/-- The divided half-normal descendant constructor as a complex-linear
endomorphism of the actual space of Laurent fields. -/
def derivativeNormalFieldLinear (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    Module.End ℂ (VertexOperator ℂ (Carrier o)) where
  toFun := derivativeNormalField o i n
  map_add' := derivativeNormalField_add o i n
  map_smul' c B := by
    simpa only [RingHom.id_apply] using derivativeNormalField_smul o i n c B

theorem derivativeNormalField_zero (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    derivativeNormalField o i n (0 : VertexOperator ℂ (Carrier o)) = 0 :=
  (derivativeNormalFieldLinear o i n).map_zero

end HMT.IV.LatticeTwistedNormalLinear
end

#print axioms HMT.IV.LatticeTwistedNormalLinear.normalCoefficient_add
#print axioms HMT.IV.LatticeTwistedNormalLinear.normalCoefficient_smul
#print axioms HMT.IV.LatticeTwistedNormalLinear.derivativeNormalField_add
#print axioms HMT.IV.LatticeTwistedNormalLinear.derivativeNormalField_smul
#print axioms HMT.IV.LatticeTwistedNormalLinear.derivativeNormalFieldLinear
#print axioms HMT.IV.LatticeTwistedNormalLinear.derivativeNormalField_zero
