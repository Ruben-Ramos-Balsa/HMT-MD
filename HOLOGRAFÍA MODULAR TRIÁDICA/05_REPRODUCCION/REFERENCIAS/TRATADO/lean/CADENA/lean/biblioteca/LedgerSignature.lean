import Route108Events

/-! Article VI, section 05: deterministic five-integer reader from the complete
108-step digital ledger. This supplies the signature type of MassCharacter
without asserting that the reader is additive on histories. -/

namespace HMT.VI.LedgerSignature

open scoped BigOperators
open HMT.VI.EventReconstruction
open HMT.VI.RouteEvents

abbrev DigitalRoute := Fin 108 → Fin 9

def digitValue (a : Fin 9) : ℤ := (a.val : ℤ) + 1

def integerRoute (d : DigitalRoute) : Route108 := fun t => digitValue (d t)

def events (d : DigitalRoute) : Events := routeEvents (integerRoute d)

def actionCount (d : DigitalRoute) : ℤ :=
  ((Finset.univ.filter (fun t : Fin 108 =>
    digitValue (d t) ∈ ({1, 3, 5, 7} : Finset ℤ))).card : ℤ)

/-- The integer total is retained; no division by six occurs in the signature. -/
def eventTotal (d : DigitalRoute) : ℤ := ∑ m : Fin 12, events d m

/-- The predecessor of step 1 is step 108. -/
def predecessor (t : Fin 108) : Fin 108 := t - 1

theorem predecessor_first : predecessor 0 = 107 := by decide

def j2 (a : Fin 9) : ℤ :=
  if digitValue a = 9 then 0
  else if digitValue a ∈ ({2, 4, 6, 8} : Finset ℤ) then 1 else -1

theorem j2_chart : ∀ a : Fin 9,
    j2 a = if digitValue a ∈ ({1, 3, 5, 7} : Finset ℤ) then -1
      else if digitValue a ∈ ({2, 4, 6, 8} : Finset ℤ) then 1 else 0 := by decide

def torsionEvent (d : DigitalRoute) (t : Fin 108) : ℤ :=
  if digitValue (d t) = 9 then j2 (d (predecessor t)) else 0

def torsionTotal (d : DigitalRoute) : ℤ := ∑ t : Fin 108, torsionEvent d t

def coronaClosures : Finset (Fin 108) := {26, 53, 80, 107}

theorem coronaClosures_exact : ∀ t : Fin 108, t ∈ coronaClosures ↔
    t.val + 1 = 27 ∨ t.val + 1 = 54 ∨ t.val + 1 = 81 ∨ t.val + 1 = 108 := by decide

def torsionCoronas (d : DigitalRoute) : ℤ := ∑ t ∈ coronaClosures, torsionEvent d t

def torsionDefect (d : DigitalRoute) : ℤ := torsionTotal d - 2 * torsionCoronas d

def blockIndex (a : Fin 4) (j : Fin 3) : Fin 12 := ⟨a.val + 4 * j.val, by omega⟩

def tower120 (d : DigitalRoute) : ℤ :=
  ∑ a : Fin 4, Int.sign (events d (blockIndex a 0) + events d (blockIndex a 1) +
    events d (blockIndex a 2))

def eventSign (d : DigitalRoute) (m : Fin 12) : ℤ := Int.sign (events d m)

def autocorrelation (d : DigitalRoute) : ℤ :=
  ∑ m : Fin 12, eventSign d m * eventSign d (m + 3)

/-- Definitionally `Fin 5 → ℤ`, the character's integer-signature interface. -/
def signature (d : DigitalRoute) : Fin 5 → ℤ :=
  ![actionCount d, eventTotal d, torsionDefect d, tower120 d, autocorrelation d]

theorem total_from_reconstruction (e : Events) : (extract e).total = ∑ m : Fin 12, e m := by
  rw [Fin.sum_univ_add (a := 6) (b := 6)]
  simp [extract, paired, first, second, Finset.sum_add_distrib, Fin.natAdd,
    Fin.castAdd, Fin.castLE, Nat.add_comm]

theorem signature_total_preserved (d : DigitalRoute) :
    signature d 1 = (extract (events d)).total := by
  simpa [signature, eventTotal] using (total_from_reconstruction (events d)).symm

theorem ledger_events_reconstruct (d : DigitalRoute) :
    reconstruct (extract (events d)) = events d := reconstruct_extract _

theorem ledger_coordinates_integral (d : DigitalRoute) : IntegralImage (extract (events d)) :=
  extract_integral _

theorem signature_formula (d : DigitalRoute) :
    signature d = ![actionCount d, eventTotal d,
      torsionTotal d - 2 * torsionCoronas d, tower120 d,
      ∑ m : Fin 12, Int.sign (events d m) * Int.sign (events d (m + 3))] := rfl

#print axioms j2_chart
#print axioms coronaClosures_exact
#print axioms signature_total_preserved
#print axioms ledger_events_reconstruct

end HMT.VI.LedgerSignature
