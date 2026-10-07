import LatticeFiniteRepresentation
import Mathlib.RepresentationTheory.Maschke
import Mathlib.RepresentationTheory.Submodule
import Mathlib.RepresentationTheory.Character
import Mathlib.Algebra.Category.ModuleCat.Simple
import Mathlib.CategoryTheory.Action.Limits
import Mathlib.CategoryTheory.Limits.Constructions.EpiMono

/-! A simple constituent of the actual twisted regular representation.
The central character is inherited by restriction. No irreducible dimension,
polarization, or classification theorem is supplied as an input. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeFiniteIrreducible

open LatticeTwistedFiniteQuotient LatticeFiniteRepresentation

abbrev GroupAlgebra (o : Fin 12) := MonoidAlgebra ℂ (FiniteExtension o)
abbrev RegularModule (o : Fin 12) := (finiteRepresentation o).asModule

instance regularModule_addCommGroup (o : Fin 12) : AddCommGroup (RegularModule o) :=
  inferInstanceAs (AddCommGroup (RegularSpace o))

instance regularModule_nontrivial (o : Fin 12) : Nontrivial (RegularModule o) :=
  (finiteRepresentation o).asModuleEquiv.toEquiv.nontrivial

instance regularModule_finite (o : Fin 12) : Module.Finite ℂ (RegularModule o) :=
  Module.Finite.of_injective (finiteRepresentation o).asModuleEquiv.toLinearMap
    (finiteRepresentation o).asModuleEquiv.injective

theorem simple_constituent_exists (o : Fin 12) :
    ∃ S : Submodule (GroupAlgebra o) (RegularModule o),
      IsSimpleModule (GroupAlgebra o) S := by
  exact IsSemisimpleModule.exists_simple_submodule (GroupAlgebra o) (RegularModule o)

def simpleConstituent (o : Fin 12) : Submodule (GroupAlgebra o) (RegularModule o) :=
  Classical.choose (simple_constituent_exists o)

instance simpleConstituent_simple (o : Fin 12) :
    IsSimpleModule (GroupAlgebra o) (simpleConstituent o) :=
  Classical.choose_spec (simple_constituent_exists o)

abbrev FiniteSpace (o : Fin 12) : Type := ↥(simpleConstituent o)

instance finiteSpace_nontrivial (o : Fin 12) : Nontrivial (FiniteSpace o) :=
  IsSimpleModule.nontrivial (GroupAlgebra o) (FiniteSpace o)

instance finiteSpace_finite (o : Fin 12) : Module.Finite ℂ (FiniteSpace o) :=
  Module.Finite.of_injective ((simpleConstituent o).subtype.restrictScalars ℂ)
    (simpleConstituent o).subtype_injective

def constituentRepresentation (o : Fin 12) :
    Representation ℂ (FiniteExtension o) (FiniteSpace o) :=
  Representation.ofModule' (FiniteSpace o)

def inclusion (o : Fin 12) : FiniteSpace o →ₗ[ℂ] RegularSpace o :=
  (finiteRepresentation o).asModuleEquiv.toLinearMap.comp
    ((simpleConstituent o).subtype.restrictScalars ℂ)

theorem inclusion_injective (o : Fin 12) : Function.Injective (inclusion o) :=
  (finiteRepresentation o).asModuleEquiv.injective.comp
    (simpleConstituent o).subtype_injective

theorem inclusion_intertwines (o : Fin 12) (g : FiniteExtension o)
    (v : FiniteSpace o) :
    inclusion o (constituentRepresentation o g v) =
      finiteRepresentation o g (inclusion o v) := by
  change (finiteRepresentation o).asModuleEquiv
    ((MonoidAlgebra.of ℂ (FiniteExtension o) g) • (v : RegularModule o)) = _
  rw [Representation.asModuleEquiv_map_smul]
  simp only [MonoidAlgebra.of_apply, Representation.asAlgebraHom_single, one_smul]
  rfl

theorem constituent_center (o : Fin 12) (s : ZMod 2) :
    constituentRepresentation o (s,0) =
      complexSign s • (1 : Module.End ℂ (FiniteSpace o)) := by
  apply LinearMap.ext
  intro v
  apply inclusion_injective o
  rw [inclusion_intertwines, finiteAction_center]
  simp

