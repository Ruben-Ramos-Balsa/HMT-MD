import Std

/-! Certificado nuevo del resultado recuperado: H4 y sus tres órbitas H12.
Dominio: registros enteros arbitrarios, no sólo la coordenada archivada.
Propietario: IV, sections/registro_imagen_integral.tex, líneas 87–145.
-/
namespace HMT.IVRegistro

abbrev Block := Int × Int × Int × Int

def h4 (x : Block) : Block :=
  (x.1 + x.2.1 + x.2.2.1 + x.2.2.2,
   x.1 + x.2.1 - x.2.2.1 - x.2.2.2,
   x.1 - x.2.1 + x.2.2.1 - x.2.2.2,
   x.1 - x.2.1 - x.2.2.1 + x.2.2.2)

def scale4 (x : Block) : Block :=
  (4*x.1, 4*x.2.1, 4*x.2.2.1, 4*x.2.2.2)

def decode (u : Block) : Block :=
  let v := h4 u
  (v.1 / 4, v.2.1 / 4, v.2.2.1 / 4, v.2.2.2 / 4)

def Compatible (u : Block) : Prop :=
  (h4 u).1 % 4 = 0 ∧ (h4 u).2.1 % 4 = 0 ∧
  (h4 u).2.2.1 % 4 = 0 ∧ (h4 u).2.2.2 % 4 = 0

theorem h4_square (x : Block) : h4 (h4 x) = scale4 x := by
  rcases x with ⟨a,b,c,d⟩
  simp only [h4, scale4, Prod.mk.injEq]
  omega

theorem decode_h4 (x : Block) : decode (h4 x) = x := by
  rcases x with ⟨a,b,c,d⟩
  simp only [decode, h4_square, scale4, Prod.mk.injEq]
  omega

theorem h4_injective (x y : Block) (h : h4 x = h4 y) : x = y := by
  have := congrArg decode h
  simpa only [decode_h4] using this

theorem image_compatible (x : Block) : Compatible (h4 x) := by
  simp only [Compatible, h4_square, scale4]
  omega

theorem recover_compatible (u : Block) (h : Compatible u) : h4 (decode u) = u := by
  rcases u with ⟨a,b,c,d⟩
  simp only [Compatible, h4] at h
  simp only [decode, h4, Prod.mk.injEq]
  omega

theorem image_iff (u : Block) : (∃ x, h4 x = u) ↔ Compatible u := by
  constructor
  · rintro ⟨x, rfl⟩
    exact image_compatible x
  · intro h
    exact ⟨decode u, recover_compatible u h⟩

/-- r=0,1,2 represents (r,r+3,r+6,r+9), not four adjacent windows. -/
abbrev Register := Fin 3 → Block
def h12 (k : Register) : Register := fun r => h4 (k r)
def decode12 (u : Register) : Register := fun r => decode (u r)

theorem h12_square (k : Register) : h12 (h12 k) = fun r => scale4 (k r) := by
  funext r
  exact h4_square (k r)

theorem recovery12 (k : Register) : decode12 (h12 k) = k := by
  funext r
  exact decode_h4 (k r)

theorem h12_injective (k l : Register) (h : h12 k = h12 l) : k = l := by
  have := congrArg decode12 h
  simpa only [recovery12] using this

/-- The full record and a projection are different: one coordinate is insufficient. -/
theorem first_coordinate_not_injective :
    ((0,0,0,0) : Block) ≠ ((0,1,0,0) : Block) ∧
    (((0,0,0,0) : Block).1) = (((0,1,0,0) : Block).1) := by decide

end HMT.IVRegistro

#print axioms HMT.IVRegistro.h4_square
#print axioms HMT.IVRegistro.decode_h4
#print axioms HMT.IVRegistro.h4_injective
#print axioms HMT.IVRegistro.image_compatible
#print axioms HMT.IVRegistro.recover_compatible
#print axioms HMT.IVRegistro.image_iff
#print axioms HMT.IVRegistro.h12_square
#print axioms HMT.IVRegistro.recovery12
#print axioms HMT.IVRegistro.h12_injective
#print axioms HMT.IVRegistro.first_coordinate_not_injective
