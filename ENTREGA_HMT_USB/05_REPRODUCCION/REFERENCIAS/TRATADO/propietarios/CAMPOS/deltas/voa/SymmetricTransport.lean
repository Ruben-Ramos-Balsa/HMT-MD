import Mathlib.LinearAlgebra.SymmetricAlgebra.Basic
import Mathlib.Algebra.TrivSqZeroExt
import Mathlib.RingTheory.Derivation.Basic
import Mathlib.Algebra.Algebra.Bilinear
import Mathlib.Tactic

/-!
# Algebraic symmetric Fock transport in arbitrary degree

Source: Article V, `30_fock_gibbs.tex`, lines 17--101, with the symmetric
construction in `20_completaciones_cuanticas.tex`, lines 37--147.

The carrier is the symmetric algebra: the algebraic finite-particle domain,
for an arbitrary module, with no restriction to a fixed number of modes.
Creation is multiplication by a generator. Annihilation is the unique
derivation specified by a dual vector. The square-zero extension constructs
that derivation from the universal property; it is not assumed.

This module proves algebraic CCR and naturality for every linear map.
It does not assert Hilbert completion, bounded second quantization, or
identification of the algebraic dual with a Hilbert adjoint.
-/

noncomputable section

namespace HMT.FockTransport.Symmetric

variable {R M N P : Type*} [CommRing R]
  [AddCommGroup M] [Module R M]
  [AddCommGroup N] [Module R N]
  [AddCommGroup P] [Module R P]

/-- Algebraic second quantization, defined by the universal property. -/
def gamma (T : M →ₗ[R] N) : SymmetricAlgebra R M →ₐ[R] SymmetricAlgebra R N :=
  SymmetricAlgebra.lift ((SymmetricAlgebra.ι R N).comp T)

@[simp] theorem gamma_generator (T : M →ₗ[R] N) (f : M) :
    gamma T (SymmetricAlgebra.ι R M f) = SymmetricAlgebra.ι R N (T f) := by
  simp [gamma]

@[simp] theorem gamma_identity :
    gamma (LinearMap.id : M →ₗ[R] M) = AlgHom.id R (SymmetricAlgebra R M) := by
  apply SymmetricAlgebra.algHom_ext
  ext f
  simp

theorem gamma_composition (T : M →ₗ[R] N) (U : N →ₗ[R] P) :
    gamma (U.comp T) = (gamma U).comp (gamma T) := by
  apply SymmetricAlgebra.algHom_ext
  ext f
  simp

@[simp] theorem gamma_vacuum (T : M →ₗ[R] N) : gamma T 1 = 1 := map_one _

/-- Creation preserves the algebraic finite-particle domain. -/
def creation (f : M) : SymmetricAlgebra R M →ₗ[R] SymmetricAlgebra R M :=
  LinearMap.mulLeft R (SymmetricAlgebra.ι R M f)

@[simp] theorem creation_apply (f : M) (x : SymmetricAlgebra R M) :
    creation f x = SymmetricAlgebra.ι R M f * x := rfl

