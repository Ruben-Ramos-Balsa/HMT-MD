import ChargeChartCompatibility

open HMT.I HMT.I.TerminalSelector HMT.I.ChargeChartCompatibility

example (word : Nat) :
    RegionalW24.dualChargeWord word = wordCharge (transform6 word) :=
  dualChargeWord_eq_wordCharge_transform6 word

example (prefixes : Fin 3 → Nat) (inc : HistoricalIncidenceEvaluation.Incidence) :
    readWithDualCharge (fun word => wordCharge (transform6 word)) prefixes inc =
      HistoricalIncidenceEvaluation.read prefixes inc :=
  readWithDualCharge_terminal prefixes inc

example (prefixes : Fin 3 → Nat)
    (schedule : List HistoricalIncidenceEvaluation.Incidence) (p : Fin 8) :
    (((HistoricalIncidenceEvaluation.atPosition schedule p).map
      (readWithDualCharge (fun word => wordCharge (transform6 word)) prefixes)).eraseDups) =
      HistoricalIncidenceEvaluation.readPosition prefixes schedule p :=
  readPosition_terminal prefixes schedule p
