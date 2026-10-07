import TPKRegions

/-!
Simple minimal D3 regions, their diagonal support and trit census.
Both selectors are downstream of the proved emission metadata and D3 quotient.
No numerical target or reference catalogue is an input.
-/
namespace TPKSimpleRegions
open TPKOrbits
set_option maxRecDepth 1000000
set_option maxHeartbeats 0

def tritCensus (w : Word) : Nat × Nat × Nat :=
  ((toList w).count 0, (toList w).count 1, (toList w).count 2)

theorem census_invariant (g : D3) (w : Word) : tritCensus (act g w) = tritCensus w := by
  cases g <;> cases w <;>
    simp [tritCensus, act, rotate, swap, toList, List.count_cons,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

theorem same_census_on_orbit {w v : Word} (h : v ∈ orbit w) :
    tritCensus v = tritCensus w := by
  obtain ⟨g, hg⟩ := (mem_orbit w v).1 h
  rw [← hg, census_invariant]

def simpleMinimal (r : Word) : Bool :=
  (orbit r).length == 6 &&
    (orbit r).all (fun w => (TPKRegions.fibre w).length == 1 &&
      (TPKRegions.fibre w).all (fun row => row.multiplicity == 144))

theorem simple_minimal_spec (r : Word) :
    simpleMinimal r = true ↔ (orbit r).length = 6 ∧
      ∀ w ∈ orbit r, (TPKRegions.fibre w).length = 1 ∧
        ∀ row ∈ TPKRegions.fibre w, row.multiplicity = 144 := by
  simp only [simpleMinimal, Bool.and_eq_true, beq_iff_eq, List.all_eq_true]

theorem simple_single_fibre {r w : Word} (hr : simpleMinimal r = true) (hw : w ∈ orbit r) :
    ∃ row : TPKRegions.RegionalRow, TPKRegions.fibre w = [row] ∧ row.multiplicity = 144 := by
  have h := (simple_minimal_spec r).1 hr
  obtain ⟨row, heq⟩ := List.length_eq_one_iff.mp (h.2 w hw).1
  exact ⟨row, heq, (h.2 w hw).2 row (by rw [heq]; simp)⟩

def rawDiagonals (r : Word) : List Nat :=
  (orbit r).flatMap (fun w => (TPKRegions.fibre w).map TPKRegions.RegionalRow.diagonal)
def diagonalSupport (r : Word) : List Nat :=
  (List.range 9).filter (fun d => (rawDiagonals r).contains d)

theorem diagonal_support_exact (r : Word) (d : Nat) :
    d ∈ diagonalSupport r ↔
      ∃ w ∈ orbit r, ∃ row ∈ TPKRegions.fibre w, row.diagonal = d := by
  simp only [diagonalSupport, List.mem_filter, List.mem_range, List.contains_iff_mem]
  constructor
  · intro h
    simpa only [rawDiagonals, List.mem_flatMap, List.mem_map] using h.2
  · intro h
    have hm : d ∈ rawDiagonals r := by
      simpa only [rawDiagonals, List.mem_flatMap, List.mem_map] using h
    obtain ⟨w, _, row, hr, heq⟩ := h
    have hrow : row ∈ TPKRegions.rows := (List.mem_filter.mp hr).1
    have hd := (TPKRegions.metadata_valid row hrow).1
    rw [heq] at hd
    exact ⟨hd, hm⟩

def radicalSingletons : List Word :=
  representatives.filter (fun r => simpleMinimal r && diagonalSupport r == [0, 3, 6])

def radicalWitness : List Word := [⟨0, 1, 1, 2, 1, 1⟩, ⟨0, 1, 2, 1, 2, 1⟩, ⟨0, 1, 2, 2, 0, 2⟩, ⟨0, 1, 1, 1, 2, 0⟩, ⟨0, 0, 2, 1, 1, 2⟩, ⟨0, 0, 2, 2, 2, 0⟩]

theorem radical_singletons_checked : radicalSingletons = radicalWitness := by
  unfold radicalSingletons simpleMinimal diagonalSupport rawDiagonals TPKRegions.fibre
  simp only [TPKOrbits.representatives_checked, TPKRegions.rows_checked]
  decide +kernel

theorem radical_singletons_count : radicalSingletons.length = 6 := by
  rw [radical_singletons_checked]
  decide +kernel

theorem radical_membership (r : Word) :
    r ∈ radicalSingletons ↔ r ∈ representatives ∧ simpleMinimal r = true ∧
      diagonalSupport r = [0, 3, 6] := by
  simp only [radicalSingletons, List.mem_filter, Bool.and_eq_true, beq_iff_eq]

def closureCensus : Nat × Nat × Nat :=
  (TPKRegions.closureOrbits.map tritCensus).headD (0, 0, 0)

theorem closure_census_generated : closureCensus = (2, 3, 1) := by
  rw [closureCensus, TPKRegions.closure_orbit_checked]
  decide +kernel

def propagationOrbits : List Word :=
  radicalSingletons.filter (fun r => tritCensus r == closureCensus)
def autoscaleOrbits : List Word :=
  radicalSingletons.filter (fun r => tritCensus r == (2, 2, 2))

theorem propagation_selection_spec (r : Word) :
    r ∈ propagationOrbits ↔ r ∈ radicalSingletons ∧ tritCensus r = closureCensus := by
  simp only [propagationOrbits, List.mem_filter, beq_iff_eq]

theorem autoscale_selection_spec (r : Word) :
    r ∈ autoscaleOrbits ↔ r ∈ radicalSingletons ∧ tritCensus r = (2, 2, 2) := by
  simp only [autoscaleOrbits, List.mem_filter, beq_iff_eq]

theorem propagation_orbit_checked : propagationOrbits = [⟨0, 1, 1, 1, 2, 0⟩] := by
  rw [propagationOrbits, radical_singletons_checked, closure_census_generated]
  decide +kernel

theorem autoscale_orbit_checked : autoscaleOrbits = [⟨0, 0, 2, 1, 1, 2⟩] := by
  rw [autoscaleOrbits, radical_singletons_checked]
  decide +kernel

theorem propagation_orbit_unique : propagationOrbits.length = 1 := by
  rw [propagation_orbit_checked]
  decide +kernel

theorem autoscale_orbit_unique : autoscaleOrbits.length = 1 := by
  rw [autoscale_orbit_checked]
  decide +kernel

def orientSelected (rs : List Word) : List Word :=
  rs.flatMap (fun r => (orbit r).filter TPKRegions.hasOrientation)
def propagationWords : List Word := orientSelected propagationOrbits
def autoscaleWords : List Word := orientSelected autoscaleOrbits

theorem propagation_oriented_checked : propagationWords = [⟨2, 0, 1, 1, 0, 1⟩] := by
  unfold propagationWords orientSelected TPKRegions.hasOrientation TPKRegions.fibre
  simp only [propagation_orbit_checked, TPKRegions.rows_checked]
  decide +kernel

theorem autoscale_oriented_checked : autoscaleWords = [⟨1, 2, 1, 2, 0, 0⟩] := by
  unfold autoscaleWords orientSelected TPKRegions.hasOrientation TPKRegions.fibre
  simp only [autoscale_orbit_checked, TPKRegions.rows_checked]
  decide +kernel

theorem propagation_orientation_unique : propagationWords.length = 1 := by
  rw [propagation_oriented_checked]
  decide +kernel

theorem autoscale_orientation_unique : autoscaleWords.length = 1 := by
  rw [autoscale_oriented_checked]
  decide +kernel

theorem orient_selected_spec (rs : List Word) (w : Word) :
    w ∈ orientSelected rs ↔
      ∃ r ∈ rs, w ∈ orbit r ∧
        ∃ row ∈ TPKRegions.fibre w, row.diagonal = 6 ∧ row.heading = .es := by
  simp only [orientSelected, List.mem_flatMap, List.mem_filter,
    TPKRegions.hasOrientation, List.any_eq_true, Bool.and_eq_true, beq_iff_eq]

def propagationFibre : List TPKRegions.RegionalRow := propagationWords.flatMap TPKRegions.fibre
def autoscaleFibre : List TPKRegions.RegionalRow := autoscaleWords.flatMap TPKRegions.fibre

theorem propagation_fibre_checked :
    propagationFibre = [⟨⟨850, 963, 890, 149, 252, 212⟩, 144, 6, .es, [7, 7, 1, 3, 3, 9]⟩] := by
  unfold propagationFibre TPKRegions.fibre
  simp only [propagation_oriented_checked, TPKRegions.rows_checked]
  decide +kernel

theorem autoscale_fibre_checked :
    autoscaleFibre = [⟨⟨830, 943, 830, 109, 252, 252⟩, 144, 6, .es, [5, 5, 5, 9, 3, 3]⟩] := by
  unfold autoscaleFibre TPKRegions.fibre
  simp only [autoscale_oriented_checked, TPKRegions.rows_checked]
  decide +kernel

theorem selected_fibre_counts : propagationFibre.length = 1 ∧ autoscaleFibre.length = 1 := by
  rw [propagation_fibre_checked, autoscale_fibre_checked]
  decide +kernel

theorem selected_fibre_masses :
    (propagationFibre.map TPKRegions.RegionalRow.multiplicity) = [144] ∧
    (autoscaleFibre.map TPKRegions.RegionalRow.multiplicity) = [144] := by
  rw [propagation_fibre_checked, autoscale_fibre_checked]
  decide +kernel

theorem selected_words_distinct :
    propagationWords ≠ autoscaleWords ∧
    propagationWords ≠ TPKRegions.orientedClosure ∧
    autoscaleWords ≠ TPKRegions.orientedClosure := by
  rw [propagation_oriented_checked, autoscale_oriented_checked, TPKRegions.oriented_closure_checked]
  decide +kernel

def propagationOrbitWords : List Word := propagationOrbits.flatMap orbit
def autoscaleOrbitWords : List Word := autoscaleOrbits.flatMap orbit
def closureOrbitWords : List Word := TPKRegions.closureOrbits.flatMap orbit

theorem selected_orbits_pairwise_disjoint :
    (∀ w ∈ propagationOrbitWords, w ∉ autoscaleOrbitWords) ∧
    (∀ w ∈ propagationOrbitWords, w ∉ closureOrbitWords) ∧
    (∀ w ∈ autoscaleOrbitWords, w ∉ closureOrbitWords) := by
  unfold propagationOrbitWords autoscaleOrbitWords closureOrbitWords
  rw [propagation_orbit_checked, autoscale_orbit_checked, TPKRegions.closure_orbit_checked]
  decide +kernel

theorem selected_orbit_sizes :
    propagationOrbitWords.length = 6 ∧ autoscaleOrbitWords.length = 6 := by
  unfold propagationOrbitWords autoscaleOrbitWords
  rw [propagation_orbit_checked, autoscale_orbit_checked]
  decide +kernel

theorem selected_census_values :
    propagationWords.map tritCensus = [(2, 3, 1)] ∧
    autoscaleWords.map tritCensus = [(2, 2, 2)] := by
  rw [propagation_oriented_checked, autoscale_oriented_checked]
  decide +kernel

theorem selected_supports :
    ∀ r ∈ propagationOrbits ++ autoscaleOrbits, diagonalSupport r = [0, 3, 6] := by
  intro r hr
  rcases List.mem_append.mp hr with hp | ha
  · exact ((radical_membership r).1 ((propagation_selection_spec r).1 hp).1).2.2
  · exact ((radical_membership r).1 ((autoscale_selection_spec r).1 ha).1).2.2

theorem selected_simple :
    ∀ r ∈ propagationOrbits ++ autoscaleOrbits, simpleMinimal r = true := by
  intro r hr
  rcases List.mem_append.mp hr with hp | ha
  · exact ((radical_membership r).1 ((propagation_selection_spec r).1 hp).1).2.1
  · exact ((radical_membership r).1 ((autoscale_selection_spec r).1 ha).1).2.1

theorem selected_representatives (r : Word)
    (hr : r ∈ propagationOrbits ++ autoscaleOrbits) : r ∈ representatives := by
  rcases List.mem_append.mp hr with hp | ha
  · exact ((radical_membership r).1 ((propagation_selection_spec r).1 hp).1).1
  · exact ((radical_membership r).1 ((autoscale_selection_spec r).1 ha).1).1

theorem selected_words_produced (w : Word)
    (hw : w ∈ propagationWords ++ autoscaleWords) : w ∈ producedWords := by
  rcases List.mem_append.mp hw with hp | ha
  · obtain ⟨r, hr, hwr, _⟩ := (orient_selected_spec propagationOrbits w).1 hp
    exact orbit_stays_produced
      (representatives_produced (selected_representatives r (List.mem_append.mpr (Or.inl hr)))) hwr
  · obtain ⟨r, hr, hwr, _⟩ := (orient_selected_spec autoscaleOrbits w).1 ha
    exact orbit_stays_produced
      (representatives_produced (selected_representatives r (List.mem_append.mpr (Or.inr hr)))) hwr

theorem selected_fibres_pairwise_disjoint :
    (∀ row ∈ propagationFibre, row ∉ autoscaleFibre) ∧
    (∀ row ∈ propagationFibre, row ∉ TPKRegions.closureFibre) ∧
    (∀ row ∈ autoscaleFibre, row ∉ TPKRegions.closureFibre) := by
  rw [propagation_fibre_checked, autoscale_fibre_checked, TPKRegions.closure_fibre_checked]
  decide +kernel

end TPKSimpleRegions

#print axioms TPKSimpleRegions.census_invariant
#print axioms TPKSimpleRegions.same_census_on_orbit
#print axioms TPKSimpleRegions.simple_minimal_spec
#print axioms TPKSimpleRegions.simple_single_fibre
#print axioms TPKSimpleRegions.diagonal_support_exact
#print axioms TPKSimpleRegions.radical_singletons_checked
#print axioms TPKSimpleRegions.radical_singletons_count
#print axioms TPKSimpleRegions.radical_membership
#print axioms TPKSimpleRegions.closure_census_generated
#print axioms TPKSimpleRegions.propagation_selection_spec
#print axioms TPKSimpleRegions.autoscale_selection_spec
#print axioms TPKSimpleRegions.propagation_orbit_checked
#print axioms TPKSimpleRegions.autoscale_orbit_checked
#print axioms TPKSimpleRegions.propagation_orbit_unique
#print axioms TPKSimpleRegions.autoscale_orbit_unique
#print axioms TPKSimpleRegions.propagation_oriented_checked
#print axioms TPKSimpleRegions.autoscale_oriented_checked
#print axioms TPKSimpleRegions.propagation_orientation_unique
#print axioms TPKSimpleRegions.autoscale_orientation_unique
#print axioms TPKSimpleRegions.orient_selected_spec
#print axioms TPKSimpleRegions.propagation_fibre_checked
#print axioms TPKSimpleRegions.autoscale_fibre_checked
#print axioms TPKSimpleRegions.selected_fibre_counts
#print axioms TPKSimpleRegions.selected_fibre_masses
#print axioms TPKSimpleRegions.selected_words_distinct
#print axioms TPKSimpleRegions.selected_orbits_pairwise_disjoint
#print axioms TPKSimpleRegions.selected_orbit_sizes
#print axioms TPKSimpleRegions.selected_census_values
#print axioms TPKSimpleRegions.selected_supports
#print axioms TPKSimpleRegions.selected_simple
#print axioms TPKSimpleRegions.selected_representatives
#print axioms TPKSimpleRegions.selected_words_produced
#print axioms TPKSimpleRegions.selected_fibres_pairwise_disjoint
