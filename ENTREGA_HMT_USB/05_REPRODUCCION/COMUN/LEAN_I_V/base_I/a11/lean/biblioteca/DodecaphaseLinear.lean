/-
  Exact integral operators of registro_k.tex, subsections k-hadamard and
  k-transversal. Indices here are zero-based: the step-three orbits are
  (0,3,6,9), (1,4,7,10), (2,5,8,11), not three contiguous blocks.
  This is an internal linear reader on supplied Int-valued registers.
  It does not assert that an arbitrary register is produced by TPK events.
-/
import Std

namespace DodecaphaseLinear

abbrev Vector12 := Fin 12 → Int

def scale (a : Int) (v : Vector12) : Vector12 := fun i => a * v i

def H4 (v : Fin 4 → Int) (i : Fin 4) : Int :=
  match i.val with
  | 0 => v 0 + v 1 + v 2 + v 3
  | 1 => v 0 + v 1 - v 2 - v 3
  | 2 => v 0 - v 1 + v 2 - v 3
  | _ => v 0 - v 1 - v 2 + v 3

def orbitIndex (orbit : Fin 3) (sector : Fin 4) : Fin 12 :=
  ⟨orbit.val + 3 * sector.val, by omega⟩

def H12 (v : Vector12) (i : Fin 12) : Int :=
  match i.val with
  | 0 => v 0 + v 3 + v 6 + v 9
  | 1 => v 1 + v 4 + v 7 + v 10
  | 2 => v 2 + v 5 + v 8 + v 11
  | 3 => v 0 + v 3 - v 6 - v 9
  | 4 => v 1 + v 4 - v 7 - v 10
  | 5 => v 2 + v 5 - v 8 - v 11
  | 6 => v 0 - v 3 + v 6 - v 9
  | 7 => v 1 - v 4 + v 7 - v 10
  | 8 => v 2 - v 5 + v 8 - v 11
  | 9 => v 0 - v 3 - v 6 + v 9
  | 10 => v 1 - v 4 - v 7 + v 10
  | _ => v 2 - v 5 - v 8 + v 11

-- This identifies the displayed coordinate definition with the source's
-- P_orb^-1 (H4 ⊕ H4 ⊕ H4) P_orb, on every orbit and sector.
theorem H12_orbit_action (v : Vector12) (orbit : Fin 3) (sector : Fin 4) :
    H12 v (orbitIndex orbit sector) =
      H4 (fun j => v (orbitIndex orbit j)) sector := by
  have ho : orbit = 0 ∨ orbit = 1 ∨ orbit = 2 := by omega
  have hs : sector = 0 ∨ sector = 1 ∨ sector = 2 ∨ sector = 3 := by omega
  rcases ho with h | h | h
  all_goals subst orbit
  all_goals rcases hs with h | h | h | h
  all_goals subst sector; rfl

theorem H4_square (v : Fin 4 → Int) (i : Fin 4) : H4 (H4 v) i = 4 * v i := by
  have hi : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by omega
  rcases hi with h | h | h | h
  all_goals subst i; simp only [H4]; omega

theorem fin12_cases (i : Fin 12) :
    i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨
    i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 := by
  omega

theorem H12_square_pointwise (v : Vector12) (i : Fin 12) :
    H12 (H12 v) i = 4 * v i := by
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i; simp only [H12]; omega

theorem H12_square (v : Vector12) : H12 (H12 v) = scale 4 v := by
  funext i
  exact H12_square_pointwise v i

theorem H12_injective (u v : Vector12) (h : H12 u = H12 v) : u = v := by
  funext i
  have hh := congrArg (fun w : Vector12 => H12 w i) h
  dsimp only at hh
  rw [H12_square_pointwise, H12_square_pointwise] at hh
  omega

theorem H12_add (u v : Vector12) :
    H12 (fun i => u i + v i) = fun i => H12 u i + H12 v i := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i; simp only [H12]; omega

theorem H12_scale (a : Int) (v : Vector12) : H12 (scale a v) = scale a (H12 v) := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i; simp only [H12, scale, Int.mul_add, Int.mul_sub]

-- The inverse is stated as an exact integral equation, without unsafe division.
theorem inverse_equation (u k : Vector12) :
    H12 k = u ↔ scale 4 k = H12 u := by
  constructor
  · intro h
    rw [← h, H12_square]
  · intro h
    apply H12_injective
    rw [H12_square, h]

def InImage (u : Vector12) : Prop := ∃ k : Vector12, H12 k = u

theorem image_iff_integral_equation (u : Vector12) :
    InImage u ↔ ∃ k : Vector12, scale 4 k = H12 u := by
  constructor
  · rintro ⟨k, hk⟩
    exact ⟨k, (inverse_equation u k).mp hk⟩
  · rintro ⟨k, hk⟩
    exact ⟨k, (inverse_equation u k).mpr hk⟩

