import Std

namespace HMTMD

theorem app_defect : 2025 - 810 = (459 - 405) + 9 * (174 - 45) := by
  decide

theorem hexad_incidence : 6 * (6 * 5 / 2) = 90 := by
  decide

theorem octad_incidence : 8 * (6 * 5 / 2) = 120 := by
  decide

theorem tower_180 : 2 * 90 = 180 := by decide
theorem tower_210 : 90 + 120 = 210 := by decide
theorem tower_240 : 2 * 120 = 240 := by decide
theorem tower_270 : 3 * 90 = 270 := by decide
theorem tower_360 : 3 * 120 = 360 := by decide
theorem tower_420 : 2 * (90 + 120) = 420 := by decide

theorem barbero_residue_diophantine : 4 * 12 - 3 * 1 = 45 := by
  decide

theorem electron_coefficients : 27 - 5 = 22 ∧ 3 * 5 = 15 := by
  decide

def ell (sC nu120 : Int) : Int := (sC + nu120) % 2

example : ell (-3) 0 = 1 := by native_decide
example : ell (-4) 1 = 1 := by native_decide
example : ell 1 2 = 1 := by native_decide

end HMTMD
