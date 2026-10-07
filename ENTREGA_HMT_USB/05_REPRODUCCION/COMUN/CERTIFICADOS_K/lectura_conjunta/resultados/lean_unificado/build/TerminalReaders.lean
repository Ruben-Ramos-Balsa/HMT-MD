import Mathlib

/-!
# N69 terminal readers

Executable translation of `transform6`, `linear_word`, `build_label_atlas`,
`edge_label_matches`, and the Boolean part of
`reader_type_profile_all_fields` in the two terminal-selector Python owners.

The N69 rows are explicit inputs. Six-trit words are encoded as natural
numbers below 729, with leading zeroes retained by fixed-width digit access.
The atlas forgets witness multiplicities and metadata, retaining precisely
the existence of each reader type needed by heterotypy. Pairing within one
row agrees with the Python equality-of-time join when input times are unique.
No assertion of the provenance of the rows or of a selected register is made.
-/

namespace HMT.I.TerminalSelector

structure N69Row where
  /-- Three six-trit channel words, in the order stored in `B`. -/
  bands : Array Nat
  /-- Six-trit words in the order `q`, `a`, `c`, `colw_mod`. -/
  fields : Array Nat
  time : Nat
  deriving Repr, Inhabited, DecidableEq

def validN69Row (row : N69Row) : Bool :=
  row.bands.size == 3 && row.fields.size == 4 &&
    row.bands.all (· < 729) && row.fields.all (· < 729)

/-- Left-to-right digit, with indices 0 through 5. -/
def digit6 (word index : Nat) : Nat :=
  (word / 3 ^ (5 - index)) % 3

/-- The Paley--Witt matrix `A_W` in the Python owner; row-vector convention. -/
def wittMatrix : Array (Array Nat) := #[
  #[0, 1, 1, 1, 1, 1],
  #[1, 0, 1, 2, 2, 1],
  #[1, 1, 0, 1, 2, 2],
  #[1, 2, 1, 0, 1, 2],
  #[1, 2, 2, 1, 0, 1],
  #[1, 1, 2, 2, 1, 0]]

/-- `transform6`: multiply the six-trit row by `A_W` over F₃. -/
def transform6 (word : Nat) : Nat := Id.run do
  let mut output := 0
  for j in [:6] do
    let mut total := 0
    for i in [:6] do
      total := total + digit6 word i * (wittMatrix[i]!)[j]!
    output := 3 * output + total % 3
  return output

/-- `linear_word`: three channel words and three coefficients over F₃. -/
def linearWord (bands coefficients : Array Nat) : Nat := Id.run do
  let mut output := 0
  for j in [:6] do
    let mut total := 0
    for i in [:3] do
      total := total + coefficients[i]! * digit6 bands[i]! j
    output := 3 * output + total % 3
  return output

def wordCharge (word : Nat) : Nat :=
  ((List.range 6).foldl (fun total j => total + digit6 word j) 0) % 3

/-- `(t - 1) % 3`, including the Python value 2 at `t = 0`. -/
def readerPhase (time : Nat) : Nat := (time + 2) % 3

/-- The twelve comparison labels of a row; repeated words are intentional. -/
def comparisonWords (row : N69Row) : Array Nat := Id.run do
  let visible := row.bands.map wordCharge
  let dual := row.bands.map (fun band => wordCharge (transform6 band))
  let phase := readerPhase row.time
  let mut outputs := #[]
  for charge in #[visible, dual] do
    for offset in [:3] do
      let selected := (phase + offset) % 3
      -- 2 is the canonical residue of the Python orientation -1.
      for orientation in #[1, 2] do
        let coefficients := charge.map fun value =>
          (orientation * (if value == selected then 1 else 2)) % 3
        outputs := outputs.push (linearWord row.bands coefficients)
  return outputs

/-- The affine `Witt-dual-mas-fase` word of a row. -/
def affineWord (row : N69Row) : Nat :=
  let phase := readerPhase row.time
  let coefficients := row.bands.map fun band =>
    (wordCharge (transform6 band) + phase) % 3
  linearWord row.bands coefficients

/-- Six left cyclic rotations, in the same order as Python `rotations`. -/
def rotations6 (word : Nat) : Array Nat := Id.run do
  let mut rotated := word
  let mut result := #[]
  for _ in [:6] do
    result := result.push rotated
    rotated := (rotated % 243) * 3 + rotated / 243
  return result

abbrev ReaderAtlas := Std.HashMap Nat Nat

/-- Bit 0 denotes comparison; bit 1 denotes affine. -/
def insertReader (atlas : ReaderAtlas) (child residue readerBit : Nat) : ReaderAtlas :=
  let key := child * 729 + residue
  atlas.insert key (atlas.getD key 0 ||| readerBit)

/--
Precompute all child-word/residue incidences. All four fields and all six
rotations are quantified, without prescribing a field or reader orientation.
For valid rows with distinct times this is the existential projection of the
Python labelled atlas and its same-time join, not a new source of N69 rows.
-/
def makeAtlas (rows : Array N69Row) : ReaderAtlas := Id.run do
  let mut atlas : ReaderAtlas := Std.HashMap.emptyWithCapacity 32768
  for row in rows do
    let residues := row.fields.flatMap rotations6
    for child in comparisonWords row do
      for residue in residues do
        atlas := insertReader atlas child residue 1
    let child := affineWord row
    for residue in residues do
      atlas := insertReader atlas child residue 2
  return atlas

/-- Coordinate `i` of the twelve decimal triples, indexed from zero. -/
def decimalCoordinate (numerator index : Nat) : Nat :=
  (numerator / 1000 ^ (11 - index)) % 1000

/-- Base-729 child block, with zero-based index (there are thirteen blocks). -/
def ternaryChild (numerator index : Nat) : Nat :=
  ((numerator * 729 ^ (index + 1)) / 10 ^ 36) % 729

/-- Oriented difference reduced in ℤ, not truncated subtraction in ℕ. -/
def orientedResidue (numerator source target : Nat) : Nat :=
  (((decimalCoordinate numerator source : Int) -
    (decimalCoordinate numerator target : Int)) % 729).toNat

def edgeReaderMask (atlas : ReaderAtlas) (numerator source target : Nat) : Nat :=
  atlas.getD
    (ternaryChild numerator target * 729 + orientedResidue numerator source target) 0

def hasComparison (mask : Nat) : Bool := mask % 2 == 1

def hasAffine (mask : Nat) : Bool := (mask / 2) % 2 == 1

/--
Reader heterotypy on the two edges 4→8 and 8→12 (human indices). Either
comparison/affine orientation is permitted; neither edge's type is fixed.
The caller supplies a decimal numerator below 10^36 and a precomputed atlas.
-/
def heterotypic (atlas : ReaderAtlas) (numerator : Nat) : Bool :=
  let left := edgeReaderMask atlas numerator 3 7
  let right := edgeReaderMask atlas numerator 7 11
  (hasComparison left && hasAffine right) ||
    (hasAffine left && hasComparison right)

end HMT.I.TerminalSelector
