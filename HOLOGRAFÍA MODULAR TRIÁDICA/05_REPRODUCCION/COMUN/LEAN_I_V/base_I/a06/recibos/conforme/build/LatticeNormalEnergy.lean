import LatticeNormalTranslation
import LatticeEnergyModes
import LatticeChargedFieldEnergy

/-! Energy covariance of the actual normal products. All sums are finite on
each input vector; no global frequency cutoff or energy law is postulated. -/

noncomputable section
namespace HMT.IV.LatticeNormalEnergy

open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeNormalOrderedField LatticeNormalTranslation LatticeEnergyGrading
open LatticeEnergyModes

def EnergyCovariant (o : Fin 12) (d : ℂ)
    (B : VertexOperator ℂ (LatticeCarrier o)) : Prop :=
  ∀ k : ℤ, energy o * HVertexOperator.coeff B k -
    HVertexOperator.coeff B k * energy o =
      (d + (k : ℂ)) • HVertexOperator.coeff B k

theorem locallyFiniteSum_commutator
    {V : Type*} [AddCommGroup V] [Module ℂ V]
    (S : Module.End ℂ V) (P : ℕ → Module.End ℂ V)
    (hP : ∀ v, (Function.support (fun a => P a v)).Finite)
    (c : ℂ) (h : ∀ a, S * P a - P a * S = c • P a) :
    S * locallyFiniteSum P hP - locallyFiniteSum P hP * S =
      c • locallyFiniteSum P hP := by
  apply LinearMap.ext
  intro v
  apply locallyFiniteSum_commutator_of_telescoping S P P hP hP c v
    (fun _ => 0) (by simp) rfl
  intro a
  simpa only [LinearMap.sub_apply, Module.End.mul_apply,
    LinearMap.smul_apply, sub_self, add_zero] using LinearMap.congr_fun (h a) v

theorem creationTerm_energy (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (d : ℂ)
    (hB : EnergyCovariant o d B) (k : ℤ) (a : ℕ) :
    energy o * creationTerm o i n B k a -
      creationTerm o i n B k a * energy o =
      (d + (n : ℂ) + 1 + (k : ℂ)) • creationTerm o i n B k a := by
  have he := energy_create o (a+n) i
  change energy o * onCarrier o (create o (a+n) i) -
    onCarrier o (create o (a+n) i) * energy o =
      (((a+n : ℕ) : ℂ)+1) • onCarrier o (create o (a+n) i) at he
  change energy o * (((a+n).choose n : ℂ) •
      (onCarrier o (create o (a+n) i) * HVertexOperator.coeff B (k-a))) -
    (((a+n).choose n : ℂ) •
      (onCarrier o (create o (a+n) i) * HVertexOperator.coeff B (k-a))) * energy o = _
  rw [commutator_smul, commutator_mul, he, hB]
  simp only [creationTerm, smul_add, smul_mul_assoc, mul_smul_comm, smul_smul]
  push_cast
  module

theorem annihilationTerm_energy (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (d : ℂ)
    (hB : EnergyCovariant o d B) (k : ℤ) (a : ℕ) :
    energy o * annihilationTerm o i n B k a -
      annihilationTerm o i n B k a * energy o =
      (d + (n : ℂ) + 1 + (k : ℂ)) • annihilationTerm o i n B k a := by
  have he := energy_hmode o i (a : ℤ)
  change energy o * hmode o i (a : ℤ) - hmode o i (a : ℤ) * energy o =
    (-((a : ℤ) : ℂ)) • hmode o i (a : ℤ) at he
  change energy o * (((-1 : ℂ)^n * ((a+n).choose n : ℂ)) •
      (HVertexOperator.coeff B (k+a+n+1) * hmode o i (a : ℤ))) -
    (((-1 : ℂ)^n * ((a+n).choose n : ℂ)) •
      (HVertexOperator.coeff B (k+a+n+1) * hmode o i (a : ℤ))) * energy o = _
  rw [commutator_smul, commutator_mul, hB, he]
  simp only [annihilationTerm, smul_add, smul_mul_assoc, mul_smul_comm, smul_smul]
  push_cast
  module

theorem normalField_energy_covariant (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (d : ℂ)
    (hB : EnergyCovariant o d B) :
    EnergyCovariant o (d + (n : ℂ) + 1) (normalField o i n B) := by
  intro k
  have hc := locallyFiniteSum_commutator (energy o)
    (creationTerm o i n B k) (creationTerm_finite o i n B k)
    (d + (n : ℂ) + 1 + (k : ℂ)) (creationTerm_energy o i n B d hB k)
  have ha := locallyFiniteSum_commutator (energy o)
    (annihilationTerm o i n B k) (annihilationTerm_finite o i n B k)
    (d + (n : ℂ) + 1 + (k : ℂ)) (annihilationTerm_energy o i n B d hB k)
  apply LinearMap.ext
  intro v
  have hc' := LinearMap.congr_fun hc v
  have ha' := LinearMap.congr_fun ha v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at hc' ha'
  simp only [normalField_coefficient, Module.End.mul_apply, LinearMap.sub_apply,
    LinearMap.smul_apply, normalCoefficient_apply, map_add, smul_add]
  change energy o (∑ᶠ a, creationTerm o i n B k a v) -
    (∑ᶠ a, creationTerm o i n B k a (energy o v)) =
    (d + (n : ℂ) + 1 + (k : ℂ)) • (∑ᶠ a, creationTerm o i n B k a v) at hc'
  change energy o (∑ᶠ a, annihilationTerm o i n B k a v) -
    (∑ᶠ a, annihilationTerm o i n B k a (energy o v)) =
    (d + (n : ℂ) + 1 + (k : ℂ)) • (∑ᶠ a, annihilationTerm o i n B k a v) at ha'
  rw [← hc', ← ha']
  abel

end HMT.IV.LatticeNormalEnergy
end

#print axioms HMT.IV.LatticeNormalEnergy.locallyFiniteSum_commutator
#print axioms HMT.IV.LatticeNormalEnergy.creationTerm_energy
#print axioms HMT.IV.LatticeNormalEnergy.annihilationTerm_energy
#print axioms HMT.IV.LatticeNormalEnergy.normalField_energy_covariant
