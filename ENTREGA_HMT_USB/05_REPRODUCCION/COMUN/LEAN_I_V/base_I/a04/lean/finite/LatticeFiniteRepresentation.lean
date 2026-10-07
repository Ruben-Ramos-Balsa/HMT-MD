import LatticeParityNondegenerate
import Mathlib.RepresentationTheory.Basic

/-! The finite central extension already obtained from the marked lattice acts
on its twisted regular space. The action uses the inherited triangular cocycle,
not an independently chosen matrix or a target dimension. The central sign is
proved to act by minus the identity. An irreducible constituent is constructed
in the next module; this regular space is not identified with that constituent. -/

noncomputable section
namespace HMT.IV.LatticeFiniteRepresentation

open LatticeCocycle LatticeTwistedFiniteQuotient

def complexSign (s : ZMod 2) : ℂ := (TC.sign s : ℤ)

@[simp] theorem complexSign_zero : complexSign 0 = 1 := by
  norm_num [complexSign, TC.sign]

@[simp] theorem complexSign_one : complexSign 1 = -1 := by
  norm_num [complexSign, TC.sign]

theorem complexSign_add (s t : ZMod 2) :
    complexSign (s+t) = complexSign s * complexSign t := by
  simp [complexSign, TC.sign_add]

theorem complexSign_sq (s : ZMod 2) : complexSign s * complexSign s = 1 := by
  unfold complexSign
  exact_mod_cast TC.sign_sq s

abbrev RegularSpace (o : Fin 12) := ParityVector o → ℂ

def finiteAction (o : Fin 12) (a : FiniteExtension o) :
    Module.End ℂ (RegularSpace o) where
  toFun f x := complexSign (a.1 + TC.tau (parityGram o) x a.2) * f (x+a.2)
  map_add' f g := by
    funext x
    exact mul_add _ _ _
  map_smul' c f := by
    funext x
    change _ * (c * _) = c * (_ * _)
    ring

@[simp] theorem finiteAction_apply (o : Fin 12) (a : FiniteExtension o)
    (f : RegularSpace o) (x : ParityVector o) :
    finiteAction o a f x =
      complexSign (a.1 + TC.tau (parityGram o) x a.2) * f (x+a.2) := rfl

theorem finiteAction_one (o : Fin 12) : finiteAction o 1 = 1 := by
  apply LinearMap.ext
  intro f
  funext x
  change complexSign (0 + TC.tau (parityGram o) x 0) * f (x+0) = f x
  simp [TC.tau_zero_right]

theorem finiteAction_mul (o : Fin 12) (a b : FiniteExtension o) :
    finiteAction o (a*b) = finiteAction o a * finiteAction o b := by
  apply LinearMap.ext
  intro f
  funext x
  change complexSign (a.1+b.1+TC.tau (parityGram o) a.2 b.2 +
      TC.tau (parityGram o) x (a.2+b.2)) * f (x+(a.2+b.2)) =
    complexSign (a.1+TC.tau (parityGram o) x a.2) *
      (complexSign (b.1+TC.tau (parityGram o) (x+a.2) b.2) * f ((x+a.2)+b.2))
  have h : a.1+b.1+TC.tau (parityGram o) a.2 b.2 +
      TC.tau (parityGram o) x (a.2+b.2) =
      (a.1+TC.tau (parityGram o) x a.2) +
      (b.1+TC.tau (parityGram o) (x+a.2) b.2) := by
    rw [TriangularCocycle.tau_add_left, TriangularCocycle.tau_add_right]
    ring
  rw [h, complexSign_add, add_assoc, mul_assoc]

def finiteRepresentation (o : Fin 12) :
    Representation ℂ (FiniteExtension o) (RegularSpace o) where
  toFun := finiteAction o
  map_one' := finiteAction_one o
  map_mul' := finiteAction_mul o

theorem finiteAction_center (o : Fin 12) (s : ZMod 2) :
    finiteRepresentation o (s,0) = complexSign s • (1 : Module.End ℂ (RegularSpace o)) := by
  apply LinearMap.ext
  intro f
  funext x
  change complexSign (s+TC.tau (parityGram o) x 0) * f (x+0) = complexSign s * f x
  simp [TC.tau_zero_right]

theorem central_involution_negative (o : Fin 12) :
    finiteRepresentation o (1,0) = -(1 : Module.End ℂ (RegularSpace o)) := by
  rw [finiteAction_center, complexSign_one]
  apply LinearMap.ext
  intro f
  funext x
  change (-1:ℂ) * f x = -f x
  ring

theorem regularSpace_finrank (o : Fin 12) :
    Module.finrank ℂ (RegularSpace o) = 2 ^ LatticeCocycle.BasisSize o := by
  simp [RegularSpace, ParityVector, Module.finrank_pi, ZMod.card]

end HMT.IV.LatticeFiniteRepresentation
end
