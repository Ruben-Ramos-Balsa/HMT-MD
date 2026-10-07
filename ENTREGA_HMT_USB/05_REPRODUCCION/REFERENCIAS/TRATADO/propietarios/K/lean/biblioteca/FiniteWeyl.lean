import APPArithmetic
import TPKTransport
import ClosureAnalytic
import Mathlib.Analysis.SpecialFunctions.Complex.CircleAddChar
import Mathlib.Tactic

/-!
# Finite Weyl realization and explicitly typed duality

The phase support is the observable nonadic quotient of the TPK clock.
The two potentials are the residue publications of the APP sum/product.
Complex phases are evaluated only afterwards, from the closure reader
already constructed in `ClosureAnalytic`; its identification with pi is
used in the proof of the character laws, not to select an upstream state.

Source: article IV, 01_hilbert_nonadico.tex and 02_dualidad_t.tex;
the oriented plaquette computation is in sections/extension.tex.
-/

noncomputable section
open Finset

namespace FiniteWeyl

set_option maxRecDepth 8192

abbrev Phase := ZMod 9
abbrev Wave := Phase → ℂ

def clockPhase (p : TPKTransport.Phase) : Phase := (p.val : Phase)

theorem clock_phase_advance (p : TPKTransport.Phase) :
    clockPhase (TPKTransport.nextPhase p) = clockPhase p + 1 := by
  fin_cases p <;> decide

def sumPotential (x y : Phase) : Phase := x + y
def productPotential (x y : Phase) : Phase := x * y
def deltaX (f : Phase → Phase → Phase) (x y : Phase) : Phase := f (x + 1) y - f x y
def deltaY (f : Phase → Phase → Phase) (x y : Phase) : Phase := f x (y + 1) - f x y
def curvature (f g : Phase → Phase → Phase) (x y : Phase) : Phase :=
  deltaX (deltaY g) x y - deltaY (deltaX f) x y

theorem app_sum_publication (i j : APPArithmetic.Digit) :
    ((APPArithmetic.value i + APPArithmetic.value j : Nat) : Phase) =
      sumPotential (APPArithmetic.value i) (APPArithmetic.value j) := by
  simp [sumPotential]

theorem app_product_publication (i j : APPArithmetic.Digit) :
    ((APPArithmetic.value i * APPArithmetic.value j : Nat) : Phase) =
      productPotential (APPArithmetic.value i) (APPArithmetic.value j) := by
  simp [productPotential]

theorem plaquette_curvatures (x y : Phase) :
    curvature sumPotential sumPotential x y = 0 ∧
    curvature productPotential productPotential x y = 0 ∧
    curvature sumPotential productPotential x y = 1 ∧
    curvature productPotential sumPotential x y = -1 := by
  simp only [curvature, deltaX, deltaY, sumPotential, productPotential]
  constructor
  · ring
  · constructor
    · ring
    · constructor <;> ring

def complexPlane (v : TRITCore.Plane) : ℂ := (v.1 : ℂ) + Complex.I * (v.2 : ℂ)

theorem trit_elliptic_realization (v : TRITCore.Plane) :
    complexPlane (TRITCore.J 1 v) = Complex.I * complexPlane v := by
  simp [complexPlane, TRITCore.J, mul_add, ← mul_assoc]
  ring

/-- The complex realization uses the internally constructed closure value. -/
def phase (r : Phase) : ℂ :=
  Complex.exp (2 * (ClosureAnalytic.value : ℂ) * Complex.I * (r.val : ℂ) / 9)

theorem phase_recognition (r : Phase) : phase r = ZMod.stdAddChar r := by
  rw [phase, ClosureAnalytic.value_eq_pi, ZMod.stdAddChar_apply, ZMod.toCircle_apply]
  rfl

theorem phase_zero : phase 0 = 1 := by
  rw [phase_recognition, AddChar.map_zero_eq_one]

theorem phase_add (r s : Phase) : phase (r + s) = phase r * phase s := by
  simp only [phase_recognition, AddChar.map_add_eq_mul]

theorem phase_injective : Function.Injective phase := by
  intro r s h
  simp only [phase_recognition] at h
  exact ZMod.injective_stdAddChar h

theorem phase_norm (r : Phase) : ‖phase r‖ = 1 := by
  rw [phase_recognition, ZMod.stdAddChar_apply]
  exact Circle.norm_coe _

theorem phase_ne_zero (r : Phase) : phase r ≠ 0 := by
  intro h
  have hn := phase_norm r
  rw [h, norm_zero] at hn
  norm_num at hn

