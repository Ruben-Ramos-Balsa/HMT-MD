import Std

/-!
Chronological central electronic register and its two finite readers.
Source: article I, electron.tex, "Dos lectores del retorno electrónico".
Emission reads the current cell before transport. This is the specified
observable central route, not the general two-cursor TPKTransport route,
and not a reconstruction of the full enriched state from 108 symbols.
-/

namespace ElectronReturn

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

def cycleLength : Nat := 108
def stepsPerPhase : Nat := 9
def phaseCount : Nat := 12
def halfCycle : Nat := cycleLength / 2

structure VisibleState where
  row : Int
  col : Int
  horizontal : Int
  vertical : Int
  deriving DecidableEq, Repr

def initial : VisibleState := ⟨5, 5, 1, 1⟩

/-- The source's cellular inversion selects the center independently of either reader. -/
theorem cellular_fixed_iff (r c : Int) :
    ((10-r, 10-c) : Int × Int) = (r,c) ↔ r = 5 ∧ c = 5 := by
  simp only [Prod.mk.injEq]
  omega

theorem initial_is_fixed_center :
    ((10-initial.row, 10-initial.col) : Int × Int) = (initial.row, initial.col) ∧
      initial.row = 5 ∧ initial.col = 5 := by decide

/-- Zero-based tick: the source's (+1,-1,0) calendar. -/
def selector (tick : Nat) : Int :=
  if tick % 3 = 0 then 1 else if tick % 3 = 1 then -1 else 0

def positiveRoot9 (n : Int) : Int := 1 + (n-1) % 9
def quotient9 (n : Int) : Int := (n-1) / 9

theorem positive_root_bounds (n : Int) : 1 ≤ positiveRoot9 n ∧ positiveRoot9 n ≤ 9 := by
  unfold positiveRoot9
  omega

theorem residual_quotient_reconstruction (n : Int) :
    positiveRoot9 n + 9 * quotient9 n = n := by
  have h := Int.emod_add_ediv (n-1) 9
  unfold positiveRoot9 quotient9
  omega

def rawReading (tick : Nat) (s : VisibleState) : Int :=
  if selector tick = 1 then s.row + s.col
  else if selector tick = -1 then s.row * s.col else 9

def emit (tick : Nat) (s : VisibleState) : Nat :=
  (positiveRoot9 (rawReading tick s) % 3).toNat

/-- Flips occur after the numbered steps 27,54,81 of this finite window. -/
def flipAfter (tick : Nat) : Bool :=
  tick + 1 == 27 || tick + 1 == 54 || tick + 1 == 81

def transport (tick : Nat) (s : VisibleState) : VisibleState :=
  let r := if selector tick = -1 then positiveRoot9 (s.row + s.vertical) else s.row
  let c := if selector tick = 1 then positiveRoot9 (s.col + s.horizontal) else s.col
  let h := if flipAfter tick then -s.horizontal else s.horizontal
  let v := if flipAfter tick then -s.vertical else s.vertical
  ⟨r, c, h, v⟩

def stateAt : Nat → VisibleState
  | 0 => initial
  | n+1 => transport n (stateAt n)

def emittedAt (tick : Nat) : Nat := emit tick (stateAt tick)

def gamma : List Nat := (List.range cycleLength).map emittedAt

/-- The orientation sampled at the start of each nine-step phase. -/
def tau : List Int :=
  (List.range phaseCount).map (fun phase => (stateAt (stepsPerPhase * phase)).horizontal)

theorem gamma_length : gamma.length = 108 := by simp [gamma, cycleLength]
theorem tau_length : tau.length = 12 := by simp [tau, phaseCount]
theorem half_cycle_value : halfCycle = 54 := by decide

theorem emitted_trit_bounds (tick : Nat) : emittedAt tick < 3 := by
  unfold emittedAt emit
  have h0 : 0 ≤ positiveRoot9 (rawReading tick (stateAt tick)) % 3 := by omega
  have h1 : positiveRoot9 (rawReading tick (stateAt tick)) % 3 < 3 := by omega
  omega

/-- These two words are display targets, not inputs of `stateAt` or `gamma`. -/
def displayedA : List Nat := [1,0,0,0,0,0,2,2,0]
def displayedB : List Nat := [1,2,0,2,0,0,0,0,0]
def displayedHalf : List Nat :=
  (List.replicate 3 displayedA).flatten ++ (List.replicate 3 displayedB).flatten

theorem first_nine_emissions : (List.range 9).map emittedAt = displayedA := by decide
theorem reverse_nine_emissions : (List.range 9).map (fun t => emittedAt (27+t)) = displayedB := by decide

theorem generated_gamma : gamma = displayedHalf ++ displayedHalf := by decide
theorem generated_tau : tau = [1,1,1,-1,-1,-1,1,1,1,-1,-1,-1] := by decide

theorem cell_return_26 : (stateAt 26).row = 5 ∧ (stateAt 26).col = 5 ∧ 26 % 3 = 2 := by decide
theorem registered_return_27 :
    (stateAt 27).row = 5 ∧ (stateAt 27).col = 5 ∧ 27 % 3 = 0 := by decide
theorem registered_return_minimal :
    ∀ n : Fin 27, 0 < n.val → n.val % 3 = 0 →
      ¬ ((stateAt n.val).row = 5 ∧ (stateAt n.val).col = 5) := by decide

theorem orientation_flips :
    ((stateAt 26).horizontal, (stateAt 27).horizontal,
      (stateAt 54).horizontal, (stateAt 81).horizontal) = (1,-1,1,-1) := by decide

