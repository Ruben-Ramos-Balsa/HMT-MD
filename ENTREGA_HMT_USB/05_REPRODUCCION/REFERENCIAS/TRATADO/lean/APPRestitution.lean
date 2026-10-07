import Std

/-!
Restitución aritmética de la representación positiva nonádica.

Correspondencia con source/chapters/01_app.tex:
  def:app-residuo, eq:app-rho-q, thm:app-reconstruccion.
El dominio sustantivo es Nat positivo. Los representantes residuales pertenecen
al intervalo entero cerrado de uno a nueve; el cociente pertenece a Nat.
-/

namespace HMT.APP

def rho9 (n : Nat) : Nat := (n - 1) % 9 + 1

def q9 (n : Nat) : Nat := (n - 1) / 9

theorem rho9_bounds (n : Nat) : 1 ≤ rho9 n ∧ rho9 n ≤ 9 := by
  unfold rho9
  omega

theorem reconstruct (n : Nat) (hn : 0 < n) : n = rho9 n + 9 * q9 n := by
  unfold rho9 q9
  omega

theorem recover_residue (r q : Nat) (hr1 : 1 ≤ r) (hr9 : r ≤ 9) :
    rho9 (r + 9 * q) = r := by
  unfold rho9
  omega

theorem recover_quotient (r q : Nat) (hr1 : 1 ≤ r) (hr9 : r ≤ 9) :
    q9 (r + 9 * q) = q := by
  unfold q9
  omega

theorem reconstruction_unique (n r q : Nat) (hn : 0 < n)
    (hr1 : 1 ≤ r) (hr9 : r ≤ 9) (heq : n = r + 9 * q) :
    rho9 n = r ∧ q9 n = q := by
  subst n
  exact ⟨recover_residue r q hr1 hr9, recover_quotient r q hr1 hr9⟩

abbrev Positive := { n : Nat // 0 < n }

abbrev Digit9 := { r : Nat // 1 ≤ r ∧ r ≤ 9 }

def encode (n : Positive) : Digit9 × Nat :=
  (⟨rho9 n.val, rho9_bounds n.val⟩, q9 n.val)

def decode (rq : Digit9 × Nat) : Positive :=
  ⟨rq.1.val + 9 * rq.2, by have hr := rq.1.property.1; omega⟩

theorem decode_encode (n : Positive) : decode (encode n) = n := by
  apply Subtype.ext
  change rho9 n.val + 9 * q9 n.val = n.val
  exact (reconstruct n.val n.property).symm

theorem encode_decode (rq : Digit9 × Nat) : encode (decode rq) = rq := by
  rcases rq with ⟨⟨r, hr⟩, q⟩
  apply Prod.ext
  · apply Subtype.ext
    change rho9 (r + 9 * q) = r
    exact recover_residue r q hr.1 hr.2
  · change q9 (r + 9 * q) = q
    exact recover_quotient r q hr.1 hr.2

theorem encode_injective (n m : Positive) (h : encode n = encode m) : n = m := by
  calc
    n = decode (encode n) := (decode_encode n).symm
    _ = decode (encode m) := congrArg decode h
    _ = m := decode_encode m

theorem encode_surjective (rq : Digit9 × Nat) : ∃ n : Positive, encode n = rq := by
  exact ⟨decode rq, encode_decode rq⟩

theorem encode_bijective :
    (∀ n m : Positive, encode n = encode m → n = m) ∧
    (∀ rq : Digit9 × Nat, ∃ n : Positive, encode n = rq) := by
  exact ⟨encode_injective, encode_surjective⟩

#print axioms rho9_bounds
#print axioms reconstruct
#print axioms recover_residue
#print axioms recover_quotient
#print axioms reconstruction_unique
#print axioms decode_encode
#print axioms encode_decode
#print axioms encode_injective
#print axioms encode_surjective
#print axioms encode_bijective

end HMT.APP
