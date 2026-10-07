import MarkedNeighborGroup

/-!
The pairing character of the marked ternary neighbour is constructed from the
integral glue. A displayed simple root maps to one, so the index-three statement
is a conclusion, not a field of the lattice data. No Leech/VOA classification is
used. Source: IV, excepcional.tex, proof of exc:teorema-leech, lines 690–716.
-/
namespace HMT.IV.CoxeterNeighbor

set_option maxHeartbeats 2000000

theorem radial_mem_glue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) : radial t ∈ glue C := by
  refine ⟨(fun i => 1 + 3 * t i), (fun i => 1 + 3 * t i), 0, ?_, ?_⟩
  · simpa using C.zero_mem
  · intro i
    ext <;> simp [radial]

noncomputable def integralPairing {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (v : Space n) (hv : v ∈ glue C) (x : glue C) : ℤ :=
  Classical.choose (hC x x.property v hv)

theorem cast_integralPairing {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (v : Space n) (hv : v ∈ glue C) (x : glue C) :
    (integralPairing C hC v hv x : ℚ) = pairing x v :=
  (Classical.choose_spec (hC x x.property v hv)).symm

noncomputable def integerPairHom {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (v : Space n) (hv : v ∈ glue C) : glue C →+ ℤ where
  toFun := integralPairing C hC v hv
  map_zero' := by
    apply Int.cast_injective (α := ℚ)
    rw [cast_integralPairing]
    simp [pairing, localPair]
  map_add' := by
    intro x y
    apply Int.cast_injective (α := ℚ)
    rw [cast_integralPairing, Int.cast_add, cast_integralPairing, cast_integralPairing]
    exact pairing_add_left (x : Space n) (y : Space n) v

noncomputable def pairingCharacter {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (v : Space n) (hv : v ∈ glue C) : glue C →+ ZMod 3 :=
  (Int.castAddHom (ZMod 3)).comp (integerPairHom C hC v hv)

def kernelInGlue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n) :
    AddSubgroup (glue C) := (kernelSubgroup C v).comap (glue C).subtype

theorem pairingCharacter_ker {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (v : Space n) (hv : v ∈ glue C) :
    (pairingCharacter C hC v hv).ker = kernelInGlue C v := by
  ext x
  change (integralPairing C hC v hv x : ZMod 3) = 0 ↔
    (x : Space n) ∈ kernel C v
  rw [ZMod.intCast_zmod_eq_zero_iff_dvd]
  constructor
  · rintro ⟨k, hk⟩
    refine ⟨x.property, k, ?_⟩
    rw [← cast_integralPairing C hC v hv x, hk]
    push_cast
    rfl
  · rintro ⟨_, k, hk⟩
    refine ⟨k, ?_⟩
    apply Int.cast_injective (α := ℚ)
    rw [cast_integralPairing, hk]
    push_cast
    rfl

def simpleRoot {n : ℕ} (j : Fin n) : Space n :=
  fun i => if i = j then (1, 0) else (0, 0)

theorem simpleRoot_mem_glue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (j : Fin n) : simpleRoot j ∈ glue C := by
  refine ⟨(fun i => if i = j then 1 else 0), 0, 0, ?_, ?_⟩
  · simpa using C.zero_mem
  · intro i
    by_cases h : i = j <;> simp [simpleRoot, h]

theorem simpleRoot_pairing_radial {n : ℕ} (j : Fin n) (t : Fin n → ℤ) :
    pairing (simpleRoot j) (radial t) = 1 + 3 * (t j : ℚ) := by
  classical
  unfold pairing
  have term : ∀ i, localPair (simpleRoot j i) (radial t i) =
      if i = j then 1 + 3 * (t j : ℚ) else 0 := by
    intro i
    by_cases h : i = j
    · subst i
      simp [simpleRoot, radial, localPair]
      ring
    · simp [simpleRoot, h, localPair]
  simp_rw [term]
  simp

theorem pairingCharacter_simpleRoot {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (t : Fin n → ℤ) (j : Fin n) :
    pairingCharacter C hC (radial t) (radial_mem_glue C t)
      ⟨simpleRoot j, simpleRoot_mem_glue C j⟩ = 1 := by
  have h : integralPairing C hC (radial t) (radial_mem_glue C t)
      ⟨simpleRoot j, simpleRoot_mem_glue C j⟩ = 1 + 3 * t j := by
    apply Int.cast_injective (α := ℚ)
    rw [cast_integralPairing, simpleRoot_pairing_radial]
    push_cast
    rfl
  change (integralPairing C hC (radial t) (radial_mem_glue C t)
      ⟨simpleRoot j, simpleRoot_mem_glue C j⟩ : ZMod 3) = 1
  rw [h]
  push_cast
  have h3 : (3 : ZMod 3) = 0 := by decide
  rw [h3]
  simp

theorem pairingCharacter_surjective {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : IntegralGlue C) (t : Fin n → ℤ) (j : Fin n) :
    Function.Surjective (pairingCharacter C hC (radial t) (radial_mem_glue C t)) := by
  intro z
  refine ⟨z.val • (⟨simpleRoot j, simpleRoot_mem_glue C j⟩ : glue C), ?_⟩
  rw [map_nsmul, pairingCharacter_simpleRoot]
  simp

noncomputable def markedKernelQuotientEquiv
    (C : AddSubgroup (Fin 12 → ZMod 3)) (hC : IntegralGlue C) (o : Fin 12) :
    (glue C) ⧸ (kernelInGlue C (radial (marked o))) ≃+ ZMod 3 := by
  let f := pairingCharacter C hC (radial (marked o)) (radial_mem_glue C (marked o))
  have hf : Function.Surjective f := pairingCharacter_surjective C hC (marked o) o
  have hk : f.ker = kernelInGlue C (radial (marked o)) := pairingCharacter_ker C hC _ _
  rw [← hk]
  exact QuotientAddGroup.quotientKerEquivOfSurjective f hf

theorem markedKernel_quotient_card
    (C : AddSubgroup (Fin 12 → ZMod 3)) (hC : IntegralGlue C) (o : Fin 12) :
    Nat.card ((glue C) ⧸ (kernelInGlue C (radial (marked o)))) = 3 := by
  rw [Nat.card_congr (markedKernelQuotientEquiv C hC o).toEquiv]
  simp

theorem markedKernel_index
    (C : AddSubgroup (Fin 12 → ZMod 3)) (hC : IntegralGlue C) (o : Fin 12) :
    (kernelInGlue C (radial (marked o))).index = 3 := by
  rw [AddSubgroup.index_eq_card]
  exact markedKernel_quotient_card C hC o

theorem witt_markedKernel_index (o : Fin 12) :
    (kernelInGlue wittCode (radial (marked o))).index = 3 :=
  markedKernel_index wittCode witt_glue_integral o

theorem witt_markedKernel_relindex (o : Fin 12) :
    (kernelSubgroup wittCode (radial (marked o))).relindex (glue wittCode) = 3 :=
  witt_markedKernel_index o

#print axioms radial_mem_glue
#print axioms cast_integralPairing
#print axioms integerPairHom
#print axioms pairingCharacter_ker
#print axioms simpleRoot_mem_glue
#print axioms simpleRoot_pairing_radial
#print axioms pairingCharacter_simpleRoot
#print axioms pairingCharacter_surjective
#print axioms markedKernelQuotientEquiv
#print axioms markedKernel_quotient_card
#print axioms markedKernel_index
#print axioms witt_markedKernel_index
#print axioms witt_markedKernel_relindex

end HMT.IV.CoxeterNeighbor
