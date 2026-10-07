import LatticeTwistedPositiveSector
import LatticeTwistedLowWeights
import LatticeEvenGrading

/-! The two actual positive sectors are assembled as a direct sum, together
with their existing conformal actions. Vacuum and weight-one statements are
proved for this carrier. No multiplication between the sectors is inferred
from a direct sum: this file does not declare an orbifold vertex algebra. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeOrbifoldCarrier
open LatticeEvenVertexFields LatticeEvenConformal
open LatticeTwistedPositiveSector

abbrev Space (o : Fin 12) := evenSpace o × positiveSector o

def modes (o : Fin 12) (m : ℤ) : Module.End ℂ (Space o) :=
  (evenConformalMode o m).prodMap (positiveConformalMode o m)

@[simp] theorem modes_apply (o : Fin 12) (m : ℤ) (v : Space o) :
    modes o m v = (evenConformalMode o m v.1, positiveConformalMode o m v.2) := rfl

def vacuum (o : Fin 12) : Space o := (evenVacuum o, 0)

def conformalState (o : Fin 12) : Space o := (evenConformalState o, 0)

theorem virasoro_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    modes o m * modes o n - modes o n * modes o m =
      ((m-n:ℤ):ℂ) • modes o (m+n) +
        (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
          (LinearMap.id : Module.End ℂ (Space o)) else 0) := by
  apply LinearMap.ext
  intro v
  have he := LinearMap.congr_fun (even_virasoro_central_charge_twentyFour o m n) v.1
  have ht := LinearMap.congr_fun (positive_virasoro_central_charge_twentyFour o m n) v.2
  apply Prod.ext
  · by_cases hmn : m+n=0
    · simpa only [if_pos hmn, LinearMap.sub_apply, Module.End.mul_apply,
        LinearMap.add_apply, LinearMap.smul_apply, LinearMap.id_apply, modes_apply,
        Prod.fst_sub, Prod.fst_add, Prod.smul_fst] using he
    · simpa only [if_neg hmn, LinearMap.sub_apply, Module.End.mul_apply,
        LinearMap.add_apply, LinearMap.smul_apply, LinearMap.zero_apply, modes_apply,
        Prod.fst_sub, Prod.fst_add, Prod.smul_fst, Prod.fst_zero] using he
  · by_cases hmn : m+n=0
    · simpa only [if_pos hmn, LinearMap.sub_apply, Module.End.mul_apply,
        LinearMap.add_apply, LinearMap.smul_apply, LinearMap.id_apply, modes_apply,
        Prod.snd_sub, Prod.snd_add, Prod.smul_snd] using ht
    · simpa only [if_neg hmn, LinearMap.sub_apply, Module.End.mul_apply,
        LinearMap.add_apply, LinearMap.smul_apply, LinearMap.zero_apply, modes_apply,
        Prod.snd_sub, Prod.snd_add, Prod.smul_snd, Prod.snd_zero] using ht

theorem modes_vacuum (o : Fin 12) (m : ℤ) (hm : -1 ≤ m) :
    modes o m (vacuum o) = 0 := by
  simp only [vacuum, modes_apply, map_zero, evenConformalMode_vacuum o m hm]
  rfl

theorem modes_create_conformalState (o : Fin 12) :
    modes o (-2) (vacuum o) = conformalState o := by
  simp only [vacuum, conformalState, modes_apply, map_zero, evenConformalMode_neg_two_vacuum]

theorem conformalState_weight_two (o : Fin 12) :
    modes o 0 (conformalState o) = (2:ℂ) • conformalState o := by
  simp only [conformalState, modes_apply, map_zero, evenConformalState_weight_two,
    Prod.smul_mk, smul_zero]

theorem eigenspace_components (o : Fin 12) (c : ℂ) (v : Space o) :
    v ∈ Module.End.eigenspace (modes o 0) c ↔
      v.1 ∈ Module.End.eigenspace (evenConformalMode o 0) c ∧
      v.2 ∈ Module.End.eigenspace (positiveConformalMode o 0) c := by
  rcases v with ⟨a,b⟩
  simp only [Module.End.mem_eigenspace_iff, modes_apply, Prod.smul_mk, Prod.mk.injEq]

theorem twisted_low_eigenvector_zero (o : Fin 12) (v : positiveSector o)
    (e : ℕ) (he : e≤1) (hv : positiveConformalMode o 0 v = (e:ℂ) • v) : v=0 := by
  apply Subtype.ext
  apply LatticeTwistedLowWeights.low_weight_vector_zero o v.val e he
  exact congrArg Subtype.val hv

theorem weight_one_zero (o : Fin 12) :
    Module.End.eigenspace (modes o 0) (1:ℂ) = ⊥ := by
  apply le_antisymm _ bot_le
  intro v hv
  apply (Submodule.mem_bot ℂ).mpr
  rcases (eigenspace_components o 1 v).mp hv with ⟨he,ht⟩
  apply Prod.ext
  · simpa only [even_weight_one_zero, Submodule.mem_bot] using he
  · apply twisted_low_eigenvector_zero o v.2 1 (by omega)
    simpa using Module.End.mem_eigenspace_iff.mp ht

theorem weight_zero_vacuum_line (o : Fin 12) :
    Module.End.eigenspace (modes o 0) (0:ℂ) = Submodule.span ℂ {vacuum o} := by
  ext v
  constructor
  · intro hv
    rcases (eigenspace_components o 0 v).mp hv with ⟨he,ht⟩
    rw [even_weight_zero_vacuum_line, Submodule.mem_span_singleton] at he
    obtain ⟨c,hc⟩ := he
    have hz : v.2=0 := twisted_low_eigenvector_zero o v.2 0 (by omega)
      (by simpa using Module.End.mem_eigenspace_iff.mp ht)
    rw [Submodule.mem_span_singleton]
    refine ⟨c, ?_⟩
    apply Prod.ext
    · exact hc
    · simpa [vacuum] using hz.symm
  · rw [Submodule.mem_span_singleton]
    rintro ⟨c, rfl⟩
    apply Module.End.mem_eigenspace_iff.mpr
    simp [map_smul, modes_vacuum o 0 (by omega)]

end HMT.IV.LatticeOrbifoldCarrier
end
