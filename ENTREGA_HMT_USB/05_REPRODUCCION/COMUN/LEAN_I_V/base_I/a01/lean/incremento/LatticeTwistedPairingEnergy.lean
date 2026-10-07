import LatticeTwistedPairingGrading

/-! The existing tensor pairing intertwines the actual conformal zero mode.
Eigenvectors with different complex eigenvalues are orthogonal. -/

noncomputable section
namespace HMT.IV.LatticeTwistedPairingEnergy
open LatticeTwistedCarrier LatticeTwistedLowWeights LatticeHalfWeightBasis
open LatticeTwistedTensorPairing LatticeTwistedPairingGrading
open LatticeTwistedPositiveSector

theorem tensorPairing_energy (o : Fin 12) (u v : Carrier o) :
    tensorPairing o (conformalMode o 0 u) v =
      tensorPairing o u (conformalMode o 0 v) := by
  have he : LinearMap.comp (tensorPairing o) (conformalMode o 0) =
      (tensorPairing o).compl₂ (conformalMode o 0) := by
    apply (twistedBasis o).ext
    intro p
    apply (twistedBasis o).ext
    intro q
    change tensorPairing o (conformalMode o 0 (twistedBasis o p)) (twistedBasis o q) =
      tensorPairing o (twistedBasis o p) (conformalMode o 0 (twistedBasis o q))
    rw [conformal_basis_weight, conformal_basis_weight]
    simp only [map_smul, LinearMap.smul_apply, smul_eq_mul]
    by_cases h : twiceWeight o p.1 = twiceWeight o q.1
    · rw [h]
    · rw [tensorPairing_basis_off_weight o p q h, mul_zero, mul_zero]
  exact LinearMap.congr_fun (LinearMap.congr_fun he u) v

theorem positivePairing_energy (o : Fin 12) (u v : positiveSector o) :
    positivePairing o (positiveConformalMode o 0 u) v =
      positivePairing o u (positiveConformalMode o 0 v) :=
  tensorPairing_energy o u.val v.val

theorem positivePairing_off_eigen (o : Fin 12) (u v : positiveSector o) (a b : ℂ)
    (hu : positiveConformalMode o 0 u = a • u)
    (hv : positiveConformalMode o 0 v = b • v) (hab : a ≠ b) :
    positivePairing o u v = 0 := by
  have h := positivePairing_energy o u v
  rw [hu, hv] at h
  simp only [map_smul, LinearMap.smul_apply, smul_eq_mul] at h
  by_contra hn
  exact hab (mul_right_cancel₀ hn h)

end HMT.IV.LatticeTwistedPairingEnergy
end
