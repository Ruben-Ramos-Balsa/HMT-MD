import LatticeTwistedCorrectionPreservation
import LatticeTwistedTensorField
import LatticeNormalOrderedField

/-! Composition of an arbitrary linear field assignment with the actual
pointwise-polynomial correction exponential. The ramified variable is t,
z=t^2, so correction degree d shifts the coefficient index by 2*d.
The assignment W remains an explicit parameter; this module does not assume
or construct its Jacobi identity. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedCorrectedStateField

open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier LatticeFockMonomialParity
open LatticeTwistedCorrection LatticeTwistedCorrectionPreservation
open scoped BigOperators

abbrev FieldAssignment (o : Fin 12) :=
  LatticeCarrier o →ₗ[ℂ] VertexOperator ℂ (Carrier o)

def stateTerm (o : Fin 12) (W : FieldAssignment o) (k : ℤ) (d : ℕ) :
    LatticeCarrier o →ₗ[ℂ] Module.End ℂ (Carrier o) where
  toFun v := HVertexOperator.coeff (W (correctionExponentialCoefficient o d v))
    (k+2*(d:ℤ))
  map_add' v w := by
    simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply]
  map_smul' c v := by
    simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply, RingHom.id_apply]

theorem stateTerm_zero_of_correction_zero (o : Fin 12) (W : FieldAssignment o)
    (k : ℤ) (d : ℕ) (v : LatticeCarrier o)
    (h : correctionExponentialCoefficient o d v = 0) :
    stateTerm o W k d v = 0 := by
  ext w
  simp [stateTerm, h, HVertexOperator.coeff]

theorem stateTerm_finite (o : Fin 12) (W : FieldAssignment o)
    (k : ℤ) (v : LatticeCarrier o) :
    (Function.support (fun d => stateTerm o W k d v)).Finite := by
  obtain ⟨N,hN⟩ := correctionExponential_polynomial_on_state o v
  apply (Finset.range N).finite_toSet.subset
  intro d hd
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact hd (stateTerm_zero_of_correction_zero o W k d v (hN d (by omega)))

def correctedCoefficient (o : Fin 12) (W : FieldAssignment o) (k : ℤ) :
    LatticeCarrier o →ₗ[ℂ] Module.End ℂ (Carrier o) where
  toFun v := ∑ᶠ d, stateTerm o W k d v
  map_add' v w := by
    simp only [map_add]
    exact finsum_add_distrib (stateTerm_finite o W k v) (stateTerm_finite o W k w)
  map_smul' c v := by
    simp only [map_smul]
    exact (smul_finsum c (fun d => stateTerm o W k d v)).symm

theorem correctedCoefficient_eq_sum (o : Fin 12) (W : FieldAssignment o)
    (k : ℤ) (v : LatticeCarrier o) :
    correctedCoefficient o W k v = ∑ᶠ d,
      HVertexOperator.coeff (W (correctionExponentialCoefficient o d v))
        (k+2*(d:ℤ)) := rfl

theorem field_has_bound (o : Fin 12) (B : VertexOperator ℂ (Carrier o))
    (w : Carrier o) : ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff B k w = 0 := by
  refine ⟨HahnSeries.order ((HahnModule.of ℂ).symm (B w)), ?_⟩
  intro k hk
  exact VertexOperator.coeff_eq_zero_of_lt_order B k w hk

