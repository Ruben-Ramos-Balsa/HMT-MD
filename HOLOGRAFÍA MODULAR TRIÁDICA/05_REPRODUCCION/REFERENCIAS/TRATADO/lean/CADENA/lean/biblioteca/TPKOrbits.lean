import TPKCensus

/-!
D3 acts on six-coordinate emissions and their ternary publication.
All finite witnesses below are outputs whose equality to TPKCensus is
proved by kernel reduction. No catalogue or cardinal is an input.
-/
namespace TPKOrbits
set_option maxRecDepth 1000000
set_option maxHeartbeats 0

structure Word where
  a : Nat
  b : Nat
  c : Nat
  d : Nat
  e : Nat
  f : Nat
  deriving DecidableEq, Repr

def toList (w : Word) : List Nat := [w.a, w.b, w.c, w.d, w.e, w.f]
def ofList (w : List Nat) : Word :=
  ⟨w.getD 0 0, w.getD 1 0, w.getD 2 0, w.getD 3 0, w.getD 4 0, w.getD 5 0⟩

theorem ofList_toList (w : Word) : ofList (toList w) = w := by cases w; rfl

def rotate (w : Word) : Word := ⟨w.c, w.a, w.b, w.e, w.f, w.d⟩
def swap (w : Word) : Word := ⟨w.d, w.e, w.f, w.a, w.b, w.c⟩

theorem rotate_cube (w : Word) : rotate (rotate (rotate w)) = w := by cases w; rfl
theorem swap_square (w : Word) : swap (swap w) = w := by cases w; rfl
theorem dihedral_relation (w : Word) :
    swap (rotate (swap w)) = rotate (rotate w) := by cases w; rfl

inductive D3 where
  | one | r | r2 | s | sr | sr2
  deriving DecidableEq, Repr

def actions : List D3 := [.one, .r, .r2, .s, .sr, .sr2]

theorem actions_complete (g : D3) : g ∈ actions := by cases g <;> decide

def act : D3 → Word → Word
  | .one, w => w
  | .r, w => rotate w
  | .r2, w => rotate (rotate w)
  | .s, w => swap w
  | .sr, w => swap (rotate w)
  | .sr2, w => swap (rotate (rotate w))

def compose : D3 → D3 → D3
  | .one, .one => .one
  | .one, .r => .r
  | .one, .r2 => .r2
  | .one, .s => .s
  | .one, .sr => .sr
  | .one, .sr2 => .sr2
  | .r, .one => .r
  | .r, .r => .r2
  | .r, .r2 => .one
  | .r, .s => .sr2
  | .r, .sr => .s
  | .r, .sr2 => .sr
  | .r2, .one => .r2
  | .r2, .r => .one
  | .r2, .r2 => .r
  | .r2, .s => .sr
  | .r2, .sr => .sr2
  | .r2, .sr2 => .s
  | .s, .one => .s
  | .s, .r => .sr
  | .s, .r2 => .sr2
  | .s, .s => .one
  | .s, .sr => .r
  | .s, .sr2 => .r2
  | .sr, .one => .sr
  | .sr, .r => .sr2
  | .sr, .r2 => .s
  | .sr, .s => .r2
  | .sr, .sr => .one
  | .sr, .sr2 => .r
  | .sr2, .one => .sr2
  | .sr2, .r => .s
  | .sr2, .r2 => .sr
  | .sr2, .s => .r
  | .sr2, .sr => .r2
  | .sr2, .sr2 => .one

def inverse : D3 → D3
  | .one => .one
  | .r => .r2
  | .r2 => .r
  | .s => .s
  | .sr => .sr
  | .sr2 => .sr2

theorem compose_associative (g h k : D3) :
    compose (compose g h) k = compose g (compose h k) := by
  cases g <;> cases h <;> cases k <;> rfl

theorem compose_identity (g : D3) :
    compose .one g = g ∧ compose g .one = g := by cases g <;> exact ⟨rfl, rfl⟩

theorem compose_inverse (g : D3) :
    compose (inverse g) g = .one ∧ compose g (inverse g) = .one := by
  cases g <;> exact ⟨rfl, rfl⟩

theorem action_composition (g h : D3) (w : Word) :
    act (compose g h) w = act g (act h w) := by
  cases g <;> cases h <;> cases w <;> rfl

theorem action_inverse (g : D3) (w : Word) :
    act (inverse g) (act g w) = w := by cases g <;> cases w <;> rfl

def psi (w : Word) : Word :=
  ⟨(3 - w.a % 3) % 3, (3 - w.b % 3) % 3, (3 - w.c % 3) % 3,
   (3 - w.d % 3) % 3, (3 - w.e % 3) % 3, (3 - w.f % 3) % 3⟩

theorem psi_toList (w : Word) : toList (psi w) = TPKCensus.ternary (toList w) := rfl

theorem psi_equivariant (g : D3) (w : Word) :
    psi (act g w) = act g (psi w) := by cases g <;> rfl

def orbit (w : Word) : List Word := (actions.map (fun g => act g w)).eraseDups

theorem mem_orbit (w v : Word) : v ∈ orbit w ↔ ∃ g : D3, act g w = v := by
  rw [orbit, TPKCensus.mem_eraseDups, List.mem_map]
  constructor
  · rintro ⟨g, _, h⟩
    exact ⟨g, h⟩
  · rintro ⟨g, h⟩
    exact ⟨g, actions_complete g, h⟩

theorem orbit_refl (w : Word) : w ∈ orbit w := (mem_orbit w w).2 ⟨.one, rfl⟩

theorem orbit_symm {w v : Word} (h : v ∈ orbit w) : w ∈ orbit v := by
  obtain ⟨g, hg⟩ := (mem_orbit w v).1 h
  apply (mem_orbit v w).2
  exact ⟨inverse g, by rw [← hg]; exact action_inverse g w⟩

theorem orbit_trans {u v w : Word} (h₁ : v ∈ orbit u) (h₂ : w ∈ orbit v) :
    w ∈ orbit u := by
  obtain ⟨g, hg⟩ := (mem_orbit u v).1 h₁
  obtain ⟨h, hh⟩ := (mem_orbit v w).1 h₂
  apply (mem_orbit u w).2
  exact ⟨compose h g, by rw [action_composition, hg, hh]⟩

def orbitSetoid : Setoid Word where
  r w v := v ∈ orbit w
  iseqv := ⟨orbit_refl, fun h => orbit_symm h, fun h₁ h₂ => orbit_trans h₁ h₂⟩

def emissionWords : List Word := TPKCensus.emitted.map ofList
def producedWords : List Word := TPKCensus.ternaryImage.map ofList

