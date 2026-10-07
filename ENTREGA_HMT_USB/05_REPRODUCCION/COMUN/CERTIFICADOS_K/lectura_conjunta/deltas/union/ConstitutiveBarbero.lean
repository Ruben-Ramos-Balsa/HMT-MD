import IncidenceChain
import ContractiveChannels
import Mathlib.LinearAlgebra.Matrix.Trace

/-! The marked chain functional transported through the proved constitutive
inverse. No target value of Barbero--Immirzi is supplied to this construction. -/
noncomputable section
namespace HMT.OrientedReturn
open HMT.III.Constitutive
open Set

def constitutivePrimitive (s : ℝ) : ℝ :=
  12 * s ^ 3 / (1 - s ^ 9) - s ^ 4 / (1 - s ^ 12) -
    (Real.log s) ^ 2 / (20 * Real.pi)

theorem return90_thirtieth (q : ℝ) :
    returnSeries 90 q = (q ^ 30) ^ 3 / (1 - (q ^ 30) ^ 9) := by
  norm_num [returnSeries, ← pow_mul]

theorem return120_thirtieth (q : ℝ) :
    returnSeries 120 q = (q ^ 30) ^ 4 / (1 - (q ^ 30) ^ 12) := by
  norm_num [returnSeries, ← pow_mul]

theorem primitive_thirtieth (q : ℝ) :
    constitutivePrimitive (q ^ 30) = fundamentalReturn q -
      (30 * Real.log q) ^ 2 / (20 * Real.pi) := by
  unfold constitutivePrimitive fundamentalReturn
  rw [return90_thirtieth, return120_thirtieth, Real.log_pow]
  norm_num
  ring

def angularFunctional (x y : ℝ) : ℝ :=
  180 * x * y / Real.pi + fundamentalReturn (Real.exp (-x + y)) -
    fundamentalReturn (Real.exp (-x - y))

def barbero (Q : OrientedChannels) : ℝ :=
  180 * Q.angularX * Q.angularY / Real.pi +
    chainReader Q.qMinus fundamentalChain - chainReader Q.qPlus fundamentalChain

theorem barbero_angular (Q : OrientedChannels) :
    barbero Q = angularFunctional Q.angularX Q.angularY := by
  rw [barbero, angularFunctional, Q.angular_channels.1, Q.angular_channels.2,
    chainReader_fundamental, chainReader_fundamental]

theorem angular_degree_conversion (x y : ℝ) :
    Real.pi * (180 * x / Real.pi) * (180 * y / Real.pi) / 180 =
      180 * x * y / Real.pi := by
  field_simp [Real.pi_ne_zero]
  ring

theorem barbero_factorization (Q : OrientedChannels) :
    barbero Q = constitutivePrimitive (Q.qMinus ^ 30) -
      constitutivePrimitive (Q.qPlus ^ 30) := by
  rw [primitive_thirtieth, primitive_thirtieth, Q.angular_log_channels.1,
    Q.angular_log_channels.2, barbero, chainReader_fundamental, chainReader_fundamental]
  field_simp [Real.pi_ne_zero]
  ring

def recoveredFunctional (rMinus rPlus : ℝ)
    (hm : rMinus ∈ Ioo (3 / 4) 1) (hp : rPlus ∈ Ioo (3 / 4) 1) : ℝ :=
  constitutivePrimitive (recover rMinus hm) - constitutivePrimitive (recover rPlus hp)

theorem barbero_from_constitutive (Q : OrientedChannels) :
    barbero Q = recoveredFunctional (channelResponse Q.qMinus) (channelResponse Q.qPlus)
      (channelResponse_bounds Q.minus_mem) (channelResponse_bounds Q.plus_mem) := by
  rw [barbero_factorization, recoveredFunctional]
  have hm : recover (channelResponse Q.qMinus) (channelResponse_bounds Q.minus_mem) =
      Q.qMinus ^ 30 := by
    simpa only [channelResponse_eq Q.minus_mem] using recover_response (channel_power_mem Q.minus_mem)
  have hp : recover (channelResponse Q.qPlus) (channelResponse_bounds Q.plus_mem) =
      Q.qPlus ^ 30 := by
    simpa only [channelResponse_eq Q.plus_mem] using recover_response (channel_power_mem Q.plus_mem)
  rw [hm, hp]

theorem angularFunctional_odd (x y : ℝ) : angularFunctional x (-y) = -angularFunctional x y := by
  unfold angularFunctional
  rw [sub_neg_eq_add]
  have h : -x + -y = -x - y := by ring
  rw [h]
  ring

theorem angularFunctional_balanced (x : ℝ) : angularFunctional x 0 = 0 := by
  simp [angularFunctional]

/-- Ordinary trace on the two labelled scalar channels; no arbitrary
spectral functional calculus is assumed by this finite realization. -/
def orientationMatrix : Matrix (Fin 2) (Fin 2) ℝ := Matrix.diagonal ![1, -1]
def primitiveMatrix (sPlus sMinus : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  Matrix.diagonal ![constitutivePrimitive sPlus, constitutivePrimitive sMinus]

theorem oriented_trace (sPlus sMinus : ℝ) :
    -Matrix.trace (orientationMatrix * primitiveMatrix sPlus sMinus) =
      constitutivePrimitive sMinus - constitutivePrimitive sPlus := by
  simp [orientationMatrix, primitiveMatrix, Matrix.trace, Matrix.diagonal_mul_diagonal,
    Fin.sum_univ_two]
  ring

theorem barbero_trace (Q : OrientedChannels) :
    barbero Q = -Matrix.trace (orientationMatrix * primitiveMatrix (Q.qPlus ^ 30) (Q.qMinus ^ 30)) := by
  rw [oriented_trace, barbero_factorization]

#print axioms barbero_angular
#print axioms angular_degree_conversion
#print axioms barbero_factorization
#print axioms barbero_from_constitutive
#print axioms angularFunctional_odd
#print axioms barbero_trace
end HMT.OrientedReturn
