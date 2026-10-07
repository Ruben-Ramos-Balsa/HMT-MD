import HistoricalIncidenceEvaluation

open HMT.I.HistoricalIncidenceEvaluation HMT.I.GeneratedN69Rows
open HMT.I.TerminalSelector

example : regionalRecovered = [55, 175, 498, 437, 98, 28, 687, 714] :=
  regional_recovered_evaluation

example : ∀ p : Fin 8,
    ∃! w, readPosition regionalPrefixes historicalSchedule p = [w] :=
  regional_positions_singleton

example : regionalRecovered.Perm s8Input := regional_recovered_perm

example (n : Nat) : n ∈ selectedFromHistoricalIncidences ↔
    n = 234543140729659824621058914794146601 :=
  historical_selection_unique n

example : ∃! n, n ∈ selectedFromHistoricalIncidences :=
  historical_selection_existsUnique