theorem phase_neg_mul (r : Phase) : phase (-r) * phase r = 1 := by
  rw [← phase_add, neg_add_cancel, phase_zero]

theorem phase_pow_nine (r : Phase) : phase r ^ 9 = 1 := by
  rw [phase_recognition, ← AddChar.map_nsmul_eq_pow]
  simp only [nsmul_eq_mul]
  change ZMod.stdAddChar ((9 : Phase) * r) = 1
  simp only [show (9 : Phase) = 0 by decide, zero_mul,
    AddChar.map_zero_eq_one]

def translate (a : Phase) (f : Wave) : Wave := fun r => f (r - a)
def modulate (b : Phase) (f : Wave) : Wave := fun r => phase (b * r) * f r
def X : Wave → Wave := translate 1
def Z : Wave → Wave := modulate 1
def omega : ℂ := phase 1

theorem phase_as_power (r : Phase) : phase r = omega ^ r.val := by
  simp only [omega, phase_recognition]
  rw [← AddChar.map_nsmul_eq_pow]
  simp [nsmul_eq_mul]

theorem translate_add (a c : Phase) (f : Wave) :
    translate a (translate c f) = translate (a + c) f := by
  funext r
  simp only [translate]
  congr 1
  ring

theorem modulate_add (b d : Phase) (f : Wave) :
    modulate b (modulate d f) = modulate (b + d) f := by
  funext r
  simp only [modulate, add_mul, phase_add]
  ring

theorem translate_zero (f : Wave) : translate 0 f = f := by
  funext r
  simp [translate]

theorem modulate_zero (f : Wave) : modulate 0 f = f := by
  funext r
  simp [modulate, phase_zero]

theorem translate_inverse (a : Phase) (f : Wave) : translate (-a) (translate a f) = f := by
  rw [translate_add, neg_add_cancel, translate_zero]

theorem modulate_inverse (b : Phase) (f : Wave) : modulate (-b) (modulate b f) = f := by
  rw [modulate_add, neg_add_cancel, modulate_zero]

theorem weyl_relation (a b : Phase) (f : Wave) :
    modulate b (translate a f) = fun r =>
      phase (b * a) * translate a (modulate b f) r := by
  funext r
  simp only [modulate, translate, ← mul_assoc, ← phase_add]
  congr 2
  ring

theorem ZX_eq_omega_XZ (f : Wave) : Z (X f) = fun r => omega * X (Z f) r := by
  simpa only [one_mul, X, Z, omega] using weyl_relation 1 1 f

theorem translate_iterate (a : Phase) (n : Nat) (f : Wave) :
    TPKTransport.iterate (translate a) n f = translate (n * a) f := by
  induction n with
  | zero => simp [TPKTransport.iterate, translate_zero]
  | succ n ih =>
    rw [TPKTransport.iterate, ih, translate_add]
    have he : a + (n : Phase) * a = ((n + 1 : Nat) : Phase) * a := by push_cast; ring
    rw [he]

theorem modulate_iterate (b : Phase) (n : Nat) (f : Wave) :
    TPKTransport.iterate (modulate b) n f = modulate (n * b) f := by
  induction n with
  | zero => simp [TPKTransport.iterate, modulate_zero]
  | succ n ih =>
    rw [TPKTransport.iterate, ih, modulate_add]
    have he : b + (n : Phase) * b = ((n + 1 : Nat) : Phase) * b := by push_cast; ring
    rw [he]

theorem X_nine (f : Wave) : TPKTransport.iterate X 9 f = f := by
  rw [X, translate_iterate]
  change translate ((9 : Phase) * 1) f = f
  simp only [show (9 : Phase) = 0 by decide, zero_mul, translate_zero]

theorem Z_nine (f : Wave) : TPKTransport.iterate Z 9 f = f := by
  rw [Z, modulate_iterate]
  change modulate ((9 : Phase) * 1) f = f
  simp only [show (9 : Phase) = 0 by decide, zero_mul, modulate_zero]

abbrev Displacement := Phase × Phase

def area (u v : Displacement) : Phase := u.1 * v.2 - u.2 * v.1
def cocycle (u v : Displacement) : Phase := u.2 * v.1

theorem area_alternating (u : Displacement) : area u u = 0 := by
  simp [area, mul_comm]

theorem area_basis : area (1, 0) (0, 1) = 1 ∧ area (0, 1) (1, 0) = -1 := by
  norm_num [area]