/- Literal output witnesses, not defining inputs to emissionWords/producedWords. -/
def emissionWitness : List Word := [
  ⟨252, 109, 252, 903, 850, 850⟩,
  ⟨232, 189, 292, 923, 870, 810⟩,
  ⟨272, 169, 272, 923, 810, 870⟩,
  ⟨252, 149, 212, 943, 830, 830⟩,
  ⟨227, 114, 227, 998, 885, 885⟩,
  ⟨292, 189, 232, 903, 850, 850⟩,
  ⟨232, 189, 292, 963, 850, 890⟩,
  ⟨292, 129, 292, 943, 830, 830⟩,
  ⟨292, 189, 232, 923, 810, 870⟩,
  ⟨272, 169, 272, 963, 890, 850⟩,
  ⟨252, 149, 212, 963, 850, 890⟩,
  ⟨292, 189, 232, 943, 830, 830⟩,
  ⟨212, 149, 252, 963, 890, 850⟩,
  ⟨272, 169, 272, 963, 850, 890⟩,
  ⟨292, 129, 292, 983, 810, 810⟩,
  ⟨292, 129, 292, 963, 890, 850⟩,
  ⟨272, 169, 272, 983, 810, 810⟩,
  ⟨212, 149, 252, 943, 830, 830⟩,
  ⟨252, 109, 252, 943, 830, 830⟩,
  ⟨272, 169, 272, 923, 870, 810⟩,
  ⟨252, 109, 252, 923, 870, 810⟩,
  ⟨272, 169, 272, 903, 850, 850⟩,
  ⟨232, 189, 292, 943, 830, 830⟩,
  ⟨212, 149, 252, 923, 810, 870⟩,
  ⟨252, 149, 212, 983, 810, 810⟩,
  ⟨272, 169, 272, 943, 830, 830⟩,
  ⟨923, 870, 810, 232, 189, 292⟩,
  ⟨903, 850, 850, 252, 109, 252⟩,
  ⟨943, 830, 830, 252, 149, 212⟩,
  ⟨923, 810, 870, 272, 169, 272⟩,
  ⟨998, 885, 885, 227, 114, 227⟩,
  ⟨963, 850, 890, 232, 189, 292⟩,
  ⟨903, 850, 850, 292, 189, 232⟩,
  ⟨963, 890, 850, 272, 169, 272⟩,
  ⟨963, 850, 890, 252, 149, 212⟩,
  ⟨943, 830, 830, 292, 129, 292⟩,
  ⟨923, 810, 870, 292, 189, 232⟩,
  ⟨963, 850, 890, 272, 169, 272⟩,
  ⟨983, 810, 810, 292, 129, 292⟩,
  ⟨943, 830, 830, 292, 189, 232⟩,
  ⟨963, 890, 850, 212, 149, 252⟩,
  ⟨963, 890, 850, 292, 129, 292⟩,
  ⟨943, 830, 830, 212, 149, 252⟩,
  ⟨983, 810, 810, 272, 169, 272⟩,
  ⟨923, 870, 810, 272, 169, 272⟩,
  ⟨943, 830, 830, 252, 109, 252⟩,
  ⟨923, 870, 810, 252, 109, 252⟩,
  ⟨943, 830, 830, 232, 189, 292⟩,
  ⟨903, 850, 850, 272, 169, 272⟩,
  ⟨983, 810, 810, 252, 149, 212⟩,
  ⟨923, 810, 870, 212, 149, 252⟩,
  ⟨943, 830, 830, 272, 169, 272⟩,
  ⟨694, 438, 581, 232, 189, 292⟩,
  ⟨674, 418, 521, 252, 109, 252⟩,
  ⟨614, 498, 501, 252, 149, 212⟩,
  ⟨694, 478, 541, 272, 169, 272⟩,
  ⟨669, 443, 556, 227, 114, 227⟩,
  ⟨634, 418, 561, 232, 189, 292⟩,
  ⟨674, 418, 521, 292, 189, 232⟩,
  ⟨634, 458, 521, 272, 169, 272⟩,
  ⟨634, 418, 561, 252, 149, 212⟩,
  ⟨614, 498, 501, 292, 129, 292⟩,
  ⟨694, 478, 541, 292, 189, 232⟩,
  ⟨634, 418, 561, 272, 169, 272⟩,
  ⟨654, 478, 581, 292, 129, 292⟩,
  ⟨614, 498, 501, 292, 189, 232⟩,
  ⟨634, 458, 521, 212, 149, 252⟩,
  ⟨634, 458, 521, 292, 129, 292⟩,
  ⟨614, 498, 501, 212, 149, 252⟩,
  ⟨654, 478, 581, 272, 169, 272⟩,
  ⟨694, 438, 581, 272, 169, 272⟩,
  ⟨614, 498, 501, 252, 109, 252⟩,
  ⟨694, 438, 581, 252, 109, 252⟩,
  ⟨614, 498, 501, 232, 189, 292⟩,
  ⟨674, 418, 521, 272, 169, 272⟩,
  ⟨654, 478, 581, 252, 149, 212⟩,
  ⟨694, 478, 541, 212, 149, 252⟩,
  ⟨614, 498, 501, 272, 169, 272⟩,
  ⟨252, 109, 252, 674, 418, 521⟩,
  ⟨232, 189, 292, 694, 438, 581⟩,
  ⟨272, 169, 272, 694, 478, 541⟩,
  ⟨252, 149, 212, 614, 498, 501⟩,
  ⟨227, 114, 227, 669, 443, 556⟩,
  ⟨292, 189, 232, 674, 418, 521⟩,
  ⟨232, 189, 292, 634, 418, 561⟩,
  ⟨292, 129, 292, 614, 498, 501⟩,
  ⟨292, 189, 232, 694, 478, 541⟩,
  ⟨272, 169, 272, 634, 458, 521⟩,
  ⟨252, 149, 212, 634, 418, 561⟩,
  ⟨292, 189, 232, 614, 498, 501⟩,
  ⟨212, 149, 252, 634, 458, 521⟩,
  ⟨272, 169, 272, 634, 418, 561⟩,
  ⟨292, 129, 292, 654, 478, 581⟩,
  ⟨292, 129, 292, 634, 458, 521⟩,
  ⟨272, 169, 272, 654, 478, 581⟩,
  ⟨212, 149, 252, 614, 498, 501⟩,
  ⟨252, 109, 252, 614, 498, 501⟩,
  ⟨272, 169, 272, 694, 438, 581⟩,
  ⟨252, 109, 252, 694, 438, 581⟩,
  ⟨272, 169, 272, 674, 418, 521⟩,
  ⟨232, 189, 292, 614, 498, 501⟩,
  ⟨212, 149, 252, 694, 478, 541⟩,
  ⟨252, 149, 212, 654, 478, 581⟩,
  ⟨272, 169, 272, 614, 498, 501⟩,
  ⟨923, 870, 810, 561, 418, 634⟩,
  ⟨903, 850, 850, 581, 438, 694⟩,
  ⟨943, 830, 830, 581, 478, 654⟩,
  ⟨923, 810, 870, 501, 498, 614⟩,
  ⟨998, 885, 885, 556, 443, 669⟩,
  ⟨963, 850, 890, 561, 418, 634⟩,
  ⟨903, 850, 850, 521, 418, 674⟩,
  ⟨963, 890, 850, 501, 498, 614⟩,
  ⟨963, 850, 890, 581, 478, 654⟩,
  ⟨943, 830, 830, 521, 458, 634⟩,
  ⟨923, 810, 870, 521, 418, 674⟩,
  ⟨963, 850, 890, 501, 498, 614⟩,
  ⟨983, 810, 810, 521, 458, 634⟩,
  ⟨943, 830, 830, 521, 418, 674⟩,
  ⟨963, 890, 850, 541, 478, 694⟩,
  ⟨963, 890, 850, 521, 458, 634⟩,
  ⟨943, 830, 830, 541, 478, 694⟩,
  ⟨983, 810, 810, 501, 498, 614⟩,
  ⟨923, 870, 810, 501, 498, 614⟩,
  ⟨943, 830, 830, 581, 438, 694⟩,
  ⟨923, 870, 810, 581, 438, 694⟩,
  ⟨943, 830, 830, 561, 418, 634⟩,
  ⟨903, 850, 850, 501, 498, 614⟩,
  ⟨983, 810, 810, 581, 478, 654⟩,
  ⟨923, 810, 870, 541, 478, 694⟩,
  ⟨943, 830, 830, 501, 498, 614⟩,
  ⟨581, 438, 694, 903, 850, 850⟩,
  ⟨561, 418, 634, 923, 870, 810⟩,
  ⟨501, 498, 614, 923, 810, 870⟩,
  ⟨581, 478, 654, 943, 830, 830⟩,
  ⟨556, 443, 669, 998, 885, 885⟩,
  ⟨521, 418, 674, 903, 850, 850⟩,
  ⟨561, 418, 634, 963, 850, 890⟩,
  ⟨521, 458, 634, 943, 830, 830⟩,
  ⟨521, 418, 674, 923, 810, 870⟩,
  ⟨501, 498, 614, 963, 890, 850⟩,
  ⟨581, 478, 654, 963, 850, 890⟩,
  ⟨521, 418, 674, 943, 830, 830⟩,
  ⟨541, 478, 694, 963, 890, 850⟩,
  ⟨501, 498, 614, 963, 850, 890⟩,
  ⟨521, 458, 634, 983, 810, 810⟩,
  ⟨521, 458, 634, 963, 890, 850⟩,
  ⟨501, 498, 614, 983, 810, 810⟩,
  ⟨541, 478, 694, 943, 830, 830⟩,
  ⟨581, 438, 694, 943, 830, 830⟩,
  ⟨501, 498, 614, 923, 870, 810⟩,
  ⟨581, 438, 694, 923, 870, 810⟩,
  ⟨501, 498, 614, 903, 850, 850⟩,
  ⟨561, 418, 634, 943, 830, 830⟩,
  ⟨541, 478, 694, 923, 810, 870⟩,
  ⟨581, 478, 654, 983, 810, 810⟩,
  ⟨501, 498, 614, 943, 830, 830⟩,
  ⟨252, 212, 149, 890, 850, 963⟩,
  ⟨232, 292, 189, 810, 870, 923⟩,
  ⟨272, 272, 169, 810, 810, 983⟩,
  ⟨252, 252, 109, 830, 830, 943⟩,
  ⟨227, 227, 114, 885, 885, 998⟩,
  ⟨292, 292, 129, 890, 850, 963⟩,
  ⟨232, 292, 189, 850, 850, 903⟩,
  ⟨292, 232, 189, 830, 830, 943⟩,
  ⟨292, 292, 129, 810, 810, 983⟩,
  ⟨272, 272, 169, 850, 890, 963⟩,
  ⟨252, 252, 109, 850, 850, 903⟩,
  ⟨292, 292, 129, 830, 830, 943⟩,
  ⟨212, 252, 149, 850, 890, 963⟩,
  ⟨272, 272, 169, 850, 850, 903⟩,
  ⟨292, 232, 189, 870, 810, 923⟩,
  ⟨292, 232, 189, 850, 890, 963⟩,
  ⟨272, 272, 169, 870, 810, 923⟩,
  ⟨212, 252, 149, 830, 830, 943⟩,
  ⟨252, 212, 149, 830, 830, 943⟩,
  ⟨272, 272, 169, 810, 870, 923⟩,
  ⟨252, 212, 149, 810, 870, 923⟩,
  ⟨272, 272, 169, 890, 850, 963⟩,
  ⟨232, 292, 189, 830, 830, 943⟩,
  ⟨212, 252, 149, 810, 810, 983⟩,
  ⟨252, 252, 109, 870, 810, 923⟩,
  ⟨272, 272, 169, 830, 830, 943⟩,
  ⟨810, 870, 923, 232, 292, 189⟩,
  ⟨890, 850, 963, 252, 212, 149⟩,
  ⟨830, 830, 943, 252, 252, 109⟩,
  ⟨810, 810, 983, 272, 272, 169⟩,
  ⟨885, 885, 998, 227, 227, 114⟩,
  ⟨850, 850, 903, 232, 292, 189⟩,
  ⟨890, 850, 963, 292, 292, 129⟩,
  ⟨850, 890, 963, 272, 272, 169⟩,
  ⟨850, 850, 903, 252, 252, 109⟩,
  ⟨830, 830, 943, 292, 232, 189⟩,
  ⟨810, 810, 983, 292, 292, 129⟩,
  ⟨850, 850, 903, 272, 272, 169⟩,
  ⟨870, 810, 923, 292, 232, 189⟩,
  ⟨830, 830, 943, 292, 292, 129⟩,
  ⟨850, 890, 963, 212, 252, 149⟩,
  ⟨850, 890, 963, 292, 232, 189⟩,
  ⟨830, 830, 943, 212, 252, 149⟩,
  ⟨870, 810, 923, 272, 272, 169⟩,
  ⟨810, 870, 923, 272, 272, 169⟩,
  ⟨830, 830, 943, 252, 212, 149⟩,
  ⟨810, 870, 923, 252, 212, 149⟩,
  ⟨830, 830, 943, 232, 292, 189⟩,
  ⟨890, 850, 963, 272, 272, 169⟩,
  ⟨870, 810, 923, 252, 252, 109⟩,
  ⟨810, 810, 983, 212, 252, 149⟩,
  ⟨830, 830, 943, 272, 272, 169⟩,
  ⟨581, 654, 478, 129, 292, 292⟩,
  ⟨561, 634, 418, 149, 212, 252⟩,
  ⟨501, 614, 498, 149, 252, 212⟩,
  ⟨581, 694, 438, 169, 272, 272⟩,
  ⟨556, 669, 443, 114, 227, 227⟩,
  ⟨521, 634, 458, 129, 292, 292⟩,
  ⟨561, 634, 418, 189, 292, 232⟩,
  ⟨521, 674, 418, 169, 272, 272⟩,
  ⟨521, 634, 458, 149, 252, 212⟩,
  ⟨501, 614, 498, 189, 232, 292⟩,
  ⟨581, 694, 438, 189, 292, 232⟩,
  ⟨521, 634, 458, 169, 272, 272⟩,
  ⟨541, 694, 478, 189, 232, 292⟩,
  ⟨501, 614, 498, 189, 292, 232⟩,
  ⟨521, 674, 418, 109, 252, 252⟩,
  ⟨521, 674, 418, 189, 232, 292⟩,
  ⟨501, 614, 498, 109, 252, 252⟩,
  ⟨541, 694, 478, 169, 272, 272⟩,
  ⟨581, 654, 478, 169, 272, 272⟩,
  ⟨501, 614, 498, 149, 212, 252⟩,
  ⟨581, 654, 478, 149, 212, 252⟩,
  ⟨501, 614, 498, 129, 292, 292⟩,
  ⟨561, 634, 418, 169, 272, 272⟩,
  ⟨541, 694, 478, 149, 252, 212⟩,
  ⟨581, 694, 438, 109, 252, 252⟩,
  ⟨501, 614, 498, 169, 272, 272⟩,
  ⟨149, 212, 252, 561, 634, 418⟩,
  ⟨129, 292, 292, 581, 654, 478⟩,
  ⟨169, 272, 272, 581, 694, 438⟩,
  ⟨149, 252, 212, 501, 614, 498⟩,
  ⟨114, 227, 227, 556, 669, 443⟩,
  ⟨189, 292, 232, 561, 634, 418⟩,
  ⟨129, 292, 292, 521, 634, 458⟩,
  ⟨189, 232, 292, 501, 614, 498⟩,
  ⟨189, 292, 232, 581, 694, 438⟩,
  ⟨169, 272, 272, 521, 674, 418⟩,
  ⟨149, 252, 212, 521, 634, 458⟩,
  ⟨189, 292, 232, 501, 614, 498⟩,
  ⟨109, 252, 252, 521, 674, 418⟩,
  ⟨169, 272, 272, 521, 634, 458⟩,
  ⟨189, 232, 292, 541, 694, 478⟩,
  ⟨189, 232, 292, 521, 674, 418⟩,
  ⟨169, 272, 272, 541, 694, 478⟩,
  ⟨109, 252, 252, 501, 614, 498⟩,
  ⟨149, 212, 252, 501, 614, 498⟩,
  ⟨169, 272, 272, 581, 654, 478⟩,
  ⟨149, 212, 252, 581, 654, 478⟩,
  ⟨169, 272, 272, 561, 634, 418⟩,
  ⟨129, 292, 292, 501, 614, 498⟩,
  ⟨109, 252, 252, 581, 694, 438⟩,
  ⟨149, 252, 212, 541, 694, 478⟩,
  ⟨169, 272, 272, 501, 614, 498⟩,
  ⟨810, 983, 810, 458, 634, 521⟩,
  ⟨890, 963, 850, 478, 654, 581⟩,
  ⟨830, 943, 830, 478, 694, 541⟩,
  ⟨810, 923, 870, 498, 614, 501⟩,
  ⟨885, 998, 885, 443, 669, 556⟩,
  ⟨850, 963, 890, 458, 634, 521⟩,
  ⟨890, 963, 850, 418, 634, 561⟩,
  ⟨850, 903, 850, 498, 614, 501⟩,
  ⟨850, 963, 890, 478, 694, 541⟩,
  ⟨830, 943, 830, 418, 674, 521⟩,
  ⟨810, 923, 870, 418, 634, 561⟩,
  ⟨850, 963, 890, 498, 614, 501⟩,
  ⟨870, 923, 810, 418, 674, 521⟩,
  ⟨830, 943, 830, 418, 634, 561⟩,
  ⟨850, 903, 850, 438, 694, 581⟩,
  ⟨850, 903, 850, 418, 674, 521⟩,
  ⟨830, 943, 830, 438, 694, 581⟩,
  ⟨870, 923, 810, 498, 614, 501⟩,
  ⟨810, 983, 810, 498, 614, 501⟩,
  ⟨830, 943, 830, 478, 654, 581⟩,
  ⟨810, 983, 810, 478, 654, 581⟩,
  ⟨830, 943, 830, 458, 634, 521⟩,
  ⟨890, 963, 850, 498, 614, 501⟩,
  ⟨870, 923, 810, 478, 694, 541⟩,
  ⟨810, 923, 870, 438, 694, 581⟩,
  ⟨830, 943, 830, 498, 614, 501⟩,
  ⟨478, 654, 581, 890, 963, 850⟩,
  ⟨458, 634, 521, 810, 983, 810⟩,
  ⟨498, 614, 501, 810, 923, 870⟩,
  ⟨478, 694, 541, 830, 943, 830⟩,
  ⟨443, 669, 556, 885, 998, 885⟩,
  ⟨418, 634, 561, 890, 963, 850⟩,
  ⟨458, 634, 521, 850, 963, 890⟩,
  ⟨418, 674, 521, 830, 943, 830⟩,
  ⟨418, 634, 561, 810, 923, 870⟩,
  ⟨498, 614, 501, 850, 903, 850⟩,
  ⟨478, 694, 541, 850, 963, 890⟩,
  ⟨418, 634, 561, 830, 943, 830⟩,
  ⟨438, 694, 581, 850, 903, 850⟩,
  ⟨498, 614, 501, 850, 963, 890⟩,
  ⟨418, 674, 521, 870, 923, 810⟩,
  ⟨418, 674, 521, 850, 903, 850⟩,
  ⟨498, 614, 501, 870, 923, 810⟩,
  ⟨438, 694, 581, 830, 943, 830⟩,
  ⟨478, 654, 581, 830, 943, 830⟩,
  ⟨498, 614, 501, 810, 983, 810⟩,
  ⟨478, 654, 581, 810, 983, 810⟩,
  ⟨498, 614, 501, 890, 963, 850⟩,
  ⟨458, 634, 521, 830, 943, 830⟩,
  ⟨438, 694, 581, 810, 923, 870⟩,
  ⟨478, 694, 541, 870, 923, 810⟩,
  ⟨498, 614, 501, 830, 943, 830⟩,
  ⟨149, 212, 252, 890, 963, 850⟩,
  ⟨129, 292, 292, 810, 983, 810⟩,
  ⟨169, 272, 272, 810, 923, 870⟩,
  ⟨149, 252, 212, 830, 943, 830⟩,
  ⟨114, 227, 227, 885, 998, 885⟩,
  ⟨189, 292, 232, 890, 963, 850⟩,
  ⟨129, 292, 292, 850, 963, 890⟩,
  ⟨189, 232, 292, 830, 943, 830⟩,
  ⟨189, 292, 232, 810, 923, 870⟩,
  ⟨169, 272, 272, 850, 903, 850⟩,
  ⟨149, 252, 212, 850, 963, 890⟩,
  ⟨189, 292, 232, 830, 943, 830⟩,
  ⟨109, 252, 252, 850, 903, 850⟩,
  ⟨169, 272, 272, 850, 963, 890⟩,
  ⟨189, 232, 292, 870, 923, 810⟩,
  ⟨189, 232, 292, 850, 903, 850⟩,
  ⟨169, 272, 272, 870, 923, 810⟩,
  ⟨109, 252, 252, 830, 943, 830⟩,
  ⟨149, 212, 252, 830, 943, 830⟩,
  ⟨169, 272, 272, 810, 983, 810⟩,
  ⟨149, 212, 252, 810, 983, 810⟩,
  ⟨169, 272, 272, 890, 963, 850⟩,
  ⟨129, 292, 292, 830, 943, 830⟩,
  ⟨109, 252, 252, 810, 923, 870⟩,
  ⟨149, 252, 212, 870, 923, 810⟩,
  ⟨169, 272, 272, 830, 943, 830⟩,
  ⟨810, 983, 810, 129, 292, 292⟩,
  ⟨890, 963, 850, 149, 212, 252⟩,
  ⟨830, 943, 830, 149, 252, 212⟩,
  ⟨810, 923, 870, 169, 272, 272⟩,
  ⟨885, 998, 885, 114, 227, 227⟩,
  ⟨850, 963, 890, 129, 292, 292⟩,
  ⟨890, 963, 850, 189, 292, 232⟩,
  ⟨850, 903, 850, 169, 272, 272⟩,
  ⟨850, 963, 890, 149, 252, 212⟩,
  ⟨830, 943, 830, 189, 232, 292⟩,
  ⟨810, 923, 870, 189, 292, 232⟩,
  ⟨850, 963, 890, 169, 272, 272⟩,
  ⟨870, 923, 810, 189, 232, 292⟩,
  ⟨830, 943, 830, 189, 292, 232⟩,
  ⟨850, 903, 850, 109, 252, 252⟩,
  ⟨850, 903, 850, 189, 232, 292⟩,
  ⟨830, 943, 830, 109, 252, 252⟩,
  ⟨870, 923, 810, 169, 272, 272⟩,
  ⟨810, 983, 810, 169, 272, 272⟩,
  ⟨830, 943, 830, 149, 212, 252⟩,
  ⟨810, 983, 810, 149, 212, 252⟩,
  ⟨830, 943, 830, 129, 292, 292⟩,
  ⟨890, 963, 850, 169, 272, 272⟩,
  ⟨870, 923, 810, 149, 252, 212⟩,
  ⟨810, 923, 870, 109, 252, 252⟩,
  ⟨830, 943, 830, 169, 272, 272⟩,
  ⟨478, 541, 694, 232, 292, 189⟩,
  ⟨458, 521, 634, 252, 212, 149⟩,
  ⟨498, 501, 614, 252, 252, 109⟩,
  ⟨478, 581, 654, 272, 272, 169⟩,
  ⟨443, 556, 669, 227, 227, 114⟩,
  ⟨418, 521, 674, 232, 292, 189⟩,
  ⟨458, 521, 634, 292, 292, 129⟩,
  ⟨418, 561, 634, 272, 272, 169⟩,
  ⟨418, 521, 674, 252, 252, 109⟩,
  ⟨498, 501, 614, 292, 232, 189⟩,
  ⟨478, 581, 654, 292, 292, 129⟩,
  ⟨418, 521, 674, 272, 272, 169⟩,
  ⟨438, 581, 694, 292, 232, 189⟩,
  ⟨498, 501, 614, 292, 292, 129⟩,
  ⟨418, 561, 634, 212, 252, 149⟩,
  ⟨418, 561, 634, 292, 232, 189⟩,
  ⟨498, 501, 614, 212, 252, 149⟩,
  ⟨438, 581, 694, 272, 272, 169⟩,
  ⟨478, 541, 694, 272, 272, 169⟩,
  ⟨498, 501, 614, 252, 212, 149⟩,
  ⟨478, 541, 694, 252, 212, 149⟩,
  ⟨498, 501, 614, 232, 292, 189⟩,
  ⟨458, 521, 634, 272, 272, 169⟩,
  ⟨438, 581, 694, 252, 252, 109⟩,
  ⟨478, 581, 654, 212, 252, 149⟩,
  ⟨498, 501, 614, 272, 272, 169⟩,
  ⟨252, 212, 149, 458, 521, 634⟩,
  ⟨232, 292, 189, 478, 541, 694⟩,
  ⟨272, 272, 169, 478, 581, 654⟩,
  ⟨252, 252, 109, 498, 501, 614⟩,
  ⟨227, 227, 114, 443, 556, 669⟩,
  ⟨292, 292, 129, 458, 521, 634⟩,
  ⟨232, 292, 189, 418, 521, 674⟩,
  ⟨292, 232, 189, 498, 501, 614⟩,
  ⟨292, 292, 129, 478, 581, 654⟩,
  ⟨272, 272, 169, 418, 561, 634⟩,
  ⟨252, 252, 109, 418, 521, 674⟩,
  ⟨292, 292, 129, 498, 501, 614⟩,
  ⟨212, 252, 149, 418, 561, 634⟩,
  ⟨272, 272, 169, 418, 521, 674⟩,
  ⟨292, 232, 189, 438, 581, 694⟩,
  ⟨292, 232, 189, 418, 561, 634⟩,
  ⟨272, 272, 169, 438, 581, 694⟩,
  ⟨212, 252, 149, 498, 501, 614⟩,
  ⟨252, 212, 149, 498, 501, 614⟩,
  ⟨272, 272, 169, 478, 541, 694⟩,
  ⟨252, 212, 149, 478, 541, 694⟩,
  ⟨272, 272, 169, 458, 521, 634⟩,
  ⟨232, 292, 189, 498, 501, 614⟩,
  ⟨212, 252, 149, 478, 581, 654⟩,
  ⟨252, 252, 109, 438, 581, 694⟩,
  ⟨272, 272, 169, 498, 501, 614⟩,
  ⟨810, 870, 923, 674, 521, 418⟩,
  ⟨890, 850, 963, 694, 541, 478⟩,
  ⟨830, 830, 943, 694, 581, 438⟩,
  ⟨810, 810, 983, 614, 501, 498⟩,
  ⟨885, 885, 998, 669, 556, 443⟩,
  ⟨850, 850, 903, 674, 521, 418⟩,
  ⟨890, 850, 963, 634, 521, 458⟩,
  ⟨850, 890, 963, 614, 501, 498⟩,
  ⟨850, 850, 903, 694, 581, 438⟩,
  ⟨830, 830, 943, 634, 561, 418⟩,
  ⟨810, 810, 983, 634, 521, 458⟩,
  ⟨850, 850, 903, 614, 501, 498⟩,
  ⟨870, 810, 923, 634, 561, 418⟩,
  ⟨830, 830, 943, 634, 521, 458⟩,
  ⟨850, 890, 963, 654, 581, 478⟩,
  ⟨850, 890, 963, 634, 561, 418⟩,
  ⟨830, 830, 943, 654, 581, 478⟩,
  ⟨870, 810, 923, 614, 501, 498⟩,
  ⟨810, 870, 923, 614, 501, 498⟩,
  ⟨830, 830, 943, 694, 541, 478⟩,
  ⟨810, 870, 923, 694, 541, 478⟩,
  ⟨830, 830, 943, 674, 521, 418⟩,
  ⟨890, 850, 963, 614, 501, 498⟩,
  ⟨870, 810, 923, 694, 581, 438⟩,
  ⟨810, 810, 983, 654, 581, 478⟩,
  ⟨830, 830, 943, 614, 501, 498⟩,
  ⟨694, 541, 478, 890, 850, 963⟩,
  ⟨674, 521, 418, 810, 870, 923⟩,
  ⟨614, 501, 498, 810, 810, 983⟩,
  ⟨694, 581, 438, 830, 830, 943⟩,
  ⟨669, 556, 443, 885, 885, 998⟩,
  ⟨634, 521, 458, 890, 850, 963⟩,
  ⟨674, 521, 418, 850, 850, 903⟩,
  ⟨634, 561, 418, 830, 830, 943⟩,
  ⟨634, 521, 458, 810, 810, 983⟩,
  ⟨614, 501, 498, 850, 890, 963⟩,
  ⟨694, 581, 438, 850, 850, 903⟩,
  ⟨634, 521, 458, 830, 830, 943⟩,
  ⟨654, 581, 478, 850, 890, 963⟩,
  ⟨614, 501, 498, 850, 850, 903⟩,
  ⟨634, 561, 418, 870, 810, 923⟩,
  ⟨634, 561, 418, 850, 890, 963⟩,
  ⟨614, 501, 498, 870, 810, 923⟩,
  ⟨654, 581, 478, 830, 830, 943⟩,
  ⟨694, 541, 478, 830, 830, 943⟩,
  ⟨614, 501, 498, 810, 870, 923⟩,
  ⟨694, 541, 478, 810, 870, 923⟩,
  ⟨614, 501, 498, 890, 850, 963⟩,
  ⟨674, 521, 418, 830, 830, 943⟩,
  ⟨654, 581, 478, 810, 810, 983⟩,
  ⟨694, 581, 438, 870, 810, 923⟩,
  ⟨614, 501, 498, 830, 830, 943⟩
]

