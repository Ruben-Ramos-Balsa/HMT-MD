import Std

/-
  Injective decimal coupling of the two finite-emission signatures.
  Source read in full: source_passages/extension.tex, especially
  eq:emisor-seis, eq:acoplamiento and the injective-factorization proof.
  This module receives signature residues already produced by the emitter;
  it does not select their trajectories and does not assume image censuses.
-/
namespace EmissionCode

abbrev Digit := Fin 10
abbrev Code := Fin 1000
abbrev Signature := Fin 6 → Digit
abbrev Word := Fin 6 → Code

def ofNat (n : Nat) : Digit := ⟨n % 10, Nat.mod_lt _ (by decide)⟩

def encodeValue (s e : Digit) : Nat :=
  100 * s.val + 10 * ((s.val + e.val) % 10) + (3 * s.val + 5 * e.val + 1) % 10

theorem encodeValue_lt (s e : Digit) : encodeValue s e < 1000 := by
  have hs := s.isLt
  have hb := Nat.mod_lt (s.val + e.val) (by decide : 0 < 10)
  have hc := Nat.mod_lt (3 * s.val + 5 * e.val + 1) (by decide : 0 < 10)
  unfold encodeValue
  omega

def encode (s e : Digit) : Code := ⟨encodeValue s e, encodeValue_lt s e⟩

theorem encode_val (s e : Digit) :
    (encode s e).val = 100 * s.val + 10 * ((s.val + e.val) % 10) +
      (3 * s.val + 5 * e.val + 1) % 10 := rfl

def hundreds (u : Code) : Digit :=
  ⟨u.val / 100, by have h := u.isLt; omega⟩

def tens (u : Code) : Digit := ⟨(u.val / 10) % 10, Nat.mod_lt _ (by decide)⟩
def units (u : Code) : Digit := ⟨u.val % 10, Nat.mod_lt _ (by decide)⟩

def recoverS (u : Code) : Digit := hundreds u

-- Adding 10 before Nat subtraction realizes the source's modular difference.
def recoverE (u : Code) : Digit :=
  ⟨((tens u).val + 10 - (hundreds u).val) % 10, Nat.mod_lt _ (by decide)⟩

theorem encode_hundreds (s e : Digit) : hundreds (encode s e) = s := by
  apply Fin.ext
  have hs := s.isLt
  have hb := Nat.mod_lt (s.val + e.val) (by decide : 0 < 10)
  have hc := Nat.mod_lt (3 * s.val + 5 * e.val + 1) (by decide : 0 < 10)
  change (100 * s.val + 10 * ((s.val + e.val) % 10) +
    (3 * s.val + 5 * e.val + 1) % 10) / 100 = s.val
  omega

theorem decimal_tens (a b c : Nat) (hb : b < 10) (hc : c < 10) :
    ((100 * a + 10 * b + c) / 10) % 10 = b := by
  have hdiv : (100 * a + 10 * b + c) / 10 = 10 * a + b := by omega
  rw [hdiv]
  simp [Nat.add_mod, Nat.mul_mod, Nat.mod_eq_of_lt hb]

theorem encode_tens_val (s e : Digit) :
    (tens (encode s e)).val = (s.val + e.val) % 10 := by
  have hb := Nat.mod_lt (s.val + e.val) (by decide : 0 < 10)
  have hc := Nat.mod_lt (3 * s.val + 5 * e.val + 1) (by decide : 0 < 10)
  change ((100 * s.val + 10 * ((s.val + e.val) % 10) +
    (3 * s.val + 5 * e.val + 1) % 10) / 10) % 10 = (s.val + e.val) % 10
  exact decimal_tens s.val ((s.val + e.val) % 10)
    ((3 * s.val + 5 * e.val + 1) % 10) hb hc

theorem encode_units_val (s e : Digit) :
    (units (encode s e)).val = (3 * s.val + 5 * e.val + 1) % 10 := by
  change (100 * s.val + 10 * ((s.val + e.val) % 10) +
    (3 * s.val + 5 * e.val + 1) % 10) % 10 = (3 * s.val + 5 * e.val + 1) % 10
  simp [Nat.add_mod, Nat.mul_mod]

theorem recoverS_encode (s e : Digit) : recoverS (encode s e) = s :=
  encode_hundreds s e

theorem recoverE_encode (s e : Digit) : recoverE (encode s e) = e := by
  apply Fin.ext
  change ((tens (encode s e)).val + 10 - (hundreds (encode s e)).val) % 10 = e.val
  rw [encode_tens_val, encode_hundreds]
  have hs := s.isLt
  have he := e.isLt
  omega

theorem encode_injective (s e s' e' : Digit) (h : encode s e = encode s' e') :
    s = s' ∧ e = e' := by
  constructor
  · exact (recoverS_encode s e).symm.trans
      ((congrArg recoverS h).trans (recoverS_encode s' e'))
  · exact (recoverE_encode s e).symm.trans
      ((congrArg recoverE h).trans (recoverE_encode s' e'))

theorem decimal_reconstruction (u : Code) :
    u.val = 100 * (hundreds u).val + 10 * (tens u).val + (units u).val := by
  have hu := u.isLt
  dsimp [hundreds, tens, units]
  omega

