import ConstitutiveBarbero

/-! Recover the same oriented functional from the normalized constitutive
readings. Traces below are finite labelled-channel realizations. -/
noncomputable section
namespace HMT.OrientedReturn
open HMT.III.Constitutive
open Set

def speedImpedanceFunctional (Z c : ℝ)
    (hm : Real.sqrt (Z / c) ∈ Ioo (3 / 4) 1)
    (hp : 1 / Real.sqrt (Z * c) ∈ Ioo (3 / 4) 1) : ℝ :=
  recoveredFunctional (Real.sqrt (Z / c)) (1 / Real.sqrt (Z * c)) hm hp

theorem vacuum_minus_reading_mem (Q : OrientedChannels) :
    Real.sqrt (Q.vacuum.impedance / Q.vacuum.speed) ∈ Ioo (3 / 4) 1 := by
  rw [← Q.vacuum.recover_rMinus]
  exact channelResponse_bounds Q.minus_mem

theorem vacuum_plus_reading_mem (Q : OrientedChannels) :
    1 / Real.sqrt (Q.vacuum.impedance * Q.vacuum.speed) ∈ Ioo (3 / 4) 1 := by
  rw [← Q.vacuum.recover_rPlus]
  exact channelResponse_bounds Q.plus_mem

theorem barbero_from_speed_impedance (Q : OrientedChannels) :
    barbero Q = speedImpedanceFunctional Q.vacuum.impedance Q.vacuum.speed
      (vacuum_minus_reading_mem Q) (vacuum_plus_reading_mem Q) := by
  unfold speedImpedanceFunctional
  simpa only [← Q.vacuum.recover_rMinus, ← Q.vacuum.recover_rPlus]
    using barbero_from_constitutive Q

/-- Simultaneously transport orientation and the already constructed channel
evaluation. This is not a claim of an unimplemented general spectral calculus. -/
theorem simultaneous_trace_invariant
    (U V R M : Matrix (Fin 2) (Fin 2) ℝ) (hVU : V * U = 1) :
    Matrix.trace ((U * R * V) * (U * M * V)) = Matrix.trace (R * M) := by
  calc
    Matrix.trace ((U * R * V) * (U * M * V)) =
        Matrix.trace (U * (R * (V * U) * M) * V) := by congr 1; simp only [Matrix.mul_assoc]
    _ = Matrix.trace (U * (R * M) * V) := by rw [hVU]; simp
    _ = Matrix.trace (V * (U * (R * M))) := Matrix.trace_mul_comm _ _
    _ = Matrix.trace (R * M) := by rw [← Matrix.mul_assoc, hVU, Matrix.one_mul]

theorem barbero_transported_trace (Q : OrientedChannels)
    (U V : Matrix (Fin 2) (Fin 2) ℝ) (hVU : V * U = 1) :
    barbero Q = -Matrix.trace ((U * orientationMatrix * V) *
      (U * primitiveMatrix (Q.qPlus ^ 30) (Q.qMinus ^ 30) * V)) := by
  rw [simultaneous_trace_invariant U V _ _ hVU]
  exact barbero_trace Q

/-- Repetition of the two labelled channels over an arbitrary finite nonempty
index type, retaining its multiplicity instead of changing the functional. -/
def amplifiedProduct (n : ℕ) (sPlus sMinus : ℝ) :
    Matrix (Fin 2 × Fin n) (Fin 2 × Fin n) ℝ :=
  Matrix.diagonal (fun i => if i.1 = 0 then constitutivePrimitive sPlus
    else -constitutivePrimitive sMinus)

theorem amplified_trace (n : ℕ) (sPlus sMinus : ℝ) :
    Matrix.trace (amplifiedProduct n sPlus sMinus) =
      (n : ℝ) * (constitutivePrimitive sPlus - constitutivePrimitive sMinus) := by
  simp [amplifiedProduct, Matrix.trace_diagonal, Fintype.sum_prod_type,
    Fin.sum_univ_two]
  ring

theorem barbero_nonadic_amplification (Q : OrientedChannels) (m : ℕ) :
    barbero Q = -Matrix.trace (amplifiedProduct (9 ^ m) (Q.qPlus ^ 30) (Q.qMinus ^ 30)) /
      (9 : ℝ) ^ m := by
  rw [amplified_trace, barbero_factorization]
  push_cast
  field_simp
  ring

#print axioms barbero_from_speed_impedance
#print axioms simultaneous_trace_invariant
#print axioms barbero_transported_trace
#print axioms amplified_trace
#print axioms barbero_nonadic_amplification
end HMT.OrientedReturn