def wordWitness : List Word := [
  ⟨0, 2, 0, 0, 2, 2⟩,
  ⟨2, 0, 2, 1, 0, 0⟩,
  ⟨1, 2, 1, 1, 0, 0⟩,
  ⟨0, 1, 1, 2, 1, 1⟩,
  ⟨1, 0, 1, 1, 0, 0⟩,
  ⟨2, 0, 2, 0, 2, 2⟩,
  ⟨2, 0, 2, 0, 2, 1⟩,
  ⟨2, 0, 2, 2, 1, 1⟩,
  ⟨1, 2, 1, 0, 1, 2⟩,
  ⟨0, 1, 1, 0, 2, 1⟩,
  ⟨1, 1, 0, 0, 1, 2⟩,
  ⟨1, 2, 1, 0, 2, 1⟩,
  ⟨2, 0, 2, 0, 1, 2⟩,
  ⟨1, 1, 0, 2, 1, 1⟩,
  ⟨0, 2, 0, 2, 1, 1⟩,
  ⟨0, 2, 0, 1, 0, 0⟩,
  ⟨1, 2, 1, 0, 2, 2⟩,
  ⟨1, 1, 0, 1, 0, 0⟩,
  ⟨0, 1, 1, 1, 0, 0⟩,
  ⟨1, 2, 1, 2, 1, 1⟩,
  ⟨1, 0, 0, 2, 0, 2⟩,
  ⟨0, 2, 2, 0, 2, 0⟩,
  ⟨2, 1, 1, 0, 1, 1⟩,
  ⟨1, 0, 0, 1, 2, 1⟩,
  ⟨1, 0, 0, 1, 0, 1⟩,
  ⟨0, 2, 1, 2, 0, 2⟩,
  ⟨0, 2, 2, 2, 0, 2⟩,
  ⟨0, 1, 2, 1, 2, 1⟩,
  ⟨0, 2, 1, 0, 1, 1⟩,
  ⟨2, 1, 1, 2, 0, 2⟩,
  ⟨0, 2, 1, 1, 2, 1⟩,
  ⟨0, 1, 2, 1, 1, 0⟩,
  ⟨0, 1, 2, 2, 0, 2⟩,
  ⟨2, 1, 1, 1, 1, 0⟩,
  ⟨2, 1, 1, 0, 2, 0⟩,
  ⟨1, 0, 0, 0, 2, 0⟩,
  ⟨0, 2, 2, 1, 2, 1⟩,
  ⟨1, 0, 0, 0, 1, 1⟩,
  ⟨1, 0, 0, 1, 1, 0⟩,
  ⟨2, 1, 1, 1, 2, 1⟩,
  ⟨2, 0, 1, 2, 0, 2⟩,
  ⟨1, 2, 1, 0, 2, 0⟩,
  ⟨2, 2, 2, 1, 2, 1⟩,
  ⟨0, 1, 2, 1, 0, 1⟩,
  ⟨2, 2, 0, 2, 0, 2⟩,
  ⟨1, 2, 1, 2, 0, 2⟩,
  ⟨2, 2, 0, 0, 1, 1⟩,
  ⟨2, 2, 2, 2, 0, 2⟩,
  ⟨2, 2, 0, 1, 2, 1⟩,
  ⟨2, 0, 1, 1, 2, 1⟩,
  ⟨2, 0, 1, 0, 2, 0⟩,
  ⟨1, 2, 1, 1, 2, 1⟩,
  ⟨2, 2, 2, 1, 1, 0⟩,
  ⟨0, 2, 0, 1, 2, 1⟩,
  ⟨2, 0, 2, 2, 0, 1⟩,
  ⟨1, 2, 1, 2, 2, 2⟩,
  ⟨1, 0, 1, 0, 1, 2⟩,
  ⟨2, 0, 2, 1, 2, 1⟩,
  ⟨2, 0, 2, 2, 2, 0⟩,
  ⟨2, 0, 2, 2, 2, 2⟩,
  ⟨0, 1, 1, 2, 2, 0⟩,
  ⟨1, 2, 1, 2, 2, 0⟩,
  ⟨1, 2, 1, 2, 0, 1⟩,
  ⟨0, 2, 0, 2, 0, 1⟩,
  ⟨1, 1, 0, 2, 2, 2⟩,
  ⟨1, 0, 0, 0, 2, 2⟩,
  ⟨0, 2, 2, 1, 0, 2⟩,
  ⟨2, 1, 1, 1, 2, 0⟩,
  ⟨1, 0, 0, 0, 0, 1⟩,
  ⟨1, 0, 0, 2, 1, 0⟩,
  ⟨0, 2, 1, 0, 2, 2⟩,
  ⟨0, 1, 2, 0, 0, 1⟩,
  ⟨0, 2, 1, 1, 2, 0⟩,
  ⟨2, 1, 1, 1, 1, 2⟩,
  ⟨0, 2, 1, 0, 0, 1⟩,
  ⟨1, 0, 0, 1, 1, 2⟩,
  ⟨0, 1, 2, 2, 2, 2⟩,
  ⟨0, 1, 2, 1, 1, 2⟩,
  ⟨2, 1, 1, 2, 2, 2⟩,
  ⟨2, 1, 1, 1, 0, 2⟩,
  ⟨1, 0, 0, 1, 0, 2⟩,
  ⟨2, 1, 1, 0, 2, 2⟩,
  ⟨0, 2, 2, 0, 0, 1⟩,
  ⟨1, 0, 0, 1, 2, 0⟩,
  ⟨1, 0, 0, 2, 2, 2⟩,
  ⟨2, 1, 1, 0, 0, 1⟩,
  ⟨1, 0, 2, 0, 2, 2⟩,
  ⟨0, 2, 2, 1, 0, 0⟩,
  ⟨0, 0, 1, 1, 0, 0⟩,
  ⟨1, 2, 0, 2, 1, 1⟩,
  ⟨2, 1, 0, 1, 0, 0⟩,
  ⟨0, 2, 2, 0, 2, 1⟩,
  ⟨1, 1, 2, 2, 1, 1⟩,
  ⟨0, 0, 1, 0, 1, 2⟩,
  ⟨1, 2, 0, 0, 2, 1⟩,
  ⟨2, 2, 2, 0, 1, 2⟩,
  ⟨0, 0, 1, 0, 2, 1⟩,
  ⟨1, 1, 2, 1, 0, 0⟩,
  ⟨1, 1, 2, 0, 1, 2⟩,
  ⟨2, 2, 2, 2, 1, 1⟩,
  ⟨1, 0, 2, 2, 1, 1⟩,
  ⟨1, 0, 2, 1, 0, 0⟩,
  ⟨0, 0, 1, 0, 2, 2⟩,
  ⟨0, 2, 2, 2, 1, 1⟩,
  ⟨2, 2, 2, 1, 0, 0⟩,
  ⟨1, 2, 0, 1, 0, 0⟩,
  ⟨0, 0, 1, 2, 1, 1⟩,
  ⟨0, 1, 1, 1, 2, 0⟩,
  ⟨2, 2, 0, 0, 0, 1⟩,
  ⟨1, 1, 2, 0, 0, 1⟩,
  ⟨0, 0, 2, 1, 1, 2⟩,
  ⟨1, 1, 0, 0, 0, 1⟩,
  ⟨2, 2, 0, 1, 2, 0⟩,
  ⟨2, 2, 0, 2, 2, 0⟩,
  ⟨2, 2, 0, 1, 1, 2⟩,
  ⟨1, 1, 2, 2, 1, 0⟩,
  ⟨0, 0, 2, 2, 2, 0⟩,
  ⟨1, 0, 1, 2, 1, 0⟩,
  ⟨1, 1, 2, 2, 2, 0⟩,
  ⟨2, 2, 0, 2, 1, 0⟩,
  ⟨1, 0, 1, 1, 1, 2⟩,
  ⟨0, 1, 1, 1, 1, 2⟩,
  ⟨0, 1, 1, 0, 0, 1⟩,
  ⟨1, 1, 2, 1, 2, 0⟩,
  ⟨1, 0, 1, 0, 0, 1⟩,
  ⟨0, 0, 2, 0, 0, 1⟩,
  ⟨1, 1, 2, 1, 1, 2⟩,
  ⟨0, 0, 1, 2, 2, 0⟩,
  ⟨1, 2, 0, 0, 1, 1⟩,
  ⟨1, 1, 2, 0, 0, 2⟩,
  ⟨0, 0, 1, 1, 1, 2⟩,
  ⟨0, 0, 1, 1, 1, 0⟩,
  ⟨1, 2, 0, 2, 2, 0⟩,
  ⟨2, 1, 0, 1, 1, 2⟩,
  ⟨2, 2, 0, 0, 0, 2⟩,
  ⟨2, 1, 0, 1, 0, 1⟩,
  ⟨2, 1, 0, 2, 2, 0⟩,
  ⟨1, 1, 2, 1, 0, 1⟩,
  ⟨1, 1, 2, 0, 1, 1⟩,
  ⟨0, 0, 1, 0, 1, 1⟩,
  ⟨1, 2, 0, 1, 1, 2⟩,
  ⟨0, 0, 1, 0, 0, 2⟩,
  ⟨0, 0, 1, 1, 0, 1⟩,
  ⟨0, 2, 2, 1, 1, 0⟩,
  ⟨0, 1, 0, 1, 0, 1⟩,
  ⟨2, 0, 1, 0, 1, 1⟩,
  ⟨0, 2, 2, 0, 2, 2⟩,
  ⟨1, 2, 1, 1, 0, 1⟩,
  ⟨0, 1, 0, 0, 2, 2⟩,
  ⟨1, 2, 0, 0, 2, 2⟩,
  ⟨2, 2, 2, 0, 2, 2⟩,
  ⟨1, 1, 2, 2, 0, 0⟩,
  ⟨1, 1, 2, 0, 2, 2⟩,
  ⟨0, 1, 0, 2, 0, 0⟩,
  ⟨0, 1, 0, 1, 1, 0⟩,
  ⟨1, 0, 2, 1, 1, 0⟩,
  ⟨2, 2, 2, 1, 0, 1⟩,
  ⟨1, 2, 0, 2, 0, 0⟩,
  ⟨0, 1, 0, 2, 1, 1⟩,
  ⟨1, 1, 0, 0, 2, 2⟩,
  ⟨1, 0, 1, 0, 1, 0⟩,
  ⟨0, 1, 1, 2, 0, 1⟩,
  ⟨0, 2, 2, 0, 1, 0⟩,
  ⟨0, 2, 2, 1, 2, 0⟩,
  ⟨1, 0, 1, 1, 2, 1⟩,
  ⟨2, 0, 0, 1, 1, 2⟩,
  ⟨0, 2, 2, 2, 2, 2⟩,
  ⟨0, 2, 2, 1, 1, 2⟩,
  ⟨2, 0, 0, 0, 1, 0⟩,
  ⟨1, 1, 0, 0, 1, 0⟩,
  ⟨1, 1, 0, 1, 0, 2⟩,
  ⟨2, 0, 0, 1, 2, 0⟩,
  ⟨1, 0, 1, 2, 2, 2⟩,
  ⟨2, 1, 1, 0, 1, 0⟩,
  ⟨0, 1, 0, 1, 2, 1⟩,
  ⟨1, 0, 2, 2, 0, 1⟩,
  ⟨0, 1, 0, 0, 1, 0⟩,
  ⟨0, 1, 0, 1, 0, 2⟩,
  ⟨1, 0, 2, 2, 2, 0⟩,
  ⟨2, 0, 2, 0, 1, 0⟩,
  ⟨2, 0, 1, 2, 2, 2⟩,
  ⟨0, 1, 0, 2, 2, 0⟩,
  ⟨2, 0, 1, 0, 1, 0⟩,
  ⟨0, 1, 0, 2, 0, 1⟩,
  ⟨1, 0, 2, 0, 1, 0⟩,
  ⟨0, 1, 0, 2, 2, 2⟩,
  ⟨0, 1, 0, 0, 2, 1⟩,
  ⟨1, 2, 1, 0, 1, 0⟩,
  ⟨2, 0, 1, 1, 0, 2⟩,
  ⟨2, 2, 0, 1, 0, 2⟩,
  ⟨2, 2, 0, 0, 1, 0⟩,
  ⟨0, 1, 0, 2, 0, 2⟩,
  ⟨2, 2, 2, 2, 0, 1⟩,
  ⟨0, 2, 1, 0, 1, 0⟩,
  ⟨2, 2, 2, 0, 1, 0⟩,
  ⟨0, 1, 1, 0, 1, 0⟩,
  ⟨0, 2, 2, 2, 0, 1⟩,
  ⟨1, 0, 1, 2, 0, 1⟩,
  ⟨2, 0, 0, 2, 0, 2⟩,
  ⟨2, 1, 1, 2, 0, 1⟩,
  ⟨2, 0, 0, 1, 2, 1⟩,
  ⟨1, 1, 0, 1, 2, 1⟩,
  ⟨0, 1, 0, 0, 1, 1⟩,
  ⟨2, 0, 1, 0, 2, 2⟩,
  ⟨2, 0, 1, 1, 0, 1⟩,
  ⟨2, 0, 1, 2, 1, 1⟩,
  ⟨2, 0, 2, 2, 0, 0⟩,
  ⟨1, 2, 1, 2, 0, 0⟩,
  ⟨1, 2, 1, 1, 1, 0⟩,
  ⟨2, 2, 2, 2, 2, 0⟩,
  ⟨1, 2, 0, 1, 1, 0⟩,
  ⟨2, 1, 1, 2, 2, 0⟩,
  ⟨2, 0, 2, 1, 1, 2⟩,
  ⟨2, 1, 1, 0, 0, 2⟩,
  ⟨0, 1, 2, 2, 2, 0⟩,
  ⟨2, 0, 2, 1, 0, 1⟩,
  ⟨2, 2, 2, 1, 1, 2⟩,
  ⟨2, 2, 2, 0, 1, 1⟩,
  ⟨0, 1, 2, 0, 0, 2⟩,
  ⟨2, 2, 0, 2, 2, 2⟩,
  ⟨1, 1, 0, 1, 2, 0⟩,
  ⟨2, 2, 0, 2, 1, 1⟩,
  ⟨1, 1, 2, 2, 0, 2⟩,
  ⟨0, 0, 2, 2, 1, 1⟩,
  ⟨1, 0, 1, 2, 0, 2⟩,
  ⟨2, 2, 0, 0, 1, 2⟩,
  ⟨1, 1, 2, 2, 2, 2⟩,
  ⟨0, 1, 1, 2, 2, 2⟩,
  ⟨0, 0, 2, 0, 1, 2⟩,
  ⟨1, 2, 0, 2, 2, 2⟩,
  ⟨2, 2, 0, 1, 0, 0⟩,
  ⟨0, 0, 1, 2, 0, 2⟩,
  ⟨2, 1, 0, 0, 1, 2⟩,
  ⟨2, 1, 0, 2, 0, 2⟩,
  ⟨0, 0, 1, 2, 2, 2⟩,
  ⟨0, 0, 1, 2, 1, 0⟩,
  ⟨2, 2, 2, 1, 2, 0⟩,
  ⟨0, 1, 2, 2, 1, 0⟩,
  ⟨1, 0, 0, 2, 2, 0⟩,
  ⟨2, 0, 2, 0, 0, 1⟩,
  ⟨2, 0, 2, 2, 1, 0⟩,
  ⟨2, 2, 2, 0, 0, 1⟩,
  ⟨2, 1, 0, 0, 0, 1⟩
]