theorem cocycle_identity (u v w : Displacement) :
    cocycle u v + cocycle (u + v) w = cocycle v w + cocycle u (v + w) := by
  simp only [cocycle, Prod.fst_add, Prod.snd_add]
  ring

theorem antisymmetric_cocycle (u v : Displacement) :
    cocycle u v - cocycle v u = -area u v := by
  unfold cocycle area
  ring

@[ext] structure Heisenberg where
  a : Phase
  b : Phase
  t : Phase
  deriving DecidableEq, Fintype

def heisMul (g h : Heisenberg) : Heisenberg :=
  ⟨g.a + h.a, g.b + h.b, g.t + h.t + g.b * h.a⟩

def heisInv (g : Heisenberg) : Heisenberg := ⟨-g.a, -g.b, -g.t + g.a * g.b⟩

instance : Group Heisenberg where
  one := ⟨0, 0, 0⟩
  mul := heisMul
  inv := heisInv
  mul_assoc g h k := by
    change heisMul (heisMul g h) k = heisMul g (heisMul h k)
    ext <;> dsimp [heisMul] <;> ring
  one_mul g := by
    change heisMul ⟨0, 0, 0⟩ g = g
    ext <;> simp [heisMul]
  mul_one g := by
    change heisMul g ⟨0, 0, 0⟩ = g
    ext <;> simp [heisMul]
  inv_mul_cancel g := by
    change heisMul (heisInv g) g = ⟨0, 0, 0⟩
    ext <;> dsimp [heisMul, heisInv] <;> ring

theorem heisenberg_card : Fintype.card Heisenberg = 729 := by decide

def central (t : Phase) : Heisenberg := ⟨0, 0, t⟩
def sectionMap (u : Displacement) : Heisenberg := ⟨u.1, u.2, 0⟩
def projection (g : Heisenberg) : Displacement := (g.a, g.b)

theorem projection_product (g h : Heisenberg) : projection (g * h) = projection g + projection h := rfl

theorem central_product (t s : Phase) : central (t + s) = central t * central s := by
  change central (t + s) = heisMul (central t) (central s)
  ext <;> simp [central, heisMul]

theorem central_commutes (t : Phase) (g : Heisenberg) : central t * g = g * central t := by
  change heisMul (central t) g = heisMul g (central t)
  ext <;> simp [heisMul, central, add_comm]

theorem projection_kernel (g : Heisenberg) : projection g = 0 ↔ ∃ t, g = central t := by
  constructor
  · intro h
    refine ⟨g.t, ?_⟩
    have ha := congrArg Prod.fst h
    have hb := congrArg Prod.snd h
    ext <;> simp_all [projection, central]
  · rintro ⟨t, rfl⟩
    rfl

theorem projection_surjective : Function.Surjective projection := by
  intro u
  exact ⟨sectionMap u, rfl⟩

theorem central_injective : Function.Injective central := by
  intro t s h
  exact congrArg Heisenberg.t h

theorem center_iff (g : Heisenberg) :
    (∀ h : Heisenberg, g * h = h * g) ↔ ∃ t, g = central t := by
  constructor
  · intro hc
    have hb := congrArg Heisenberg.t (hc ⟨1, 0, 0⟩)
    have ha := congrArg Heisenberg.t (hc ⟨0, 1, 0⟩)
    change g.t + 0 + g.b * 1 = 0 + g.t + 0 * g.a at hb
    change g.t + 0 + g.b * 0 = 0 + g.t + 1 * g.a at ha
    have hb0 : g.b = 0 := by simpa using hb
    have ha0 : g.a = 0 := by simpa using ha.symm
    refine ⟨g.t, ?_⟩
    ext <;> simp_all [central]
  · rintro ⟨t, rfl⟩ h
    exact central_commutes t h

theorem commutator_formula (u v : Displacement) :
    sectionMap u * sectionMap v * (sectionMap u)⁻¹ * (sectionMap v)⁻¹ =
      central (-area u v) := by
  change heisMul (heisMul (heisMul (sectionMap u) (sectionMap v))
    (heisInv (sectionMap u))) (heisInv (sectionMap v)) = central (-area u v)
  ext <;> simp only [heisMul, heisInv, sectionMap, central, area] <;> ring

/-- The ordered section is X^a Z^b, hence its phase is evaluated at r-a. -/
def action (g : Heisenberg) (f : Wave) : Wave :=
  fun r => phase (g.t + g.b * (r - g.a)) * f (r - g.a)

