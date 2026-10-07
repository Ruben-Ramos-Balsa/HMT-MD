import Std

/-! Completación exterior de dos modos, con amplitudes enteras arbitrarias.
Base ordenada: vacío, e0, e1, e0∧e1. Las matrices son la restricción entera
de la representación exterior, no una teoría física de espín–estadística.
Propietarios: V, 20_completaciones_cuanticas.tex:86–134;
30_fock_gibbs.tex:51–125. Incluye también un lema condicional de dimensión
arbitraria: la idempotencia se deduce de CAR, linealidad y nilpotencia.
-/
namespace HMT.VFermiones

abbrev State := Int × Int × Int × Int
def zero : State := (0,0,0,0)
def plus (x y : State) : State :=
  (x.1+y.1, x.2.1+y.2.1, x.2.2.1+y.2.2.1, x.2.2.2+y.2.2.2)
def scale (t : Int) (x : State) : State :=
  (t*x.1, t*x.2.1, t*x.2.2.1, t*x.2.2.2)
def create (i : Bool) (x : State) : State :=
  if i then (0,0,x.1,-x.2.1) else (0,x.1,0,x.2.2.1)
def annihilate (i : Bool) (x : State) : State :=
  if i then (x.2.2.1,-x.2.2.2,0,0) else (x.2.1,0,x.2.2.2,0)
def number (i : Bool) (x : State) : State := create i (annihilate i x)

theorem creation_nilpotent (i : Bool) (x : State) :
    create i (create i x) = zero := by
  cases i <;> simp [create, zero]

theorem annihilation_nilpotent (i : Bool) (x : State) :
    annihilate i (annihilate i x) = zero := by
  cases i <;> simp [annihilate, zero]

theorem car_same_mode (i : Bool) (x : State) :
    plus (annihilate i (create i x)) (create i (annihilate i x)) = x := by
  rcases x with ⟨a,b,c,d⟩
  cases i <;> simp [create, annihilate, plus]

theorem car_distinct_modes (i j : Bool) (h : i ≠ j) (x : State) :
    plus (annihilate i (create j x)) (create j (annihilate i x)) = zero := by
  cases i <;> cases j <;> simp_all [create, annihilate, plus, zero] <;> omega

theorem creators_anticommute (x : State) :
    plus (create false (create true x)) (create true (create false x)) = zero := by
  simp [create, plus, zero] <;> omega

theorem annihilators_anticommute (x : State) :
    plus (annihilate false (annihilate true x))
      (annihilate true (annihilate false x)) = zero := by
  simp [annihilate, plus, zero] <;> omega

theorem occupation_idempotent (i : Bool) (x : State) :
    number i (number i x) = number i x := by
  cases i <;> simp [number, create, annihilate]

/-- No fixed mode count: the three hypotheses are ordinary operator laws. -/
theorem abstract_occupation_idempotent {I : Type}
    (c a : (I → Int) → (I → Int))
    (hcar : ∀ x, a (c x) = fun i => x i - c (a x) i)
    (hsub : ∀ x y, c (fun i => x i - y i) = fun i => c x i - c y i)
    (hcc : ∀ x, c (c x) = fun _ => 0) (x : I → Int) :
    c (a (c (a x))) = c (a x) := by
  rw [hcar, hsub, hcc]
  funext i
  simp

/-- The exterior lift of exchanging the one-particle basis: the top wedge changes sign. -/
def exchange (x : State) : State := (x.1,x.2.2.1,x.2.1,-x.2.2.2)

theorem exchange_involution (x : State) : exchange (exchange x) = x := by
  rcases x with ⟨a,b,c,d⟩
  simp [exchange]

theorem transport_creation (i : Bool) (x : State) :
    exchange (create i x) = create (!i) (exchange x) := by
  cases i <;> simp [create, exchange]

theorem transport_annihilation (i : Bool) (x : State) :
    exchange (annihilate i x) = annihilate (!i) (exchange x) := by
  cases i <;> simp [annihilate, exchange]

theorem transport_occupation (i : Bool) (x : State) :
    exchange (number i x) = number (!i) (exchange x) := by
  simp only [number, transport_creation, transport_annihilation]

def gammaScalar (t : Int) (x : State) : State :=
  (x.1,t*x.2.1,t*x.2.2.1,(t*t)*x.2.2.2)

theorem scalar_creation_transport (t : Int) (i : Bool) (x : State) :
    gammaScalar t (create i x) = scale t (create i (gammaScalar t x)) := by
  cases i <;> simp [gammaScalar, create, scale, Int.mul_assoc, Int.mul_neg]

theorem scalar_annihilation_adjoint (t : Int) (i : Bool) (x : State) :
    annihilate i (gammaScalar t x) = scale t (gammaScalar t (annihilate i x)) := by
  cases i <;> simp [gammaScalar, annihilate, scale, Int.mul_assoc, Int.mul_neg]

/-- Omitting the graded sign destroys creation transport. -/
def unsignedExchange (x : State) : State := (x.1,x.2.2.1,x.2.1,x.2.2.2)
theorem unsigned_exchange_fails :
    unsignedExchange (create false (0,0,1,0)) ≠
      create true (unsignedExchange (0,0,1,0)) := by decide

end HMT.VFermiones

#print axioms HMT.VFermiones.creation_nilpotent
#print axioms HMT.VFermiones.annihilation_nilpotent
#print axioms HMT.VFermiones.car_same_mode
#print axioms HMT.VFermiones.car_distinct_modes
#print axioms HMT.VFermiones.creators_anticommute
#print axioms HMT.VFermiones.annihilators_anticommute
#print axioms HMT.VFermiones.occupation_idempotent
#print axioms HMT.VFermiones.abstract_occupation_idempotent
#print axioms HMT.VFermiones.exchange_involution
#print axioms HMT.VFermiones.transport_creation
#print axioms HMT.VFermiones.transport_annihilation
#print axioms HMT.VFermiones.transport_occupation
#print axioms HMT.VFermiones.scalar_creation_transport
#print axioms HMT.VFermiones.scalar_annihilation_adjoint
#print axioms HMT.VFermiones.unsigned_exchange_fails
