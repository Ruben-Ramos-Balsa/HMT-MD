import LatticeTwistedContragredientTruncation
import LatticeTwistedCorrectionInverse

/-! The coordinate-inversion exponential is a formal unit on the actual
positive sector. Both signs are pointwise polynomial by the proved local
nilpotence of L(1); no global cutoff or nilpotence of L(-1) is introduced. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeTwistedCoordinateExponential
open LatticeTwistedPositiveSector LatticeTwistedContragredientTruncation
open HMT.Formal.FiniteExponentialProduct
open LatticeTwistedCorrectionInverse (expCoeff_fin_zero)
open PowerSeries
open scoped BigOperators

theorem formal_exponential_inverse {A : Type*} [Ring A] [Algebra ℂ A]
    (s : PowerSeries A) (hs : constantCoeff A s = 0) :
    mk (expCoeff_fin s) * mk (expCoeff_fin (-s)) = 1 := by
  apply PowerSeries.ext
  intro n
  have h := expCoeff_fin_add_eq_coeff_mul s (-s) hs (by simp [hs])
    (Commute.refl s).neg_right n
  rw [add_neg_cancel, expCoeff_fin_zero] at h
  exact h.symm

theorem formal_inverse_exponential {A : Type*} [Ring A] [Algebra ℂ A]
    (s : PowerSeries A) (hs : constantCoeff A s = 0) :
    mk (expCoeff_fin (-s)) * mk (expCoeff_fin s) = 1 := by
  apply PowerSeries.ext
  intro n
  have h := expCoeff_fin_add_eq_coeff_mul (-s) s (by simp [hs]) hs
    (Commute.refl s).neg_left n
  rw [neg_add_cancel, expCoeff_fin_zero] at h
  exact h.symm

theorem negative_linear_potential {A : Type*} [Ring A] (a : A) :
    -(C A a * X) = C A (-a) * X := by rw [map_neg, neg_mul]

abbrev EndSpace (o : Fin 12) := Module.End ℂ (positiveSector o)

def potential (o : Fin 12) : PowerSeries (EndSpace o) :=
  C _ (lowering o) * X

theorem potential_constant (o : Fin 12) :
    constantCoeff (EndSpace o) (potential o) = 0 := by simp [potential]

theorem potential_power_coefficient (o : Fin 12) (k n : ℕ) :
    coeff (EndSpace o) n ((potential o)^k) =
      if n=k then (lowering o)^k else 0 := by
  rw [potential, (commute_X (C _ (lowering o))).mul_pow, ← map_pow,
    coeff_C_mul_X_pow]

theorem exponential_coefficient (o : Fin 12) (n : ℕ) :
    expCoeff_fin (potential o) n = inversionCoefficient o n := by
  rw [expCoeff_fin, Finset.sum_eq_single n]
  · rw [potential_power_coefficient, if_pos rfl]
    simp [inversionCoefficient, coeff_exp]
  · intro k _ hk
    rw [potential_power_coefficient, if_neg (Ne.symm hk), smul_zero]
  · simp

def coordinateExponential (o : Fin 12) : PowerSeries (EndSpace o) :=
  mk (inversionCoefficient o)

def inverseCoordinateExponential (o : Fin 12) : PowerSeries (EndSpace o) :=
  mk (expCoeff_fin (-potential o))

theorem coordinateExponential_eq (o : Fin 12) :
    mk (expCoeff_fin (potential o)) = coordinateExponential o := by
  apply PowerSeries.ext
  intro n
  simp only [coordinateExponential, coeff_mk, exponential_coefficient]

theorem coordinateExponential_mul_inverse (o : Fin 12) :
    coordinateExponential o * inverseCoordinateExponential o = 1 := by
  have h := formal_exponential_inverse (potential o) (potential_constant o)
  simpa only [coordinateExponential_eq,
    inverseCoordinateExponential] using h

theorem inverseCoordinateExponential_mul (o : Fin 12) :
    inverseCoordinateExponential o * coordinateExponential o = 1 := by
  have h := formal_inverse_exponential (potential o) (potential_constant o)
  simpa only [coordinateExponential_eq,
    inverseCoordinateExponential] using h

def coordinateUnit (o : Fin 12) : (PowerSeries (EndSpace o))ˣ where
  val := coordinateExponential o
  inv := inverseCoordinateExponential o
  val_inv := coordinateExponential_mul_inverse o
  inv_val := inverseCoordinateExponential_mul o

theorem coordinateExponential_coefficient_finite (o : Fin 12)
    (v : positiveSector o) :
    (Function.support (fun n : ℕ => coeff (EndSpace o) n
      (coordinateExponential o) v)).Finite := by
  simpa only [coordinateExponential, coeff_mk] using inversionCoefficient_finite o v

theorem negative_potential_power_coefficient (o : Fin 12) (k n : ℕ) :
    coeff (EndSpace o) n ((-potential o)^k) =
      if n=k then (-lowering o)^k else 0 := by
  have hp : -potential o = C _ (-lowering o) * X := by
    exact negative_linear_potential (lowering o)
  rw [hp,
    (commute_X (C _ (-lowering o))).mul_pow, ← map_pow, coeff_C_mul_X_pow]

theorem inverseCoordinateExponential_coefficient (o : Fin 12) (n : ℕ) :
    coeff (EndSpace o) n (inverseCoordinateExponential o) =
      (n.factorial:ℂ)⁻¹ • (-lowering o)^n := by
  rw [inverseCoordinateExponential, coeff_mk, expCoeff_fin, Finset.sum_eq_single n]
  · rw [negative_potential_power_coefficient, if_pos rfl]
    simp [coeff_exp]
  · intro k _ hk
    rw [negative_potential_power_coefficient, if_neg (Ne.symm hk), smul_zero]
  · simp

theorem inverseCoordinateExponential_coefficient_finite (o : Fin 12)
    (v : positiveSector o) :
    (Function.support (fun n : ℕ => coeff (EndSpace o) n
      (inverseCoordinateExponential o) v)).Finite := by
  obtain ⟨b, hb⟩ := lowering_power_eventually_zero o v
  apply (Finset.range b).finite_toSet.subset
  intro n hn
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra h
  apply hn
  change (coeff (EndSpace o) n (inverseCoordinateExponential o)) v = 0
  rw [inverseCoordinateExponential_coefficient,
    ← neg_one_smul ℂ (lowering o), smul_pow]
  simp only [LinearMap.smul_apply, hb n (by omega), smul_zero]

end HMT.IV.LatticeTwistedCoordinateExponential
end

#print axioms HMT.IV.LatticeTwistedCoordinateExponential.coordinateUnit
#print axioms HMT.IV.LatticeTwistedCoordinateExponential.coordinateExponential_coefficient_finite