theorem action_ordered (g : Heisenberg) (f : Wave) :
    action g f = fun r => phase g.t * translate g.a (modulate g.b f) r := by
  funext r
  simp only [action, translate, modulate, phase_add]
  ring

theorem action_one (f : Wave) : action 1 f = f := by
  funext r
  change phase (0 + 0 * (r - 0)) * f (r - 0) = f r
  simp [phase_zero]

theorem action_product (g h : Heisenberg) (f : Wave) :
    action (g * h) f = action g (action h f) := by
  funext r
  change phase ((g.t + h.t + g.b * h.a) + (g.b + h.b) * (r - (g.a + h.a))) *
    f (r - (g.a + h.a)) = phase (g.t + g.b * (r - g.a)) *
    (phase (h.t + h.b * (r - g.a - h.a)) * f (r - g.a - h.a))
  rw [← mul_assoc, ← phase_add]
  have he : g.t + h.t + g.b * h.a + (g.b + h.b) * (r - (g.a + h.a)) =
      g.t + g.b * (r - g.a) + (h.t + h.b * (r - g.a - h.a)) := by ring
  rw [he]
  congr 2
  ring

theorem action_inverse (g : Heisenberg) (f : Wave) : action g⁻¹ (action g f) = f := by
  rw [← action_product, inv_mul_cancel, action_one]

theorem action_central (t : Phase) (f : Wave) :
    action (central t) f = fun r => phase t * f r := by
  funext r
  simp [action, central]

theorem action_commutator (u v : Displacement) (f : Wave) :
    action (sectionMap u) (action (sectionMap v)
      (action (sectionMap u)⁻¹ (action (sectionMap v)⁻¹ f))) =
      fun r => phase (-area u v) * f r := by
  rw [← action_product, ← action_product, ← action_product]
  rw [commutator_formula, action_central]

def delta (s : Phase) : Wave := fun r => if r = s then 1 else 0

theorem action_kernel (g : Heisenberg) (h : ∀ f, action g f = f) : g = 1 := by
  have ha : g.a = 0 := by
    have hd := congrFun (h (delta 0)) g.a
    by_contra hne
    simp only [action, sub_self, mul_zero, add_zero, delta, if_pos, mul_one, hne, if_false] at hd
    exact phase_ne_zero g.t hd
  have ht : g.t = 0 := by
    have hv := congrFun (h (fun _ => 1)) 0
    simp only [action, ha, sub_self, mul_zero, add_zero, mul_one] at hv
    exact phase_injective (hv.trans phase_zero.symm)
  have hb : g.b = 0 := by
    have hv := congrFun (h (fun _ => 1)) 1
    simp only [action, ha, ht, sub_zero, mul_one, zero_add] at hv
    exact phase_injective (hv.trans phase_zero.symm)
  ext <;> assumption

theorem action_faithful (g h : Heisenberg) (he : action g = action h) : g = h := by
  have hk : h⁻¹ * g = 1 := action_kernel _ (by
    intro f
    rw [action_product, show action g f = action h f from congrFun he f, action_inverse])
  exact (inv_mul_eq_one.mp hk).symm

def inner (f g : Wave) : ℂ := ∑ r, star (f r) * g r

theorem delta_orthonormal (a b : Phase) :
    inner (delta a) (delta b) = if a = b then 1 else 0 := by
  simp [inner, delta, eq_comm]

theorem phase_star_mul (r : Phase) : star (phase r) * phase r = 1 := by
  rw [phase_recognition, ZMod.stdAddChar_apply]
  change (starRingEnd ℂ) (ZMod.toCircle r : ℂ) * (ZMod.toCircle r : ℂ) = 1
  rw [← Circle.coe_inv_eq_conj, ← Circle.coe_mul, inv_mul_cancel, Circle.coe_one]

theorem translate_inner (a : Phase) (f g : Wave) :
    inner (translate a f) (translate a g) = inner f g := by
  simp only [inner, translate]
  apply Finset.sum_bij (fun r _ => r - a)
  · intro r hr
    simp
  · intro r hr s hs h
    have hh := congrArg (fun x : Phase => x + a) h
    simpa only [sub_add_cancel] using hh
  · intro r hr
    exact ⟨r + a, by simp, by ring⟩
  · intro r hr
    rfl

