import LatticeTwistedParity

/-! The positive fixed sector of the actual twisted carrier. Its description
as the image of the parity projector is proved, and the existing Virasoro
operators restrict to it with their proved central charge. A nonzero vector is
exhibited in the first oscillator layer. No twisted vertex or orbifold product
is assumed by this construction. -/

noncomputable section
namespace HMT.IV.LatticeTwistedPositiveSector
open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFiniteIrreducible
open LatticeTwistedCarrier LatticeTwistedParity LatticeTwistedOscillatorTensor
open LatticeHalfIntegerHeisenberg hiding halfMode

def positiveSector (o : Fin 12) : Submodule ℂ (Carrier o) where
  carrier := {v | liftedTheta o v = v}
  zero_mem' := map_zero _
  add_mem' {a b} ha hb := by
    change liftedTheta o (a+b) = a+b
    rw [map_add, ha, hb]
  smul_mem' c v hv := by
    change liftedTheta o (c • v) = c • v
    rw [map_smul, hv]

theorem mem_positiveSector (o : Fin 12) (v : Carrier o) :
    v ∈ positiveSector o ↔ liftedTheta o v = v := Iff.rfl

theorem evenProjector_fixed_identity (o : Fin 12) (v : Carrier o)
    (hv : v ∈ positiveSector o) : evenProjector o v = v := by
  change (2:ℂ)⁻¹ • (v + liftedTheta o v) = v
  rw [show liftedTheta o v = v from hv]
  module

theorem positiveSector_eq_projector_range (o : Fin 12) :
    positiveSector o = LinearMap.range (evenProjector o) := by
  ext v
  constructor
  · intro hv
    exact ⟨v, evenProjector_fixed_identity o v hv⟩
  · rintro ⟨u, rfl⟩
    exact even_fixed o u

def positiveRangeEquiv (o : Fin 12) :
    positiveSector o ≃ₗ[ℂ] LinearMap.range (evenProjector o) where
  toFun v := ⟨v.val, (positiveSector_eq_projector_range o) ▸ v.property⟩
  invFun v := ⟨v.val, (positiveSector_eq_projector_range o).symm ▸ v.property⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem conformalMode_mem_positive (o : Fin 12) (m : ℤ) (v : Carrier o)
    (hv : v ∈ positiveSector o) : conformalMode o m v ∈ positiveSector o := by
  change liftedTheta o (conformalMode o m v) = conformalMode o m v
  rw [liftedTheta_comm_conformal_apply, show liftedTheta o v = v from hv]

def positiveConformalMode (o : Fin 12) (m : ℤ) :
    Module.End ℂ (positiveSector o) :=
  (conformalMode o m).restrict (fun v hv => conformalMode_mem_positive o m v hv)

theorem positiveConformalMode_coe (o : Fin 12) (m : ℤ) (v : positiveSector o) :
    (positiveConformalMode o m v).val = conformalMode o m v.val := rfl

theorem positive_virasoro_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    positiveConformalMode o m * positiveConformalMode o n -
      positiveConformalMode o n * positiveConformalMode o m =
        ((m-n:ℤ):ℂ) • positiveConformalMode o (m+n) +
          (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
            (LinearMap.id : Module.End ℂ (positiveSector o)) else 0) := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  have h := LinearMap.congr_fun
    (LatticeTwistedCarrier.virasoro_central_charge_twentyFour o m n) v.val
  by_cases hmn : m+n=0
  · simpa only [if_pos hmn, LinearMap.sub_apply, Module.End.mul_apply,
      LinearMap.add_apply, LinearMap.smul_apply, LinearMap.id_apply,
      Submodule.coe_sub, Submodule.coe_add, Submodule.coe_smul,
      positiveConformalMode_coe] using h
  · simpa only [if_neg hmn, LinearMap.sub_apply, Module.End.mul_apply,
      LinearMap.add_apply, LinearMap.smul_apply, LinearMap.zero_apply,
      Submodule.coe_sub, Submodule.coe_add, Submodule.coe_smul, Submodule.coe_zero,
      positiveConformalMode_coe] using h

theorem first_oscillator_mem_positive (o : Fin 12) (i : Fin (BasisSize o))
    (t : FiniteSpace o) : halfMode o i (-1) (groundEmbedding o t) ∈ positiveSector o :=
  first_oscillator_positive o i t

theorem first_oscillator_ne_zero (o : Fin 12) (i : Fin (BasisSize o))
    (t : FiniteSpace o) (ht : t ≠ 0) :
    halfMode o i (-1) (groundEmbedding o t) ≠ 0 := by
  intro hz
  let evaluation : HalfFock o →ₐ[ℂ] ℂ :=
    SymmetricAlgebra.lift (Finsupp.lapply (0,i) : Oscillators o →ₗ[ℂ] ℂ)
  let reader : Carrier o →ₗ[ℂ] FiniteSpace o :=
    (TensorProduct.lid ℂ (FiniteSpace o)).toLinearMap.comp
      (evaluation.toLinearMap.rTensor (FiniteSpace o))
  have hr := congrArg reader hz
  have he : evaluation (create o 0 i 1) = 1 := by
    change evaluation (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o 0 i) * 1) = 1
    simp [evaluation, modeVector]
  apply ht
  change reader (create o 0 i 1 ⊗ₜ[ℂ] t) = reader 0 at hr
  rw [map_zero] at hr
  change evaluation (create o 0 i 1) • t = 0 at hr
  rwa [he, one_smul] at hr

theorem positiveSector_nonzero (o : Fin 12) :
    ∃ v : Carrier o, v ∈ positiveSector o ∧ v ≠ 0 := by
  obtain ⟨t, ht⟩ := exists_ne (0 : FiniteSpace o)
  have hr : BasisSize o = 24 := NeighborRank.witt_marked_integer_rank o
  let i : Fin (BasisSize o) := ⟨0, by rw [hr]; decide⟩
  exact ⟨halfMode o i (-1) (groundEmbedding o t),
    first_oscillator_mem_positive o i t, first_oscillator_ne_zero o i t ht⟩

instance positiveSector_nontrivial (o : Fin 12) : Nontrivial (positiveSector o) := by
  obtain ⟨v, hv, hn⟩ := positiveSector_nonzero o
  exact ⟨⟨⟨v,hv⟩, 0, fun h => hn (congrArg Subtype.val h)⟩⟩

end HMT.IV.LatticeTwistedPositiveSector
end