theorem inverse_unique (u k l : Vector12)
    (hk : scale 4 k = H12 u) (hl : scale 4 l = H12 u) : k = l := by
  apply H12_injective
  exact ((inverse_equation u k).mpr hk).trans ((inverse_equation u l).mpr hl).symm

-- A witnessed image carries its actual integral inverse, not an arbitrary root.
structure ImageRegister where
  signed : Vector12
  integral : Vector12
  equation : H12 integral = signed

theorem image_register_inverse (r : ImageRegister) :
    scale 4 r.integral = H12 r.signed :=
  (inverse_equation r.signed r.integral).mp r.equation

def shift (step : Nat) (i : Fin 12) : Fin 12 :=
  ⟨(i.val + step) % 12, Nat.mod_lt _ (by decide)⟩

def D3 (v : Vector12) : Vector12 := fun i => v i - v (shift 3 i)
def D4 (v : Vector12) : Vector12 := fun i => v i - v (shift 4 i)

def Q (v : Vector12) : Int :=
  v 0 + v 1 + v 2 + v 3 + v 4 + v 5 +
  v 6 + v 7 + v 8 + v 9 + v 10 + v 11

-- Eleven concrete edges form a spanning tree of the step-three/step-four graph.
-- The argument is universal in v; only the fixed index set is enumerated.
theorem joint_kernel_constant (v : Vector12)
    (h3 : D3 v = fun _ => 0) (h4 : D4 v = fun _ => 0) :
    ∀ i : Fin 12, v i = v 0 := by
  have e3 (j : Fin 12) : v j = v (shift 3 j) := by
    have h := congrArg (fun w : Vector12 => w j) h3
    change v j - v (shift 3 j) = 0 at h
    omega
  have e4 (j : Fin 12) : v j = v (shift 4 j) := by
    have h := congrArg (fun w : Vector12 => w j) h4
    change v j - v (shift 4 j) = 0 at h
    omega
  have h03 : v 0 = v 3 := e3 0
  have h14 : v 1 = v 4 := e3 1
  have h25 : v 2 = v 5 := e3 2
  have h36 : v 3 = v 6 := e3 3
  have h47 : v 4 = v 7 := e3 4
  have h58 : v 5 = v 8 := e3 5
  have h69 : v 6 = v 9 := e3 6
  have h710 : v 7 = v 10 := e3 7
  have h811 : v 8 = v 11 := e3 8
  have h04 : v 0 = v 4 := e4 0
  have h15 : v 1 = v 5 := e4 1
  intro i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i; omega

theorem D3_sub (u v : Vector12) :
    D3 (fun i => u i - v i) = fun i => D3 u i - D3 v i := by
  funext i
  simp only [D3]
  omega

theorem D4_sub (u v : Vector12) :
    D4 (fun i => u i - v i) = fun i => D4 u i - D4 v i := by
  funext i
  simp only [D4]
  omega

theorem Q_sub (u v : Vector12) :
    Q (fun i => u i - v i) = Q u - Q v := by
  simp only [Q]
  omega

theorem Q_constant (c : Int) : Q (fun _ => c) = 12 * c := by
  simp only [Q]
  omega

theorem same_differences_constant (u v : Vector12)
    (h3 : D3 u = D3 v) (h4 : D4 u = D4 v) :
    ∀ i : Fin 12, u i - v i = u 0 - v 0 := by
  apply joint_kernel_constant (fun i => u i - v i)
  · rw [D3_sub, h3]
    funext i
    omega
  · rw [D4_sub, h4]
    funext i
    omega

-- The total charge removes the sole constant-vector ambiguity.
theorem transversal_injective (u v : Vector12)
    (h3 : D3 u = D3 v) (h4 : D4 u = D4 v) (hq : Q u = Q v) : u = v := by
  have hc := same_differences_constant u v h3 h4
  have hf : (fun i => u i - v i) = (fun _ => u 0 - v 0) := funext hc
  have hs := Q_sub u v
  rw [hf, Q_constant, hq] at hs
  have hz : u 0 - v 0 = 0 := by omega
  funext i
  have hi := hc i
  omega

#print axioms H12_orbit_action
#print axioms H4_square
#print axioms fin12_cases
#print axioms H12_square_pointwise
#print axioms H12_square
#print axioms H12_injective
#print axioms H12_add
#print axioms H12_scale
#print axioms inverse_equation
#print axioms image_iff_integral_equation
#print axioms inverse_unique
#print axioms image_register_inverse
#print axioms joint_kernel_constant
#print axioms D3_sub
#print axioms D4_sub
#print axioms Q_sub
#print axioms Q_constant
#print axioms same_differences_constant
#print axioms transversal_injective

end DodecaphaseLinear
