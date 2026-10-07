import Mathlib

/-!
# The oriented ternary action on a glued A₂ lattice and its marked neighbour

Source: IV, `moonshine_comparacion.tex`, `km:estabilidad-vecino` (lines 28–120).
The rational coordinates below are simple-root coordinates, with Gram matrix
`[[2,-1],[-1,2]]`.  No VOA or Monster object is postulated.  The general
neighbour lemma takes integrality explicitly; the displayed Paley–Witt
instance proves it from the code, leaving no such hypothesis at its endpoint.
-/

namespace HMT.IV.CoxeterNeighbor

set_option maxHeartbeats 2000000

abbrev Space (n : ℕ) := Fin n → ℚ × ℚ

def localPair (x y : ℚ × ℚ) : ℚ :=
  2 * x.1 * y.1 - x.1 * y.2 - x.2 * y.1 + 2 * x.2 * y.2

def pairing {n : ℕ} (x y : Space n) : ℚ := ∑ i, localPair (x i) (y i)

/-- `false` is C and `true` is C⁻¹ = R C R. -/
def turn (s : Bool) (x : ℚ × ℚ) : ℚ × ℚ :=
  if s then (x.2 - x.1, -x.1) else (-x.2, x.1 - x.2)

def action {n : ℕ} (s : Fin n → Bool) (x : Space n) : Space n :=
  fun i => turn (s i) (x i)

theorem action_add {n : ℕ} (s : Fin n → Bool) (x y : Space n) :
    action s (x + y) = action s x + action s y := by
  funext i
  cases h : s i <;> ext <;> simp [action, turn, h] <;> ring

theorem action_smul {n : ℕ} (s : Fin n → Bool) (q : ℚ) (x : Space n) :
    action s (q • x) = q • action s x := by
  funext i
  cases h : s i <;> ext <;> simp [action, turn, h] <;> ring

theorem action_cube {n : ℕ} (s : Fin n → Bool) (x : Space n) :
    action s (action s (action s x)) = x := by
  funext i
  cases h : s i <;> ext <;> simp [action, turn, h] <;> ring

theorem action_quadratic {n : ℕ} (s : Fin n → Bool) (x : Space n) :
    action s (action s x) + action s x + x = 0 := by
  funext i
  cases h : s i <;> ext <;> simp [action, turn, h] <;> ring

theorem action_fixed_iff {n : ℕ} (s : Fin n → Bool) (x : Space n) :
    action s x = x ↔ x = 0 := by
  constructor
  · intro h
    have hp := action_quadratic s x
    rw [h, h] at hp
    funext i
    have h₁ := congrArg (fun z : Space n => (z i).1) hp
    have h₂ := congrArg (fun z : Space n => (z i).2) hp
    ext <;> simp only [Pi.add_apply, Prod.fst_add, Prod.snd_add,
      Pi.zero_apply, Prod.fst_zero, Prod.snd_zero] at * <;> linarith
  · rintro rfl
    funext i
    cases h : s i <;> simp [action, turn, h]

def actionEquiv {n : ℕ} (s : Fin n → Bool) : Space n ≃ₗ[ℚ] Space n where
  toFun := action s
  invFun := fun x => action s (action s x)
  left_inv := action_cube s
  right_inv := action_cube s
  map_add' := action_add s
  map_smul' := action_smul s

theorem action_pairing {n : ℕ} (s : Fin n → Bool) (x y : Space n) :
    pairing (action s x) (action s y) = pairing x y := by
  apply Finset.sum_congr rfl
  intro i _
  cases h : s i <;> simp [action, turn, localPair, h] <;> ring

theorem pairing_add_right {n : ℕ} (x y z : Space n) :
    pairing x (y + z) = pairing x y + pairing x z := by
  unfold pairing
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  simp [localPair]
  ring

theorem pairing_smul_right {n : ℕ} (q : ℚ) (x y : Space n) :
    pairing x (q • y) = q * pairing x y := by
  unfold pairing
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  simp [localPair]
  ring

