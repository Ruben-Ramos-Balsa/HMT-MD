import LatticeStateFieldParity

/-!
The fixed subspace of the existing lattice involution is stable under every
coefficient of its own state-fields. More generally, homogeneous parities
multiply. The restriction uses the actual state-field map and the existing
even projector; it is the untwisted fixed space, not an orbifold or a twisted
sector. No choice of an additional carrier or product is made.
-/

noncomputable section
namespace HMT.IV.LatticeEvenVertexFields

open LatticeOscillatorFock LatticeParityCarrier LatticeStateFieldMap
open LatticeStateFieldParity

def paritySpace (o : Fin 12) (s : ℂ) : Submodule ℂ (LatticeCarrier o) :=
  LinearMap.ker (carrierTheta o - s • LinearMap.id)

theorem mem_paritySpace (o : Fin 12) (s : ℂ) (v : LatticeCarrier o) :
    v ∈ paritySpace o s ↔ carrierTheta o v = s • v := by
  simp only [paritySpace, LinearMap.mem_ker, LinearMap.sub_apply,
    LinearMap.smul_apply, LinearMap.id_apply, sub_eq_zero]

def evenSpace (o : Fin 12) : Submodule ℂ (LatticeCarrier o) := paritySpace o 1

theorem mem_evenSpace (o : Fin 12) (v : LatticeCarrier o) :
    v ∈ evenSpace o ↔ carrierTheta o v = v := by
  simp only [evenSpace, mem_paritySpace, one_smul]

theorem evenProjector_mem (o : Fin 12) (v : LatticeCarrier o) :
    evenProjector o v ∈ evenSpace o :=
  (mem_evenSpace o _).2 (even_fixed o v)

theorem evenProjector_eq_self (o : Fin 12) (v : LatticeCarrier o)
    (hv : v ∈ evenSpace o) : evenProjector o v = v := by
  have h := (mem_evenSpace o v).1 hv
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply, h]
  module

theorem evenSpace_eq_range (o : Fin 12) :
    evenSpace o = LinearMap.range (evenProjector o) := by
  ext v
  constructor
  · intro hv
    exact ⟨v, evenProjector_eq_self o v hv⟩
  · rintro ⟨w, rfl⟩
    exact evenProjector_mem o w

theorem stateField_coefficient_parity (o : Fin 12) (s t : ℂ)
    (u v : LatticeCarrier o)
    (hu : carrierTheta o u = s • u) (hv : carrierTheta o v = t • v) (k : ℤ) :
    carrierTheta o (HVertexOperator.coeff (stateField o u) k v) =
      (s*t) • HVertexOperator.coeff (stateField o u) k v := by
  rw [theta_stateField_apply, hu, hv, map_smul]
  simp only [HVertexOperator.coeff_smul, Pi.smul_apply,
    LinearMap.smul_apply, map_smul, smul_smul]
  rw [mul_comm t s]

theorem stateField_coefficient_mem_parity (o : Fin 12) (s t : ℂ)
    (u v : LatticeCarrier o) (hu : u ∈ paritySpace o s)
    (hv : v ∈ paritySpace o t) (k : ℤ) :
    HVertexOperator.coeff (stateField o u) k v ∈ paritySpace o (s*t) :=
  (mem_paritySpace o _ _).2
    (stateField_coefficient_parity o s t u v
      ((mem_paritySpace o _ _).1 hu) ((mem_paritySpace o _ _).1 hv) k)

theorem stateField_coefficient_even (o : Fin 12) (u v : LatticeCarrier o)
    (hu : u ∈ evenSpace o) (hv : v ∈ evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (stateField o u) k v ∈ evenSpace o := by
  simpa only [one_mul] using stateField_coefficient_mem_parity o 1 1 u v hu hv k

theorem vacuum_mem_evenSpace (o : Fin 12) : vacuum o ∈ evenSpace o :=
  (mem_evenSpace o _).2 (carrierTheta_vacuum o)

def evenVacuum (o : Fin 12) : evenSpace o := ⟨vacuum o, vacuum_mem_evenSpace o⟩

/-- Each coefficient is an actual endomorphism of the same fixed subspace. -/
def evenCoefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    Module.End ℂ (evenSpace o) where
  toFun v := ⟨HVertexOperator.coeff (stateField o u.val) k v.val,
    stateField_coefficient_even o u.val v.val u.property v.property k⟩
  map_add' v w := by apply Subtype.ext; exact map_add _ _ _
  map_smul' c v := by apply Subtype.ext; exact map_smul _ _ _

theorem evenCoefficient_coe (o : Fin 12) (u v : evenSpace o) (k : ℤ) :
    (evenCoefficient o u k v).val =
      HVertexOperator.coeff (stateField o u.val) k v.val := rfl

theorem evenCoefficient_vacuum (o : Fin 12) (k : ℤ) :
    evenCoefficient o (evenVacuum o) k =
      if k=0 then (LinearMap.id : Module.End ℂ (evenSpace o)) else 0 := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  simp only [evenCoefficient_coe, evenVacuum, stateField_vacuum_coefficient]
  split_ifs <;> rfl

theorem evenCoefficient_creates (o : Fin 12) (u : evenSpace o) :
    evenCoefficient o u 0 (evenVacuum o) = u := by
  apply Subtype.ext
  exact (stateField_creates o u.val).2

theorem evenCoefficient_negative_vacuum (o : Fin 12) (u : evenSpace o)
    (k : ℤ) (hk : k < 0) : evenCoefficient o u k (evenVacuum o) = 0 := by
  apply Subtype.ext
  exact (stateField_creates o u.val).1 k hk

theorem evenCoefficient_laurent_bound (o : Fin 12) (u v : evenSpace o) :
    ∃ b : ℤ, ∀ k < b, evenCoefficient o u k v = 0 := by
  obtain ⟨b,hb⟩ := stateField_laurent_bound o u.val v.val
  refine ⟨b, fun k hk => ?_⟩
  apply Subtype.ext
  exact hb k hk

end HMT.IV.LatticeEvenVertexFields
end
