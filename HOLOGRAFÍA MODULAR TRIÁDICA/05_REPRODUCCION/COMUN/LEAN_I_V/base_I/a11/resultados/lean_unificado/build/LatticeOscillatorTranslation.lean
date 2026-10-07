import LatticeEulerEnergy
import Mathlib.RingTheory.Derivation.Lie

/-!
The oscillator part of translation on the existing symmetric Fock algebra.
A frequency n+1 generator is sent to (n+1) times the frequency n+2 generator.
Its extension is an actual derivation constructed by the universal property,
not an operator specified by a desired energy commutator. The lift here acts
only on oscillators. Full charged-state translation and Virasoro relations
are not claimed by this module.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeOscillatorTranslation

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeEulerEnergy HMT.IV.LatticeEnergyGrading
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeChargeEnergy HMT.IV.LatticeParityCarrier
open HMT.FockTransport.Symmetric
open scoped TensorProduct

def shiftFrequency (o : Fin 12) : Module.End ℂ (Oscillators o) :=
  (oscillatorBasis o).constr ℂ fun p =>
    (p.1+1 : ℂ) • oscillatorBasis o (p.1+1,p.2)

@[simp] theorem shiftFrequency_basis (o : Fin 12) (p : Mode o) :
    shiftFrequency o (oscillatorBasis o p) =
      (p.1+1 : ℂ) • oscillatorBasis o (p.1+1,p.2) :=
  Basis.constr_basis _ _ _ _

private def translationSeed (o : Fin 12) :
    Oscillators o →ₗ[ℂ] TrivSqZeroExt (Fock o) (Fock o) where
  toFun x := (SymmetricAlgebra.ι ℂ (Oscillators o) x,
    SymmetricAlgebra.ι ℂ (Oscillators o) (shiftFrequency o x))
  map_add' x y := by ext <;> simp
  map_smul' z x := by
    ext <;> simp [Algebra.smul_def, TrivSqZeroExt.algebraMap_eq_inl']

private def translationJet (o : Fin 12) :
    Fock o →ₐ[ℂ] TrivSqZeroExt (Fock o) (Fock o) :=
  SymmetricAlgebra.lift (translationSeed o)

private theorem translationJet_fst_hom (o : Fin 12) :
    (TrivSqZeroExt.fstHom ℂ (Fock o) (Fock o)).comp (translationJet o) =
      AlgHom.id ℂ (Fock o) := by
  apply SymmetricAlgebra.algHom_ext
  ext x
  simp [translationJet, translationSeed]

private theorem translationJet_fst (o : Fin 12) (x : Fock o) :
    (translationJet o x).fst = x :=
  AlgHom.congr_fun (translationJet_fst_hom o) x

def translation (o : Fin 12) : Derivation ℂ (Fock o) (Fock o) where
  toLinearMap := ((TrivSqZeroExt.sndHom (Fock o) (Fock o)).restrictScalars ℂ).comp
    (translationJet o).toLinearMap
  map_one_eq_zero' := by simp
  leibniz' x y := by
    change (translationJet o (x*y)).snd =
      x • (translationJet o y).snd + y • (translationJet o x).snd
    simp [map_mul, TrivSqZeroExt.snd_mul, translationJet_fst, smul_eq_mul,
      op_smul_eq_smul, mul_comm]

@[simp] theorem translation_generator (o : Fin 12) (v : Oscillators o) :
    translation o (SymmetricAlgebra.ι ℂ (Oscillators o) v) =
      SymmetricAlgebra.ι ℂ (Oscillators o) (shiftFrequency o v) := by
  change (translationJet o (SymmetricAlgebra.ι ℂ (Oscillators o) v)).snd = _
  simp [translationJet, translationSeed]

@[simp] theorem translation_mode (o : Fin 12) (p : Mode o) :
    translation o (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) =
      (p.1+1 : ℂ) •
        SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o (p.1+1,p.2)) := by
  rw [translation_generator, shiftFrequency_basis, map_smul]

theorem derivation_ext_generators (o : Fin 12)
    (D F : Derivation ℂ (Fock o) (Fock o))
    (h : ∀ v, D (SymmetricAlgebra.ι ℂ (Oscillators o) v) =
      F (SymmetricAlgebra.ι ℂ (Oscillators o) v)) : D = F := by
  ext v
  induction v using SymmetricAlgebra.induction with
  | algebraMap z => simp
  | ι x => exact h x
  | mul x y hx hy => rw [D.leibniz, F.leibniz, hx, hy]
  | add x y hx hy => rw [map_add, map_add, hx, hy]

theorem euler_translation_bracket (o : Fin 12) :
    ⁅euler o, translation o⁆ = translation o := by
  apply derivation_ext_generators
  have hg : (⁅euler o, translation o⁆.toLinearMap).comp
      (SymmetricAlgebra.ι ℂ (Oscillators o)) =
      (translation o).toLinearMap.comp (SymmetricAlgebra.ι ℂ (Oscillators o)) := by
    apply (oscillatorBasis o).ext
    intro p
    change euler o (translation o (SymmetricAlgebra.ι ℂ (Oscillators o)
      (oscillatorBasis o p))) -
      translation o (euler o (SymmetricAlgebra.ι ℂ (Oscillators o)
        (oscillatorBasis o p))) = _
    change euler o (translation o (SymmetricAlgebra.ι ℂ (Oscillators o)
      (oscillatorBasis o p))) - translation o (euler o
      (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p))) =
      translation o (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p))
    simp only [translation_mode, euler_mode, Derivation.map_smul, smul_smul]
    rw [← sub_smul]
    congr 1
    push_cast
    ring
  exact fun v => LinearMap.congr_fun hg v

