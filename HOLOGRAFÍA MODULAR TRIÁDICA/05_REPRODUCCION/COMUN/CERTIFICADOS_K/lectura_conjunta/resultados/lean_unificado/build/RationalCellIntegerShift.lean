import RadixCellSelection

/-!
Exact translation between rational fractional bounds and absolute cell
coordinates. Translating a rational enclosure by an integer translates its
first/last cells and the parent-cylinder clipping bounds by the same amount.
This changes coordinates only; it does not define another selector.
-/

namespace HMT.I.RationalCellIntegerShift

open RadixCellSelection

theorem first_integer_shift (q : ℚ) (m : Int) (scale : Nat) :
    first (q + m) scale = first q scale + m * scale := by
  unfold first
  have he : (q + m) * scale = q * scale + ((m * (scale : Int) : Int) : ℚ) := by
    push_cast
    ring
  rw [he, Int.floor_add_intCast]

theorem last_integer_shift (q : ℚ) (m : Int) (scale : Nat) :
    last (q + m) scale = last q scale + m * scale := by
  unfold last
  have he : (q + m) * scale = q * scale + ((m * (scale : Int) : Int) : ℚ) := by
    push_cast
    ring
  rw [he, Int.ceil_add_intCast]
  omega

theorem max_first_integer_shift (q : ℚ) (m parent : Int) (scale : Nat) :
    max (parent + m * scale) (first (q + m) scale) =
      max parent (first q scale) + m * scale := by
  rw [first_integer_shift]
  omega

theorem min_last_integer_shift (q : ℚ) (m parent : Int) (scale : Nat) :
    min (parent + m * scale) (last (q + m) scale) =
      min parent (last q scale) + m * scale := by
  rw [last_integer_shift]
  omega

end HMT.I.RationalCellIntegerShift

#print axioms HMT.I.RationalCellIntegerShift.first_integer_shift
#print axioms HMT.I.RationalCellIntegerShift.last_integer_shift
#print axioms HMT.I.RationalCellIntegerShift.max_first_integer_shift
#print axioms HMT.I.RationalCellIntegerShift.min_last_integer_shift
