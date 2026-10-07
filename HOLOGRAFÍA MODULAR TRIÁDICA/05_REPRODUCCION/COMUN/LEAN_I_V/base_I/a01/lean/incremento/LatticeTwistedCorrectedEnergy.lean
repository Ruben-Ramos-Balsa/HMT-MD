import LatticeTwistedCorrectedStateField

/-! Covariance is transported through the existing correction exponential.
Its degree lowers source energy by d and shifts the ramified exponent by 2d;
the two contributions cancel exactly. -/

noncomputable section
namespace HMT.IV.LatticeTwistedCorrectedEnergy
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeEnergyGrading LatticeEnergyModes LatticeTwistedCorrection LatticeTwistedCorrectedStateField

def energyCommutator (o : Fin 12) :
    Module.End ℂ (Carrier o) →ₗ[ℂ] Module.End ℂ (Carrier o) where
  toFun T := conformalMode o 0 * T - T * conformalMode o 0
  map_add' A B := by simp only [mul_add, add_mul]; abel
  map_smul' c A := by simp only [mul_smul_comm, smul_mul_assoc, smul_sub, RingHom.id_apply]

def EnergyCovariant (o : Fin 12) (W : FieldAssignment o) : Prop :=
  ∀ u k, energyCommutator o (HVertexOperator.coeff (W u) k) =
    HVertexOperator.coeff (W (energy o u)) k +
      ((k:ℂ)/2) • HVertexOperator.coeff (W u) k

theorem stateTerm_energy (o : Fin 12) (W : FieldAssignment o)
    (hW : EnergyCovariant o W) (u : LatticeCarrier o) (k : ℤ) (d : ℕ) :
    energyCommutator o (stateTerm o W k d u) =
      stateTerm o W k d (energy o u) + ((k:ℂ)/2) • stateTerm o W k d u := by
  change energyCommutator o (HVertexOperator.coeff
    (W (correctionExponentialCoefficient o d u)) (k+2*(d:ℤ))) = _
  rw [hW, correctionExponential_lowersEnergy]
  rw [show correctionExponentialCoefficient o d (energy o u) -
      (d:ℂ) • correctionExponentialCoefficient o d u =
      correctionExponentialCoefficient o d (energy o u) +
        (-(d:ℂ)) • correctionExponentialCoefficient o d u by module]
  simp only [map_add, map_smul, HVertexOperator.coeff_add, HVertexOperator.coeff_smul,
    Pi.add_apply, Pi.smul_apply]
  change stateTerm o W k d (energy o u) + (-(d:ℂ)) • stateTerm o W k d u +
    (((k+2*(d:ℤ):ℤ):ℂ)/2) • stateTerm o W k d u =
      stateTerm o W k d (energy o u) + ((k:ℂ)/2) • stateTerm o W k d u
  have hs : (((k+2*(d:ℤ):ℤ):ℂ)/2) = (k:ℂ)/2+(d:ℂ) := by push_cast; ring
  rw [hs]
  module

theorem correctedAssignment_energy (o : Fin 12) (W : FieldAssignment o)
    (hW : EnergyCovariant o W) : EnergyCovariant o (correctedAssignment o W) := by
  intro u k
  change energyCommutator o (∑ᶠ d, stateTerm o W k d u) =
    (∑ᶠ d, stateTerm o W k d (energy o u)) +
      ((k:ℂ)/2) • ∑ᶠ d, stateTerm o W k d u
  have hm := (energyCommutator o).toAddMonoidHom.map_finsum (stateTerm_finite o W k u)
  change energyCommutator o (∑ᶠ d, stateTerm o W k d u) =
    ∑ᶠ d, energyCommutator o (stateTerm o W k d u) at hm
  rw [hm]
  simp_rw [stateTerm_energy o W hW u k]
  rw [smul_finsum' _ (stateTerm_finite o W k u)]
  apply finsum_add_distrib (stateTerm_finite o W k (energy o u))
  apply (stateTerm_finite o W k u).subset
  intro d hd hz
  apply hd
  change ((k:ℂ)/2) • stateTerm o W k d u = 0
  change stateTerm o W k d u = 0 at hz
  rw [hz, smul_zero]

end HMT.IV.LatticeTwistedCorrectedEnergy
end