theorem constituent_central_involution_negative (o : Fin 12) :
    constituentRepresentation o (1,0) =
      -(1 : Module.End ℂ (FiniteSpace o)) := by
  apply LinearMap.ext
  intro v
  apply inclusion_injective o
  rw [inclusion_intertwines, central_involution_negative]
  simp only [LinearMap.neg_apply, Module.End.one_apply, map_neg]

def finiteFDRep (o : Fin 12) : FDRep ℂ (FiniteExtension o) :=
  FDRep.of (V := FiniteSpace o) (constituentRepresentation o)

def constituentModuleEquiv (o : Fin 12) :
    (constituentRepresentation o).asModule ≃ₗ[GroupAlgebra o] FiniteSpace o where
  __ := (constituentRepresentation o).asModuleEquiv.toAddEquiv
  map_smul' r v := by
    change (constituentRepresentation o).asAlgebraHom r
      ((constituentRepresentation o).asModuleEquiv v) =
        r • (constituentRepresentation o).asModuleEquiv v
    induction r using MonoidAlgebra.induction_on with
    | hM g => rw [Representation.asAlgebraHom_of]; rfl
    | hadd a b ha hb => simp only [map_add, LinearMap.add_apply, add_smul, ha, hb]
    | hsmul c a ha => simp only [map_smul, LinearMap.smul_apply, ha, smul_assoc]

instance constituent_asModule_simple (o : Fin 12) :
    IsSimpleModule (GroupAlgebra o) (constituentRepresentation o).asModule :=
  IsSimpleModule.congr (constituentModuleEquiv o)

open CategoryTheory

instance finiteFDRep_simple (o : Fin 12) : Simple (finiteFDRep o) where
  mono_isIso_iff_nonzero := by
    intro X f hf
    haveI := hf
    constructor
    · intro hi hzero
      haveI := hi
      have hinj := (ConcreteCategory.bijective_of_isIso f).2
      have hz : ∀ v : FiniteSpace o, v = 0 := by
        intro v
        obtain ⟨x, hx⟩ := hinj v
        rw [hzero] at hx
        exact hx.symm
      exact (not_subsingleton (FiniteSpace o)) ⟨fun a b => (hz a).trans (hz b).symm⟩
    · intro hn
      let F := (forget₂ (FDRep ℂ (FiniteExtension o)) (Rep ℂ (FiniteExtension o))) ⋙
        Rep.toModuleMonoidAlgebra
      let fA := (F.map f).hom
      have hnA : fA ≠ 0 := by
        intro heq
        apply hn
        apply Action.Hom.ext
        apply ModuleCat.hom_ext
        apply LinearMap.ext
        intro x
        exact LinearMap.congr_fun heq ((Representation.asModuleEquiv X.ρ).symm x)
      haveI : IsSimpleModule (MonoidAlgebra ℂ (FiniteExtension o)) (F.obj (finiteFDRep o)) := by
        change IsSimpleModule (GroupAlgebra o) (constituentRepresentation o).asModule
        infer_instance
      have hsurj := LinearMap.surjective_of_ne_zero hnA
      have hinj : Function.Injective f.hom.hom := by
        haveI : Mono ((Action.forget (FGModuleCat ℂ) (FiniteExtension o)).map f) :=
          inferInstance
        haveI : Mono f.hom := inferInstanceAs
          (Mono ((Action.forget (FGModuleCat ℂ) (FiniteExtension o)).map f))
        exact (ModuleCat.mono_iff_injective
          ((forget₂ (FGModuleCat ℂ) (ModuleCat ℂ)).map f.hom)).mp inferInstance
      let e : X ≃ₗ[ℂ] FiniteSpace o := LinearEquiv.ofBijective f.hom.hom ⟨hinj, hsurj⟩
      let iso : X ≅ finiteFDRep o := Action.mkIso e.toFGModuleCatIso (fun g => f.comm g)
      exact iso.isIso_hom

end HMT.IV.LatticeFiniteIrreducible
end