theorem simultaneous_orientations :
    ∀ n : Fin 109, (stateAt n.val).horizontal = (stateAt n.val).vertical := by decide

theorem chronological_state_bounds :
    ∀ n : Fin 109,
      1 ≤ (stateAt n.val).row ∧ (stateAt n.val).row ≤ 9 ∧
      1 ≤ (stateAt n.val).col ∧ (stateAt n.val).col ≤ 9 ∧
      ((stateAt n.val).horizontal = 1 ∨ (stateAt n.val).horizontal = -1) ∧
      ((stateAt n.val).vertical = 1 ∨ (stateAt n.val).vertical = -1) := by decide

def cyclicNat (word : List Nat) (tick : Nat) : Nat := word.getD (tick % word.length) 0
def cyclicInt (word : List Int) (tick : Nat) : Int := word.getD (tick % word.length) 0

theorem gamma_period_54 :
    ∀ t : Fin 108, cyclicNat gamma (t.val+54) = cyclicNat gamma t.val := by
  rw [generated_gamma]
  decide

def discrepancy (word : List Nat) (shift : Nat) : Nat :=
  (List.range word.length).countP (fun t => cyclicNat word t != cyclicNat word (t+shift))

def discrepancyReader (word : List Nat) : Int × Int × Int :=
  ((discrepancy word 27 : Int) + (discrepancy word 36 : Int),
    (discrepancy word 1 : Int), ((discrepancy word 4 : Int) - (discrepancy word 3 : Int)) / 2)

theorem central_discrepancies :
    (discrepancy gamma 1, discrepancy gamma 3, discrepancy gamma 4,
      discrepancy gamma 27, discrepancy gamma 36) = (54,56,68,48,32) := by
  rw [generated_gamma]
  decide

theorem central_discrepancies_even :
    ∀ k : Fin 108, discrepancy gamma k.val % 2 = 0 := by
  rw [generated_gamma]
  decide

theorem discrepancy_reader_central : discrepancyReader gamma = (80,54,6) := by
  rw [generated_gamma]
  decide

def correlation (word : List Int) (shift : Nat) : Int :=
  ((List.range word.length).map (fun t => cyclicInt word t * cyclicInt word (t+shift))).sum

def window (word : List Int) (start width : Nat) : Int :=
  ((List.range width).map (fun j => cyclicInt word (start+j))).sum

def windowSquares (word : List Int) (width : Nat) : Int :=
  ((List.range word.length).map (fun t => (window word t width)^2)).sum

def antipodal (word : List Int) : Int :=
  ((List.range 6).map (fun t => cyclicInt word t * cyclicInt word (t+6))).sum

def windowContrast (word : List Int) : Int := 4 * windowSquares word 3 - 3 * windowSquares word 4

def windowReader (word : List Int) : Int × Int × Int :=
  (windowContrast word, (halfCycle : Int), antipodal word)

theorem central_correlations :
    (correlation tau 1, correlation tau 2, correlation tau 3) = (4,-4,-12) := by
  rw [generated_tau]
  decide

theorem central_window_squares : (windowSquares tau 3, windowSquares tau 4) = (44,32) := by
  rw [generated_tau]
  decide

theorem central_antipodal : antipodal tau = 6 := by
  rw [generated_tau]
  decide

theorem central_contrast : windowContrast tau = 80 := by
  rw [generated_tau]
  decide

theorem central_contrast_correlation :
    windowContrast tau = -2*correlation tau 1 - 4*correlation tau 2 - 6*correlation tau 3 := by
  rw [generated_tau]
  decide

theorem window_reader_central : windowReader tau = (80,54,6) := by
  rw [generated_tau]
  decide

theorem readers_agree : discrepancyReader gamma = windowReader tau := by
  rw [discrepancy_reader_central, window_reader_central]

theorem both_readers_central :
    discrepancyReader gamma = (80,54,6) ∧ windowReader tau = (80,54,6) :=
  ⟨discrepancy_reader_central, window_reader_central⟩

end ElectronReturn

#print axioms ElectronReturn.positive_root_bounds
#print axioms ElectronReturn.cellular_fixed_iff
#print axioms ElectronReturn.initial_is_fixed_center
#print axioms ElectronReturn.residual_quotient_reconstruction
#print axioms ElectronReturn.gamma_length
#print axioms ElectronReturn.tau_length
#print axioms ElectronReturn.half_cycle_value
#print axioms ElectronReturn.emitted_trit_bounds
#print axioms ElectronReturn.first_nine_emissions
#print axioms ElectronReturn.reverse_nine_emissions
#print axioms ElectronReturn.generated_gamma
#print axioms ElectronReturn.generated_tau
#print axioms ElectronReturn.cell_return_26
#print axioms ElectronReturn.registered_return_27
#print axioms ElectronReturn.registered_return_minimal
#print axioms ElectronReturn.orientation_flips
#print axioms ElectronReturn.simultaneous_orientations
#print axioms ElectronReturn.chronological_state_bounds
#print axioms ElectronReturn.gamma_period_54
#print axioms ElectronReturn.central_discrepancies
#print axioms ElectronReturn.central_discrepancies_even
#print axioms ElectronReturn.discrepancy_reader_central
#print axioms ElectronReturn.central_correlations
#print axioms ElectronReturn.central_window_squares
#print axioms ElectronReturn.central_antipodal
#print axioms ElectronReturn.central_contrast
#print axioms ElectronReturn.central_contrast_correlation
#print axioms ElectronReturn.window_reader_central
#print axioms ElectronReturn.readers_agree
#print axioms ElectronReturn.both_readers_central
