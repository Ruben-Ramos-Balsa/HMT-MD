import FiniteWeyl
import Mathlib.Analysis.InnerProductSpace.l2Space

/-!
Hilbert-space realization of the already constructed exchange of the two
integer publications. The pointwise identity of FiniteWeyl is lifted to
ell-two together with the full weighted operator domain. No finite-support
restriction is used in the domain transport.
-/
noncomputable section
namespace HMT.IV.HilbertTDuality

open FiniteWeyl.Duality
open scoped ENNReal

abbrev State := lp (fun _ : ℤ × ℤ => ℂ) 2

theorem memlp_swap (f : WaveFunction) :
    Memℓp (swapFunction f) 2 ↔ Memℓp f 2 := by
  rw [memℓp_gen_iff (by norm_num : (0 : ℝ) < (2 : ℝ≥0∞).toReal),
      memℓp_gen_iff (by norm_num : (0 : ℝ) < (2 : ℝ≥0∞).toReal)]
  exact (Equiv.prodComm ℤ ℤ).summable_iff
    (f := fun v : ℤ × ℤ => ‖f v‖ ^ (2 : ℝ≥0∞).toReal)

def exchange (f : State) : State :=
  ⟨swapFunction f, (memlp_swap f).mpr f.property⟩

theorem exchange_apply (f : State) (v : ℤ × ℤ) :
    exchange f v = f v.swap := rfl

theorem exchange_involutive : Function.Involutive exchange := by
  intro f
  apply lp.ext
  exact swapFunction_involutive f

theorem exchange_norm (f : State) : ‖exchange f‖ = ‖f‖ := by
  rw [lp.norm_eq_tsum_rpow (by norm_num : (0 : ℝ) < (2 : ℝ≥0∞).toReal),
      lp.norm_eq_tsum_rpow (by norm_num : (0 : ℝ) < (2 : ℝ≥0∞).toReal)]
  congr 1
  exact (Equiv.prodComm ℤ ℤ).tsum_eq (fun v => ‖f v‖ ^ (2 : ℝ≥0∞).toReal)

def exchangeIsometry : State ≃ₗᵢ[ℂ] State where
  toFun := exchange
  invFun := exchange
  left_inv := exchange_involutive
  right_inv := exchange_involutive
  map_add' f g := by apply lp.ext; rfl
  map_smul' c f := by apply lp.ext; rfl
  norm_map' := exchange_norm

def InDomain (r : ℝ) (f : State) : Prop :=
  Memℓp (multiplyEnergy r f) 2

theorem domain_exchange_iff (r : ℝ) (f : State) :
    InDomain r⁻¹ (exchange f) ↔ InDomain r f := by
  unfold InDomain
  have h : multiplyEnergy r⁻¹ (exchange f) =
      swapFunction (multiplyEnergy r f) := by
    have hc := pointwise_conjugation r (swapFunction f)
    rw [swapFunction_involutive] at hc
    exact hc.symm
  rw [h]
  exact memlp_swap (multiplyEnergy r f)

