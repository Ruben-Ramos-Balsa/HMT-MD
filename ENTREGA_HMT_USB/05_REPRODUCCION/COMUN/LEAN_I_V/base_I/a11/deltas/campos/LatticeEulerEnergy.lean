import LatticeEnergyGrading
import LatticeChargeEnergy
import Mathlib.Algebra.TrivSqZeroExt

/-!
The oscillator Euler operator is constructed as a derivation by the universal
property of the symmetric algebra and a square-zero lift. Its action is first
fixed on oscillator generators by their frequency. The monomial energy and
the decomposition of the already constructed total energy are consequences.
No Virasoro structure or additional operator equality is assumed.
-/

noncomputable section
namespace HMT.IV.LatticeEulerEnergy

open scoped BigOperators TensorProduct
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCocycle HMT.IV.LatticeChargeEnergy
open HMT.IV.LatticeEnergyGrading

def frequency (o : Fin 12) : Module.End ℂ (Oscillators o) :=
  (oscillatorBasis o).constr ℂ fun p =>
    (p.1+1 : ℂ) • oscillatorBasis o p

@[simp] theorem frequency_basis (o : Fin 12) (p : Mode o) :
    frequency o (oscillatorBasis o p) = (p.1+1 : ℂ) • oscillatorBasis o p :=
  Basis.constr_basis _ _ _ _

private def eulerSeed (o : Fin 12) :
    Oscillators o →ₗ[ℂ] TrivSqZeroExt (Fock o) (Fock o) where
  toFun x := (SymmetricAlgebra.ι ℂ (Oscillators o) x,
    SymmetricAlgebra.ι ℂ (Oscillators o) (frequency o x))
  map_add' x y := by ext <;> simp
  map_smul' z x := by
    ext <;> simp [Algebra.smul_def, TrivSqZeroExt.algebraMap_eq_inl']

private def eulerJet (o : Fin 12) : Fock o →ₐ[ℂ] TrivSqZeroExt (Fock o) (Fock o) :=
  SymmetricAlgebra.lift (eulerSeed o)

private theorem eulerJet_fst_hom (o : Fin 12) :
    (TrivSqZeroExt.fstHom ℂ (Fock o) (Fock o)).comp (eulerJet o) =
      AlgHom.id ℂ (Fock o) := by
  apply SymmetricAlgebra.algHom_ext
  ext x
  simp [eulerJet, eulerSeed]

private theorem eulerJet_fst (o : Fin 12) (x : Fock o) : (eulerJet o x).fst = x :=
  AlgHom.congr_fun (eulerJet_fst_hom o) x

def euler (o : Fin 12) : Derivation ℂ (Fock o) (Fock o) where
  toLinearMap := ((TrivSqZeroExt.sndHom (Fock o) (Fock o)).restrictScalars ℂ).comp
    (eulerJet o).toLinearMap
  map_one_eq_zero' := by simp
  leibniz' x y := by
    change (eulerJet o (x*y)).snd = x • (eulerJet o y).snd + y • (eulerJet o x).snd
    simp [map_mul, TrivSqZeroExt.snd_mul, eulerJet_fst, smul_eq_mul,
      op_smul_eq_smul, mul_comm]

@[simp] theorem euler_generator (o : Fin 12) (x : Oscillators o) :
    euler o (SymmetricAlgebra.ι ℂ (Oscillators o) x) =
      SymmetricAlgebra.ι ℂ (Oscillators o) (frequency o x) := by
  change (eulerJet o (SymmetricAlgebra.ι ℂ (Oscillators o) x)).snd = _
  simp [eulerJet, eulerSeed]

@[simp] theorem euler_mode (o : Fin 12) (p : Mode o) :
    euler o (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) =
      (p.1+1 : ℂ) • SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p) := by
  rw [euler_generator, frequency_basis, map_smul]

theorem derivation_homogeneous_power {A : Type*} [CommRing A] [Algebra ℂ A]
    (D : Derivation ℂ A A) (x : A) (c : ℂ) (hx : D x = c • x) (n : ℕ) :
    D (x^n) = (c * (n : ℂ)) • x^n := by
  cases n with
  | zero => simp
  | succ n =>
    rw [D.leibniz_pow, hx]
    simp [Nat.add_sub_cancel, Algebra.smul_def, smul_eq_mul, nsmul_eq_mul,
      map_mul, map_natCast, pow_succ]
    ring

theorem derivation_homogeneous_product {A ι : Type*} [CommRing A] [Algebra ℂ A]
    (D : Derivation ℂ A A) (s : Finset ι) (f : ι → A) (c : ι → ℂ)
    (hf : ∀ i ∈ s, D (f i) = c i • f i) :
    D (∏ i ∈ s, f i) = (∑ i ∈ s, c i) • ∏ i ∈ s, f i := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih =>
    rw [Finset.prod_insert hi, Finset.sum_insert hi, D.leibniz,
      hf i (Finset.mem_insert_self _ _), ih (fun j hj => hf j (Finset.mem_insert_of_mem hj))]
    simp [Algebra.smul_def, smul_eq_mul, map_add]
    ring

theorem euler_monomial (o : Fin 12) (a : Occupation o) :
    euler o (monomialBasis o a) =
      (occupationWeight o a : ℂ) • monomialBasis o a := by
  rw [monomialBasis_product]
  change euler o (∏ p ∈ a.support,
    (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) ^ a p) = _
  have h := derivation_homogeneous_product (euler o) a.support
    (fun p => (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) ^ a p)
    (fun p => (p.1+1 : ℂ) * (a p : ℂ)) (fun p _ =>
      derivation_homogeneous_power (euler o) _ _ (euler_mode o p) (a p))
  rw [h]
  congr 1
  simp only [occupationWeight, Finsupp.sum, Nat.cast_sum, Nat.cast_mul, Nat.cast_add,
    Nat.cast_one]

theorem carrierEuler_basis (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    onCarrier o (euler o).toLinearMap (carrierBasis o (a,x)) =
      (occupationWeight o a : ℂ) • carrierBasis o (a,x) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, onCarrier_pure,
    TensorProduct.smul_tmul']
  change euler o (monomialBasis o a) ⊗ₜ[ℂ] latticeBasisComplex o x = _
  rw [euler_monomial]

theorem energy_eq_euler_plus_charge (o : Fin 12) :
    energy o = onCarrier o (euler o).toLinearMap + onLattice o (chargeEnergy o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [energy_basis, LinearMap.add_apply, carrierEuler_basis,
    carrierChargeEnergy_basis, totalWeight, Nat.cast_add, add_smul]

end HMT.IV.LatticeEulerEnergy
end

#print axioms HMT.IV.LatticeEulerEnergy.frequency_basis
#print axioms HMT.IV.LatticeEulerEnergy.euler_generator
#print axioms HMT.IV.LatticeEulerEnergy.euler_mode
#print axioms HMT.IV.LatticeEulerEnergy.euler_monomial
#print axioms HMT.IV.LatticeEulerEnergy.carrierEuler_basis
#print axioms HMT.IV.LatticeEulerEnergy.energy_eq_euler_plus_charge