theorem correctedCoefficient_bounded (o : Fin 12) (W : FieldAssignment o)
    (v : LatticeCarrier o) (w : Carrier o) :
    ∃ b : ℤ, ∀ k < b, correctedCoefficient o W k v w = 0 := by
  classical
  obtain ⟨N,hN⟩ := correctionExponential_polynomial_on_state o v
  have hfinite : ∀ d : Fin N, ∃ c : ℤ, ∀ k < c,
      HVertexOperator.coeff (W (correctionExponentialCoefficient o (d:ℕ) v)) k w = 0 :=
    fun _ => field_has_bound o _ w
  choose c hc using hfinite
  let b : ℤ := -(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
    (fun d => (-(c d - 2*(d:ℕ))).toNat)))
  refine ⟨b, ?_⟩
  intro k hk
  have hz : ∀ d : ℕ, stateTerm o W k d v w = 0 := by
    intro d
    by_cases hd : d < N
    · let d' : Fin N := ⟨d,hd⟩
      have hsup : (-(c d' - 2*(d:ℤ))).toNat ≤
          (Finset.univ : Finset (Fin N)).sup
            (fun q => (-(c q - 2*(q:ℕ))).toNat) :=
        Finset.le_sup (f := fun q : Fin N => (-(c q - 2*(q:ℕ))).toNat)
          (Finset.mem_univ d')
      have hlow : k+2*(d:ℤ) < c d' := by
        dsimp only [b] at hk
        simp only [Int.ofNat_eq_coe] at hk
        omega
      exact hc d' _ hlow
    · rw [stateTerm_zero_of_correction_zero o W k d v (hN d (by omega)),
        LinearMap.zero_apply]
  change (∑ᶠ d, stateTerm o W k d v) w = 0
  let ev : Module.End ℂ (Carrier o) →+ Carrier o :=
    { toFun := fun f => f w, map_zero' := rfl, map_add' := fun _ _ => rfl }
  change ev (∑ᶠ d, stateTerm o W k d v) = 0
  rw [ev.map_finsum (stateTerm_finite o W k v)]
  change (∑ᶠ d, stateTerm o W k d v w) = 0
  simp only [hz, finsum_zero]

def correctedField (o : Fin 12) (W : FieldAssignment o) (v : LatticeCarrier o) :
    VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (fun k => correctedCoefficient o W k v)
    (correctedCoefficient_bounded o W v)

theorem correctedField_coefficient (o : Fin 12) (W : FieldAssignment o)
    (v : LatticeCarrier o) (k : ℤ) :
    HVertexOperator.coeff (correctedField o W v) k = correctedCoefficient o W k v := rfl

def correctedAssignment (o : Fin 12) (W : FieldAssignment o) : FieldAssignment o where
  toFun := correctedField o W
  map_add' v w := by
    apply HVertexOperator.coeff_inj
    funext k
    rw [HVertexOperator.coeff_add]
    change correctedCoefficient o W k (v+w) =
      correctedCoefficient o W k v + correctedCoefficient o W k w
    exact map_add _ _ _
  map_smul' c v := by
    apply HVertexOperator.coeff_inj
    funext k
    rw [HVertexOperator.coeff_smul]
    change correctedCoefficient o W k (c • v) = c • correctedCoefficient o W k v
    exact map_smul _ _ _

theorem correctedAssignment_coefficient (o : Fin 12) (W : FieldAssignment o)
    (v : LatticeCarrier o) (k : ℤ) :
    HVertexOperator.coeff (correctedAssignment o W v) k = ∑ᶠ d,
      HVertexOperator.coeff (W (correctionExponentialCoefficient o d v))
        (k+2*(d:ℤ)) := rfl

theorem correctedCoefficient_pure_charge (o : Fin 12) (W : FieldAssignment o)
    (k : ℤ) (x : Lattice o) :
    correctedCoefficient o W k (carrierBasis o (0,x)) =
      HVertexOperator.coeff (W (carrierBasis o (0,x))) k := by
  change (∑ᶠ d, stateTerm o W k d (carrierBasis o (0,x))) = _
  rw [finsum_eq_single _ 0]
  · simp only [stateTerm, LinearMap.coe_mk, AddHom.coe_mk,
      correctionExponential_pure_charge, if_pos rfl, if_true, Nat.cast_zero, mul_zero, add_zero]
  · intro d hd
    apply stateTerm_zero_of_correction_zero
    rw [correctionExponential_pure_charge, if_neg hd]

theorem correctedAssignment_pure_charge (o : Fin 12) (W : FieldAssignment o)
    (x : Lattice o) :
    correctedAssignment o W (carrierBasis o (0,x)) = W (carrierBasis o (0,x)) := by
  apply HVertexOperator.coeff_inj
  funext k
  exact correctedCoefficient_pure_charge o W k x

theorem correctedAssignment_vacuum (o : Fin 12) (W : FieldAssignment o) :
    correctedAssignment o W (vacuum o) = W (vacuum o) := by
  rw [← vacuum_is_empty_monomial]
  exact correctedAssignment_pure_charge o W 0

end HMT.IV.LatticeTwistedCorrectedStateField
end
