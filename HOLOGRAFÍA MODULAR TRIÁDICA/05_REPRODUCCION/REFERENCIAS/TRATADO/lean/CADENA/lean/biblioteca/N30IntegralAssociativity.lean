import N30IntegralComposition

/-!
Coherence of the decimal normalization when three prospective finite families
are combined. This is a consequence of the explicit decimal quotient, not a
new selection of the terminal family. Event times are retained by `merge`.
-/
namespace HMT.N30IntegralComposition

open DodecaphaseLinear IncidenceRegister TerminalChannels IntegralEventRegister
open N30FamilyPublication

/-- The exact integer normalization defect is a cocycle. -/
theorem carryCorrection_cocycle (x y z : Int) :
    carryCorrection x y + carryCorrection (x + y) z =
      carryCorrection y z + carryCorrection x (y + z) := by
  unfold carryCorrection
  rw [add_assoc]
  omega

/-- Combining three families preserves the same normalization defect in
either bracketing. The equalities of boundary predicates are explicit. -/
theorem mergerCarry_cocycle (f g k : Family)
    (hgf : g.boundary = f.boundary) (hkg : k.boundary = g.boundary) :
    (fun m => mergerCarry f g m + mergerCarry (merge f g hgf) k m) =
      (fun m => mergerCarry g k m + mergerCarry f (merge g k hkg) m) := by
  funext m
  have hfg := merge_counts f g hgf m
  have hgk := merge_counts g k hkg m
  simp only [mergerCarry, hfg.1, hfg.2.1, hfg.2.2,
    hgk.1, hgk.2.1, hgk.2.2]
  have hA := carryCorrection_cocycle (A (familyLedger f) m)
    (A (familyLedger g) m) (A (familyLedger k) m)
  have hC := carryCorrection_cocycle (C (familyLedger f) m)
    (C (familyLedger g) m) (C (familyLedger k) m)
  have hV := carryCorrection_cocycle (V (familyLedger f) m)
    (V (familyLedger g) m) (V (familyLedger k) m)
  omega

theorem triple_publication_coherent (f g k : Family)
    (hgf : g.boundary = f.boundary) (hkg : k.boundary = g.boundary) :
    publishedVector (merge (merge f g hgf) k (hkg.trans hgf)) =
      publishedVector (merge f (merge g k hkg) hgf) := by
  rw [merge_publication_with_carry, merge_publication_with_carry,
    merge_publication_with_carry, merge_publication_with_carry]
  have h := mergerCarry_cocycle f g k hgf hkg
  funext m
  have hm := congrArg (fun v : Vector12 => v m) h
  dsimp only at hm ⊢
  omega

/-- Incremental integral reconstruction and reconstruction after the other
bracketing return exactly the same published vector. -/
theorem triple_integral_reconstruction_coherent (f g k : Family)
    (hgf : g.boundary = f.boundary) (hkg : k.boundary = g.boundary) :
    (((integralData f).add (mergerContribution f g)).add
      (mergerContribution (merge f g hgf) k)).register =
      ((integralData f).add (mergerContribution f (merge g k hkg))).register := by
  calc
    _ = ((integralData (merge f g hgf)).add
        (mergerContribution (merge f g hgf) k)).register := by
      rw [register_add, merge_integral_accumulation f g hgf,
        register_add, reconstruct_published]
    _ = publishedVector (merge (merge f g hgf) k (hkg.trans hgf)) :=
      merge_integral_accumulation (merge f g hgf) k (hkg.trans hgf)
    _ = publishedVector (merge f (merge g k hkg) hgf) :=
      triple_publication_coherent f g k hgf hkg
    _ = _ := (merge_integral_accumulation f (merge g k hkg) hgf).symm

#print axioms carryCorrection_cocycle
#print axioms mergerCarry_cocycle
#print axioms triple_publication_coherent
#print axioms triple_integral_reconstruction_coherent

end HMT.N30IntegralComposition
