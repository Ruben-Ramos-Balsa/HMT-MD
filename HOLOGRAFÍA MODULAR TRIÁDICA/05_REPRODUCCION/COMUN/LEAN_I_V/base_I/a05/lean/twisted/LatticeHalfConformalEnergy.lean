import LatticeHalfConformalHeisenberg
import LatticeHalfConformalVacuum

/-! Energy commutators of the actual quadratic half-integer modes.
Both summands have total oscillator frequency m. Transport through their
pointwise finite sums gives [Q0,Qm]=-m Qm before any scalar shift. -/

noncomputable section
namespace HMT.IV.LatticeHalfConformalEnergy
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfConformalModes LatticeHalfConformalHeisenberg
open LatticeHalfConformalVacuum LatticeConformalHeisenberg
open scoped BigOperators

theorem half_product_energy (o : Fin 12) (i j : Fin (BasisSize o))
    (a b : ℤ) (v : HalfFock o) :
    quadraticMode o 0 (halfMode o i a (halfMode o j b v)) -
      halfMode o i a (halfMode o j b (quadraticMode o 0 v)) =
        (-(a:ℂ)-(b:ℂ)-1) • halfMode o i a (halfMode o j b v) := by
  have h1 := quadraticMode_half_commutator_apply o i 0 a (halfMode o j b v)
  have h2 := congrArg (halfMode o i a)
    (quadraticMode_half_commutator_apply o j 0 b v)
  simp only [zero_add, map_sub, map_smul] at h1 h2
  calc
    _ = (quadraticMode o 0 (halfMode o i a (halfMode o j b v)) -
        halfMode o i a (quadraticMode o 0 (halfMode o j b v))) +
      (halfMode o i a (quadraticMode o 0 (halfMode o j b v)) -
        halfMode o i a (halfMode o j b (quadraticMode o 0 v))) := by abel
    _ = _ := by rw [h1,h2]; module

theorem creation_half_energy (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) (v : HalfFock o) :
    quadraticMode o 0 (creationHalfTerm o i j m a v) -
      creationHalfTerm o i j m a (quadraticMode o 0 v) =
        (-(m:ℂ)) • creationHalfTerm o i j m a v := by
  have hc : create o a i = halfMode o i (-(a:ℤ)-1) := by
    rw [show -(a:ℤ)-1=Int.negSucc a by omega, halfMode_negSucc]
  simp only [creationHalfTerm, LinearMap.comp_apply, hc]
  rw [half_product_energy]
  congr 1
  push_cast
  ring

theorem annihilation_half_energy (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) (v : HalfFock o) :
    quadraticMode o 0 (annihilationHalfTerm o i j m a v) -
      annihilationHalfTerm o i j m a (quadraticMode o 0 v) =
        (-(m:ℂ)) • annihilationHalfTerm o i j m a v := by
  change quadraticMode o 0 (halfMode o j (m-a-1) (halfMode o i (a:ℤ) v)) -
    halfMode o j (m-a-1) (halfMode o i (a:ℤ) (quadraticMode o 0 v)) = _
  rw [half_product_energy]
  change (-(↑(m-↑a-1):ℂ)-(↑(a:ℤ):ℂ)-1) •
    halfMode o j (m-a-1) (halfMode o i (a:ℤ) v) =
    (-(m:ℂ)) • halfMode o j (m-a-1) (halfMode o i (a:ℤ) v)
  congr 1
  push_cast
  ring