theorem emission_witness_checked : emissionWords = emissionWitness := by
  simp only [emissionWords, TPKCensus.emitted, TPKCensus.signatureImage,
    TPKCensus.signatures_additive_checked, TPKCensus.signatures_multiplicative_checked]
  decide +kernel

theorem word_witness_checked : producedWords = wordWitness := by
  simp only [producedWords, TPKCensus.ternaryImage, TPKCensus.emitted,
    TPKCensus.signatureImage, TPKCensus.signatures_additive_checked,
    TPKCensus.signatures_multiplicative_checked]
  decide +kernel

theorem emission_roundtrip :
    emissionWords.map toList = TPKCensus.emitted := by
  rw [emission_witness_checked]
  simp only [TPKCensus.emitted, TPKCensus.signatureImage,
    TPKCensus.signatures_additive_checked, TPKCensus.signatures_multiplicative_checked]
  decide +kernel

theorem word_roundtrip : producedWords.map toList = TPKCensus.ternaryImage := by
  rw [word_witness_checked]
  simp only [TPKCensus.ternaryImage, TPKCensus.emitted,
    TPKCensus.signatureImage, TPKCensus.signatures_additive_checked,
    TPKCensus.signatures_multiplicative_checked]
  decide +kernel

theorem produced_from_emissions : producedWords = (emissionWords.map psi).eraseDups := by
  rw [word_witness_checked, emission_witness_checked]
  decide +kernel