theorem pairing_comm {n : ℕ} (x y : Space n) : pairing x y = pairing y x := by
  apply Finset.sum_congr rfl
  intro i _
  dsimp [localPair]
  ring

/-- An integer lift of a word contributes c·(2,1)/3.  Changing its lift by
three changes only the root-lattice representative. -/
def glue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) : AddSubgroup (Space n) where
  carrier := {x | ∃ a b c : Fin n → ℤ,
    (fun i => (c i : ZMod 3)) ∈ C ∧
    ∀ i, x i = ((a i : ℚ) + 2 * c i / 3, (b i : ℚ) + c i / 3)}
  zero_mem' := by
    refine ⟨0, 0, 0, by simpa using C.zero_mem, ?_⟩
    intro i
    ext <;> simp
  add_mem' := by
    rintro x y ⟨a, b, c, hc, hx⟩ ⟨d, e, f, hf, hy⟩
    refine ⟨a + d, b + e, c + f, ?_, ?_⟩
    · simpa using C.add_mem hc hf
    · intro i
      simp only [Pi.add_apply, hx, hy, Prod.mk_add_mk, Int.cast_add]
      ext <;> simp only [Prod.fst, Prod.snd] <;> ring
  neg_mem' := by
    rintro x ⟨a, b, c, hc, hx⟩
    refine ⟨-a, -b, -c, ?_, ?_⟩
    · simpa only [Pi.neg_apply, Int.cast_neg] using C.neg_mem hc
    · intro i
      simp only [Pi.neg_apply, hx, Prod.neg_mk, Int.cast_neg]
      ext <;> simp only [Prod.fst, Prod.snd] <;> ring

/-- Each local Coxeter block fixes every discriminant class, so it preserves
the glue for every additive ternary code, not just a selected finite list. -/
theorem action_mem_glue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (s : Fin n → Bool) {x : Space n} (hx : x ∈ glue C) : action s x ∈ glue C := by
  obtain ⟨a, b, c, hc, hx⟩ := hx
  refine ⟨(fun i => if s i then b i - a i - c i else -b i - c i),
    (fun i => if s i then -a i - c i else a i - b i), c, hc, ?_⟩
  intro i
  cases h : s i <;> ext <;> simp [action, turn, h, hx] <;> ring

theorem action_mem_glue_iff {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (s : Fin n → Bool) (x : Space n) : action s x ∈ glue C ↔ x ∈ glue C := by
  constructor
  · intro h
    simpa only [action_cube] using action_mem_glue C s (action_mem_glue C s h)
  · exact action_mem_glue C s

def signWord {n : ℕ} (s : Fin n → Bool) : Fin n → ℤ := fun i => if s i then 1 else -1

def radial {n : ℕ} (t : Fin n → ℤ) : Space n :=
  fun i => (1 + 3 * (t i : ℚ), 1 + 3 * (t i : ℚ))

def shift {n : ℕ} (s : Fin n → Bool) (t : Fin n → ℤ) : Space n :=
  (1 / 3 : ℚ) • (action s (radial t) - radial t)

theorem shift_mem_glue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (s : Fin n → Bool) (t : Fin n → ℤ)
    (hc : (fun i => (signWord s i : ZMod 3)) ∈ C) : shift s t ∈ glue C := by
  refine ⟨(fun i => if s i then -t i - 1 else -2 * t i),
    (fun i => if s i then -2 * t i - 1 else -t i), signWord s, hc, ?_⟩
  intro i
  cases h : s i <;> ext <;> simp [shift, radial, action, turn, signWord, h] <;> ring

theorem inverse_action {n : ℕ} (s : Fin n → Bool) (x : Space n) :
    action (fun i => !(s i)) x = action s (action s x) := by
  funext i
  cases h : s i <;> ext <;> simp [action, turn, h] <;> ring

theorem inverse_signWord {n : ℕ} (s : Fin n → Bool) :
    signWord (fun i => !(s i)) = - signWord s := by
  funext i
  cases h : s i <;> simp [signWord, h]

theorem shift_pairing {n : ℕ} (s : Fin n → Bool) (t : Fin n → ℤ) :
    pairing (shift s t) (radial t) = -∑ i, (1 + 3 * (t i : ℚ)) ^ 2 := by
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro i _
  cases h : s i <;> simp [shift, radial, action, turn, localPair, h] <;> ring

/-- The marked chamber vector has one coefficient 4 and eleven coefficients 1. -/
def marked (o : Fin 12) : Fin 12 → ℤ := fun i => if i = o then 1 else 0

theorem marked_shift_pairing (s : Fin 12 → Bool) (o : Fin 12) :
    pairing (shift s (marked o)) (radial (marked o)) = -27 := by
  rw [shift_pairing]
  have hterm : (fun i : Fin 12 => (1 + 3 * ((marked o i : ℤ) : ℚ)) ^ 2) =
      fun i => 1 + if i = o then 15 else 0 := by
    funext i
    by_cases h : i = o <;> norm_num [marked, h]
  rw [hterm, Finset.sum_add_distrib]
  norm_num

theorem pairing_add_left {n : ℕ} (x y z : Space n) :
    pairing (x + y) z = pairing x z + pairing y z := by
  rw [pairing_comm, pairing_add_right]
  congr 1 <;> apply pairing_comm

theorem pairing_smul_left {n : ℕ} (q : ℚ) (x y : Space n) :
    pairing (q • x) y = q * pairing x y := by
  rw [pairing_comm, pairing_smul_right, pairing_comm y x]

/-- The integrality proved upstream from self-orthogonality of the code. -/
def IntegralGlue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) : Prop :=
  ∀ x ∈ glue C, ∀ y ∈ glue C, ∃ k : ℤ, pairing x y = k

