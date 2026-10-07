import LatticeEvenTranslation
import LatticeConformalTranslation
import LatticeVirasoroRelations
import LatticeLowWeightParity

/-! The conformal field of the untwisted fixed carrier is the existing even
state-field of the same quadratic state. Its modes are its actual coefficients.
All operator identities and low-weight facts below are transported through
the injective inclusion; no new normal-product calculation is made. -/

noncomputable section
namespace HMT.IV.LatticeEvenConformal
open LatticeCocycle LatticeOscillatorFock LatticeEvenVertexFields LatticeEvenTranslation
open LatticeConformalState LatticeConformalTranslation LatticeConformalEnergy
open LatticeVirasoroRelations LatticeEnergyGrading LatticeLowWeightParity
open LatticeWeightShells LatticeFullGradedTrace

def evenConformalState (o : Fin 12) : evenSpace o :=
  ⟨conformalState o, conformalState_mem_even o⟩

theorem evenConformalState_coe (o : Fin 12) :
    (evenConformalState o).val = conformalState o := rfl

def evenConformalField (o : Fin 12) : VertexOperator ℂ (evenSpace o) :=
  evenField o (evenConformalState o)

def evenConformalMode (o : Fin 12) (m : ℤ) : Module.End ℂ (evenSpace o) :=
  HVertexOperator.coeff (evenConformalField o) (-m-2)

theorem evenConformalMode_coe (o : Fin 12) (m : ℤ) (u : evenSpace o) :
    (evenConformalMode o m u).val = conformalMode o m u.val := by
  rw [evenConformalMode, evenConformalField, evenField_coefficient, evenCoefficient_coe]
  rfl

theorem even_virasoro_commutator (o : Fin 12) (m n : ℤ) :
    evenConformalMode o m * evenConformalMode o n -
        evenConformalMode o n * evenConformalMode o m =
      ((m-n:ℤ):ℂ) • evenConformalMode o (m+n) +
        (if m+n=0 then ((BasisSize o : ℂ)/12 * ((m:ℂ)^3-(m:ℂ))) •
          (LinearMap.id : Module.End ℂ (evenSpace o)) else 0) := by
  apply LinearMap.ext
  intro u
  apply Subtype.ext
  have h := LinearMap.congr_fun (virasoro_commutator o m n) u.val
  by_cases hmn : m+n=0
  · simpa only [if_pos hmn, LinearMap.sub_apply, Module.End.mul_apply,
      LinearMap.add_apply, LinearMap.smul_apply, LinearMap.id_apply,
      Submodule.coe_sub, Submodule.coe_add, Submodule.coe_smul,
      evenConformalMode_coe] using h
  · simpa only [if_neg hmn, LinearMap.sub_apply, Module.End.mul_apply,
      LinearMap.add_apply, LinearMap.smul_apply, LinearMap.zero_apply,
      Submodule.coe_sub, Submodule.coe_add, Submodule.coe_smul, Submodule.coe_zero,
      evenConformalMode_coe] using h

theorem even_virasoro_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    evenConformalMode o m * evenConformalMode o n -
        evenConformalMode o n * evenConformalMode o m =
      ((m-n:ℤ):ℂ) • evenConformalMode o (m+n) +
        (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
          (LinearMap.id : Module.End ℂ (evenSpace o)) else 0) := by
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  rw [even_virasoro_commutator, hr]
  norm_num

theorem evenConformalMode_neg_one_eq_translation (o : Fin 12) :
    evenConformalMode o (-1) = evenTranslation o := by
  apply LinearMap.ext
  intro u
  apply Subtype.ext
  rw [evenConformalMode_coe, evenTranslation_coe, conformalMode_neg_one_eq_translation]

theorem evenConformalMode_zero_energy (o : Fin 12) (u : evenSpace o) :
    (evenConformalMode o 0 u).val = energy o u.val := by
  rw [evenConformalMode_coe, conformalMode_zero_eq_energy]

theorem evenConformalState_weight_two (o : Fin 12) :
    evenConformalMode o 0 (evenConformalState o) = (2:ℂ) • evenConformalState o := by
  apply Subtype.ext
  rw [evenConformalMode_zero_energy]
  exact conformalState_weight_two o

