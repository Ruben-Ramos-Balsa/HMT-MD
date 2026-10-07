import RegionalPublicationComposition

/-!
State-local residual recurrence in 06e_certificado_generacion_monodromica_rev7,
the forward extension anchored at R36:
  d = Dig_729(epsilon), epsilon' = 729*epsilon-d, N' = 729*N+d.

This formalizes the real-coordinate realization of the already constructed
internal regional character. The step reads only the current prefix and
residual, not rational enclosures or future publications. Its agreement with
the existing rational publication is proved afterwards. It is not a new
construction of the regional character, nor the pre-R36 nine-step TPK map.
-/

noncomputable section
namespace HMT.I.RegionalResidualDynamics

open RegionalPublicationComposition

structure State where
  prefixValue : Int
  residual : ℝ
  residual_nonneg : 0 ≤ residual
  residual_lt_one : residual < 1

theorem state_ext (a b : State) (hp : a.prefixValue = b.prefixValue)
    (hr : a.residual = b.residual) : a = b := by
  cases a
  cases b
  cases hp
  cases hr
  rfl

def nextDigit (s : State) : Int := ⌊729 * s.residual⌋

def step (s : State) : State :=
  ⟨729 * s.prefixValue + nextDigit s, Int.fract (729 * s.residual),
    Int.fract_nonneg _, Int.fract_lt_one _⟩

theorem digit_bounds (s : State) : 0 ≤ nextDigit s ∧ nextDigit s < 729 := by
  constructor
  · exact Int.floor_nonneg.mpr (mul_nonneg (by norm_num) s.residual_nonneg)
  · have hf := Int.floor_le (729 * s.residual)
    have hh : (nextDigit s : ℝ) < 729 := by
      unfold nextDigit
      nlinarith [s.residual_lt_one]
    exact_mod_cast hh

theorem residual_update (s : State) :
    (step s).residual = 729 * s.residual - nextDigit s := rfl

theorem prefix_update (s : State) :
    (step s).prefixValue = 729 * s.prefixValue + nextDigit s := rfl

theorem conserved_balance (s : State) :
    ((step s).prefixValue : ℝ) + (step s).residual =
      729 * ((s.prefixValue : ℝ) + s.residual) := by
  rw [prefix_update, residual_update]
  push_cast
  ring

def realize (x : ℝ) : State :=
  ⟨⌊x⌋, Int.fract x, Int.fract_nonneg _, Int.fract_lt_one _⟩

theorem step_realize (x : ℝ) : step (realize x) = realize (729 * x) := by
  have hx : 729 * x = ((729 * ⌊x⌋ : Int) : ℝ) + 729 * Int.fract x := by
    simp only [Int.fract, Int.cast_mul, Int.cast_ofNat]
    ring
  apply state_ext
  · change 729 * ⌊x⌋ + ⌊729 * Int.fract x⌋ = ⌊729 * x⌋
    rw [hx, Int.floor_intCast_add]
  · change Int.fract (729 * Int.fract x) = Int.fract (729 * x)
    rw [hx, Int.fract_intCast_add]

/-- The regional value is the internal character already produced by the
imported construction, not a conventional constant supplied as input. -/
def stateAt (c : Channel) (n : Nat) : State :=
  realize (value c * (729 : ℝ)^n)

theorem step_stateAt (c : Channel) (n : Nat) :
    step (stateAt c n) = stateAt c (n + 1) := by
  unfold stateAt
  rw [step_realize]
  congr 1
  rw [pow_succ]
  ring

def run : Nat → State → State
  | 0, s => s
  | n + 1, s => step (run n s)

theorem run_stateAt (c : Channel) (start n : Nat) :
    run n (stateAt c start) = stateAt c (start + n) := by
  induction n with
  | zero => simp [run]
  | succ n ih => rw [run, ih, step_stateAt, Nat.add_assoc]

theorem history_unique (s : State) (history : Nat → State)
    (h0 : history 0 = s) (hstep : ∀ n, history (n + 1) = step (history n)) :
    ∀ n, history n = run n s := by
  intro n
  induction n with
  | zero => exact h0
  | succ n ih => rw [hstep, ih, run]

/-- The old publication is a posterior certificate of the prefix in this state. -/
theorem state_prefix_eq_publication (c : Channel) (n : Nat) :
    (stateAt c n).prefixValue = (publish c 729 (by decide) n : Int) := by
  rw [publish_eq_prefix]
  have h := RadixCellSelection.prefix_as_cell (value c) (value_nonnegative c) 729 n
  simpa [stateAt, realize, RadixCellSelection.cell] using h.symm

theorem state_digit_eq_published_block (c : Channel) (n : Nat) :
    nextDigit (stateAt c n) =
      (publish c 729 (by decide) (n + 1) % 729 : Nat) := by
  have hs := congrArg State.prefixValue (step_stateAt c n)
  change 729 * (stateAt c n).prefixValue + nextDigit (stateAt c n) =
    (stateAt c (n + 1)).prefixValue at hs
  rw [state_prefix_eq_publication, state_prefix_eq_publication] at hs
  have hp := publication_step c 729 (by decide) n
  omega

/-- The real coordinate at depth six, corresponding to the R36 depth.
This is not an identification with the complete historical enriched state.
Every later step uses the preceding residual state; no enclosure is read by
`step` or `run`. The exact residual is not reconstructed from its finite prefix. -/
def r36RealCoordinate (c : Channel) : State := stateAt c 6

theorem r36_forward_publication (c : Channel) (n : Nat) :
    (run n (r36RealCoordinate c)).prefixValue = (publish c 729 (by decide) (6 + n) : Int) ∧
    nextDigit (run n (r36RealCoordinate c)) =
      (publish c 729 (by decide) (6 + n + 1) % 729 : Nat) := by
  unfold r36RealCoordinate
  rw [run_stateAt]
  exact ⟨state_prefix_eq_publication c _, state_digit_eq_published_block c _⟩

end HMT.I.RegionalResidualDynamics
end

#print axioms HMT.I.RegionalResidualDynamics.digit_bounds
#print axioms HMT.I.RegionalResidualDynamics.residual_update
#print axioms HMT.I.RegionalResidualDynamics.prefix_update
#print axioms HMT.I.RegionalResidualDynamics.conserved_balance
#print axioms HMT.I.RegionalResidualDynamics.step_realize
#print axioms HMT.I.RegionalResidualDynamics.step_stateAt
#print axioms HMT.I.RegionalResidualDynamics.run_stateAt
#print axioms HMT.I.RegionalResidualDynamics.history_unique
#print axioms HMT.I.RegionalResidualDynamics.state_prefix_eq_publication
#print axioms HMT.I.RegionalResidualDynamics.state_digit_eq_published_block
#print axioms HMT.I.RegionalResidualDynamics.r36_forward_publication