def SelfOrthogonal {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) : Prop :=
  ∀ c ∈ C, ∀ d ∈ C, ∑ i, c i * d i = 0

/-- The discriminant computation: code self-orthogonality gives integrality
of every pairing in the whole glued lattice. -/
theorem integralGlue_of_selfOrthogonal {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (hC : SelfOrthogonal C) : IntegralGlue C := by
  rintro x ⟨a, b, c, hc, hx⟩ y ⟨d, e, f, hf, hy⟩
  have hz : ((∑ i, c i * f i : ℤ) : ZMod 3) = 0 := by
    simpa only [Int.cast_sum, Int.cast_mul] using hC _ hc _ hf
  obtain ⟨k, hk⟩ := (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mp hz
  let r : ℤ := ∑ i, (2 * a i * d i - a i * e i - b i * d i +
    2 * b i * e i + a i * f i + c i * d i)
  refine ⟨r + 2 * k, ?_⟩
  have hpair : pairing x y = (r : ℚ) + 2 * (∑ i, (c i : ℚ) * f i) / 3 := by
    simp only [pairing, r, Int.cast_sum, Int.cast_add, Int.cast_sub, Int.cast_mul,
      Int.cast_ofNat]
    rw [Finset.mul_sum, Finset.sum_div, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    rw [hx, hy]
    dsimp [localPair]
    ring
  have hkq := congrArg (fun z : ℤ => (z : ℚ)) hk
  push_cast at hkq ⊢
  rw [hpair, hkq]
  ring

def kernel {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n) : Set (Space n) :=
  {x | x ∈ glue C ∧ ∃ k : ℤ, pairing x v = 3 * (k : ℚ)}

/-- The source neighbour N₀ + ℤ(v/3), with no Leech recognition built in. -/
def neighbor {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n) : Set (Space n) :=
  {w | ∃ x ∈ kernel C v, ∃ k : ℤ, w = x + (k : ℚ) • ((1 / 3 : ℚ) • v)}

theorem shift_marked_mem_kernel (C : AddSubgroup (Fin 12 → ZMod 3))
    (s : Fin 12 → Bool) (o : Fin 12)
    (hc : (fun i => (signWord s i : ZMod 3)) ∈ C) :
    shift s (marked o) ∈ kernel C (radial (marked o)) := by
  exact ⟨shift_mem_glue C s (marked o) hc, -9, by rw [marked_shift_pairing]; norm_num⟩

theorem action_mem_kernel (C : AddSubgroup (Fin 12 → ZMod 3))
    (s : Fin 12 → Bool) (o : Fin 12) (hint : IntegralGlue C)
    (hc : (fun i => (signWord s i : ZMod 3)) ∈ C)
    {x : Space 12} (hx : x ∈ kernel C (radial (marked o))) :
    action s x ∈ kernel C (radial (marked o)) := by
  let v := radial (marked o)
  let z := shift (fun i => !(s i)) (marked o)
  have hnc : (fun i => (signWord (fun i => !(s i)) i : ZMod 3)) ∈ C := by
    rw [inverse_signWord]
    simpa only [Pi.neg_apply, Int.cast_neg] using C.neg_mem hc
  have hz : z ∈ glue C := shift_mem_glue C _ _ hnc
  obtain ⟨m, hm⟩ := hint x hx.1 z hz
  obtain ⟨r, hr⟩ := hx.2
  refine ⟨action_mem_glue C s hx.1, r + m, ?_⟩
  have hback : action s (action s v) = v + (3 : ℚ) • z := by
    dsimp [z, shift]
    rw [inverse_action]
    module
  have hp := action_pairing s x (action s (action s v))
  rw [action_cube, hback, pairing_add_right, pairing_smul_right] at hp
  change pairing (action s x) v = _
  change pairing x v = _ at hr
  rw [hr, hm] at hp
  rw [hp]
  push_cast
  ring

theorem kernel_add_zsmul {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (v : Space n) {x y : Space n} (hx : x ∈ kernel C v)
    (hy : y ∈ kernel C v) (k : ℤ) : x + (k : ℚ) • y ∈ kernel C v := by
  refine ⟨(glue C).add_mem hx.1 ?_, ?_⟩
  · simpa only [Int.cast_smul_eq_zsmul] using (glue C).zsmul_mem hy.1 k
  · obtain ⟨a, ha⟩ := hx.2
    obtain ⟨b, hb⟩ := hy.2
    refine ⟨a + k * b, ?_⟩
    rw [pairing_add_left, pairing_smul_left, ha, hb]
    push_cast
    ring

/-- Forward preservation of the entire neighbour, not a finite sample. -/
theorem action_mem_neighbor (C : AddSubgroup (Fin 12 → ZMod 3))
    (s : Fin 12 → Bool) (o : Fin 12) (hint : IntegralGlue C)
    (hc : (fun i => (signWord s i : ZMod 3)) ∈ C)
    {w : Space 12} (hw : w ∈ neighbor C (radial (marked o))) :
    action s w ∈ neighbor C (radial (marked o)) := by
  obtain ⟨x, hx, k, rfl⟩ := hw
  refine ⟨action s x + (k : ℚ) • shift s (marked o),
    kernel_add_zsmul C _ (action_mem_kernel C s o hint hc hx)
      (shift_marked_mem_kernel C s o hc) k, k, ?_⟩
  rw [action_add, action_smul, action_smul]
  dsimp [shift]
  module

/-- Exact setwise preservation, gNα = Nα, with the same marked origin. -/
theorem action_mem_neighbor_iff (C : AddSubgroup (Fin 12 → ZMod 3))
    (s : Fin 12 → Bool) (o : Fin 12) (hint : IntegralGlue C)
    (hc : (fun i => (signWord s i : ZMod 3)) ∈ C) (w : Space 12) :
    action s w ∈ neighbor C (radial (marked o)) ↔
      w ∈ neighbor C (radial (marked o)) := by
  constructor
  · intro h
    simpa only [action_cube] using action_mem_neighbor C s o hint hc
      (action_mem_neighbor C s o hint hc h)
  · exact action_mem_neighbor C s o hint hc

/-- The constructed action is a metric-preserving bijection of the neighbour. -/
def neighborEquiv (C : AddSubgroup (Fin 12 → ZMod 3))
    (s : Fin 12 → Bool) (o : Fin 12) (hint : IntegralGlue C)
    (hc : (fun i => (signWord s i : ZMod 3)) ∈ C) :
    neighbor C (radial (marked o)) ≃ neighbor C (radial (marked o)) where
  toFun := fun x => ⟨action s x, action_mem_neighbor C s o hint hc x.property⟩
  invFun := fun x => ⟨action s (action s x), action_mem_neighbor C s o hint hc
    (action_mem_neighbor C s o hint hc x.property)⟩
  left_inv := fun x => Subtype.ext (action_cube s x)
  right_inv := fun x => Subtype.ext (action_cube s x)

/-! ## The actual Paley–Witt chart from `exc:aw`, without an input code oracle. -/

def paleyWitt : Matrix (Fin 6) (Fin 6) (ZMod 3) :=
  !![0, 1, 1, 1, 1, 1;
     1, 0, 1, 2, 2, 1;
     1, 1, 0, 1, 2, 2;
     1, 2, 1, 0, 1, 2;
     1, 2, 2, 1, 0, 1;
     1, 1, 2, 2, 1, 0]

def encode (w : Fin 6 → ZMod 3) : Fin 12 → ZMod 3 :=
  fun i => if h : i.val < 6 then w ⟨i.val, h⟩ else
    Matrix.vecMul w paleyWitt ⟨i.val - 6, by have := i.isLt; omega⟩

def encoder : (Fin 6 → ZMod 3) →ₗ[ZMod 3] (Fin 12 → ZMod 3) where
  toFun := encode
  map_add' := by
    intro w u
    ext i
    by_cases h : i.val < 6 <;> simp [encode, h, Matrix.add_vecMul]
  map_smul' := by
    intro q w
    ext i
    by_cases h : i.val < 6 <;> simp [encode, h, Matrix.vecMul_smul]

def wittCode : AddSubgroup (Fin 12 → ZMod 3) := (LinearMap.range encoder).toAddSubgroup

theorem wittCode_selfOrthogonal : SelfOrthogonal wittCode := by
  rintro c ⟨w, rfl⟩ d ⟨u, rfl⟩
  change ∑ i, encode w i * encode u i = 0
  norm_num [encode, Fin.append, Matrix.vecMul, dotProduct,
    Fin.sum_univ_succ, paleyWitt]
  ring_nf!
  reduce_mod_char

/-- Position 6 is the seventh displayed coordinate (the unique residue 2). -/
def wittOrientation : Fin 12 → Bool := fun i => decide (i ≠ 6)

theorem witt_fullSupport_word :
    (fun i => (signWord wittOrientation i : ZMod 3)) ∈ wittCode := by
  exact ⟨fun _ => 1, by decide⟩

theorem witt_glue_integral : IntegralGlue wittCode :=
  integralGlue_of_selfOrthogonal wittCode wittCode_selfOrthogonal

/-- No integrality or membership hypothesis remains for the displayed code. -/
theorem witt_neighbor_invariant (o : Fin 12) (x : Space 12) :
    action wittOrientation x ∈ neighbor wittCode (radial (marked o)) ↔
      x ∈ neighbor wittCode (radial (marked o)) :=
  action_mem_neighbor_iff wittCode wittOrientation o witt_glue_integral
    witt_fullSupport_word x

def wittNeighborEquiv (o : Fin 12) :
    neighbor wittCode (radial (marked o)) ≃ neighbor wittCode (radial (marked o)) :=
  neighborEquiv wittCode wittOrientation o witt_glue_integral witt_fullSupport_word

theorem pairing_self_nonneg {n : ℕ} (x : Space n) : 0 ≤ pairing x x := by
  apply Finset.sum_nonneg
  intro i _
  dsimp [localPair]
  nlinarith [sq_nonneg ((x i).1), sq_nonneg ((x i).2),
    sq_nonneg ((x i).1 - (x i).2)]

theorem pairing_self_eq_zero_iff {n : ℕ} (x : Space n) : pairing x x = 0 ↔ x = 0 := by
  constructor
  · intro hx
    have hlocal : ∀ i ∈ (Finset.univ : Finset (Fin n)), 0 ≤ localPair (x i) (x i) := by
      intro i _
      dsimp [localPair]
      nlinarith [sq_nonneg ((x i).1), sq_nonneg ((x i).2),
        sq_nonneg ((x i).1 - (x i).2)]
    have hz := (Finset.sum_eq_zero_iff_of_nonneg hlocal).mp hx
    funext i
    have hi := hz i (Finset.mem_univ i)
    dsimp [localPair] at hi
    ext <;> simp only [Pi.zero_apply, Prod.fst_zero, Prod.snd_zero]
    · nlinarith [sq_nonneg ((x i).2), sq_nonneg ((x i).1 - (x i).2)]
    · nlinarith [sq_nonneg ((x i).1), sq_nonneg ((x i).1 - (x i).2)]
  · rintro rfl
    simp [pairing, localPair]

def rootDifference (o : Fin 12) : Space 12 := fun i => if i = o then (1, -1) else 0

theorem rootDifference_mem_kernel (C : AddSubgroup (Fin 12 → ZMod 3)) (o : Fin 12) :
    rootDifference o ∈ kernel C (radial (marked o)) := by
  constructor
  · refine ⟨(fun i => if i = o then 1 else 0),
      (fun i => if i = o then -1 else 0), 0, by simpa using C.zero_mem, ?_⟩
    intro i
    by_cases h : i = o <;> ext <;> simp [rootDifference, h]
  · refine ⟨0, ?_⟩
    have he : pairing (rootDifference o) (radial (marked o)) = 0 := by
      apply Finset.sum_eq_zero
      intro i _
      by_cases h : i = o
      · simp [rootDifference, radial, localPair, h]
        ring
      · simp [rootDifference, radial, localPair, h]
    simpa using he

theorem rootDifference_ne_zero (o : Fin 12) : rootDifference o ≠ 0 := by
  intro h
  have := congrArg (fun z : Space 12 => (z o).1) h
  norm_num [rootDifference] at this

theorem wittNeighbor_order (o : Fin 12) : orderOf (wittNeighborEquiv o) = 3 := by
  apply orderOf_eq_prime
  · apply Equiv.ext
    intro x
    apply Subtype.ext
    change action wittOrientation (action wittOrientation
      (action wittOrientation x.val)) = x.val
    exact action_cube _ _
  · intro h
    let x : neighbor wittCode (radial (marked o)) :=
      ⟨rootDifference o, rootDifference o, rootDifference_mem_kernel wittCode o,
        0, by simp⟩
    have hx := congrArg (fun e => (e x : Space 12)) h
    change action wittOrientation (rootDifference o) = rootDifference o at hx
    exact rootDifference_ne_zero o ((action_fixed_iff _ _).mp hx)

theorem action_square_fixed_iff {n : ℕ} (s : Fin n → Bool) (x : Space n) :
    action s (action s x) = x ↔ x = 0 := by
  constructor
  · intro h
    have hh := congrArg (action s) h
    rw [action_cube] at hh
    exact (action_fixed_iff _ _).mp hh.symm
  · intro h
    rw [h, (action_fixed_iff s 0).mpr rfl, (action_fixed_iff s 0).mpr rfl]

/-- The complete new reticular connection, with the actual displayed code and
orientation: fixed-point-free order-three metric symmetry of every marked
neighbour.  Leech classification and VOA recognition are not premises. -/
theorem witt_marked_neighbor_symmetry (o : Fin 12) :
    orderOf (wittNeighborEquiv o) = 3 ∧
    (∀ x y : Space 12, pairing (action wittOrientation x) (action wittOrientation y) =
      pairing x y) ∧
    (∀ x : Space 12, action wittOrientation x = x ↔ x = 0) ∧
    (∀ x : Space 12, action wittOrientation x ∈ neighbor wittCode (radial (marked o)) ↔
      x ∈ neighbor wittCode (radial (marked o))) :=
  ⟨wittNeighbor_order o, action_pairing wittOrientation,
    action_fixed_iff wittOrientation, witt_neighbor_invariant o⟩

end HMT.IV.CoxeterNeighbor
