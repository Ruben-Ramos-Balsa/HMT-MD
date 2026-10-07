import LatticeHalfExponentialExchange
import HalfModeScalarFactor

/-! The scalar series read from the actual half-mode exchange is identified
with the pairing multiple of the universal odd scalar series. Its normalized
formal exponential is the corresponding integer power of the rational unit.
The exchange operators, pairing and finite normal-order recursion are inherited
unchanged. This module does not assert a BCH reordering of the full fields. -/

noncomputable section
namespace HMT.IV.LatticeHalfContractionFactor
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfExponentialExchange PowerSeries
open HMT.Formal.HalfModeScalarFactor

/-- Odd coefficients are the contractions already proved for the actual
annihilation potential; even coefficients vanish as in that potential. -/
def contractionSeries (o : Fin 12) (x y : Lattice o) : PowerSeries ℂ :=
  PowerSeries.mk fun r => if r%2=1 then contraction o x y r else 0

theorem contractionSeries_coefficient (o : Fin 12) (x y : Lattice o) (r : ℕ) :
    coeff ℂ r (contractionSeries o x y) =
      if r%2=1 then contraction o x y r else 0 := coeff_mk _ _

theorem contractionSeries_coefficient_even (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    coeff ℂ (2*n) (contractionSeries o x y) = 0 := by
  simp [contractionSeries_coefficient]

theorem contractionSeries_coefficient_odd (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    coeff ℂ (2*n+1) (contractionSeries o x y) =
      -2*(integerPair o x y : ℂ)/(2*(n:ℂ)+1) := by
  rw [contractionSeries_coefficient, if_pos (by omega), contraction_odd]

theorem contractionSeries_constant (o : Fin 12) (x y : Lattice o) :
    constantCoeff ℂ (contractionSeries o x y) = 0 := by
  rw [← coeff_zero_eq_constantCoeff_apply]
  exact contractionSeries_coefficient_even o x y 0

theorem contractionSeries_eq_pair_smul (o : Fin 12) (x y : Lattice o) :
    contractionSeries o x y = (integerPair o x y : ℂ) • S := by
  ext r
  by_cases hr : r%2=1
  · have he : r = 2*(r/2)+1 := by omega
    rw [he, contractionSeries_coefficient_odd]
    simp only [map_smul, coeff_S_odd, smul_eq_mul]
    ring
  · have he : r = 2*(r/2) := by omega
    rw [he, contractionSeries_coefficient_even]
    simp only [map_smul, coeff_S_even, smul_zero]

theorem contractionSeries_eq_pair_zsmul (o : Fin 12) (x y : Lattice o) :
    contractionSeries o x y = integerPair o x y • S := by
  rw [contractionSeries_eq_pair_smul, Int.cast_smul_eq_zsmul]

/-- This coefficient identity links the scalar series to the actual operator
commutator, rather than assigning a scalar solely from a desired formula. -/
theorem potential_exchange_via_contractionSeries (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) :
    coeff (HalfEnd o) r (annihilationPotential o x) * halfCreationExponentialMode o y d =
      halfCreationExponentialMode o y d * coeff (HalfEnd o) r (annihilationPotential o x) +
        if r≤d then coeff ℂ r (contractionSeries o x y) •
          halfCreationExponentialMode o y (d-r) else 0 := by
  rw [potentialCoefficient_exchange, contractionSeries_coefficient]
  by_cases hr : r%2=1 <;> by_cases hd : r≤d <;> simp [hr, hd]

def contractionFactor (o : Fin 12) (x y : Lattice o) : PowerSeries ℂ :=
  formalExp (contractionSeries o x y)

theorem contractionFactor_constant (o : Fin 12) (x y : Lattice o) :
    constantCoeff ℂ (contractionFactor o x y) = 1 :=
  constantCoeff_formalExp _

theorem contractionFactor_derivative (o : Fin 12) (x y : Lattice o) :
    derivative ℂ (contractionFactor o x y) =
      derivative ℂ (contractionSeries o x y) * contractionFactor o x y :=
  formalExp_derivative _

theorem contractionFactor_eq_rational_integer_power (o : Fin 12) (x y : Lattice o) :
    contractionFactor o x y =
      (rationalFactorUnit ^ integerPair o x y : (PowerSeries ℂ)ˣ) := by
  rw [contractionFactor, contractionSeries_eq_pair_zsmul, formalExp_zsmul_S]

theorem contractionFactor_eq_rational_nat_power (o : Fin 12) (x y : Lattice o)
    (n : ℕ) (h : integerPair o x y = n) :
    contractionFactor o x y =
      ((1-X) * (1+X : PowerSeries ℂ)⁻¹)^n := by
  rw [contractionFactor_eq_rational_integer_power, h]
  simp only [zpow_natCast, Units.val_pow_eq_pow_val, coe_rationalFactorUnit]

theorem contractionFactor_orthogonal (o : Fin 12) (x y : Lattice o)
    (h : integerPair o x y = 0) : contractionFactor o x y = 1 := by
  rw [contractionFactor_eq_rational_integer_power, h, zpow_zero, Units.val_one]

end HMT.IV.LatticeHalfContractionFactor
end