theorem emission_closed_checked :
    ∀ w ∈ emissionWords, rotate w ∈ emissionWords ∧ swap w ∈ emissionWords := by
  rw [emission_witness_checked]
  decide +kernel

theorem emission_closed (w : Word) (hw : w ∈ emissionWords) (g : D3) :
    act g w ∈ emissionWords := by
  have hr := (emission_closed_checked w hw).1
  have hrr := (emission_closed_checked (rotate w) hr).1
  cases g with
  | one => exact hw
  | r => exact hr
  | r2 => exact hrr
  | s => exact (emission_closed_checked w hw).2
  | sr => exact (emission_closed_checked (rotate w) hr).2
  | sr2 => exact (emission_closed_checked (rotate (rotate w)) hrr).2

theorem produced_closed (w : Word) (hw : w ∈ producedWords) (g : D3) :
    act g w ∈ producedWords := by
  rw [produced_from_emissions, TPKCensus.mem_eraseDups] at hw ⊢
  obtain ⟨u, hu, heq⟩ := List.mem_map.mp hw
  exact List.mem_map.mpr ⟨act g u, emission_closed u hu g,
    by rw [psi_equivariant, heq]⟩

theorem produced_closed_checked :
    ∀ w ∈ producedWords, ∀ g ∈ actions, act g w ∈ producedWords := by
  intro w hw g _
  exact produced_closed w hw g

