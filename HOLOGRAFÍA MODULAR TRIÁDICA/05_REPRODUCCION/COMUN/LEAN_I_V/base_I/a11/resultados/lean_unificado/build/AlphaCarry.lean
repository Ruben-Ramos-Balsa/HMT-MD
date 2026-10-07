import Std

/- Finite signed positional closure, from alpha.tex:
   eq:alpha-recurrencia and prop:alpha-telescopia.
   Supplied blocks are inputs of this downstream reader, not target constants.
   Analytic/root realization and the compatible infinite tail are separate. -/
namespace AlphaCarry

def normalizeDigit (balance incoming : Int) : Int := (balance + incoming) % 1000
def normalizeCarry (balance incoming : Int) : Int := (balance + incoming) / 1000

theorem local_reconstruction (balance incoming : Int) :
    normalizeDigit balance incoming + 1000 * normalizeCarry balance incoming =
      balance + incoming := by
  exact Int.emod_add_ediv _ _

theorem local_digit_bounds (balance incoming : Int) :
    0 ≤ normalizeDigit balance incoming ∧ normalizeDigit balance incoming < 1000 := by
  unfold normalizeDigit
  omega

theorem local_uniqueness (balance incoming digit carry : Int)
    (hlow : 0 ≤ digit) (hhigh : digit < 1000)
    (h : digit + 1000 * carry = balance + incoming) :
    digit = normalizeDigit balance incoming ∧ carry = normalizeCarry balance incoming := by
  have he := local_reconstruction balance incoming
  have hb := local_digit_bounds balance incoming
  omega

theorem local_balance (balance incoming : Int) :
    balance - normalizeDigit balance incoming =
      1000 * normalizeCarry balance incoming - incoming := by
  have := local_reconstruction balance incoming
  omega

structure Closure where
  digits : List Int
  outgoing : Int
  carries : List Int

def close : List Int → Int → Closure
  | [], incoming => ⟨[], incoming, [incoming]⟩
  | z :: zs, incoming =>
    let tail := close zs incoming
    let d := normalizeDigit z tail.outgoing
    let c := normalizeCarry z tail.outgoing
    ⟨d :: tail.digits, c, c :: tail.carries⟩

def evaluate : List Int → Int
  | [] => 0
  | z :: zs => z * 1000 ^ zs.length + evaluate zs

theorem close_length (zs : List Int) (incoming : Int) :
    (close zs incoming).digits.length = zs.length := by
  induction zs with
  | nil => rfl
  | cons z zs ih => simp only [close, List.length_cons, ih]

theorem close_carries_length (zs : List Int) (incoming : Int) :
    (close zs incoming).carries.length = zs.length + 1 := by
  induction zs with
  | nil => rfl
  | cons z zs ih => simp only [close, List.length_cons, ih]

theorem close_digit_bounds (zs : List Int) (incoming : Int) :
    ∀ d ∈ (close zs incoming).digits, 0 ≤ d ∧ d < 1000 := by
  induction zs with
  | nil => simp [close]
  | cons z zs ih =>
    intro d hd
    cases hd with
    | head => exact local_digit_bounds _ _
    | tail _ hm => exact ih d hm

theorem closure_conservation (zs : List Int) (incoming : Int) :
    evaluate (close zs incoming).digits + 1000 ^ zs.length * (close zs incoming).outgoing =
      evaluate zs + incoming := by
  induction zs with
  | nil => simp [close, evaluate]
  | cons z zs ih =>
    simp only [close, evaluate, close_length, List.length_cons, Int.pow_succ]
    have hl := local_reconstruction z (close zs incoming).outgoing
    have hlscaled := congrArg (fun t : Int => 1000 ^ zs.length * t) hl
    simp only [Int.mul_add, Int.mul_assoc] at hlscaled
    simp only [Int.mul_assoc]
    rw [Int.mul_comm (normalizeDigit z (close zs incoming).outgoing) (1000 ^ zs.length)]
    rw [Int.mul_comm z (1000 ^ zs.length)]
    omega

theorem closure_telescoping (zs : List Int) (incoming : Int) :
    evaluate zs - evaluate (close zs incoming).digits =
      1000 ^ zs.length * (close zs incoming).outgoing - incoming := by
  have := closure_conservation zs incoming
  omega

-- Two normalizations with different right boundaries retain their exact difference.
theorem boundary_change (zs : List Int) (leftBoundary rightBoundary : Int) :
    evaluate (close zs leftBoundary).digits - evaluate (close zs rightBoundary).digits =
      leftBoundary - rightBoundary - 1000 ^ zs.length *
        ((close zs leftBoundary).outgoing - (close zs rightBoundary).outgoing) := by
  have h1 := closure_conservation zs leftBoundary
  have h2 := closure_conservation zs rightBoundary
  rw [Int.mul_sub]
  omega

structure InputBlock where
  p : Int
  e : Int
  phi : Int
  k : Int

def InputBlock.balance (z : InputBlock) : Int := z.p + z.e - z.phi - z.k

theorem balance_evaluation (zs : List InputBlock) :
    evaluate (zs.map InputBlock.balance) =
      evaluate (zs.map InputBlock.p) + evaluate (zs.map InputBlock.e) -
      evaluate (zs.map InputBlock.phi) - evaluate (zs.map InputBlock.k) := by
  induction zs with
  | nil => simp [evaluate]
  | cons z zs ih =>
    simp only [List.map_cons, evaluate, List.length_map, InputBlock.balance, ih,
      Int.add_mul, Int.sub_mul]
    omega

theorem alpha_finite_identity (zs : List InputBlock) (incoming : Int) :
    evaluate (zs.map InputBlock.p) + evaluate (zs.map InputBlock.e) -
      evaluate (zs.map InputBlock.phi) - evaluate (zs.map InputBlock.k) -
      evaluate (close (zs.map InputBlock.balance) incoming).digits =
      1000 ^ zs.length * (close (zs.map InputBlock.balance) incoming).outgoing - incoming := by
  have h := closure_telescoping (zs.map InputBlock.balance) incoming
  simpa [balance_evaluation, List.length_map] using h

theorem recover_register_coordinate (z : InputBlock) (incoming : Int) :
    z.k = z.p + z.e - z.phi + incoming - normalizeDigit z.balance incoming -
      1000 * normalizeCarry z.balance incoming := by
  have h : normalizeDigit z.balance incoming + 1000 * normalizeCarry z.balance incoming =
      z.p + z.e - z.phi - z.k + incoming := local_reconstruction z.balance incoming
  omega

theorem recover_register_evaluation (zs : List InputBlock) (incoming : Int) :
    evaluate (zs.map InputBlock.k) =
      evaluate (zs.map InputBlock.p) + evaluate (zs.map InputBlock.e) -
      evaluate (zs.map InputBlock.phi) -
      evaluate (close (zs.map InputBlock.balance) incoming).digits -
      1000 ^ zs.length * (close (zs.map InputBlock.balance) incoming).outgoing + incoming := by
  have h := alpha_finite_identity zs incoming
  omega

#print axioms local_reconstruction
#print axioms local_digit_bounds
#print axioms local_uniqueness
#print axioms local_balance
#print axioms close_length
#print axioms close_carries_length
#print axioms close_digit_bounds
#print axioms closure_conservation
#print axioms closure_telescoping
#print axioms boundary_change
#print axioms balance_evaluation
#print axioms alpha_finite_identity
#print axioms recover_register_coordinate
#print axioms recover_register_evaluation

end AlphaCarry
