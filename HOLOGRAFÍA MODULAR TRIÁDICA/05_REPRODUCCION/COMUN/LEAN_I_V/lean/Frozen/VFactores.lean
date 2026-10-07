import Std

/-! Factorización fermiónica finita, para cualquier lista de pesos enteros.
No evalúa exponenciales, derivadas, límites ni la serie bosónica infinita.
Propietario: V, 50_estadisticas_ocupacion.tex, líneas 72–111.
-/
namespace HMT.VFactores

def total : List Int → Int
  | [] => 0
  | x :: xs => x + total xs

/-- One term for every binary occupation, retaining multiplicity. -/
def weights : List Int → List Int
  | [] => [1]
  | u :: us => weights us ++ (weights us).map (fun x => u*x)

def factors : List Int → Int
  | [] => 1
  | u :: us => (1+u) * factors us

theorem total_append (xs ys : List Int) : total (xs ++ ys) = total xs + total ys := by
  induction xs with
  | nil => simp [total]
  | cons x xs ih => simp [total, ih, Int.add_assoc]

theorem total_map_mul (u : Int) (xs : List Int) :
    total (xs.map (fun x => u*x)) = u * total xs := by
  induction xs with
  | nil => simp [total]
  | cons x xs ih => simp [total, ih, Int.mul_add]

theorem finite_fermionic_factorization (us : List Int) : total (weights us) = factors us := by
  induction us with
  | nil => simp [weights, total, factors]
  | cons u us ih =>
    simp only [weights, total_append, total_map_mul, ih, factors, Int.add_mul, Int.one_mul]

theorem number_of_configurations (us : List Int) : (weights us).length = 2 ^ us.length := by
  induction us with
  | nil => rfl
  | cons u us ih => simp [weights, ih, Nat.pow_succ, Nat.mul_comm, Nat.two_mul]

end HMT.VFactores

#print axioms HMT.VFactores.total_append
#print axioms HMT.VFactores.total_map_mul
#print axioms HMT.VFactores.finite_fermionic_factorization
#print axioms HMT.VFactores.number_of_configurations