theorem orbit_stays_produced {w v : Word} (hw : w ∈ producedWords)
    (hv : v ∈ orbit w) : v ∈ producedWords := by
  obtain ⟨g, hg⟩ := (mem_orbit w v).1 hv
  rw [← hg]
  exact produced_closed w hw g

def code (w : Word) : Nat := (((((w.a * 3 + w.b) * 3 + w.c) * 3 + w.d) * 3 + w.e) * 3 + w.f)
def canonical (w : Word) : Nat :=
  (actions.map (fun g => code (act g w))).foldl Nat.min (code w)

def representatives : List Word := producedWords.filter (fun w => code w == canonical w)

/- These representatives are also verified outputs of the computed quotient. -/
def representativeWitness : List Word := [
  ⟨0, 1, 1, 2, 1, 1⟩,
  ⟨0, 1, 1, 0, 2, 1⟩,
  ⟨0, 2, 1, 2, 0, 2⟩,
  ⟨0, 2, 2, 2, 0, 2⟩,
  ⟨0, 1, 2, 1, 2, 1⟩,
  ⟨0, 2, 1, 1, 2, 1⟩,
  ⟨0, 1, 2, 2, 0, 2⟩,
  ⟨0, 2, 2, 1, 2, 1⟩,
  ⟨0, 1, 1, 2, 2, 0⟩,
  ⟨0, 2, 1, 0, 2, 2⟩,
  ⟨0, 1, 2, 2, 2, 2⟩,
  ⟨0, 1, 2, 1, 1, 2⟩,
  ⟨0, 0, 1, 1, 0, 0⟩,
  ⟨1, 1, 2, 2, 1, 1⟩,
  ⟨0, 0, 1, 0, 1, 2⟩,
  ⟨0, 0, 1, 0, 2, 1⟩,
  ⟨0, 0, 1, 0, 2, 2⟩,
  ⟨0, 2, 2, 2, 1, 1⟩,
  ⟨0, 0, 1, 2, 1, 1⟩,
  ⟨0, 1, 1, 1, 2, 0⟩,
  ⟨0, 0, 2, 1, 1, 2⟩,
  ⟨0, 0, 2, 2, 2, 0⟩,
  ⟨0, 1, 1, 1, 1, 2⟩,
  ⟨1, 1, 2, 1, 1, 2⟩,
  ⟨0, 0, 1, 2, 2, 0⟩,
  ⟨0, 0, 1, 1, 1, 2⟩,
  ⟨0, 0, 1, 1, 1, 0⟩,
  ⟨0, 0, 1, 0, 1, 1⟩,
  ⟨0, 0, 1, 0, 0, 2⟩,
  ⟨0, 0, 1, 1, 0, 1⟩,
  ⟨0, 2, 2, 0, 2, 2⟩,
  ⟨0, 1, 1, 2, 0, 1⟩,
  ⟨0, 2, 2, 2, 2, 2⟩,
  ⟨0, 2, 2, 1, 1, 2⟩,
  ⟨0, 1, 2, 2, 2, 0⟩,
  ⟨0, 0, 2, 2, 1, 1⟩,
  ⟨1, 1, 2, 2, 2, 2⟩,
  ⟨0, 1, 1, 2, 2, 2⟩,
  ⟨0, 0, 2, 0, 1, 2⟩,
  ⟨0, 0, 1, 2, 0, 2⟩,
  ⟨0, 0, 1, 2, 2, 2⟩,
  ⟨0, 0, 1, 2, 1, 0⟩,
  ⟨0, 1, 2, 2, 1, 0⟩
]