private def jetSeed (d : Module.Dual R M) :
    M →ₗ[R] TrivSqZeroExt (SymmetricAlgebra R M) (SymmetricAlgebra R M) where
  toFun f := (SymmetricAlgebra.ι R M f, algebraMap R _ (d f))
  map_add' f g := by ext <;> simp
  map_smul' r f := by
    ext <;> simp [Algebra.smul_def, TrivSqZeroExt.algebraMap_eq_inl']

private def jet (d : Module.Dual R M) :
    SymmetricAlgebra R M →ₐ[R]
      TrivSqZeroExt (SymmetricAlgebra R M) (SymmetricAlgebra R M) :=
  SymmetricAlgebra.lift (jetSeed d)

private theorem jet_fst_hom (d : Module.Dual R M) :
    (TrivSqZeroExt.fstHom R (SymmetricAlgebra R M) (SymmetricAlgebra R M)).comp
      (jet d) = AlgHom.id R (SymmetricAlgebra R M) := by
  apply SymmetricAlgebra.algHom_ext
  ext f
  simp [jet, jetSeed]

private theorem jet_fst (d : Module.Dual R M) (x : SymmetricAlgebra R M) :
    (jet d x).fst = x :=
  AlgHom.congr_fun (jet_fst_hom d) x

/-- Annihilation constructed as the linear coefficient of a square-zero lift. -/
def annihilation (d : Module.Dual R M) :
    Derivation R (SymmetricAlgebra R M) (SymmetricAlgebra R M) where
  toLinearMap := ((TrivSqZeroExt.sndHom (SymmetricAlgebra R M)
    (SymmetricAlgebra R M)).restrictScalars R).comp (jet d).toLinearMap
  map_one_eq_zero' := by simp
  leibniz' x y := by
    change (jet d (x * y)).snd = x • (jet d y).snd + y • (jet d x).snd
    simp [map_mul, TrivSqZeroExt.snd_mul, jet_fst, smul_eq_mul,
      op_smul_eq_smul, mul_comm]

@[simp] theorem annihilation_generator (d : Module.Dual R M) (f : M) :
    annihilation d (SymmetricAlgebra.ι R M f) = algebraMap R _ (d f) := by
  change (jet d (SymmetricAlgebra.ι R M f)).snd = _
  simp [jet, jetSeed]

@[simp] theorem annihilation_vacuum (d : Module.Dual R M) :
    annihilation d 1 = 0 := (annihilation d).map_one_eq_zero

theorem annihilation_product (d : Module.Dual R M) (x y : SymmetricAlgebra R M) :
    annihilation d (x * y) = x * annihilation d y + y * annihilation d x := by
  simpa only [smul_eq_mul] using (annihilation d).leibniz x y

/-- Generator values determine the annihilation derivation on every degree. -/
theorem annihilation_unique (d : Module.Dual R M)
    (D : Derivation R (SymmetricAlgebra R M) (SymmetricAlgebra R M))
    (hD : ∀ f, D (SymmetricAlgebra.ι R M f) = algebraMap R _ (d f)) :
    D = annihilation d := by
  apply Derivation.ext
  intro x
  induction x using SymmetricAlgebra.induction with
  | algebraMap r => simp
  | ι f => simpa using hD f
  | mul x y hx hy => simp only [Derivation.leibniz, hx, hy]
  | add x y hx hy => simp only [map_add, hx, hy]

theorem creation_naturality (T : M →ₗ[R] N) (f : M) (x : SymmetricAlgebra R M) :
    gamma T (creation f x) = creation (T f) (gamma T x) := by
  simp

/-- Contravariance of the dual is essential for general linear transport. -/
theorem annihilation_naturality (T : M →ₗ[R] N) (d : Module.Dual R N)
    (x : SymmetricAlgebra R M) :
    annihilation d (gamma T x) = gamma T (annihilation (d.comp T) x) := by
  induction x using SymmetricAlgebra.induction with
  | algebraMap r => simp
  | ι f => simp
  | mul x y hx hy => simp only [map_mul, annihilation_product, map_add, hx, hy]
  | add x y hx hy => simp only [map_add, hx, hy]

theorem creations_commute (f g : M) (x : SymmetricAlgebra R M) :
    creation f (creation g x) = creation g (creation f x) := by
  simp only [creation_apply]
  ring

theorem annihilations_commute (d e : Module.Dual R M) (x : SymmetricAlgebra R M) :
    annihilation d (annihilation e x) = annihilation e (annihilation d x) := by
  induction x using SymmetricAlgebra.induction with
  | algebraMap r => simp
  | ι f => simp
  | mul x y hx hy =>
      simp only [annihilation_product, map_add, hx, hy]
      ring
  | add x y hx hy => simp only [map_add, hx, hy]

/-- Canonical commutation relation on the whole algebraic symmetric Fock space. -/
theorem ccr (d : Module.Dual R M) (f : M) (x : SymmetricAlgebra R M) :
    annihilation d (creation f x) - creation f (annihilation d x) = (d f) • x := by
  simp only [creation_apply, annihilation_product, annihilation_generator,
    Algebra.smul_def]
  ring

theorem creation_naturality_linear (T : M →ₗ[R] N) (f : M) :
    (gamma T).toLinearMap.comp (creation f) =
      (creation (T f)).comp (gamma T).toLinearMap := by
  ext x
  exact creation_naturality T f x

theorem annihilation_naturality_linear (T : M →ₗ[R] N) (d : Module.Dual R N) :
    (annihilation d).toLinearMap.comp (gamma T).toLinearMap =
      (gamma T).toLinearMap.comp (annihilation (d.comp T)).toLinearMap := by
  ext x
  exact annihilation_naturality T d x

theorem ccr_linear (d : Module.Dual R M) (f : M) :
    (annihilation d).toLinearMap.comp (creation f) -
      (creation f).comp (annihilation d).toLinearMap =
        (d f) • (LinearMap.id : SymmetricAlgebra R M →ₗ[R] SymmetricAlgebra R M) := by
  ext x
  exact ccr d f x

end HMT.FockTransport.Symmetric

#print axioms HMT.FockTransport.Symmetric.gamma_generator
#print axioms HMT.FockTransport.Symmetric.gamma_identity
#print axioms HMT.FockTransport.Symmetric.gamma_composition
#print axioms HMT.FockTransport.Symmetric.gamma_vacuum
#print axioms HMT.FockTransport.Symmetric.creation_apply
#print axioms HMT.FockTransport.Symmetric.annihilation_generator
#print axioms HMT.FockTransport.Symmetric.annihilation_vacuum
#print axioms HMT.FockTransport.Symmetric.annihilation_product
#print axioms HMT.FockTransport.Symmetric.annihilation_unique
#print axioms HMT.FockTransport.Symmetric.creation_naturality
#print axioms HMT.FockTransport.Symmetric.annihilation_naturality
#print axioms HMT.FockTransport.Symmetric.creations_commute
#print axioms HMT.FockTransport.Symmetric.annihilations_commute
#print axioms HMT.FockTransport.Symmetric.ccr
#print axioms HMT.FockTransport.Symmetric.creation_naturality_linear
#print axioms HMT.FockTransport.Symmetric.annihilation_naturality_linear
#print axioms HMT.FockTransport.Symmetric.ccr_linear
