import Std

/-! Acoplamiento nonádico para un tipo arbitrario de estados y lector cualquiera.
Propietario: V, 20_completaciones_cuanticas.tex, líneas 317–346.
-/
namespace HMT.VAcoplamiento

def add9 (a b : Fin 9) : Fin 9 := ⟨(a.val + b.val) % 9, Nat.mod_lt _ (by decide)⟩
def sub9 (a b : Fin 9) : Fin 9 := ⟨(a.val + 9 - b.val) % 9, Nat.mod_lt _ (by decide)⟩

theorem sub_add (a b : Fin 9) : sub9 (add9 a b) b = a := by
  apply Fin.ext
  simp only [sub9, add9]
  have ha := a.isLt
  have hb := b.isLt
  omega

theorem add_sub (a b : Fin 9) : add9 (sub9 a b) b = a := by
  apply Fin.ext
  simp only [sub9, add9]
  have ha := a.isLt
  have hb := b.isLt
  omega

def couple {S : Type} (r : S → Fin 9) (x : S × Fin 9) : S × Fin 9 :=
  (x.1, add9 x.2 (r x.1))
def uncouple {S : Type} (r : S → Fin 9) (x : S × Fin 9) : S × Fin 9 :=
  (x.1, sub9 x.2 (r x.1))

theorem recover_input {S : Type} (r : S → Fin 9) (x : S × Fin 9) :
    uncouple r (couple r x) = x := by
  rcases x with ⟨s,a⟩
  simp only [uncouple, couple, sub_add]

theorem recover_output {S : Type} (r : S → Fin 9) (x : S × Fin 9) :
    couple r (uncouple r x) = x := by
  rcases x with ⟨s,a⟩
  simp only [uncouple, couple, add_sub]

theorem couple_injective {S : Type} (r : S → Fin 9) (x y : S × Fin 9)
    (h : couple r x = couple r y) : x = y := by
  have := congrArg (uncouple r) h
  simpa only [recover_input] using this

theorem couple_surjective {S : Type} (r : S → Fin 9) (y : S × Fin 9) :
    ∃ x, couple r x = y := ⟨uncouple r y, recover_output r y⟩

/-- Discarding the apparatus is not the reversible coupling itself. -/
theorem forget_register_not_injective :
    ((), (0 : Fin 9)) ≠ ((), (1 : Fin 9)) ∧
    ((), (0 : Fin 9)).1 = ((), (1 : Fin 9)).1 := by decide

end HMT.VAcoplamiento

#print axioms HMT.VAcoplamiento.sub_add
#print axioms HMT.VAcoplamiento.add_sub
#print axioms HMT.VAcoplamiento.recover_input
#print axioms HMT.VAcoplamiento.recover_output
#print axioms HMT.VAcoplamiento.couple_injective
#print axioms HMT.VAcoplamiento.couple_surjective
#print axioms HMT.VAcoplamiento.forget_register_not_injective