theorem modulate_inner (b : Phase) (f g : Wave) :
    inner (modulate b f) (modulate b g) = inner f g := by
  apply Finset.sum_congr rfl
  intro r hr
  change star (phase (b * r) * f r) * (phase (b * r) * g r) = star (f r) * g r
  rw [star_mul]
  calc
    star (f r) * star (phase (b * r)) * (phase (b * r) * g r) =
        (star (phase (b * r)) * phase (b * r)) * (star (f r) * g r) := by ring
    _ = star (f r) * g r := by rw [phase_star_mul, one_mul]

theorem action_add (h : Heisenberg) (f g : Wave) : action h (f + g) = action h f + action h g := by
  funext r
  simp [action, mul_add]

theorem action_smul (h : Heisenberg) (c : ℂ) (f : Wave) : action h (c • f) = c • action h f := by
  funext r
  simp only [action, Pi.smul_apply, smul_eq_mul]
  ring

def actionEquiv (h : Heisenberg) : Wave ≃ₗ[ℂ] Wave where
  toFun := action h
  invFun := action h⁻¹
  left_inv := action_inverse h
  right_inv := by intro f; simpa only [inv_inv] using action_inverse h⁻¹ f
  map_add' := action_add h
  map_smul' := action_smul h

theorem action_inner (h : Heisenberg) (f g : Wave) : inner (action h f) (action h g) = inner f g := by
  have hs : inner (action h f) (action h g) =
      inner (translate h.a (modulate h.b f)) (translate h.a (modulate h.b g)) := by
    rw [action_ordered, action_ordered]
    apply Finset.sum_congr rfl
    intro r hr
    change star (phase h.t * translate h.a (modulate h.b f) r) *
      (phase h.t * translate h.a (modulate h.b g) r) = _
    rw [star_mul]
    calc
      star (translate h.a (modulate h.b f) r) * star (phase h.t) *
          (phase h.t * translate h.a (modulate h.b g) r) =
        (star (phase h.t) * phase h.t) *
          (star (translate h.a (modulate h.b f) r) * translate h.a (modulate h.b g) r) := by ring
      _ = _ := by rw [phase_star_mul, one_mul]
  rw [hs, translate_inner, modulate_inner]

namespace Duality

