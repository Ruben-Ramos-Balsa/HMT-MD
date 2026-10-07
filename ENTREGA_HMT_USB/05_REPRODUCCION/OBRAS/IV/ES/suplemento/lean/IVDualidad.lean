import Std

/-! Intercambio, involución y conjugación algebraica. No importa ℓ² ni ℝ.
La forma usa pesos enteros libres u,v; la sustitución analítica
u=R^(-2), v=R^2 y los dominios autoadjuntos quedan fuera de este archivo.
Propietario: IV, sections/02_dualidad_t.tex, líneas 14–65 y 109–140.
-/
namespace HMT.IVDualidad

abbrev Lattice := Int × Int
def swap (x : Lattice) : Lattice := (x.2, x.1)

theorem swap_involution (x : Lattice) : swap (swap x) = x := rfl

/-- Applies to a radius type only once its inversion law has been supplied. -/
def dualState {R : Type} (inv : R → R) (x : Lattice × R) : Lattice × R :=
  (swap x.1, inv x.2)

theorem dualState_involution {R : Type} (inv : R → R)
    (hinv : ∀ r, inv (inv r) = r) (x : Lattice × R) :
    dualState inv (dualState inv x) = x := by
  rcases x with ⟨p,r⟩
  simp only [dualState, swap_involution, hinv]

def energy (u v : Int) (x : Lattice) : Int :=
  u * (x.1 * x.1) + v * (x.2 * x.2)

theorem energy_exchange (u v : Int) (x : Lattice) :
    energy v u (swap x) = energy u v x := by
  exact Int.add_comm _ _

def pull {A : Type} (f : Lattice → A) : Lattice → A := fun x => f (swap x)

theorem pull_involution {A : Type} (f : Lattice → A) : pull (pull f) = f := rfl

def diagonal (u v : Int) (f : Lattice → Int) : Lattice → Int :=
  fun x => energy u v x * f x

theorem diagonal_conjugation (u v : Int) (f : Lattice → Int) :
    pull (diagonal u v (pull f)) = diagonal v u f := by
  funext x
  simp only [pull, diagonal, swap_involution, energy_exchange]

/-- Conjugating any involution by explicitly inverse maps preserves involutivity. -/
def conjugate {A B : Type} (encode : A → B) (decode : B → A)
    (op : A → A) : B → B := fun x => encode (op (decode x))

theorem conjugate_involution {A B : Type} (encode : A → B) (decode : B → A)
    (left : ∀ x, decode (encode x) = x)
    (right : ∀ y, encode (decode y) = y)
    (op : A → A) (hop : ∀ x, op (op x) = x) (y : B) :
    conjugate encode decode op (conjugate encode decode op y) = y := by
  simp only [conjugate, left, hop, right]

end HMT.IVDualidad

#print axioms HMT.IVDualidad.swap_involution
#print axioms HMT.IVDualidad.dualState_involution
#print axioms HMT.IVDualidad.energy_exchange
#print axioms HMT.IVDualidad.pull_involution
#print axioms HMT.IVDualidad.diagonal_conjugation
#print axioms HMT.IVDualidad.conjugate_involution
