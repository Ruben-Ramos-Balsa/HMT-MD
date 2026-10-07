import LatticeChargedVertexField

/-!
The actual HMT-selected lattice carrier is generated from its vacuum by the
already constructed charged fields and oscillator creation modes. This is a
spanning theorem on the entire algebraic carrier, with no bound on frequency,
occupation or lattice charge. It supplies the generation condition needed for
vertex-algebra reconstruction; it does not assume locality or an orbifold.

Source: Article I, sections/excepcional.tex, exc:voa (M(1) tensor C_epsilon[Lambda]).
-/

noncomputable section
namespace HMT.IV.LatticeFieldGeneration

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeChargedVertexField HMT.FockTransport.Symmetric
open scoped TensorProduct

/-- Invariance under the genuine oscillator modes is enough to generate all
oscillator histories above each charged ground state. -/
theorem oscillator_sector_generated (o : Fin 12)
    (S : Submodule ℂ (LatticeCarrier o))
    (hcreate : ∀ (n : ℕ) (i : Fin (BasisSize o)) (v : LatticeCarrier o),
      v ∈ S → onCarrier o (create o n i) v ∈ S)
    (x : Lattice o) (hx : (1 : Fock o) ⊗ₜ[ℂ] basisElement o x ∈ S)
    (v : Fock o) : v ⊗ₜ[ℂ] basisElement o x ∈ S := by
  let e := SymmetricAlgebra.equivMvPolynomial (oscillatorBasis o)
  have hpoly (p : MvPolynomial (Mode o) ℂ) :
      e.symm p ⊗ₜ[ℂ] basisElement o x ∈ S := by
    induction p using MvPolynomial.induction_on with
    | C c =>
      have hc := S.smul_mem c hx
      have he : e.symm (MvPolynomial.C c) = c • (1 : Fock o) := by
        change e.symm (algebraMap ℂ _ c) = _
        rw [e.symm.commutes]
        simp [Algebra.smul_def]
      rw [he]
      rw [← TensorProduct.smul_tmul']
      exact hc
    | add p q hp hq =>
      simpa only [map_add, TensorProduct.add_tmul] using S.add_mem hp hq
    | mul_X p m hp =>
      have hc := hcreate m.1 m.2 (e.symm p ⊗ₜ[ℂ] basisElement o x) hp
      simpa only [onCarrier_pure, create, creation_apply, map_mul,
        e, SymmetricAlgebra.equivMvPolynomial_symm_X,
        oscillatorBasis, Finsupp.coe_basisSingleOne, modeVector, mul_comm] using hc
  simpa only [AlgEquiv.symm_apply_apply] using hpoly (e v)

/-- Every subspace containing all charged ground states and stable under
creation modes equals the whole existing carrier. -/
theorem carrier_generated_by_ground_states (o : Fin 12)
    (S : Submodule ℂ (LatticeCarrier o))
    (hground : ∀ x : Lattice o, (1 : Fock o) ⊗ₜ[ℂ] basisElement o x ∈ S)
    (hcreate : ∀ (n : ℕ) (i : Fin (BasisSize o)) (v : LatticeCarrier o),
      v ∈ S → onCarrier o (create o n i) v ∈ S) : S = ⊤ := by
  apply top_unique
  intro v _
  rw [← (carrierBasis o).linearCombination_repr v,
    Finsupp.linearCombination_apply, Finsupp.sum]
  apply S.sum_mem
  intro p _
  apply S.smul_mem
  rw [carrierBasis, Basis.tensorProduct_apply]
  change monomialBasis o p.1 ⊗ₜ[ℂ] basisElement o p.2 ∈ S
  exact oscillator_sector_generated o S hcreate p.2 (hground p.2) _

/-- The ground states in the preceding theorem are themselves produced by
the constant coefficients of the actual charged fields acting on the vacuum. -/
theorem carrier_generated_by_fields (o : Fin 12)
    (S : Submodule ℂ (LatticeCarrier o)) (hvac : vacuum o ∈ S)
    (hcharged : ∀ (x : Lattice o) (v : LatticeCarrier o),
      v ∈ S → fieldCoefficient o x 0 v ∈ S)
    (hcreate : ∀ (n : ℕ) (i : Fin (BasisSize o)) (v : LatticeCarrier o),
      v ∈ S → onCarrier o (create o n i) v ∈ S) : S = ⊤ := by
  apply carrier_generated_by_ground_states o S _ hcreate
  intro x
  rw [← fieldCoefficient_vacuum_zero]
  exact hcharged x (vacuum o) hvac

/-- A generator retains whether it creates an oscillator or a lattice charge. -/
abbrev FieldGenerator (o : Fin 12) := Mode o ⊕ Lattice o

def generatorOperator (o : Fin 12) :
    FieldGenerator o → Module.End ℂ (LatticeCarrier o)
  | .inl m => onCarrier o (create o m.1 m.2)
  | .inr x => fieldCoefficient o x 0

/-- A finite chronological composition acting on the existing vacuum. -/
def wordState (o : Fin 12) : List (FieldGenerator o) → LatticeCarrier o
  | [] => vacuum o
  | a :: w => generatorOperator o a (wordState o w)

def generatedSpace (o : Fin 12) : Submodule ℂ (LatticeCarrier o) :=
  Submodule.span ℂ (Set.range (wordState o))

theorem wordState_mem_generatedSpace (o : Fin 12) (w : List (FieldGenerator o)) :
    wordState o w ∈ generatedSpace o :=
  Submodule.subset_span ⟨w, rfl⟩

theorem generator_preserves_generatedSpace (o : Fin 12) (a : FieldGenerator o)
    (v : LatticeCarrier o) (hv : v ∈ generatedSpace o) :
    generatorOperator o a v ∈ generatedSpace o := by
  induction hv using Submodule.span_induction with
  | mem v hv =>
    obtain ⟨w, rfl⟩ := hv
    exact wordState_mem_generatedSpace o (a :: w)
  | zero => simpa only [map_zero] using (generatedSpace o).zero_mem
  | add x y _ _ hx hy =>
    simpa only [map_add] using (generatedSpace o).add_mem hx hy
  | smul c x _ hx =>
    simpa only [map_smul] using (generatedSpace o).smul_mem c hx

/-- Unconditional spanning theorem for the explicit finite generator words:
their linear span is the entire carrier, not merely a low-weight truncation. -/
theorem generatedSpace_eq_top (o : Fin 12) : generatedSpace o = ⊤ := by
  apply carrier_generated_by_fields o
  · exact wordState_mem_generatedSpace o []
  · intro x v hv
    exact generator_preserves_generatedSpace o (.inr x) v hv
  · intro n i v hv
    exact generator_preserves_generatedSpace o (.inl (n, i)) v hv

/-- An endomorphism commuting with these field generators is uniquely
determined by its value on the vacuum. No truncation to a finite weight is used. -/
theorem endomorphism_determined_by_vacuum (o : Fin 12)
    (f g : Module.End ℂ (LatticeCarrier o))
    (hvac : f (vacuum o) = g (vacuum o))
    (hfcharged : ∀ x : Lattice o,
      f.comp (fieldCoefficient o x 0) = (fieldCoefficient o x 0).comp f)
    (hgcharged : ∀ x : Lattice o,
      g.comp (fieldCoefficient o x 0) = (fieldCoefficient o x 0).comp g)
    (hfcreate : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      f.comp (onCarrier o (create o n i)) = (onCarrier o (create o n i)).comp f)
    (hgcreate : ∀ (n : ℕ) (i : Fin (BasisSize o)),
      g.comp (onCarrier o (create o n i)) = (onCarrier o (create o n i)).comp g) :
    f = g := by
  have htop : LinearMap.ker (f - g) = ⊤ := by
    apply carrier_generated_by_fields o
    · simpa only [LinearMap.mem_ker, LinearMap.sub_apply, sub_eq_zero] using hvac
    · intro x v hv
      have heq : f v = g v := by
        simpa only [LinearMap.mem_ker, LinearMap.sub_apply, sub_eq_zero] using hv
      change f (fieldCoefficient o x 0 v) - g (fieldCoefficient o x 0 v) = 0
      have hf := LinearMap.congr_fun (hfcharged x) v
      have hg := LinearMap.congr_fun (hgcharged x) v
      simp only [LinearMap.comp_apply] at hf hg
      rw [hf, hg, heq, sub_self]
    · intro n i v hv
      have heq : f v = g v := by
        simpa only [LinearMap.mem_ker, LinearMap.sub_apply, sub_eq_zero] using hv
      change f (onCarrier o (create o n i) v) - g (onCarrier o (create o n i) v) = 0
      have hf := LinearMap.congr_fun (hfcreate n i) v
      have hg := LinearMap.congr_fun (hgcreate n i) v
      simp only [LinearMap.comp_apply] at hf hg
      rw [hf, hg, heq, sub_self]
  have hz : f - g = 0 := LinearMap.ker_eq_top.mp htop
  exact sub_eq_zero.mp hz

end HMT.IV.LatticeFieldGeneration
end

#print axioms HMT.IV.LatticeFieldGeneration.oscillator_sector_generated
#print axioms HMT.IV.LatticeFieldGeneration.carrier_generated_by_ground_states
#print axioms HMT.IV.LatticeFieldGeneration.carrier_generated_by_fields
#print axioms HMT.IV.LatticeFieldGeneration.generator_preserves_generatedSpace
#print axioms HMT.IV.LatticeFieldGeneration.generatedSpace_eq_top
#print axioms HMT.IV.LatticeFieldGeneration.endomorphism_determined_by_vacuum
