import LatticeTwistedPositiveGrading

/-! Local nilpotence of the actual positive-sector L(1). This supplies the
pointwise polynomial exponential used by contragredient coordinate inversion.
It is derived from the existing Virasoro action and positive integer grading;
translation L(-1) is not asserted to be locally nilpotent. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedContragredientTruncation
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading

def lowering (o : Fin 12) : Module.End ℂ (positiveSector o) :=
  positiveConformalMode o 1

theorem energy_lowering_commutator (o : Fin 12) :
    positiveConformalMode o 0 * lowering o -
      lowering o * positiveConformalMode o 0 = -lowering o := by
  have h := positive_virasoro_central_charge_twentyFour o 0 1
  norm_num at h
  change positiveConformalMode o 0 * positiveConformalMode o 1 -
    positiveConformalMode o 1 * positiveConformalMode o 0 =
    -positiveConformalMode o 1
  rw [h]
  exact neg_one_smul ℂ (positiveConformalMode o 1)

theorem lowering_weight (o : Fin 12) (v : positiveSector o) (c : ℂ)
    (hv : positiveConformalMode o 0 v = c • v) :
    positiveConformalMode o 0 (lowering o v) = (c-1) • lowering o v := by
  have h := LinearMap.congr_fun (energy_lowering_commutator o) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.neg_apply,
    hv, map_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem lowering_power_weight (o : Fin 12) (v : positiveSector o) (c : ℂ)
    (hv : positiveConformalMode o 0 v = c • v) (n : ℕ) :
    positiveConformalMode o 0 (((lowering o)^n) v) =
      (c-(n:ℂ)) • (((lowering o)^n) v) := by
  induction n with
  | zero => simpa using hv
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply]
    rw [lowering_weight o _ (c-(n:ℂ)) ih]
    congr 1
    push_cast
    ring

theorem lowering_power_kills_weight (o : Fin 12) (d : ℕ)
    (v : positiveSector o) (hv : v ∈ positiveWeightSpace o d) :
    ((lowering o)^d) v = 0 := by
  have hw := lowering_power_weight o v (d:ℂ)
    (Module.End.mem_eigenspace_iff.mp hv) d
  have hz : ((lowering o)^d) v ∈ positiveWeightSpace o 0 := by
    apply Module.End.mem_eigenspace_iff.mpr
    simpa using hw
  simpa only [positive_weight_zero, Submodule.mem_bot] using hz

def finiteLoweringSpace (o : Fin 12) : Submodule ℂ (positiveSector o) where
  carrier := {v | ∃ n : ℕ, ((lowering o)^n) v = 0}
  zero_mem' := ⟨0, map_zero _⟩
  add_mem' := by
    rintro u v ⟨m, hm⟩ ⟨n, hn⟩
    refine ⟨m+n, ?_⟩
    rw [map_add]
    have hu : ((lowering o)^(m+n)) u = 0 := by
      rw [Nat.add_comm, pow_add, Module.End.mul_apply, hm, map_zero]
    have hv : ((lowering o)^(m+n)) v = 0 := by
      rw [pow_add, Module.End.mul_apply, hn, map_zero]
    rw [hu, hv, add_zero]
  smul_mem' := by
    rintro c v ⟨n, hn⟩
    exact ⟨n, by rw [map_smul, hn, smul_zero]⟩

theorem finiteLoweringSpace_eq_top (o : Fin 12) : finiteLoweringSpace o = ⊤ := by
  apply top_unique
  rw [← positive_weights_span o]
  apply iSup_le
  intro d v hv
  exact ⟨d, lowering_power_kills_weight o d v hv⟩

theorem lowering_locally_nilpotent (o : Fin 12) (v : positiveSector o) :
    ∃ n : ℕ, ((lowering o)^n) v = 0 := by
  have h : v ∈ finiteLoweringSpace o := by rw [finiteLoweringSpace_eq_top]; trivial
  exact h

theorem lowering_power_eventually_zero (o : Fin 12) (v : positiveSector o) :
    ∃ b : ℕ, ∀ n ≥ b, ((lowering o)^n) v = 0 := by
  obtain ⟨b, hb⟩ := lowering_locally_nilpotent o v
  refine ⟨b, fun n hn => ?_⟩
  rw [show n = (n-b)+b by omega, pow_add, Module.End.mul_apply, hb, map_zero]

def inversionCoefficient (o : Fin 12) (n : ℕ) :
    Module.End ℂ (positiveSector o) := (n.factorial:ℂ)⁻¹ • (lowering o)^n

theorem inversionCoefficient_finite (o : Fin 12) (v : positiveSector o) :
    (Function.support (fun n : ℕ => inversionCoefficient o n v)).Finite := by
  obtain ⟨b, hb⟩ := lowering_power_eventually_zero o v
  apply (Finset.range b).finite_toSet.subset
  intro n hn
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra h
  apply hn
  simp only [inversionCoefficient, LinearMap.smul_apply, hb n (by omega), smul_zero]

theorem inversionCoefficient_zero (o : Fin 12) : inversionCoefficient o 0 = 1 := by
  simp [inversionCoefficient]

theorem inversionCoefficient_first (o : Fin 12) :
    inversionCoefficient o 1 = lowering o := by
  simp [inversionCoefficient]

end HMT.IV.LatticeTwistedContragredientTruncation
end

#print axioms HMT.IV.LatticeTwistedContragredientTruncation.lowering_locally_nilpotent
#print axioms HMT.IV.LatticeTwistedContragredientTruncation.inversionCoefficient_finite
