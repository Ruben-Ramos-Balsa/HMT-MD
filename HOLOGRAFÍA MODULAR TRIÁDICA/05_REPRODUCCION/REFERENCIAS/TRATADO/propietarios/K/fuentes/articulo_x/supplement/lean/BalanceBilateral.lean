import Std

/-!
Formalización focal de la identidad bilateral en coordenadas enteras.
Los coeficientes 8, 9, 72, 73 y 17 corresponden a la ley ya expuesta.
Este archivo no formaliza la producción de esos operadores desde APP--TRIT--TPK.
-/

namespace HMT.Bilateral

theorem balance_polynomial (x y : Int) :
    9 * ((8 * x - y) * (8 * x - y)) +
      8 * ((9 * x + y) * (9 * x + y)) =
    17 * (72 * (x * x) + y * y) := by
  simp only [Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul]
  simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  simp only [← Int.mul_assoc]
  omega

theorem scalar_norm_preserving (x y : Int) (h : y * y = x * x) :
    9 * ((8 * x - y) * (8 * x - y)) +
      8 * ((9 * x + y) * (9 * x + y)) =
    17 * 73 * (x * x) := by
  rw [balance_polynomial, h]
  omega

/-- Suma de cuadrados de las primeras `n` coordenadas enteras. -/
def squareSum : Nat → (Nat → Int) → Int
  | 0, _ => 0
  | n + 1, x => squareSum n x + x n * x n

/-- Energía de los dos registros, con pesos 9 y 8. -/
def recordedEnergy : Nat → (Nat → Int) → (Nat → Int) → Int
  | 0, _, _ => 0
  | n + 1, x, y => recordedEnergy n x y +
      (9 * ((8 * x n - y n) * (8 * x n - y n)) +
       8 * ((9 * x n + y n) * (9 * x n + y n)))

/-- Balance válido para toda dimensión finita y todo par de vectores enteros. -/
theorem finite_balance (n : Nat) (x y : Nat → Int) :
    recordedEnergy n x y = 17 * (72 * squareSum n x + squareSum n y) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [recordedEnergy, squareSum, balance_polynomial, ih]
      omega

/-- Especialización a un transporte que preserva la suma de cuadrados. -/
theorem finite_norm_preserving (n : Nat) (x y : Nat → Int)
    (h : squareSum n y = squareSum n x) :
    recordedEnergy n x y = 17 * 73 * squareSum n x := by
  rw [finite_balance, h]
  omega

/-- Recuperación sin división: la suma de ambos registros determina 17x. -/
theorem recovery_x (x y : Int) :
    (8 * x - y) + (9 * x + y) = 17 * x := by
  omega

/-- Recuperación sin división: esta combinación determina 17y. -/
theorem recovery_y (x y : Int) :
    8 * (9 * x + y) - 9 * (8 * x - y) = 17 * y := by
  omega

/-- El par completo de registros conserva exactamente ambas entradas enteras. -/
theorem readers_injective (x y x' y' : Int)
    (hminus : 8 * x - y = 8 * x' - y')
    (hplus : 9 * x + y = 9 * x' + y') :
    x = x' ∧ y = y' := by
  omega

end HMT.Bilateral

#print axioms HMT.Bilateral.balance_polynomial
#print axioms HMT.Bilateral.scalar_norm_preserving
#print axioms HMT.Bilateral.finite_balance
#print axioms HMT.Bilateral.finite_norm_preserving
#print axioms HMT.Bilateral.recovery_x
#print axioms HMT.Bilateral.recovery_y
#print axioms HMT.Bilateral.readers_injective
