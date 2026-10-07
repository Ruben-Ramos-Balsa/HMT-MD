import LatticeTwistedEvenProduct
import LatticeTwistedPairingGrading
import LatticeTwistedCoordinateExponential
import CoordinateWeightSign

/-! The contragredient matrix coefficients are constructed from the actual TE
field and the actual nondegenerate twisted pairing. The output is explicitly
the algebraic dual of the even sector. Representability in the even sector and
the Jacobi identities are not smuggled into this definition. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedContragredientCoefficients
open LatticeEvenVertexFields LatticeTwistedPositiveSector
open LatticeTwistedPositiveGrading LatticeTwistedContragredientTruncation
open LatticeTwistedEvenProduct LatticeTwistedPairingGrading CoordinateWeightSign
open scoped BigOperators DirectSum

abbrev MatrixTarget (o : Fin 12) :=
  positiveSector o →ₗ[ℂ] Module.Dual ℂ (evenSpace o)

def matrixCoefficient (o : Fin 12) (r : ℤ) :
    positiveSector o →ₗ[ℂ] MatrixTarget o where
  toFun v := (positivePairing o).compl₂ (HVertexOperator.coeff (twistedEvenField o v) r)
  map_add' u v := by
    ext w a
    simp only [LinearMap.compl₂_apply, map_add, HVertexOperator.coeff_add,
      Pi.add_apply, LinearMap.add_apply]
  map_smul' c v := by
    ext w a
    simp only [LinearMap.compl₂_apply, map_smul, HVertexOperator.coeff_smul,
      Pi.smul_apply, LinearMap.smul_apply, RingHom.id_apply]

theorem matrixCoefficient_apply (o : Fin 12) (r : ℤ)
    (v w : positiveSector o) (a : evenSpace o) :
    matrixCoefficient o r v w a =
      positivePairing o w (HVertexOperator.coeff (twistedEvenField o v) r a) := rfl

def inversionTerm (o : Fin 12) (d j : ℕ) (k : ℤ) :
    positiveSector o →ₗ[ℂ] MatrixTarget o :=
  (matrixCoefficient o ((j:ℤ)-2*(d:ℤ)-k)).comp (inversionCoefficient o j)

theorem inversionCoefficient_weight_cutoff (o : Fin 12) (d j : ℕ)
    (v : positiveSector o) (hv : v ∈ positiveWeightSpace o d) (hj : d ≤ j) :
    inversionCoefficient o j v = 0 := by
  have hz := lowering_power_kills_weight o d v hv
  have hp : ((lowering o)^j) v = 0 := by
    rw [show j = (j-d)+d by omega, pow_add, Module.End.mul_apply, hz, map_zero]
  simp only [inversionCoefficient, LinearMap.smul_apply, hp, smul_zero]

theorem inversionTerm_weight_cutoff (o : Fin 12) (d j : ℕ) (k : ℤ)
    (v : positiveSector o) (hv : v ∈ positiveWeightSpace o d) (hj : d ≤ j) :
    inversionTerm o d j k v = 0 := by
  rw [inversionTerm, LinearMap.comp_apply,
    inversionCoefficient_weight_cutoff o d j v hv hj, map_zero]

def homogeneousCoefficient (o : Fin 12) (d : ℕ) (k : ℤ) :
    positiveWeightSpace o d →ₗ[ℂ] MatrixTarget o :=
  ((-1:ℂ)^d) • (∑ j ∈ Finset.range d, inversionTerm o d j k).comp
    (positiveWeightSpace o d).subtype

theorem homogeneousCoefficient_apply (o : Fin 12) (d : ℕ) (k : ℤ)
    (v : positiveWeightSpace o d) (w : positiveSector o) (a : evenSpace o) :
    homogeneousCoefficient o d k v w a =
      (-1:ℂ)^d * ∑ j ∈ Finset.range d,
        positivePairing o w (HVertexOperator.coeff
          (twistedEvenField o (inversionCoefficient o j v.val))
          ((j:ℤ)-2*(d:ℤ)-k) a) := by
  simp only [homogeneousCoefficient, LinearMap.smul_apply, LinearMap.comp_apply,
    Submodule.subtype_apply, LinearMap.sum_apply, inversionTerm,
    matrixCoefficient_apply, smul_eq_mul]

theorem homogeneous_sum_stable (o : Fin 12) (d N : ℕ) (k : ℤ)
    (v : positiveWeightSpace o d) (hN : d ≤ N) :
    (∑ j ∈ Finset.range N, inversionTerm o d j k v.val) =
      ∑ j ∈ Finset.range d, inversionTerm o d j k v.val := by
  symm
  apply Finset.sum_subset (Finset.range_mono hN)
  intro j _ hj
  exact inversionTerm_weight_cutoff o d j k v.val v.property (by simpa using hj)

def contragredientCoefficient (o : Fin 12) (k : ℤ) :
    positiveSector o →ₗ[ℂ] MatrixTarget o :=
  (DirectSum.toModule ℂ ℕ (MatrixTarget o) (fun d => homogeneousCoefficient o d k)).comp
    (weightDecomposition (positiveConformalMode o 0) (positive_weights_span o)).symm.toLinearMap

theorem contragredientCoefficient_homogeneous (o : Fin 12) (d : ℕ) (k : ℤ)
    (v : positiveWeightSpace o d) :
    contragredientCoefficient o k v.val = homogeneousCoefficient o d k v := by
  have hd : (weightDecomposition (positiveConformalMode o 0)
      (positive_weights_span o)).symm v.val =
        DirectSum.lof ℂ ℕ (fun d => positiveWeightSpace o d) d v := by
    apply (weightDecomposition (positiveConformalMode o 0)
      (positive_weights_span o)).injective
    simp only [LinearEquiv.apply_symm_apply]
    change v.val = DirectSum.coeLinearMap (positiveWeightSpace o)
      (DirectSum.of (fun d => positiveWeightSpace o d) d v)
    rw [DirectSum.coeLinearMap_of]
  change (DirectSum.toModule ℂ ℕ (MatrixTarget o) (fun d => homogeneousCoefficient o d k))
    ((weightDecomposition (positiveConformalMode o 0) (positive_weights_span o)).symm v.val) = _
  rw [hd]
  rw [DirectSum.toModule_lof]

end HMT.IV.LatticeTwistedContragredientCoefficients
end

#print axioms HMT.IV.LatticeTwistedContragredientCoefficients.contragredientCoefficient
#print axioms HMT.IV.LatticeTwistedContragredientCoefficients.homogeneous_sum_stable
