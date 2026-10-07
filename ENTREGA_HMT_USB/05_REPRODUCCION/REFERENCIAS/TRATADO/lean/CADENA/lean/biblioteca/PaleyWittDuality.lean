import CoxeterNeighbor

/-! Autoduality of the explicit ternary code in the source chart exc:aw.
The first six coordinates are the input word; the last six are w A.
No lattice classification or VOA recognition is asserted here. -/
namespace HMT.PaleyWittDuality

open HMT.IV.CoxeterNeighbor

set_option maxHeartbeats 4000000

abbrev Word6 := Fin 6 → ZMod 3
abbrev Word12 := Fin 12 → ZMod 3

def head (v : Word12) : Word6 := fun i => v (Fin.castAdd 6 i)
def tail (v : Word12) : Word6 := fun i => v (Fin.natAdd 6 i)

theorem head_encode (w : Word6) : head (encode w) = w := by
  funext i
  simp [head, encode, i.isLt]

theorem tail_encode (w : Word6) : tail (encode w) = Matrix.vecMul w paleyWitt := by
  funext i
  simp [tail, encode, show ¬ 6 + i.val < 6 by omega]

theorem head_tail_ext (v u : Word12) (hh : head v = head u) (ht : tail v = tail u) :
    v = u := by
  funext i
  refine Fin.addCases (m := 6) (n := 6) (fun j => ?_) (fun j => ?_) i
  · exact congrFun hh j
  · exact congrFun ht j

theorem encoder_injective : Function.Injective encode := by
  intro v u h
  have hh := congrArg head h
  simpa only [head_encode] using hh

theorem paleyWitt_square : paleyWitt * paleyWitt = -(1 : Matrix (Fin 6) (Fin 6) (ZMod 3)) := by
  decide

theorem paleyWitt_symmetric : paleyWitt.transpose = paleyWitt := by
  decide

def unitWord (i : Fin 6) : Word6 := fun j => if j = i then 1 else 0

theorem basis_pairing (v : Word12) (i : Fin 6) :
    (∑ j, encode (unitWord i) j * v j) =
      head v i + Matrix.vecMul (tail v) paleyWitt i := by
  fin_cases i <;>
    norm_num [encode, unitWord, head, tail, Matrix.vecMul, dotProduct,
      Fin.sum_univ_succ, paleyWitt, Fin.castAdd, Fin.natAdd, Fin.addNat, Fin.succ] <;>
    dsimp [Fin.castLE] <;> ring

def orthogonal : Set Word12 :=
  {v | ∀ c ∈ wittCode, ∑ i, c i * v i = 0}

theorem orthogonal_head_relation (v : Word12) (hv : v ∈ orthogonal) :
    head v = -Matrix.vecMul (tail v) paleyWitt := by
  funext i
  have hc : encode (unitWord i) ∈ wittCode := ⟨unitWord i, rfl⟩
  have h := hv _ hc
  rw [basis_pairing] at h
  exact eq_neg_of_add_eq_zero_left h

theorem orthogonal_tail_relation (v : Word12) (hv : v ∈ orthogonal) :
    Matrix.vecMul (head v) paleyWitt = tail v := by
  rw [orthogonal_head_relation v hv, Matrix.neg_vecMul,
    Matrix.vecMul_vecMul, paleyWitt_square, Matrix.vecMul_neg,
    Matrix.vecMul_one, neg_neg]

theorem orthogonal_reconstructed (v : Word12) (hv : v ∈ orthogonal) :
    encode (head v) = v := by
  apply head_tail_ext
  · exact head_encode _
  · rw [tail_encode, orthogonal_tail_relation v hv]

theorem mem_orthogonal_iff (v : Word12) : v ∈ orthogonal ↔ v ∈ wittCode := by
  constructor
  · intro hv
    exact ⟨head v, orthogonal_reconstructed v hv⟩
  · intro hv c hc
    exact wittCode_selfOrthogonal c hc v hv

theorem wittCode_selfDual : orthogonal = (wittCode : Set Word12) := by
  ext v
  exact mem_orthogonal_iff v

def codeEquiv : Word6 ≃ wittCode where
  toFun := fun w => ⟨encode w, ⟨w, rfl⟩⟩
  invFun := fun c => head c.val
  left_inv := head_encode
  right_inv := by
    rintro ⟨c, w, rfl⟩
    apply Subtype.ext
    exact congrArg encode (head_encode w)

theorem code_cardinality : Nat.card wittCode = 3 ^ 6 := by
  rw [← Nat.card_congr codeEquiv, Nat.card_eq_fintype_card, Fintype.card_fun]
  simp

theorem code_cardinality_729 : Nat.card wittCode = 729 := by
  rw [code_cardinality]
  norm_num

#print axioms head_encode
#print axioms tail_encode
#print axioms head_tail_ext
#print axioms encoder_injective
#print axioms paleyWitt_square
#print axioms paleyWitt_symmetric
#print axioms basis_pairing
#print axioms orthogonal_head_relation
#print axioms orthogonal_tail_relation
#print axioms orthogonal_reconstructed
#print axioms mem_orthogonal_iff
#print axioms wittCode_selfDual
#print axioms codeEquiv
#print axioms code_cardinality
#print axioms code_cardinality_729

end HMT.PaleyWittDuality
