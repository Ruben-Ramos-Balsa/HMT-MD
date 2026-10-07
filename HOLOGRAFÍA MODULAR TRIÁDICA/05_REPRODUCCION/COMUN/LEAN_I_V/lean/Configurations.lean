import Frozen.VFactores
import Frozen.VFermiones

/-! Binary configurations with one coordinate for every ordered mode.
This module gives the old weight enumeration an explicit state space. It uses
the original finite factorization proof rather than copying its induction.
-/

namespace HMT.FockBridge

def Occupation : Nat → Type
  | 0 => Unit
  | n + 1 => Bool × Occupation n

def allStates : (n : Nat) → List (Occupation n)
  | 0 => [()]
  | n + 1 => (allStates n).map (fun s => (false, s)) ++
      (allStates n).map (fun s => (true, s))

theorem every_state_enumerated (n : Nat) (s : Occupation n) : s ∈ allStates n := by
  induction n with
  | zero => cases s; simp [allStates]
  | succ n ih =>
    rcases s with ⟨b, tail⟩
    cases b with
    | false => exact List.mem_append_left _ (List.mem_map_of_mem (ih tail))
    | true => exact List.mem_append_right _ (List.mem_map_of_mem (ih tail))

theorem enumeration_size (n : Nat) : (allStates n).length = 2 ^ n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [allStates, ih, Nat.pow_succ, Nat.mul_comm, Nat.two_mul]

def stateWeight {R : Type} [One R] [Mul R] : (us : List R) → Occupation us.length → R
  | [], _ => 1
  | u :: us, (b, tail) => if b then u * stateWeight us tail else stateWeight us tail

/-- The original weights have exactly the same order and multiplicity as these states. -/
theorem evaluation_matches_original (us : List Int) :
    (allStates us.length).map (stateWeight us) = VFactores.weights us := by
  induction us with
  | nil => rfl
  | cons u us ih =>
    simp only [List.length_cons, allStates, List.map_append, List.map_map]
    change (allStates us.length).map (stateWeight us) ++
      (allStates us.length).map (fun s => u * stateWeight us s) = _
    rw [show (allStates us.length).map (fun s => u * stateWeight us s) =
        ((allStates us.length).map (stateWeight us)).map (fun x => u * x) by
      rw [List.map_map]; rfl]
    rw [ih]
    rfl

/-- Reuse of the delivered certificate, now as a sum over actual configurations. -/
theorem original_partition_is_state_sum (us : List Int) :
    VFactores.total ((allStates us.length).map (stateWeight us)) = VFactores.factors us := by
  rw [evaluation_matches_original]
  exact VFactores.finite_fermionic_factorization us

def twoModeBasis (s : Bool × Bool) : VFermiones.State :=
  match s with
  | (false, false) => (1, 0, 0, 0)
  | (true, false) => (0, 1, 0, 0)
  | (false, true) => (0, 0, 1, 0)
  | (true, true) => (0, 0, 0, 1)

def bitValue (b : Bool) : Int := if b then 1 else 0

/-- The existing number operators really read these binary basis labels. -/
theorem two_mode_number_reads_bit (mode : Bool) (s : Bool × Bool) :
    VFermiones.number mode (twoModeBasis s) =
      VFermiones.scale (bitValue (if mode then s.2 else s.1)) (twoModeBasis s) := by
  rcases s with ⟨a, b⟩
  cases mode <;> cases a <;> cases b <;>
    rfl

theorem two_mode_idempotence (mode : Bool) (x : VFermiones.State) :
    VFermiones.number mode (VFermiones.number mode x) = VFermiones.number mode x :=
  VFermiones.occupation_idempotent mode x

theorem two_mode_basis_reconstructs (x : VFermiones.State) :
    VFermiones.plus (VFermiones.scale x.1 (twoModeBasis (false, false)))
      (VFermiones.plus (VFermiones.scale x.2.1 (twoModeBasis (true, false)))
        (VFermiones.plus (VFermiones.scale x.2.2.1 (twoModeBasis (false, true)))
          (VFermiones.scale x.2.2.2 (twoModeBasis (true, true))))) = x := by
  rcases x with ⟨a, b, c, d⟩
  simp [VFermiones.plus, VFermiones.scale, twoModeBasis]

#print axioms every_state_enumerated
#print axioms enumeration_size
#print axioms evaluation_matches_original
#print axioms original_partition_is_state_sum
#print axioms two_mode_number_reads_bit
#print axioms two_mode_basis_reconstructs

end HMT.FockBridge
