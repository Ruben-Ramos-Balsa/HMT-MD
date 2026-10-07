import N30FamilyPublication
import IntegralEventRegister

/-!
Composition of an explicitly declared finite N30 family with the integral
channel reader. Routes and directed impact words are evaluated first; no
expected register or signed-channel vector is an input. This module does not
select the canonical terminal family.

Merging families is a union with their original event times, not temporal
concatenation. Integer event counts add. Published decimal digits require the
carry correction proved below and must not be treated as additive registers.
-/
namespace HMT.N30IntegralComposition

open DodecaphaseLinear IncidenceRegister TerminalChannels IntegralEventRegister
open N30FamilyPublication

def publishedVector (f : Family) : Vector12 := blocks (familyLedger f)

def publishedChannels (f : Family) : Channels := channels (familyLedger f)

def integralData (f : Family) : Contribution where
  increments := delta (publishedChannels f)
  charge := (publishedChannels f).charge
  compatible := by
    change admissible (delta (extract (publishedVector f))) (Q (publishedVector f))
    rw [delta_extract]
    exact adjacent_admissible _

theorem integral_compatibility (f : Family) :
    (publishedChannels f).b90 = sum3 (integralData f).increments ∧
    Q (integralData f).increments = 0 ∧
    ((integralData f).charge + totalPrefix (integralData f).increments) % 12 = 0 := by
  have h := (compatible_iff_integral_conditions (publishedChannels f)).mp
    (channels_compatible (familyLedger f))
  exact ⟨h.1, h.2.1, h.2.2⟩

theorem reconstruct_published (f : Family) :
    (integralData f).register = publishedVector f := by
  change reconstruct (delta (extract (publishedVector f))) (Q (publishedVector f)) = _
  rw [delta_extract, reconstruct_adjacent]

theorem harmonic_reconstruction_agrees (f : Family) :
    recover (publishedChannels f) = (integralData f).register :=
  recover_eq_reconstruct _ (channels_compatible (familyLedger f))

theorem reconstructed_event_formula (f : Family) (m : Fin 12) :
    (integralData f).register m =
      (100 * digit10 ((f.routes.map (fun r => A (N30VisitLedger.ledger r) m)).sum) +
        10 * digit10 ((f.pairs.map (fun p => pairContribution p m)).sum) +
        digit10 ((f.routes.map (fun r => V (N30VisitLedger.ledger r) m)).sum) : Nat) := by
  rw [reconstruct_published]
  change (block (familyLedger f) m : Int) = _
  exact congrArg (fun n : Nat => (n : Int)) (family_block f m)

theorem reconstructed_digit (f : Family) (m : Fin 12) :
    (integralData f).register m =
      ((register (familyLedger f)).digits[m.val]'(by
        rw [(register (familyLedger f)).length_eq]; exact m.isLt) : Int) := by
  rw [register_digit, reconstruct_published]
  rfl

theorem family_integral_end_to_end (f : Family) :
    Compatible (publishedChannels f) ∧
    admissible (integralData f).increments (integralData f).charge ∧
    (integralData f).register = publishedVector f ∧
    recover (publishedChannels f) = (integralData f).register ∧
    RadixRecovery.decode 1000 12 (register (familyLedger f)).publish =
      (register (familyLedger f)).digits := by
  exact ⟨channels_compatible _, (integralData f).compatible,
    reconstruct_published f, harmonic_reconstruction_agrees f,
    family_publication_reversible f⟩

/-- Union of two families on the same boundary, preserving their original times. -/
def merge (f g : Family) (h : g.boundary = f.boundary) : Family where
  routes := f.routes ++ g.routes
  routes_nonempty := by
    intro he
    exact f.routes_nonempty (List.append_eq_nil_iff.mp he).1
  pairs := f.pairs ++ g.pairs
  boundary := f.boundary
  shared_boundary := by
    intro r hr
    rcases List.mem_append.mp hr with hr | hr
    · exact f.shared_boundary r hr
    · exact (g.shared_boundary r hr).trans h

