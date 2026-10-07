import LatticeNormalOrderedField

/-!
Linearity in the field argument of the actual locally finite normal product.
Finite support is inherited from the established creation/annihilation term
bounds, rather than added as a premise.  This allows the descendant recursion
on oscillator words to extend to their linear span.
-/

noncomputable section
namespace HMT.IV.LatticeNormalProductLinear

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeNormalOrderedField

set_option synthInstance.maxHeartbeats 200000

theorem creationTerm_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i n (B+C) k a =
      creationTerm o i n B k a + creationTerm o i n C k a := by
  apply LinearMap.ext
  intro v
  simp only [creationTerm, HVertexOperator.coeff_add, Pi.add_apply,
    LinearMap.smul_apply, LinearMap.comp_apply, LinearMap.add_apply, map_add, smul_add]

theorem annihilationTerm_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n (B+C) k a =
      annihilationTerm o i n B k a + annihilationTerm o i n C k a := by
  apply LinearMap.ext
  intro v
  simp only [annihilationTerm, HVertexOperator.coeff_add, Pi.add_apply,
    LinearMap.smul_apply, LinearMap.comp_apply, LinearMap.add_apply, smul_add]

theorem creationTerm_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i n (c • B) k a = c • creationTerm o i n B k a := by
  apply LinearMap.ext
  intro v
  simp only [creationTerm, HVertexOperator.coeff_smul, Pi.smul_apply,
    LinearMap.smul_apply, LinearMap.comp_apply, map_smul]
  exact smul_comm _ _ _

theorem annihilationTerm_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n (c • B) k a = c • annihilationTerm o i n B k a := by
  apply LinearMap.ext
  intro v
  simp only [annihilationTerm, HVertexOperator.coeff_smul, Pi.smul_apply,
    LinearMap.smul_apply, LinearMap.comp_apply]
  exact smul_comm _ _ _

theorem normalCoefficient_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) :
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
    (c : ℂ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) :
    normalCoefficient o i n (c • B) k = c • normalCoefficient o i n B k := by
  apply LinearMap.ext
  intro v
  simp only [normalCoefficient_apply, LinearMap.smul_apply,
    creationTerm_smul, annihilationTerm_smul]
  rw [← smul_finsum, ← smul_finsum, smul_add]

theorem normalField_add (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B C : VertexOperator ℂ (LatticeCarrier o)) :
    normalField o i n (B+C) = normalField o i n B + normalField o i n C := by
  apply HVertexOperator.coeff_inj
  funext k
  simp only [normalField_coefficient, HVertexOperator.coeff_add, Pi.add_apply,
    normalCoefficient_add]

theorem normalField_smul (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (c : ℂ) (B : VertexOperator ℂ (LatticeCarrier o)) :
    normalField o i n (c • B) = c • normalField o i n B := by
  apply HVertexOperator.coeff_inj
  funext k
  simp only [normalField_coefficient, HVertexOperator.coeff_smul, Pi.smul_apply,
    normalCoefficient_smul]

/-- The descendant constructor as a genuine complex-linear endomorphism
of the space of Laurent fields on the existing carrier. -/
def normalFieldLinear (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    Module.End ℂ (VertexOperator ℂ (LatticeCarrier o)) where
  toFun := normalField o i n
  map_add' := normalField_add o i n
  map_smul' c B := by
    simpa only [RingHom.id_apply] using normalField_smul o i n c B

theorem normalField_zero (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    normalField o i n (0 : VertexOperator ℂ (LatticeCarrier o)) = 0 :=
  (normalFieldLinear o i n).map_zero

end HMT.IV.LatticeNormalProductLinear
end

#print axioms HMT.IV.LatticeNormalProductLinear.normalCoefficient_add
#print axioms HMT.IV.LatticeNormalProductLinear.normalCoefficient_smul
#print axioms HMT.IV.LatticeNormalProductLinear.normalField_add
#print axioms HMT.IV.LatticeNormalProductLinear.normalField_smul
#print axioms HMT.IV.LatticeNormalProductLinear.normalFieldLinear
#print axioms HMT.IV.LatticeNormalProductLinear.normalField_zero
