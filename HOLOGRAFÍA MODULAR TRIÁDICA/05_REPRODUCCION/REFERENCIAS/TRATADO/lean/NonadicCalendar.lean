import Std

/-! Identidades universales del calendario nonádico, capítulo 05. -/
namespace HMT.Calendar

def phase (k : Int) : Int := k % 9
def turns (k : Int) : Int := k / 9

theorem decomposition (k : Int) : k = 9 * turns k + phase k := by
  unfold turns phase
  omega

theorem phase_bounds (k : Int) : 0 ≤ phase k ∧ phase k < 9 := by
  unfold phase
  omega

theorem phase_return (k : Int) : phase (k + 9) = phase k := by
  unfold phase
  omega

theorem memory_advance (k : Int) : turns (k + 9) = turns k + 1 := by
  unfold turns
  omega

theorem inverse_boundary_zero (k : Int) (h : phase k = 0) :
    turns (-k) = -turns k := by
  unfold phase at h
  unfold turns
  omega

theorem inverse_boundary_interior (k : Int) (h : phase k ≠ 0) :
    turns (-k) = -turns k - 1 := by
  unfold phase at h
  unfold turns
  omega

theorem non_split_generator (a : Int) (hp : a % 9 = 1)
    (ho : (9 * a) % 108 = 0) : False := by
  omega

theorem carry_cocycle (r s u : Int) :
    (r + s) / 9 + ((r + s) % 9 + u) / 9 =
    (s + u) / 9 + (r + (s + u) % 9) / 9 := by
  omega

#print axioms decomposition
#print axioms phase_bounds
#print axioms phase_return
#print axioms memory_advance
#print axioms inverse_boundary_zero
#print axioms inverse_boundary_interior
#print axioms non_split_generator
#print axioms carry_cocycle

end HMT.Calendar