abbrev PositiveRadius := {r : ℝ // 0 < r}
abbrev Datum := (ℤ × ℤ) × PositiveRadius

def transform (d : Datum) : Datum :=
  (d.1.swap, ⟨(d.2 : ℝ)⁻¹, inv_pos.mpr d.2.property⟩)

theorem transform_involutive : Function.Involutive transform := by
  rintro ⟨⟨m, w⟩, ⟨r, hr⟩⟩
  simp [transform]

def transformEquiv : Datum ≃ Datum where
  toFun := transform
  invFun := transform
  left_inv := transform_involutive
  right_inv := transform_involutive

def energyAt (r : ℝ) (v : ℤ × ℤ) : ℝ :=
  (v.1 : ℝ) ^ 2 / r ^ 2 + (v.2 : ℝ) ^ 2 * r ^ 2

def energy (d : Datum) : ℝ := energyAt d.2 d.1

theorem energyAt_swap_inv (r : ℝ) (v : ℤ × ℤ) :
    energyAt r⁻¹ v.swap = energyAt r v := by
  simp only [energyAt, Prod.fst_swap, Prod.snd_swap, inv_pow,
    div_inv_eq_mul, div_eq_mul_inv, inv_inv]
  ring

theorem energy_transform (d : Datum) : energy (transform d) = energy d := by
  exact energyAt_swap_inv d.2 d.1

theorem energy_nonneg (d : Datum) : 0 ≤ energy d := by
  unfold energy energyAt
  positivity

theorem transform_eq_self_iff (d : Datum) :
    transform d = d ↔ (d.2 : ℝ) = 1 ∧ d.1.1 = d.1.2 := by
  rcases d with ⟨⟨m, w⟩, ⟨r, hr⟩⟩
  constructor
  · intro h
    have hw : w = m := congrArg (fun x : Datum => x.1.1) h
    have hi : r⁻¹ = r := congrArg (fun x : Datum => (x.2 : ℝ)) h
    have hm : r * r = 1 := by
      calc
        r * r = r * r⁻¹ := by rw [hi]
        _ = 1 := mul_inv_cancel₀ (ne_of_gt hr)
    exact ⟨by dsimp; nlinarith, hw.symm⟩
  · rintro ⟨hr1, hmw⟩
    apply Prod.ext
    · exact Prod.ext hmw.symm hmw
    · apply Subtype.ext
      change r⁻¹ = r
      change r = 1 at hr1
      rw [hr1]
      norm_num

abbrev WaveFunction := (ℤ × ℤ) → ℂ

/-- Coordinate exchange on all complex-valued functions; no summability assumed. -/
def swapFunction (f : WaveFunction) : WaveFunction := fun v => f v.swap

theorem swapFunction_involutive : Function.Involutive swapFunction := by
  intro f
  funext v
  simp [swapFunction]

/-- Pointwise multiplication, not an unbounded Hilbert-space operator. -/
def multiplyEnergy (r : ℝ) (f : WaveFunction) : WaveFunction :=
  fun v => (energyAt r v : ℂ) * f v

theorem pointwise_conjugation (r : ℝ) (f : WaveFunction) :
    swapFunction (multiplyEnergy r (swapFunction f)) = multiplyEnergy r⁻¹ f := by
  funext v
  change (energyAt r v.swap : ℂ) * f v.swap.swap = (energyAt r⁻¹ v : ℂ) * f v
  have he : energyAt r v.swap = energyAt r⁻¹ v := by
    simpa using (energyAt_swap_inv r v.swap).symm
  rw [he]
  rfl

end Duality

end FiniteWeyl
end

#print axioms FiniteWeyl.clock_phase_advance
#print axioms FiniteWeyl.app_sum_publication
#print axioms FiniteWeyl.app_product_publication
#print axioms FiniteWeyl.plaquette_curvatures
#print axioms FiniteWeyl.trit_elliptic_realization
#print axioms FiniteWeyl.phase_recognition
#print axioms FiniteWeyl.phase_zero
#print axioms FiniteWeyl.phase_add
#print axioms FiniteWeyl.phase_injective
#print axioms FiniteWeyl.phase_norm
#print axioms FiniteWeyl.phase_ne_zero
#print axioms FiniteWeyl.phase_neg_mul
#print axioms FiniteWeyl.phase_pow_nine
#print axioms FiniteWeyl.phase_as_power
#print axioms FiniteWeyl.translate_add
#print axioms FiniteWeyl.modulate_add
#print axioms FiniteWeyl.translate_zero
#print axioms FiniteWeyl.modulate_zero
#print axioms FiniteWeyl.translate_inverse
#print axioms FiniteWeyl.modulate_inverse
#print axioms FiniteWeyl.weyl_relation
#print axioms FiniteWeyl.ZX_eq_omega_XZ
#print axioms FiniteWeyl.translate_iterate
#print axioms FiniteWeyl.modulate_iterate
#print axioms FiniteWeyl.X_nine
#print axioms FiniteWeyl.Z_nine
#print axioms FiniteWeyl.area_alternating
#print axioms FiniteWeyl.area_basis
#print axioms FiniteWeyl.cocycle_identity
#print axioms FiniteWeyl.antisymmetric_cocycle
#print axioms FiniteWeyl.heisenberg_card
#print axioms FiniteWeyl.projection_product
#print axioms FiniteWeyl.central_product
#print axioms FiniteWeyl.central_commutes
#print axioms FiniteWeyl.projection_kernel
#print axioms FiniteWeyl.projection_surjective
#print axioms FiniteWeyl.central_injective
#print axioms FiniteWeyl.center_iff
#print axioms FiniteWeyl.commutator_formula
#print axioms FiniteWeyl.action_ordered
#print axioms FiniteWeyl.action_one
#print axioms FiniteWeyl.action_product
#print axioms FiniteWeyl.action_inverse
#print axioms FiniteWeyl.action_central
#print axioms FiniteWeyl.action_commutator
#print axioms FiniteWeyl.action_kernel
#print axioms FiniteWeyl.action_faithful
#print axioms FiniteWeyl.delta_orthonormal
#print axioms FiniteWeyl.phase_star_mul
#print axioms FiniteWeyl.translate_inner
#print axioms FiniteWeyl.modulate_inner
#print axioms FiniteWeyl.action_add
#print axioms FiniteWeyl.action_smul
#print axioms FiniteWeyl.action_inner
#print axioms FiniteWeyl.Duality.transform_involutive
#print axioms FiniteWeyl.Duality.energyAt_swap_inv
#print axioms FiniteWeyl.Duality.energy_transform
#print axioms FiniteWeyl.Duality.energy_nonneg
#print axioms FiniteWeyl.Duality.transform_eq_self_iff
#print axioms FiniteWeyl.Duality.swapFunction_involutive
#print axioms FiniteWeyl.Duality.pointwise_conjugation
