import TPKFiniteCursor

/-!
Cardinal paths on APP, with the integer lift retained.

This makes explicit the winding construction in `sections/nucleo.tex`, using
the existing TPK directions, residue/quotient coordinates and finite projection.
It does not replace the enriched state by its residual endpoint, and does not
claim to generate the X/Y transition records used by TPKLifts.
-/
namespace APPRouteWinding

open TPKTransport

def displacement (v : Direction → Int) : List Direction → Int
  | [] => 0
  | d :: ds => v d + displacement v ds

theorem displacement_append (v : Direction → Int) (a b : List Direction) :
    displacement v (a ++ b) = displacement v a + displacement v b := by
  induction a with
  | nil => simp [displacement]
  | cons d ds ih => simp [displacement, ih, Int.add_assoc]

def inverseRoute (w : List Direction) : List Direction :=
  (w.map opposite).reverse

theorem displacement_inverse (v : Direction → Int)
    (hv : ∀ d, v (opposite d) = -v d) (w : List Direction) :
    displacement v (inverseRoute w) = -displacement v w := by
  induction w with
  | nil => simp [inverseRoute, displacement]
  | cons d ds ih =>
    simp only [inverseRoute, List.map_cons, List.reverse_cons,
      displacement_append] at *
    simp only [displacement, Int.add_zero, hv, ih]
    omega

/-- Lifted endpoint of a cardinal route; no modular reduction is performed. -/
def endpoint (origin : Int × Int) (w : List Direction) : Int × Int :=
  (origin.1 + displacement dx w, origin.2 + displacement dy w)

def closed (origin : Int × Int) (w : List Direction) : Prop :=
  residue9 (endpoint origin w).1 = residue9 origin.1 ∧
  residue9 (endpoint origin w).2 = residue9 origin.2

/-- Change of winding coordinates of the lift, defined before assuming closure. -/
def winding (origin : Int × Int) (w : List Direction) : Int × Int :=
  (boundaryCarry origin.1 (displacement dx w),
   boundaryCarry origin.2 (displacement dy w))

theorem closed_displacement (origin : Int × Int) (w : List Direction)
    (h : closed origin w) :
    displacement dx w = 9 * (winding origin w).1 ∧
    displacement dy w = 9 * (winding origin w).2 := by
  have hx := boundary_transport origin.1 (displacement dx w)
  have hy := boundary_transport origin.2 (displacement dy w)
  dsimp [closed, endpoint] at h
  dsimp [winding]
  omega

theorem winding_closed_formula (origin : Int × Int) (w : List Direction)
    (h : closed origin w) :
    winding origin w = (displacement dx w / 9, displacement dy w / 9) := by
  have hd := closed_displacement origin w h
  apply Prod.ext <;> omega

theorem endpoint_append (origin : Int × Int) (a b : List Direction) :
    endpoint origin (a ++ b) = endpoint (endpoint origin a) b := by
  apply Prod.ext <;> simp [endpoint, displacement_append, Int.add_assoc]

theorem winding_append (origin : Int × Int) (a b : List Direction) :
    winding origin (a ++ b) =
      ((winding origin a).1 + (winding (endpoint origin a) b).1,
       (winding origin a).2 + (winding (endpoint origin a) b).2) := by
  apply Prod.ext <;> simp [winding, endpoint, displacement_append, boundary_cocycle]

theorem inverse_endpoint (origin : Int × Int) (w : List Direction) :
    endpoint (endpoint origin w) (inverseRoute w) = origin := by
  have hx := displacement_inverse dx (fun d => (opposite_vector d).1) w
  have hy := displacement_inverse dy (fun d => (opposite_vector d).2) w
  apply Prod.ext <;> simp only [endpoint, hx, hy] <;> omega

theorem winding_inverse (origin : Int × Int) (w : List Direction) :
    winding (endpoint origin w) (inverseRoute w) =
      (-(winding origin w).1, -(winding origin w).2) := by
  have he := inverse_endpoint origin w
  have hx := congrArg Prod.fst he
  have hy := congrArg Prod.snd he
  dsimp [endpoint] at hx hy
  apply Prod.ext <;> dsimp [winding, endpoint, boundaryCarry] <;>
    simp only [hx, hy] <;> omega