theorem representatives_checked : representatives = representativeWitness := by
  rw [representatives, word_witness_checked]
  decide +kernel

theorem representatives_produced {w : Word} (hw : w ∈ representatives) :
    w ∈ producedWords := (List.mem_filter.mp hw).1

theorem representatives_nodup : representatives.Nodup := by
  rw [representatives_checked]
  decide +kernel

theorem orbit_count : representatives.length = 43 := by
  rw [representatives_checked]
  decide +kernel

theorem six_orbit_count : (representatives.filter (fun w => (orbit w).length == 6)).length = 38 := by
  rw [representatives_checked]
  decide +kernel

theorem three_orbit_count : (representatives.filter (fun w => (orbit w).length == 3)).length = 5 := by
  rw [representatives_checked]
  decide +kernel

theorem all_orbit_sizes : ∀ w ∈ representatives, (orbit w).length = 6 ∨ (orbit w).length = 3 := by
  rw [representatives_checked]
  decide +kernel

theorem orbit_cover_checked :
    ∀ w ∈ producedWords, (representatives.any (fun r => decide (w ∈ orbit r))) = true := by
  rw [word_witness_checked, representatives_checked]
  decide +kernel

theorem orbit_cover {w : Word} (hw : w ∈ producedWords) :
    ∃ r ∈ representatives, w ∈ orbit r := by
  have h := orbit_cover_checked w hw
  simpa only [List.any_eq_true, decide_eq_true_eq] using h