def operatorDomain (r : ℝ) : Submodule ℂ State where
  carrier := {f | InDomain r f}
  zero_mem' := by
    change Memℓp (fun v => (energyAt r v : ℂ) * 0) 2
    simpa using (zero_mem_ℓp' (E := fun _ : ℤ × ℤ => ℂ) (p := 2))
  add_mem' := by
    intro f g hf hg
    change Memℓp (multiplyEnergy r (f + g)) 2
    convert hf.add hg using 1
    funext v
    simp [multiplyEnergy, mul_add]
  smul_mem' := by
    intro c f hf
    change Memℓp (multiplyEnergy r (c • f)) 2
    convert hf.const_smul c using 1
    funext v
    simp [multiplyEnergy]
    ring

def hamiltonian (r : ℝ) : operatorDomain r →ₗ[ℂ] State where
  toFun f := ⟨multiplyEnergy r f.val, f.property⟩
  map_add' f g := by
    apply lp.ext
    funext v
    simp [multiplyEnergy, mul_add]
  map_smul' c f := by
    apply lp.ext
    funext v
    simp [multiplyEnergy]
    ring

def exchangeDomain (r : ℝ) : operatorDomain r ≃ₗ[ℂ] operatorDomain r⁻¹ where
  toFun f := ⟨exchange f.val, (domain_exchange_iff r f.val).mpr f.property⟩
  invFun f := ⟨exchange f.val, by
    have h := (domain_exchange_iff r⁻¹ f.val).mpr f.property
    simpa using h⟩
  left_inv f := by apply Subtype.ext; exact exchange_involutive f.val
  right_inv f := by apply Subtype.ext; exact exchange_involutive f.val
  map_add' f g := by apply Subtype.ext; apply lp.ext; rfl
  map_smul' c f := by apply Subtype.ext; apply lp.ext; rfl

theorem hamiltonian_intertwining (r : ℝ) (f : operatorDomain r) :
    hamiltonian r⁻¹ (exchangeDomain r f) = exchangeIsometry (hamiltonian r f) := by
  apply lp.ext
  funext v
  change (energyAt r⁻¹ v : ℂ) * f.val v.swap =
    (energyAt r v.swap : ℂ) * f.val v.swap
  have h := energyAt_swap_inv r v.swap
  simpa using congrArg (fun a : ℝ => (a : ℂ) * f.val v.swap) h

theorem energy_nonnegative (r : ℝ) (v : ℤ × ℤ) : 0 ≤ energyAt r v := by
  unfold energyAt
  positivity

theorem domain_iff_weighted_summable (r : ℝ) (f : State) :
    InDomain r f ↔ Summable (fun v => energyAt r v ^ 2 * ‖f v‖ ^ 2) := by
  unfold InDomain
  rw [memℓp_gen_iff (by norm_num : (0 : ℝ) < (2 : ℝ≥0∞).toReal)]
  simp only [ENNReal.toReal_ofNat, Real.rpow_two, multiplyEnergy, norm_mul,
    Complex.norm_real, Real.norm_eq_abs, mul_pow, sq_abs]

def InFormDomain (r : ℝ) (f : State) : Prop :=
  Summable (fun v => energyAt r v * ‖f v‖ ^ 2)

theorem form_domain_exchange_iff (r : ℝ) (f : State) :
    InFormDomain r⁻¹ (exchange f) ↔ InFormDomain r f := by
  unfold InFormDomain
  have h : (fun v => energyAt r⁻¹ v * ‖exchange f v‖ ^ 2) =
      (fun v => energyAt r v * ‖f v‖ ^ 2) ∘ Equiv.prodComm ℤ ℤ := by
    funext v
    have he : energyAt r⁻¹ v = energyAt r v.swap := by
      simpa using energyAt_swap_inv r v.swap
    simp only [Function.comp_apply, Equiv.prodComm_apply, exchange_apply, he]
  rw [h]
  exact (Equiv.prodComm ℤ ℤ).summable_iff

theorem single_in_domain (r : ℝ) (v : ℤ × ℤ) (a : ℂ) :
    InDomain r (lp.single 2 v a) := by
  unfold InDomain
  have h : multiplyEnergy r (lp.single 2 v a) =
      (lp.single 2 v ((energyAt r v : ℂ) * a) : State) := by
    funext u
    by_cases hu : u = v
    · subst u
      simp [multiplyEnergy, lp.single_apply_self]
    · simp [multiplyEnergy, lp.single_apply, Pi.single_eq_of_ne hu]
  rw [h]
  exact (lp.single 2 v ((energyAt r v : ℂ) * a) : State).property

theorem operator_domain_dense (r : ℝ) : Dense (operatorDomain r : Set State) := by
  intro f
  apply mem_closure_of_tendsto (lp.hasSum_single (by norm_num : (2 : ℝ≥0∞) ≠ ⊤) f)
  apply Filter.Eventually.of_forall
  intro s
  exact (operatorDomain r).sum_mem (fun v _ => single_in_domain r v (f v))

#print axioms memlp_swap
#print axioms exchange_involutive
#print axioms exchange_norm
#print axioms exchangeIsometry
#print axioms domain_exchange_iff
#print axioms operatorDomain
#print axioms hamiltonian
#print axioms exchangeDomain
#print axioms hamiltonian_intertwining
#print axioms energy_nonnegative
#print axioms domain_iff_weighted_summable
#print axioms form_domain_exchange_iff
#print axioms single_in_domain
#print axioms operator_domain_dense

end HMT.IV.HilbertTDuality
end