theorem merge_counts (f g : Family) (h : g.boundary = f.boundary) (m : Fin 12) :
    A (familyLedger (merge f g h)) m = A (familyLedger f) m + A (familyLedger g) m ∧
    C (familyLedger (merge f g h)) m = C (familyLedger f) m + C (familyLedger g) m ∧
    V (familyLedger (merge f g h)) m = V (familyLedger f) m + V (familyLedger g) m := by
  simp only [family_A, family_C, family_V, merge, List.map_append, List.sum_append,
    and_self]

def carryCorrection (x y : Int) : Int := carry10 (x + y) - carry10 x - carry10 y

theorem digit_add_with_carry (x y : Int) :
    (digit10 (x + y) : Int) = (digit10 x : Int) + (digit10 y : Int) -
      10 * carryCorrection x y := by
  have hx := decimal_reconstruct x
  have hy := decimal_reconstruct y
  have hs := decimal_reconstruct (x + y)
  unfold carryCorrection
  omega

def mergerCarry (f g : Family) : Vector12 := fun m =>
  1000 * carryCorrection (A (familyLedger f) m) (A (familyLedger g) m) +
   100 * carryCorrection (C (familyLedger f) m) (C (familyLedger g) m) +
    10 * carryCorrection (V (familyLedger f) m) (V (familyLedger g) m)

theorem merge_publication_with_carry (f g : Family) (h : g.boundary = f.boundary) :
    publishedVector (merge f g h) =
      fun m => publishedVector f m + publishedVector g m - mergerCarry f g m := by
  funext m
  have hc := merge_counts f g h m
  simp only [publishedVector, blocks, block, Nat.cast_add, Nat.cast_mul,
    Nat.cast_ofNat, hc.1, hc.2.1, hc.2.2, digit_add_with_carry, mergerCarry]
  ring

/-- Actual change in the published vector, including its decimal normalization. -/
def mergerIncrement (f g : Family) : Vector12 :=
  fun m => publishedVector g m - mergerCarry f g m

def mergerContribution (f g : Family) : Contribution where
  increments := adjacent (mergerIncrement f g)
  charge := Q (mergerIncrement f g)
  compatible := adjacent_admissible _

theorem mergerContribution_register (f g : Family) :
    (mergerContribution f g).register = mergerIncrement f g :=
  reconstruct_adjacent _

theorem merge_integral_accumulation (f g : Family) (h : g.boundary = f.boundary) :
    ((integralData f).add (mergerContribution f g)).register =
      publishedVector (merge f g h) := by
  rw [register_add, reconstruct_published, mergerContribution_register,
    merge_publication_with_carry]
  funext m
  simp only [mergerIncrement]
  omega

theorem merged_channels_reconstructed (f g : Family) (h : g.boundary = f.boundary) :
    extract (((integralData f).add (mergerContribution f g)).register) =
      publishedChannels (merge f g h) := by
  rw [merge_integral_accumulation]
  rfl

theorem merge_reconstruction_unique (f g : Family) (h : g.boundary = f.boundary)
    (z : Vector12) (hz : extract z = publishedChannels (merge f g h)) :
    z = ((integralData f).add (mergerContribution f g)).register := by
  apply extract_injective
  rw [merged_channels_reconstructed]
  exact hz

#print axioms integral_compatibility
#print axioms reconstruct_published
#print axioms harmonic_reconstruction_agrees
#print axioms reconstructed_event_formula
#print axioms reconstructed_digit
#print axioms family_integral_end_to_end
#print axioms merge_counts
#print axioms digit_add_with_carry
#print axioms merge_publication_with_carry
#print axioms mergerContribution_register
#print axioms merge_integral_accumulation
#print axioms merged_channels_reconstructed
#print axioms merge_reconstruction_unique

end HMT.N30IntegralComposition