theorem representatives_disjoint_checked :
    ∀ r ∈ representatives, ∀ s ∈ representatives,
      r = s ∨ ∀ w ∈ orbit r, w ∉ orbit s := by
  rw [representatives_checked]
  decide +kernel

theorem representative_unique {w r s : Word}
    (hr : r ∈ representatives) (hs : s ∈ representatives)
    (hwr : w ∈ orbit r) (hws : w ∈ orbit s) : r = s := by
  rcases representatives_disjoint_checked r hr s hs with h | h
  · exact h
  · exact False.elim (h w hwr hws)

theorem quotient_classification {w : Word} (hw : w ∈ producedWords) :
    ∃ r : Word, (r ∈ representatives ∧ w ∈ orbit r) ∧
      ∀ s : Word, (s ∈ representatives ∧ w ∈ orbit s) → s = r := by
  obtain ⟨r, hr, hwr⟩ := orbit_cover hw
  refine ⟨r, ⟨hr, hwr⟩, ?_⟩
  intro s hs
  exact representative_unique hs.1 hr hs.2 hwr

theorem same_orbit_iff_same_representative {w v r s : Word}
    (hr : r ∈ representatives) (hs : s ∈ representatives)
    (hw : w ∈ orbit r) (hv : v ∈ orbit s) :
    v ∈ orbit w ↔ r = s := by
  constructor
  · intro h
    exact representative_unique hr hs (orbit_trans hw h) hv
  · intro h
    subst s
    exact orbit_trans (orbit_symm hw) hv

theorem psi_trit_bounds (w : Word) :
    (psi w).a < 3 ∧ (psi w).b < 3 ∧ (psi w).c < 3 ∧
    (psi w).d < 3 ∧ (psi w).e < 3 ∧ (psi w).f < 3 := by
  exact ⟨Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide),
    Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide),
    Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide)⟩

theorem produced_trit_bounds {w : Word} (hw : w ∈ producedWords) :
    w.a < 3 ∧ w.b < 3 ∧ w.c < 3 ∧ w.d < 3 ∧ w.e < 3 ∧ w.f < 3 := by
  rw [produced_from_emissions, TPKCensus.mem_eraseDups] at hw
  obtain ⟨u, _, h⟩ := List.mem_map.mp hw
  rw [← h]
  exact psi_trit_bounds u

theorem weighted_orbit_count : 38 * 6 + 5 * 3 = producedWords.length := by
  rw [word_witness_checked]
  decide +kernel

end TPKOrbits

#print axioms TPKOrbits.ofList_toList
#print axioms TPKOrbits.rotate_cube
#print axioms TPKOrbits.swap_square
#print axioms TPKOrbits.dihedral_relation
#print axioms TPKOrbits.actions_complete
#print axioms TPKOrbits.compose_associative
#print axioms TPKOrbits.compose_identity
#print axioms TPKOrbits.compose_inverse
#print axioms TPKOrbits.action_composition
#print axioms TPKOrbits.action_inverse
#print axioms TPKOrbits.psi_toList
#print axioms TPKOrbits.psi_equivariant
#print axioms TPKOrbits.mem_orbit
#print axioms TPKOrbits.orbit_refl
#print axioms TPKOrbits.orbit_symm
#print axioms TPKOrbits.orbit_trans
#print axioms TPKOrbits.emission_witness_checked
#print axioms TPKOrbits.word_witness_checked
#print axioms TPKOrbits.emission_roundtrip
#print axioms TPKOrbits.word_roundtrip
#print axioms TPKOrbits.produced_from_emissions
#print axioms TPKOrbits.emission_closed_checked
#print axioms TPKOrbits.emission_closed
#print axioms TPKOrbits.produced_closed_checked
#print axioms TPKOrbits.produced_closed
#print axioms TPKOrbits.orbit_stays_produced
#print axioms TPKOrbits.representatives_checked
#print axioms TPKOrbits.representatives_produced
#print axioms TPKOrbits.representatives_nodup
#print axioms TPKOrbits.orbit_count
#print axioms TPKOrbits.six_orbit_count
#print axioms TPKOrbits.three_orbit_count
#print axioms TPKOrbits.all_orbit_sizes
#print axioms TPKOrbits.orbit_cover_checked
#print axioms TPKOrbits.orbit_cover
#print axioms TPKOrbits.representatives_disjoint_checked
#print axioms TPKOrbits.representative_unique
#print axioms TPKOrbits.quotient_classification
#print axioms TPKOrbits.same_orbit_iff_same_representative
#print axioms TPKOrbits.psi_trit_bounds
#print axioms TPKOrbits.produced_trit_bounds
#print axioms TPKOrbits.weighted_orbit_count
