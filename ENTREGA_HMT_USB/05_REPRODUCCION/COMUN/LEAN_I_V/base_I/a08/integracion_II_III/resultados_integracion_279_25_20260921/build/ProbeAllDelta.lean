import ArticleIIFromSharedBase
import ArticleIIIFromSharedBase
import CKMComplex
import CKMSpectral
import GeneratedAngularData
import QuarterTurn
import SelectedAngularBarbero
import ArticleIIIDimensionalReading
import ArticleIIIIISharedComposition
import CKMMassTransport
import GeneratedCKM
import NormalizedQuarterTurn
import CKMCycle
import OrientedSeries
import GeneratedCKMClosure
import MomentDerivatives
import SelectedCKM
import ArticleIICKMFromSharedBase
import PellSection
import SelectedJointCoupling
import MomentIntegral
import AngularBoundary
import AngularMoment
import PellTangentTripling
import ArticleIIICatalanPellFromSharedBase
import Lean.Util.CollectAxioms
open Lean Elab Command
run_elab do
  let env ← getEnv
  let selected : List String := ["ArticleIIFromSharedBase", "ArticleIIIFromSharedBase", "CKMComplex", "CKMSpectral", "GeneratedAngularData", "QuarterTurn", "SelectedAngularBarbero", "ArticleIIIDimensionalReading", "ArticleIIIIISharedComposition", "CKMMassTransport", "GeneratedCKM", "NormalizedQuarterTurn", "CKMCycle", "OrientedSeries", "GeneratedCKMClosure", "MomentDerivatives", "SelectedCKM", "ArticleIICKMFromSharedBase", "PellSection", "SelectedJointCoupling", "MomentIntegral", "AngularBoundary", "AngularMoment", "PellTangentTripling", "ArticleIIICatalanPellFromSharedBase"]
  for (name, _) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[idx.toNat]!
      if selected.contains owner.toString then
        let axioms ← Lean.collectAxioms name
        let names := String.intercalate "," (axioms.toList.map Name.toString)
        logInfo m!"CAPSULE_AXIOMS|{owner}|{name}|{names}"