theorem recovered_tens (u : Code) :
    ((recoverS u).val + (recoverE u).val) % 10 = (tens u).val := by
  have hs := (hundreds u).isLt
  have hb := (tens u).isLt
  change ((hundreds u).val + (((tens u).val + 10 - (hundreds u).val) % 10)) % 10 =
    (tens u).val
  omega

def ValidCode (u : Code) : Prop :=
  (units u).val = (3 * (recoverS u).val + 5 * (recoverE u).val + 1) % 10

theorem encode_valid (s e : Digit) : ValidCode (encode s e) := by
  unfold ValidCode
  rw [recoverS_encode, recoverE_encode]
  exact encode_units_val s e

theorem encode_recovered (u : Code) (h : ValidCode u) :
    encode (recoverS u) (recoverE u) = u := by
  apply Fin.ext
  rw [encode_val, recovered_tens]
  change 100 * (hundreds u).val + 10 * (tens u).val +
    (3 * (recoverS u).val + 5 * (recoverE u).val + 1) % 10 = u.val
  rw [← h]
  exact (decimal_reconstruction u).symm

theorem image_characterization (u : Code) :
    (∃ s e : Digit, encode s e = u) ↔ ValidCode u := by
  constructor
  · intro h
    obtain ⟨s, e, rfl⟩ := h
    exact encode_valid s e
  · intro h
    exact ⟨recoverS u, recoverE u, encode_recovered u h⟩

-- Actual unreduced window totals, with neutral count supplied separately.
def sourceCode (S E Z : Nat) : Nat :=
  100 * (S % 10) + 10 * ((S + E) % 10) + (3 * S + 5 * E + 7 * Z) % 10

theorem sourceCode_reduced (S E : Nat) :
    sourceCode S E 3 = (encode (ofNat S) (ofNat E)).val := by
  simp [sourceCode, encode, encodeValue, ofNat, Nat.add_mod, Nat.mul_mod]

theorem sourceCode_reduced_of_neutral (S E Z : Nat) (hZ : Z = 3) :
    sourceCode S E Z = (encode (ofNat S) (ofNat E)).val := by
  rw [hZ]
  exact sourceCode_reduced S E

-- The same modular equivalence also holds for arbitrary signed integers.
theorem signed_source_reduced (S E : Int) :
    100 * (S % 10) + 10 * ((S + E) % 10) + (3 * S + 5 * E + 7 * 3) % 10 =
    100 * (S % 10) + 10 * (((S % 10) + (E % 10)) % 10) +
      (3 * (S % 10) + 5 * (E % 10) + 1) % 10 := by
  simp [Int.add_emod, Int.mul_emod]

def encodeWord (s e : Signature) : Word := fun k => encode (s k) (e k)
def recoverSWord (u : Word) : Signature := fun k => recoverS (u k)
def recoverEWord (u : Word) : Signature := fun k => recoverE (u k)

theorem encodeWord_val_at (s e : Signature) (k : Fin 6) :
    (encodeWord s e k).val = 100 * (s k).val +
      10 * (((s k).val + (e k).val) % 10) +
      (3 * (s k).val + 5 * (e k).val + 1) % 10 := rfl

theorem recoverSWord_encode (s e : Signature) : recoverSWord (encodeWord s e) = s := by
  funext k
  exact recoverS_encode (s k) (e k)

theorem recoverEWord_encode (s e : Signature) : recoverEWord (encodeWord s e) = e := by
  funext k
  exact recoverE_encode (s k) (e k)

theorem encodeWord_injective (s e s' e' : Signature)
    (h : encodeWord s e = encodeWord s' e') : s = s' ∧ e = e' := by
  constructor
  · exact (recoverSWord_encode s e).symm.trans
      ((congrArg recoverSWord h).trans (recoverSWord_encode s' e'))
  · exact (recoverEWord_encode s e).symm.trans
      ((congrArg recoverEWord h).trans (recoverEWord_encode s' e'))

theorem word_image_characterization (u : Word) :
    (∃ s e : Signature, encodeWord s e = u) ↔ ∀ k, ValidCode (u k) := by
  constructor
  · intro h
    obtain ⟨s, e, rfl⟩ := h
    intro k
    exact encode_valid (s k) (e k)
  · intro h
    refine ⟨recoverSWord u, recoverEWord u, ?_⟩
    funext k
    exact encode_recovered (u k) (h k)

end EmissionCode

#print axioms EmissionCode.encodeValue_lt
#print axioms EmissionCode.encode_val
#print axioms EmissionCode.encode_hundreds
#print axioms EmissionCode.decimal_tens
#print axioms EmissionCode.encode_tens_val
#print axioms EmissionCode.encode_units_val
#print axioms EmissionCode.recoverS_encode
#print axioms EmissionCode.recoverE_encode
#print axioms EmissionCode.encode_injective
#print axioms EmissionCode.decimal_reconstruction
#print axioms EmissionCode.recovered_tens
#print axioms EmissionCode.encode_valid
#print axioms EmissionCode.encode_recovered
#print axioms EmissionCode.image_characterization
#print axioms EmissionCode.sourceCode_reduced
#print axioms EmissionCode.sourceCode_reduced_of_neutral
#print axioms EmissionCode.signed_source_reduced
#print axioms EmissionCode.encodeWord_val_at
#print axioms EmissionCode.recoverSWord_encode
#print axioms EmissionCode.recoverEWord_encode
#print axioms EmissionCode.encodeWord_injective
#print axioms EmissionCode.word_image_characterization
