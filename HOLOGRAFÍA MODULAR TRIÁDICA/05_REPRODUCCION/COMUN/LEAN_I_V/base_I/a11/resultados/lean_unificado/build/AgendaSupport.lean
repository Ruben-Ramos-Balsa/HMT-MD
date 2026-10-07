import HistoricalIncidenceEvaluation

/-!
Support-only interface for an incidence agenda.

This module proves invariance of the existing positional recovery under
reordering and duplication of incidences, provided the reference agenda has
one value at each position. It neither constructs an admissible history nor
asserts that a generated history has the historical incidence support.
No numerical incidence evaluation or terminal census is rerun here.
-/

namespace HMT.I.AgendaSupport

open HMT.I.HistoricalIncidenceEvaluation HMT.I.GeneratedN69Rows

private theorem eraseDups_eq_nil_iff (xs : List Nat) :
    xs.eraseDups = [] ↔ xs = [] := by
  cases xs with
  | nil => simp
  | cons a xs => simp [List.eraseDups_cons]

private theorem eraseDups_eq_singleton_iff (xs : List Nat) (w : Nat) :
    xs.eraseDups = [w] ↔ xs ≠ [] ∧ ∀ x ∈ xs, x = w := by
  cases xs with
  | nil => simp
  | cons a xs =>
    simp [List.eraseDups_cons, eraseDups_eq_nil_iff, List.filter_eq_nil_iff]
    intro h
    subst w
    rfl

/-- Equal supports suffice for equal deduplicated singleton images. -/
theorem singleton_image_of_same_support {α : Type*} [DecidableEq α]
    (f : α → Nat) (xs ys : List α) (w : Nat)
    (hsupport : ∀ x, x ∈ xs ↔ x ∈ ys)
    (href : (ys.map f).eraseDups = [w]) :
    (xs.map f).eraseDups = [w] := by
  rw [eraseDups_eq_singleton_iff] at href ⊢
  constructor
  · intro hnil
    have hxnil : xs = [] := List.map_eq_nil_iff.mp hnil
    have hynil : ys = [] := by
      apply List.eq_nil_iff_forall_not_mem.mpr
      intro y hy
      have := (hsupport y).mpr hy
      simp [hxnil] at this
    exact href.1 (by simp [hynil])
  · intro n hn
    rcases List.mem_map.mp hn with ⟨x, hx, rfl⟩
    exact href.2 (f x) (List.mem_map.mpr ⟨x, (hsupport x).mp hx, rfl⟩)

/-- Position filtering preserves equality of incidence supports. -/
theorem atPosition_same_support (agenda reference : List Incidence)
    (hsupport : ∀ inc, inc ∈ agenda ↔ inc ∈ reference) (p : Fin 8) :
    ∀ inc, inc ∈ atPosition agenda p ↔ inc ∈ atPosition reference p := by
  intro inc
  simp only [atPosition, List.mem_filter, decide_eq_true_eq]
  rw [hsupport inc]

/-- The positional singleton is invariant under agenda order and multiplicity. -/
theorem readPosition_of_same_support (prefixes : Fin 3 → Nat)
    (agenda reference : List Incidence)
    (hsupport : ∀ inc, inc ∈ agenda ↔ inc ∈ reference)
    (p : Fin 8) (w : Nat)
    (href : readPosition prefixes reference p = [w]) :
    readPosition prefixes agenda p = [w] :=
  singleton_image_of_same_support (read prefixes)
    (atPosition agenda p) (atPosition reference p) w
    (atPosition_same_support agenda reference hsupport p) href

/-- General recovery theorem: identical supports and singleton reference reads. -/
theorem recover_of_same_support (prefixes : Fin 3 → Nat)
    (agenda reference : List Incidence)
    (hsupport : ∀ inc, inc ∈ agenda ↔ inc ∈ reference)
    (hsingle : ∀ p : Fin 8, ∃ w, readPosition prefixes reference p = [w]) :
    recover prefixes agenda = recover prefixes reference := by
  have hpositions : readPosition prefixes agenda = readPosition prefixes reference := by
    funext p
    obtain ⟨w, hw⟩ := hsingle p
    rw [readPosition_of_same_support prefixes agenda reference hsupport p w hw, hw]
  simp only [recover, hpositions]

/-- The requested interface: no equality of order or multiplicities is needed. -/
theorem recover_regional_of_historical_support (agenda : List Incidence)
    (hsupport : ∀ inc, inc ∈ agenda ↔ inc ∈ historicalSchedule) :
    recover regionalPrefixes agenda = regionalRecovered := by
  exact recover_of_same_support regionalPrefixes agenda historicalSchedule hsupport
    (fun p => (regional_positions_singleton p).exists)

/-- Direct input for the existing unordered terminal selector. -/
theorem recovered_perm_of_historical_support (agenda : List Incidence)
    (hsupport : ∀ inc, inc ∈ agenda ↔ inc ∈ historicalSchedule) :
    (recover regionalPrefixes agenda).Perm HMT.I.TerminalSelector.s8Input := by
  rw [recover_regional_of_historical_support agenda hsupport]
  exact regional_recovered_perm

/-- Regression: reversal and arbitrary duplication of the reference agenda
do not alter the recovered register. -/
theorem reverse_double_historical_recovery :
    recover regionalPrefixes
      (historicalSchedule.reverse ++ historicalSchedule ++ historicalSchedule) =
      regionalRecovered := by
  apply recover_regional_of_historical_support
  intro inc
  simp

end HMT.I.AgendaSupport

#print axioms HMT.I.AgendaSupport.singleton_image_of_same_support
#print axioms HMT.I.AgendaSupport.atPosition_same_support
#print axioms HMT.I.AgendaSupport.readPosition_of_same_support
#print axioms HMT.I.AgendaSupport.recover_of_same_support
#print axioms HMT.I.AgendaSupport.recover_regional_of_historical_support
#print axioms HMT.I.AgendaSupport.recovered_perm_of_historical_support
#print axioms HMT.I.AgendaSupport.reverse_double_historical_recovery
