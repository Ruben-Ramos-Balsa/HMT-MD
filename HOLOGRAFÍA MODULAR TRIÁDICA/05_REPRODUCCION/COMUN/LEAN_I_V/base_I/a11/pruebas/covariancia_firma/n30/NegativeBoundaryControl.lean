import N30BoundaryTransport

-- This must be rejected: phase return alone does not remove the sheet term.
example : HMT.N30.Boundary.spatialSum
    (HMT.N30.walk HMT.N30.Boundary.boundaryWitness HMT.N30.Boundary.northNine) =
    HMT.N30.Boundary.potential
      (HMT.N30.finish HMT.N30.Boundary.boundaryWitness HMT.N30.Boundary.northNine) -
    HMT.N30.Boundary.potential HMT.N30.Boundary.boundaryWitness := by
  decide
