import LatticeHalfIntegerHeisenberg

/-! The existing symmetric algebra is cyclic under its creation operators.
A linear endomorphism commuting with every creator is multiplication by its
value on 1. The proof uses the finite-support generators and the symmetric
algebra induction principle, with no new basis or irreducibility assumption. -/

noncomputable section
namespace HMT.IV.LatticeHalfFockGeneration
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open HMT.FockTransport.Symmetric

theorem commuting_creators_generator (o : Fin 12) (D : Module.End ℂ (HalfFock o))
    (hD : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      D.comp (create o n i) = (create o n i).comp D)
    (x : Oscillators o) (v : HalfFock o) :
    D (SymmetricAlgebra.ι ℂ (Oscillators o) x * v) =
      SymmetricAlgebra.ι ℂ (Oscillators o) x * D v := by
  induction x using Finsupp.induction_linear with
  | zero => simp only [map_zero, zero_mul]
  | add x y hx hy => simp only [map_add, add_mul, hx, hy]
  | single p c =>
    have hs : Finsupp.single p c = c • modeVector o p.1 p.2 := by
      simp only [modeVector, Finsupp.smul_single, smul_eq_mul, mul_one]
    have h := LinearMap.congr_fun (hD p.1 p.2) v
    simp only [LinearMap.comp_apply, create, creation_apply] at h
    rw [hs]
    simp only [map_smul, smul_mul_assoc, h]

theorem commuting_creators_mul (o : Fin 12) (D : Module.End ℂ (HalfFock o))
    (hD : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      D.comp (create o n i) = (create o n i).comp D)
    (v w : HalfFock o) : D (v*w) = v*D w := by
  induction v using SymmetricAlgebra.induction generalizing w with
  | algebraMap r =>
    simpa only [Algebra.smul_def] using map_smul D r w
  | ι x => exact commuting_creators_generator o D hD x w
  | mul x y hx hy => rw [mul_assoc, hx, hy, ← mul_assoc]
  | add x y hx hy => simp only [add_mul, map_add, hx, hy]

theorem commuting_creators_apply (o : Fin 12) (D : Module.End ℂ (HalfFock o))
    (hD : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      D.comp (create o n i) = (create o n i).comp D)
    (v : HalfFock o) : D v = v*D 1 := by
  simpa only [mul_one] using commuting_creators_mul o D hD v 1

theorem endomorphism_determined_by_one (o : Fin 12)
    (D E : Module.End ℂ (HalfFock o))
    (hD : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      D.comp (create o n i) = (create o n i).comp D)
    (hE : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      E.comp (create o n i) = (create o n i).comp E)
    (h1 : D 1=E 1) : D=E := by
  apply LinearMap.ext
  intro v
  rw [commuting_creators_apply o D hD, commuting_creators_apply o E hE, h1]

theorem commuting_creators_eq_scalar (o : Fin 12) (D : Module.End ℂ (HalfFock o))
    (hD : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      D.comp (create o n i) = (create o n i).comp D)
    (c : ℂ) (h1 : D 1=c • (1 : HalfFock o)) : D=c • LinearMap.id := by
  apply LinearMap.ext
  intro v
  rw [commuting_creators_apply o D hD, h1]
  simp only [mul_smul_comm, mul_one, LinearMap.smul_apply, LinearMap.id_apply]

theorem commuting_creators_eq_zero (o : Fin 12) (D : Module.End ℂ (HalfFock o))
    (hD : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      D.comp (create o n i) = (create o n i).comp D)
    (h1 : D 1=0) : D=0 := by
  have h := commuting_creators_eq_scalar o D hD 0 (by simpa only [zero_smul] using h1)
  simpa only [zero_smul] using h

end HMT.IV.LatticeHalfFockGeneration
end

#print axioms HMT.IV.LatticeHalfFockGeneration.commuting_creators_generator
#print axioms HMT.IV.LatticeHalfFockGeneration.commuting_creators_mul
#print axioms HMT.IV.LatticeHalfFockGeneration.commuting_creators_apply
#print axioms HMT.IV.LatticeHalfFockGeneration.endomorphism_determined_by_one
#print axioms HMT.IV.LatticeHalfFockGeneration.commuting_creators_eq_scalar
#print axioms HMT.IV.LatticeHalfFockGeneration.commuting_creators_eq_zero