/-- Nine eastward edges return to the same APP vertex with winding (0,1). -/
theorem east_cycle_nonzero_winding :
    closed (1, 1) (List.replicate 9 Direction.east) ∧
    winding (1, 1) (List.replicate 9 Direction.east) = (0, 1) ∧
    endpoint (1, 1) (List.replicate 9 Direction.east) ≠ (1, 1) := by
  unfold closed
  decide

/-- Both cyclic coordinates of the APP torus are retained, not just one circle. -/
theorem two_coordinate_cycles :
    closed (1, 1) (List.replicate 9 Direction.south) ∧
    closed (1, 1) (List.replicate 9 Direction.east) ∧
    winding (1, 1) (List.replicate 9 Direction.south) = (1, 0) ∧
    winding (1, 1) (List.replicate 9 Direction.east) = (0, 1) := by
  unfold closed
  decide

/-- The finite cursor projection, including its direction, together with the
two quotient coordinates recovers the full integer cursor. -/
theorem cursor_recovered_from_projection_and_winding (a b : Cursor)
    (hp : TPKFiniteCursor.projectCursor a = TPKFiniteCursor.projectCursor b)
    (hx : quotient9 a.x = quotient9 b.x)
    (hy : quotient9 a.y = quotient9 b.y) : a = b := by
  have hpx := congrArg (fun c => c.x.val) hp
  have hpy := congrArg (fun c => c.y.val) hp
  have hpd := congrArg (fun c => c.direction) hp
  dsimp [TPKFiniteCursor.projectCursor, CommonComposition.cursorMark] at hpx hpy hpd
  have ax := lifted_coordinate_reconstruct a.x
  have bx := lifted_coordinate_reconstruct b.x
  have ay := lifted_coordinate_reconstruct a.y
  have byy := lifted_coordinate_reconstruct b.y
  simp only [residue9, quotient9] at *
  have ex : a.x = b.x := by omega
  have ey : a.y = b.y := by omega
  cases a
  cases b
  simp_all

/-- The actual TPK update and its finite projection remain linked at every depth. -/
theorem transported_projection_all_depths (s : Sheet) (n : Nat)
    (q : ObservableLift) :
    TPKFiniteCursor.projectState s (iterate step n q) =
      iterate (TPKFiniteCursor.step s) n (TPKFiniteCursor.projectState s q) :=
  TPKFiniteCursor.projectState_iterate s n q

/-- The actual additive TPK cursor makes nine eastward moves before the first
half-turn. Its residual position returns, but its winding coordinate increases. -/
theorem actual_tpk_return_retains_winding :
    let q : ObservableLift :=
      ⟨⟨1, 1, .east⟩, ⟨1, 1, .east⟩, ⟨0, by decide⟩⟩
    let c := (iterate step 27 q).plus
    c.x = 1 ∧ c.y = 10 ∧ c.direction = .west ∧
    residue9 c.x = residue9 q.plus.x ∧
    residue9 c.y = residue9 q.plus.y ∧
    quotient9 c.y = quotient9 q.plus.y + 1 := by
  decide

#print axioms APPRouteWinding.displacement_inverse
#print axioms APPRouteWinding.closed_displacement
#print axioms APPRouteWinding.winding_closed_formula
#print axioms APPRouteWinding.winding_append
#print axioms APPRouteWinding.inverse_endpoint
#print axioms APPRouteWinding.winding_inverse
#print axioms APPRouteWinding.east_cycle_nonzero_winding
#print axioms APPRouteWinding.two_coordinate_cycles
#print axioms APPRouteWinding.cursor_recovered_from_projection_and_winding
#print axioms APPRouteWinding.transported_projection_all_depths
#print axioms APPRouteWinding.actual_tpk_return_retains_winding

end APPRouteWinding
