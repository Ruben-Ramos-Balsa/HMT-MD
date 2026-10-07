import LatticeTwistedFullEnergy
import LatticeTwistedPairingEnergy
import LatticeTwistedContragredientCoefficients
import LatticeEvenGrading

/-! The actual contragredient matrix coefficient is supported on one even
homogeneous component. This follows from the constructed field energy laws,
L1 lowering, and the constructed pairing, not an assumed support condition. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeContragredientWeightSupport
open LatticeEvenVertexFields LatticeEvenConformal LatticeEvenGrading
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading
open LatticeTwistedContragredientTruncation LatticeTwistedContragredientCoefficients
open LatticeTwistedEvenProduct LatticeTwistedPairingGrading
open LatticeTwistedFullEnergy LatticeTwistedPairingEnergy

theorem inversionCoefficient_weight (o : Fin 12) (v : positiveSector o)
    (d : ℕ) (hv : v ∈ positiveWeightSpace o d) (j : ℕ) :
    positiveConformalMode o 0 (inversionCoefficient o j v) =
      ((d:ℂ)-(j:ℂ)) • inversionCoefficient o j v := by
  have h := lowering_power_weight o v (d:ℂ) (Module.End.mem_eigenspace_iff.mp hv) j
  simp only [inversionCoefficient, LinearMap.smul_apply, map_smul, h]
  exact smul_comm _ _ _

theorem homogeneousCoefficient_off_weight (o : Fin 12) (d e r : ℕ) (k : ℤ)
    (v : positiveWeightSpace o d) (w : positiveSector o)
    (hw : w ∈ positiveWeightSpace o e) (a : evenSpace o)
    (ha : a ∈ evenWeightSpace o r) (hne : (r:ℤ) ≠ (d:ℤ)+(e:ℤ)+k) :
    homogeneousCoefficient o d k v w a = 0 := by
  rw [homogeneousCoefficient_apply]
  have hz : ∀ j ∈ Finset.range d,
      positivePairing o w (HVertexOperator.coeff
        (twistedEvenField o (inversionCoefficient o j v.val))
        ((j:ℤ)-2*(d:ℤ)-k) a) = 0 := by
    intro j _
    have ho := twistedEvenField_weight o (inversionCoefficient o j v.val) a
      (r:ℂ) ((d:ℂ)-(j:ℂ)) (Module.End.mem_eigenspace_iff.mp ha)
      (inversionCoefficient_weight o v.val d v.property j) ((j:ℤ)-2*(d:ℤ)-k)
    have hs : (r:ℂ)+((d:ℂ)-(j:ℂ))+(((j:ℤ)-2*(d:ℤ)-k:ℤ):ℂ) =
        (r:ℂ)-(d:ℂ)-(k:ℂ) := by push_cast; ring
    rw [hs] at ho
    apply positivePairing_off_eigen o _ _ (e:ℂ) ((r:ℂ)-(d:ℂ)-(k:ℂ))
      (Module.End.mem_eigenspace_iff.mp hw) ho
    intro he
    apply hne
    have hc : (r:ℂ) = (d:ℂ)+(e:ℂ)+(k:ℂ) := by linear_combination -he
    exact_mod_cast hc
  rw [Finset.sum_eq_zero hz, mul_zero]

theorem contragredientCoefficient_off_weight (o : Fin 12) (d e r : ℕ) (k : ℤ)
    (v w : positiveSector o) (hv : v ∈ positiveWeightSpace o d)
    (hw : w ∈ positiveWeightSpace o e) (a : evenSpace o)
    (ha : a ∈ evenWeightSpace o r) (hne : (r:ℤ) ≠ (d:ℤ)+(e:ℤ)+k) :
    contragredientCoefficient o k v w a = 0 := by
  have h := contragredientCoefficient_homogeneous o d k (⟨v,hv⟩ : positiveWeightSpace o d)
  change contragredientCoefficient o k v = homogeneousCoefficient o d k ⟨v,hv⟩ at h
  rw [h]
  exact homogeneousCoefficient_off_weight o d e r k ⟨v,hv⟩ w hw a ha hne

end HMT.IV.LatticeContragredientWeightSupport
end
