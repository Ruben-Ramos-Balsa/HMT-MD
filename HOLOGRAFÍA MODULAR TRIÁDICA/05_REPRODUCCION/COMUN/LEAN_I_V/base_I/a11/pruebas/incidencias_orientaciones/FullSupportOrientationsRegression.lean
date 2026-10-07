import FullSupportNeighborOrientations

open HMT.I.FullSupportNeighborOrientations HMT.IV.CoxeterNeighbor

example : fullSupportWords.card = 24 := fullSupportWords_card

example (u : Word) (h : FullSupport u) :
    (fun i => (signWord (orientation u) i : ZMod 3)) = u :=
  signWord_mod3 u h

example (u : Word) (hu : u ∈ wittCode) (hf : FullSupport u) (o : Fin 12) :
    shift (orientation u) (marked o) ∈ kernel wittCode (radial (marked o)) ∧
    shift (fun i => !(orientation u i)) (marked o) ∈
      kernel wittCode (radial (marked o)) :=
  both_shifts_mem_kernel u hu hf o

example (u : Word) (hu : u ∈ wittCode) (hf : FullSupport u) (o : Fin 12) :
    orderOf (fullSupportNeighborEquiv u hu hf o) = 3 :=
  fullSupportNeighborEquiv_order u hu hf o

example (u : Word) (hu : u ∈ wittCode) (hf : FullSupport u)
    (o : Fin 12) (x : Space 12) :
    action (orientation u) x ∈ neighbor wittCode (radial (marked o)) ↔
      x ∈ neighbor wittCode (radial (marked o)) :=
  marked_neighbor_invariant u hu hf o x

example (u v : Word) (hu : FullSupport u) (hv : FullSupport v)
    (h : orientation u = orientation v) : u = v :=
  orientation_injective_on_fullSupport u v hu hv h
