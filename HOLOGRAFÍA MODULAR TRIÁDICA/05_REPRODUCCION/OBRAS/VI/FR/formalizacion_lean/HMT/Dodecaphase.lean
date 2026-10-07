/-! Microcomprobaciones exactas del vector dodecafásico canónico. -/

namespace HMT

def K : Fin 12 → Int
  | 0 => 234 | 1 => 543 | 2 => 140 | 3 => 729
  | 4 => 659 | 5 => 824 | 6 => 621 | 7 => 58
  | 8 => 914 | 9 => 794 | 10 => 146 | 11 => 601

def U : Fin 12 → Int
  | 0 => 2378 | 1 => 1406 | 2 => 2479 | 3 => -452
  | 4 => 998 | 5 => -551 | 6 => -668 | 7 => -204
  | 8 => -371 | 9 => -322 | 10 => -28 | 11 => -997

def sum12 (f : Fin 12 → Int) : Int :=
  f 0 + f 1 + f 2 + f 3 + f 4 + f 5 +
  f 6 + f 7 + f 8 + f 9 + f 10 + f 11

theorem canonical_charge : sum12 K = 6263 := by decide

def h4Block (a b c d : Int) : Int × Int × Int × Int :=
  (a + b + c + d,
   a + b - c - d,
   a - b + c - d,
   a - b - c + d)

theorem hadamard_orbit_one :
    h4Block (K 0) (K 3) (K 6) (K 9) =
      (U 0, U 3, U 6, U 9) := by decide

theorem hadamard_orbit_two :
    h4Block (K 1) (K 4) (K 7) (K 10) =
      (U 1, U 4, U 7, U 10) := by decide

theorem hadamard_orbit_three :
    h4Block (K 2) (K 5) (K 8) (K 11) =
      (U 2, U 5, U 8, U 11) := by decide

def vAlphaCoeff : Fin 12 → Int
  | 0 => 4
  | _ => 1

theorem v_alpha_norm_is_54 :
    2 * sum12 (fun i => vAlphaCoeff i * vAlphaCoeff i) = 54 := by decide

theorem v_alpha_is_isotropic_mod_18 :
    (2 * sum12 (fun i => vAlphaCoeff i * vAlphaCoeff i)) % 18 = 0 := by decide

def spectralWeights : Nat × Nat := (9, 5)

theorem spectral_jump_is_four :
    spectralWeights.1 - spectralWeights.2 = 4 := by native_decide

def typedHierarchy : List Nat := [4, 2, 6, 54]

theorem typed_hierarchy_begins_at_jump :
    typedHierarchy.head? = some 4 := by native_decide

theorem typed_hierarchy_terminates_at_54 :
    typedHierarchy.getLast? = some 54 := by native_decide

end HMT