theorem finsum_energy {V : Type*} [AddCommGroup V] [Module ℂ V]
    (f : ℕ → Module.End ℂ V) (hf : ∀ v, (Function.support (fun a => f a v)).Finite)
    (E : Module.End ℂ V) (c : ℂ)
    (he : ∀ a v, E (f a v)-f a (E v)=c • f a v) (v : V) :
    E (∑ᶠ a, f a v) - (∑ᶠ a, f a (E v)) = c • (∑ᶠ a, f a v) := by
  have h := finsum_commutator f hf E v
  have he' (a : ℕ) : f a (E v)-E (f a v)=(-c) • f a v := by
    rw [← neg_sub, he, neg_smul]
  simp only [he'] at h
  have hs : (∑ᶠ a, (-c) • f a v) = (-c) • (∑ᶠ a, f a v) :=
    ((DistribMulAction.toAddMonoidHom V (-c)).map_finsum (hf v)).symm
  rw [hs] at h
  rw [← neg_sub, h, neg_smul, neg_neg]

theorem halfNormalMode_energy (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (v : HalfFock o) :
    quadraticMode o 0 (halfNormalMode o i j m v) -
      halfNormalMode o i j m (quadraticMode o 0 v) =
        (-(m:ℂ)) • halfNormalMode o i j m v := by
  simp only [halfNormalMode_apply, map_add]
  rw [show quadraticMode o 0 (∑ᶠ a, creationHalfTerm o i j m a v) +
      quadraticMode o 0 (∑ᶠ a, annihilationHalfTerm o i j m a v) -
      ((∑ᶠ a, creationHalfTerm o i j m a (quadraticMode o 0 v)) +
       (∑ᶠ a, annihilationHalfTerm o i j m a (quadraticMode o 0 v))) =
      (quadraticMode o 0 (∑ᶠ a, creationHalfTerm o i j m a v) -
       (∑ᶠ a, creationHalfTerm o i j m a (quadraticMode o 0 v))) +
      (quadraticMode o 0 (∑ᶠ a, annihilationHalfTerm o i j m a v) -
       (∑ᶠ a, annihilationHalfTerm o i j m a (quadraticMode o 0 v))) by abel]
  rw [finsum_energy _ (creationHalfTerm_finite o i j m) _ _ (creation_half_energy o i j m),
    finsum_energy _ (annihilationHalfTerm_finite o i j m) _ _ (annihilation_half_energy o i j m)]
  rw [smul_add]

theorem quadratic_energy_comm_apply (o : Fin 12) (m : ℤ) (v : HalfFock o) :
    quadraticMode o 0 (quadraticMode o m v)-quadraticMode o m (quadraticMode o 0 v) =
      (-(m:ℂ)) • quadraticMode o m v := by
  simp only [quadraticMode_apply o m]
  have h : quadraticMode o 0
      ((2:ℂ)⁻¹ • ∑ i, ∑ j, LatticeGramDual.gramInv o i j • halfNormalMode o i j m v) -
      ((2:ℂ)⁻¹ • ∑ i, ∑ j, LatticeGramDual.gramInv o i j •
        halfNormalMode o i j m (quadraticMode o 0 v)) =
      (2:ℂ)⁻¹ • ∑ i, ∑ j, LatticeGramDual.gramInv o i j •
        (quadraticMode o 0 (halfNormalMode o i j m v) -
          halfNormalMode o i j m (quadraticMode o 0 v)) := by
    simp only [map_smul, map_sum, smul_sub, Finset.sum_sub_distrib]
  rw [h]
  simp only [halfNormalMode_energy]
  simp only [Finset.smul_sum, smul_comm (-(m:ℂ))]

theorem quadratic_energy_comm (o : Fin 12) (m : ℤ) :
    quadraticMode o 0 * quadraticMode o m - quadraticMode o m * quadraticMode o 0 =
      (-(m:ℂ)) • quadraticMode o m := by
  apply LinearMap.ext
  exact quadratic_energy_comm_apply o m

theorem shifted_energy_comm (o : Fin 12) (c : ℂ) (m : ℤ) :
    shiftedQuadraticMode o c 0 * shiftedQuadraticMode o c m -
      shiftedQuadraticMode o c m * shiftedQuadraticMode o c 0 =
        (-(m:ℂ)) • shiftedQuadraticMode o c m := by
  by_cases hm : m=0
  · subst m
    simp only [sub_self, Int.cast_zero, neg_zero, zero_smul]
  · simp only [shiftedQuadraticMode, if_pos rfl, if_true, if_neg hm, add_zero]
    have h := quadratic_energy_comm o m
    apply LinearMap.ext
    intro v
    have hv := LinearMap.congr_fun h v
    simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
      LinearMap.smul_apply, LinearMap.id_apply, map_add, map_smul]
    simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at hv
    linear_combination hv

end HMT.IV.LatticeHalfConformalEnergy
end

#print axioms HMT.IV.LatticeHalfConformalEnergy.half_product_energy
#print axioms HMT.IV.LatticeHalfConformalEnergy.creation_half_energy
#print axioms HMT.IV.LatticeHalfConformalEnergy.annihilation_half_energy
#print axioms HMT.IV.LatticeHalfConformalEnergy.finsum_energy
#print axioms HMT.IV.LatticeHalfConformalEnergy.halfNormalMode_energy
#print axioms HMT.IV.LatticeHalfConformalEnergy.quadratic_energy_comm_apply
#print axioms HMT.IV.LatticeHalfConformalEnergy.quadratic_energy_comm
#print axioms HMT.IV.LatticeHalfConformalEnergy.shifted_energy_comm