theorem translation_raises_energy (o : Fin 12) (v : Fock o) :
    euler o (translation o v) = translation o (euler o v) + translation o v := by
  have h := congrArg (fun D : Derivation ℂ (Fock o) (Fock o) => D v)
    (euler_translation_bracket o)
  dsimp only at h
  rw [Derivation.commutator_apply, sub_eq_iff_eq_add] at h
  simpa only [add_comm] using h

theorem translation_create (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (v : Fock o) :
    translation o (create o n i v) = create o n i (translation o v) +
      (n+1 : ℂ) • create o (n+1) i v := by
  change translation o (SymmetricAlgebra.ι ℂ (Oscillators o)
    (oscillatorBasis o (n,i)) * v) = _
  rw [(translation o).leibniz, translation_mode]
  change _ = SymmetricAlgebra.ι ℂ (Oscillators o)
    (oscillatorBasis o (n,i)) * translation o v +
      (n+1 : ℂ) • (SymmetricAlgebra.ι ℂ (Oscillators o)
        (oscillatorBasis o (n+1,i)) * v)
  simp only [smul_eq_mul, Algebra.smul_def]
  ring

theorem translation_theta (o : Fin 12) (v : Fock o) :
    translation o (fockTheta o v) = fockTheta o (translation o v) := by
  induction v using SymmetricAlgebra.induction with
  | algebraMap z => simp
  | ι x => simp
  | mul x y hx hy =>
    simp only [map_mul, (translation o).leibniz, hx, hy, smul_eq_mul, map_add]
  | add x y hx hy => simp only [map_add, hx, hy]

def carrierTranslation (o : Fin 12) : Module.End ℂ (LatticeCarrier o) :=
  onCarrier o (translation o).toLinearMap

theorem carrierTranslation_vacuum (o : Fin 12) :
    carrierTranslation o (vacuum o) = 0 := by
  simp [carrierTranslation, vacuum]

theorem energy_pure_general (o : Fin 12) (v : Fock o) (a : TwistedAlgebra o) :
    energy o (v ⊗ₜ[ℂ] a) =
      euler o v ⊗ₜ[ℂ] a + v ⊗ₜ[ℂ] chargeEnergy o a := by
  rw [energy_eq_euler_plus_charge, LinearMap.add_apply, onCarrier_pure,
    onLattice_pure]
  rfl

theorem carrierTranslation_energy (o : Fin 12) (v : LatticeCarrier o) :
    energy o (carrierTranslation o v) - carrierTranslation o (energy o v) =
      carrierTranslation o v := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    rw [carrierTranslation, onCarrier_pure, energy_pure_general,
      energy_pure_general, map_add, onCarrier_pure, onCarrier_pure]
    change (euler o (translation o v) ⊗ₜ[ℂ] a +
      translation o v ⊗ₜ[ℂ] chargeEnergy o a) -
      (translation o (euler o v) ⊗ₜ[ℂ] a +
        translation o v ⊗ₜ[ℂ] chargeEnergy o a) = translation o v ⊗ₜ[ℂ] a
    rw [translation_raises_energy, TensorProduct.add_tmul]
    abel
  | add v w hv hw =>
    simp only [map_add]
    calc
      _ = (energy o (carrierTranslation o v) - carrierTranslation o (energy o v)) +
          (energy o (carrierTranslation o w) - carrierTranslation o (energy o w)) := by abel
      _ = _ := by rw [hv, hw]

theorem carrierTranslation_changes_energy (o : Fin 12) (d : ℂ)
    (v : LatticeCarrier o) (hv : energy o v = d • v) :
    energy o (carrierTranslation o v) = (d+1) • carrierTranslation o v := by
  have h := carrierTranslation_energy o v
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h, add_smul, one_smul]
  abel

end HMT.IV.LatticeOscillatorTranslation
end

#print axioms HMT.IV.LatticeOscillatorTranslation.translation_generator
#print axioms HMT.IV.LatticeOscillatorTranslation.translation_mode
#print axioms HMT.IV.LatticeOscillatorTranslation.euler_translation_bracket
#print axioms HMT.IV.LatticeOscillatorTranslation.translation_raises_energy
#print axioms HMT.IV.LatticeOscillatorTranslation.translation_create
#print axioms HMT.IV.LatticeOscillatorTranslation.translation_theta
#print axioms HMT.IV.LatticeOscillatorTranslation.carrierTranslation_vacuum
#print axioms HMT.IV.LatticeOscillatorTranslation.carrierTranslation_energy
#print axioms HMT.IV.LatticeOscillatorTranslation.carrierTranslation_changes_energy