theorem evenConformalMode_neg_two_vacuum (o : Fin 12) :
    evenConformalMode o (-2) (evenVacuum o) = evenConformalState o := by
  unfold evenConformalMode evenConformalField
  rw [show -(-2:ℤ)-2=0 by omega, evenField_coefficient, evenCoefficient_creates]

theorem evenConformalMode_vacuum (o : Fin 12) (m : ℤ) (hm : -1 ≤ m) :
    evenConformalMode o m (evenVacuum o)=0 := by
  unfold evenConformalMode evenConformalField
  rw [evenField_coefficient]
  exact evenCoefficient_negative_vacuum o _ _ (by omega)

theorem even_eigenspace_eq_comap (o : Fin 12) (c : ℂ) :
    Module.End.eigenspace (evenConformalMode o 0) c =
      (Module.End.eigenspace (energy o) c).comap (evenSpace o).subtype := by
  ext u
  rw [Module.End.mem_eigenspace_iff, Submodule.mem_comap,
    Module.End.mem_eigenspace_iff]
  constructor
  · intro h
    have hc := congrArg Subtype.val h
    simpa only [Submodule.coe_smul, evenConformalMode_zero_energy] using hc
  · intro h
    apply Subtype.ext
    rw [evenConformalMode_zero_energy]
    exact h

theorem even_weight_space (o : Fin 12) (d : ℕ) :
    Module.End.eigenspace (evenConformalMode o 0) (d:ℂ) =
      (fullWeightSpace o d).comap (evenSpace o).subtype := by
  rw [even_eigenspace_eq_comap, fullWeightSpace_eq_eigenspace]

theorem even_weight_zero_vacuum_line (o : Fin 12) :
    Module.End.eigenspace (evenConformalMode o 0) 0 =
      Submodule.span ℂ {evenVacuum o} := by
  rw [even_eigenspace_eq_comap, energy_zero_is_vacuum_line]
  ext u
  simp only [Submodule.mem_comap, Submodule.subtype_apply, Submodule.mem_span_singleton]
  constructor
  · rintro ⟨c,hc⟩
    exact ⟨c, Subtype.ext hc⟩
  · rintro ⟨c,hc⟩
    exact ⟨c, congrArg Subtype.val hc⟩

theorem even_weight_one_zero (o : Fin 12) :
    Module.End.eigenspace (evenConformalMode o 0) 1 = ⊥ := by
  ext u
  rw [Submodule.mem_bot]
  constructor
  · intro hu
    apply Subtype.ext
    apply fixed_weight_one_eq_zero o u.val
    · have he : u.val ∈ Module.End.eigenspace (energy o) 1 := by
        rw [even_eigenspace_eq_comap] at hu
        exact hu
      simpa only [fullWeightSpace_eq_eigenspace, Nat.cast_one] using he
    · exact (mem_evenSpace o u.val).mp u.property
  · rintro rfl
    exact Submodule.zero_mem _

end HMT.IV.LatticeEvenConformal
end

#print axioms HMT.IV.LatticeEvenConformal.evenConformalState
#print axioms HMT.IV.LatticeEvenConformal.evenConformalState_coe
#print axioms HMT.IV.LatticeEvenConformal.evenConformalField
#print axioms HMT.IV.LatticeEvenConformal.evenConformalMode
#print axioms HMT.IV.LatticeEvenConformal.evenConformalMode_coe
#print axioms HMT.IV.LatticeEvenConformal.even_virasoro_commutator
#print axioms HMT.IV.LatticeEvenConformal.even_virasoro_central_charge_twentyFour
#print axioms HMT.IV.LatticeEvenConformal.evenConformalMode_neg_one_eq_translation
#print axioms HMT.IV.LatticeEvenConformal.evenConformalMode_zero_energy
#print axioms HMT.IV.LatticeEvenConformal.evenConformalState_weight_two
#print axioms HMT.IV.LatticeEvenConformal.evenConformalMode_neg_two_vacuum
#print axioms HMT.IV.LatticeEvenConformal.evenConformalMode_vacuum
#print axioms HMT.IV.LatticeEvenConformal.even_eigenspace_eq_comap
#print axioms HMT.IV.LatticeEvenConformal.even_weight_space
#print axioms HMT.IV.LatticeEvenConformal.even_weight_zero_vacuum_line
#print axioms HMT.IV.LatticeEvenConformal.even_weight_one_zero
