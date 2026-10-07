import RegionalTransitionRecords
import Lean.Util.FoldConsts

/- Implementation-dependency check, distinct from the theorem proofs.
   Inspect the complete value dependency closure of the four constructors,
   not merely the list of module imports. -/

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let roots := [
    `HMT.I.RegionalTransitionRecords.regionalX0,
    `HMT.I.RegionalTransitionRecords.regionalY0,
    `HMT.I.RegionalTransitionRecords.regionalX1,
    `HMT.I.RegionalTransitionRecords.regionalY1]
  let forbidden := [
    `TPKLifts.X0, `TPKLifts.Y0, `TPKLifts.X1, `TPKLifts.Y1,
    `TPKLifts.L0, `TPKLifts.L1, `TPKLifts.L0Witness, `TPKLifts.L1Witness,
    `TPKLifts.referenceBiographies, `TPKLifts.biographies,
    `HMT.I.GeneratedN69Rows.prefixInputs,
    `HMT.I.RegionalSixHundred.expectedPrefix,
    `HMT.I.TerminalSelector.n69Input,
    `Real.pi, `Real.exp, `goldenRatio]
  for root in roots do
    let mut todo := [root]
    let mut seen : NameSet := {}
    let mut count := 0
    while !todo.isEmpty do
      let name := todo.head!
      todo := todo.tail!
      unless seen.contains name do
        seen := seen.insert name
        count := count + 1
        if forbidden.contains name then
          throwError "Forbidden producer dependency: {root} reaches {name}"
        if let some info := env.find? name then
          if let some body := info.value? (allowOpaque := true) then
            todo := body.getUsedConstants.toList ++ todo
    logInfo m!"PASS_PRODUCER_DEPENDENCIES {root}: {count} declarations; no X/Y, lifts, target prefixes or conventional constants."
