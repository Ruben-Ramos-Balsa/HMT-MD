import LatticeCoxeterFock
import Mathlib.RingTheory.Binomial

/-!
Explicit quadratic correction for lifting the actual order-three lattice
isometry to its already constructed twisted algebra. Integral binomial
terms retain diagonal information which parity coordinates alone lose.
This uses the actual one-plus-eleven Witt orientation, not the separately
presented six-plus-six matrix. No trace-54 or FLM statement is asserted.
The algebra lift is multiplicative and has order three; its tensor lift
preserves the carrier vacuum and has cube identity. Commutation with the
existing unnormalized theta and an orbifold action are not asserted here.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeCoxeterTwistedLift

open HMT.IV.LatticeCocycle HMT.IV.LatticeCoxeterFock
open HMT.IV.TwistedGroupAlgebra HMT.IV.TriangularCocycle
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeOscillatorFock
open scoped BigOperators TensorProduct

theorem integer_choose_two_add (a b : ℤ) :
    Ring.choose (a+b) 2 = Ring.choose a 2 + Ring.choose b 2 + a*b := by
  rw [Ring.add_choose_eq 2 (Commute.all a b)]
  rw [show Finset.antidiagonal 2 = {(0,2), (1,1), (2,0)} from by decide]
  norm_num [Ring.choose_zero_right, Ring.choose_one_right]
  ring

def diagonalPart {n : ℕ} (D : Fin n → Fin n → ZMod 2)
    (x y : Fin n → ZMod 2) : ZMod 2 := ∑ i, x i * D i i * y i

theorem triangle_pair_plus_diagonal {n : ℕ} (D : Fin n → Fin n → ZMod 2)
    (hD : ∀ i j, D i j = D j i) (x y : Fin n → ZMod 2) :
    tau D x y + tau D y x + diagonalPart D x y = bilinear D x y := by
  have flip : tau D y x = ∑ i, ∑ j, x i * triangle D j i * y j := by
    unfold tau bilinear
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [flip]
  unfold tau bilinear diagonalPart
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [← Finset.sum_add_distrib]
  have hd : x i * D i i * y i =
      ∑ j : Fin n, if i=j then x i * D i j * y j else 0 := by simp
  rw [hd, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  by_cases hij : i=j
  · subst j
    simp [triangle]
  · rcases lt_or_gt_of_ne hij with hlt | hgt
    · simp [triangle, hlt, not_lt_of_ge hlt.le, hij]
    · simp [triangle, hgt, not_lt_of_ge hgt.le, hij, hD j i]

def quadraticCochain {n : ℕ} (D : Fin n → Fin n → ZMod 2)
    (x : Fin n → ℤ) : ZMod 2 :=
  (∑ i, ((Ring.choose (x i) 2 : ℤ) : ZMod 2) * D i i) +
    tau D (fun i => (x i : ZMod 2)) (fun i => (x i : ZMod 2))

theorem quadraticCochain_zero {n : ℕ} (D : Fin n → Fin n → ZMod 2) :
    quadraticCochain D 0 = 0 := by
  simp [quadraticCochain, Ring.choose_zero_pos ℤ (by decide : 0<2), tau, bilinear]

theorem quadraticCochain_add {n : ℕ} (D : Fin n → Fin n → ZMod 2)
    (hD : ∀ i j, D i j = D j i) (x y : Fin n → ℤ) :
    quadraticCochain D (x+y) = quadraticCochain D x + quadraticCochain D y +
      bilinear D (fun i => (x i : ZMod 2)) (fun i => (y i : ZMod 2)) := by
  have hp : (fun i => ((x+y) i : ZMod 2)) =
      (fun i => (x i : ZMod 2)) + (fun i => (y i : ZMod 2)) := by
    funext i
    simp
  have hd : (∑ i, ((Ring.choose ((x+y) i) 2 : ℤ) : ZMod 2) * D i i) =
      (∑ i, ((Ring.choose (x i) 2 : ℤ) : ZMod 2) * D i i) +
      (∑ i, ((Ring.choose (y i) 2 : ℤ) : ZMod 2) * D i i) +
      diagonalPart D (fun i => (x i : ZMod 2)) (fun i => (y i : ZMod 2)) := by
    simp only [Pi.add_apply, integer_choose_two_add, Int.cast_add, Int.cast_mul,
      add_mul, Finset.sum_add_distrib, diagonalPart]
    congr 2
    funext i
    ring
  unfold quadraticCochain
  rw [hd, hp, tau_add_left, tau_add_right, tau_add_right,
    ← triangle_pair_plus_diagonal D hD]
  ring

theorem wittCocycle_add_left (o : Fin 12) (x y z : Lattice o) :
    wittCocycle o (x+y) z = wittCocycle o x z + wittCocycle o y z := by
  simp only [wittCocycle, parityCoordinates_add, tau_add_left]

theorem wittCocycle_add_right (o : Fin 12) (x y z : Lattice o) :
    wittCocycle o x (y+z) = wittCocycle o x y + wittCocycle o x z := by
  simp only [wittCocycle, parityCoordinates_add, tau_add_right]

def cocycleBilinear (o : Fin 12) : Lattice o →ₗ[ℤ] Lattice o →ₗ[ℤ] ZMod 2 :=
  AddMonoidHom.toIntLinearMap {
    toFun := fun x => AddMonoidHom.toIntLinearMap {
      toFun := wittCocycle o x
      map_zero' := wittCocycle_zero_right o x
      map_add' := wittCocycle_add_right o x }
    map_zero' := by ext y; exact wittCocycle_zero_left o y
    map_add' := by intro x y; ext z; exact wittCocycle_add_left o x y z }

def defectBilinear (o : Fin 12) : Lattice o →ₗ[ℤ] Lattice o →ₗ[ℤ] ZMod 2 :=
  AddMonoidHom.toIntLinearMap {
    toFun := fun x => AddMonoidHom.toIntLinearMap {
      toFun := fun y => wittCocycle o (latticeAction o x) (latticeAction o y) +
        wittCocycle o x y
      map_zero' := by simp [wittCocycle_zero_right]
      map_add' := by
        intro y z
        simp only [map_add, wittCocycle_add_right]
        ring }
    map_zero' := by ext y; simp [wittCocycle_zero_left]
    map_add' := by
      intro x y
      ext z
      change wittCocycle o (latticeAction o (x+y)) (latticeAction o z) +
        wittCocycle o (x+y) z =
        (wittCocycle o (latticeAction o x) (latticeAction o z) + wittCocycle o x z) +
        (wittCocycle o (latticeAction o y) (latticeAction o z) + wittCocycle o y z)
      simp only [map_add, wittCocycle_add_left]
      ring }

theorem defectBilinear_apply (o : Fin 12) (x y : Lattice o) :
    defectBilinear o x y = wittCocycle o (latticeAction o x) (latticeAction o y) +
      wittCocycle o x y := rfl

theorem defectBilinear_symmetric (o : Fin 12) (x y : Lattice o) :
    defectBilinear o x y = defectBilinear o y x := by
  have h1 := wittCocycle_commutator o x y
  have h2 := wittCocycle_commutator o (latticeAction o x) (latticeAction o y)
  rw [parityBilinear_apply, latticeAction_pairing, ← parityBilinear_apply] at h2
  simp only [defectBilinear_apply]
  linear_combination (norm := (ring_nf; simp [CharTwo.two_eq_zero])) h2 - h1

def initialPhase (o : Fin 12) (x : Lattice o) : ZMod 2 :=
  quadraticCochain (fun i j => defectBilinear o (latticeBasis o i) (latticeBasis o j))
    (fun i => (latticeBasis o).repr x i)

theorem initialPhase_zero (o : Fin 12) : initialPhase o 0 = 0 := by
  simpa only [initialPhase, map_zero, Finsupp.zero_apply] using
    quadraticCochain_zero (fun i j => defectBilinear o (latticeBasis o i) (latticeBasis o j))

theorem initialPhase_add (o : Fin 12) (x y : Lattice o) :
    initialPhase o (x+y) = initialPhase o x + initialPhase o y + defectBilinear o x y := by
  unfold initialPhase
  simp only [map_add, Finsupp.add_apply]
  rw [show (fun i => (latticeBasis o).repr x i + (latticeBasis o).repr y i) =
      (fun i => (latticeBasis o).repr x i) + (fun i => (latticeBasis o).repr y i) from rfl]
  rw [quadraticCochain_add _ (fun i j => defectBilinear_symmetric o _ _)]
  congr 1
  exact (integral_basis_parity_expansion (latticeBasis o) (defectBilinear o) x y).symm

/-- The orbital normalization gives an order-three lift, rather than an
arbitrary lift whose cube could be a residual character. -/
def phaseExponent (o : Fin 12) (x : Lattice o) : ZMod 2 :=
  initialPhase o (latticeAction o x) +
    initialPhase o (latticeAction o (latticeAction o x))

theorem phaseExponent_zero (o : Fin 12) : phaseExponent o 0 = 0 := by
  simp [phaseExponent, initialPhase_zero]

theorem phaseExponent_coboundary (o : Fin 12) (x y : Lattice o) :
    phaseExponent o (x+y) + wittCocycle o x y =
      phaseExponent o x + phaseExponent o y +
        wittCocycle o (latticeAction o x) (latticeAction o y) := by
  simp only [phaseExponent, map_add, initialPhase_add, defectBilinear_apply,
    latticeAction_cube]
  ring_nf
  simp [CharTwo.two_eq_zero]

theorem phaseExponent_orbit (o : Fin 12) (x : Lattice o) :
    phaseExponent o x + phaseExponent o (latticeAction o x) +
      phaseExponent o (latticeAction o (latticeAction o x)) = 0 := by
  simp only [phaseExponent, latticeAction_cube]
  ring_nf
  simp [CharTwo.two_eq_zero]

def complexSign (z : ZMod 2) : ℂ := (TC.sign z : ℤ)

theorem complexSign_add (a b : ZMod 2) :
    complexSign (a+b) = complexSign a * complexSign b := by
  unfold complexSign
  rw [TC.sign_add, Int.cast_mul]

theorem complexSign_zero : complexSign 0 = 1 := by
  simp [complexSign, TC.sign]

def phase (o : Fin 12) (x : Lattice o) : ℂ := complexSign (phaseExponent o x)

theorem phase_zero (o : Fin 12) : phase o 0 = 1 := by
  rw [phase, phaseExponent_zero, complexSign_zero]

theorem phase_compatibility (o : Fin 12) (x y : Lattice o) :
    epsilon o x y * phase o (x+y) =
      phase o x * phase o y * epsilon o (latticeAction o x) (latticeAction o y) := by
  change complexSign (wittCocycle o x y) * complexSign (phaseExponent o (x+y)) =
    complexSign (phaseExponent o x) * complexSign (phaseExponent o y) *
      complexSign (wittCocycle o (latticeAction o x) (latticeAction o y))
  rw [← complexSign_add, ← complexSign_add, ← complexSign_add]
  rw [add_comm (wittCocycle o x y), phaseExponent_coboundary]

theorem phase_orbit (o : Fin 12) (x : Lattice o) :
    phase o x * phase o (latticeAction o x) *
      phase o (latticeAction o (latticeAction o x)) = 1 := by
  simp only [phase, ← complexSign_add, phaseExponent_orbit, complexSign_zero]

def twistedLinear (o : Fin 12) : Module.End ℂ (TwistedAlgebra o) :=
  (latticeBasisComplex o).constr ℂ (fun x => phase o x • basisElement o (latticeAction o x))

theorem twistedLinear_basis (o : Fin 12) (x : Lattice o) :
    twistedLinear o (basisElement o x) = phase o x • basisElement o (latticeAction o x) := by
  have h := Basis.constr_basis (latticeBasisComplex o) ℂ
    (fun x => phase o x • basisElement o (latticeAction o x)) x
  simpa only [twistedLinear, latticeBasisComplex, Finsupp.coe_basisSingleOne] using h

theorem twistedLinear_single (o : Fin 12) (x : Lattice o) (a : ℂ) :
    twistedLinear o (Finsupp.single x a) =
      Finsupp.single (latticeAction o x) (a * phase o x) := by
  rw [show Finsupp.single x a = a • basisElement o x by
        change Finsupp.single x a = a • (Finsupp.single x 1 : Lattice o →₀ ℂ)
        rw [Finsupp.smul_single, smul_eq_mul, mul_one],
    map_smul, twistedLinear_basis, smul_smul]
  change (a * phase o x) • (Finsupp.single (latticeAction o x) 1 : Lattice o →₀ ℂ) = _
  rw [Finsupp.smul_single, smul_eq_mul, mul_one]

theorem twistedLinear_cube (o : Fin 12) (f : TwistedAlgebra o) :
    twistedLinear o (twistedLinear o (twistedLinear o f)) = f := by
  induction f using Finsupp.induction_linear with
  | zero => simp
  | add f g hf hg => simp [hf, hg]
  | single x a =>
      simp only [twistedLinear_single, latticeAction_cube]
      congr 1
      calc
        ((a * phase o x) * phase o (latticeAction o x)) *
            phase o (latticeAction o (latticeAction o x)) =
          a * (phase o x * phase o (latticeAction o x) *
            phase o (latticeAction o (latticeAction o x))) := by ring
        _ = a := by rw [phase_orbit, mul_one]

theorem twistedLinear_one (o : Fin 12) : twistedLinear o 1 = 1 := by
  change twistedLinear o (Finsupp.single 0 1) = Finsupp.single 0 1
  rw [twistedLinear_single, map_zero, phase_zero, one_mul]

theorem twistedLinear_mul (o : Fin 12) (f g : TwistedAlgebra o) :
    twistedLinear o (f*g) = twistedLinear o f * twistedLinear o g := by
  change twistedLinear o (twistedMul o f g) =
    twistedMul o (twistedLinear o f) (twistedLinear o g)
  induction f using Finsupp.induction_linear with
  | zero => simp [twistedMul_zero_left]
  | add f h hf hh =>
      simp only [twistedMul_add_left, map_add, hf, hh]
      exact (twistedMul_add_left o (twistedLinear o f) (twistedLinear o h)
        (twistedLinear o g)).symm
  | single x a =>
    induction g using Finsupp.induction_linear with
    | zero => simp [twistedMul_zero_right]
    | add g h hg hh =>
        simp only [twistedMul_add_right, map_add, hg, hh]
        exact (twistedMul_add_right o (twistedLinear o (Finsupp.single x a))
          (twistedLinear o g) (twistedLinear o h)).symm
    | single y b =>
        simp only [twistedMul_single, twistedLinear_single, map_add]
        congr 1
        calc
          a*b*epsilon o x y*phase o (x+y) =
              a*b*(epsilon o x y*phase o (x+y)) := by ring
          _ = a*b*(phase o x*phase o y*
              epsilon o (latticeAction o x) (latticeAction o y)) := by
                rw [phase_compatibility]
          _ = _ := by ring

def twistedEquiv (o : Fin 12) : TwistedAlgebra o ≃ₐ[ℂ] TwistedAlgebra o :=
  AlgEquiv.ofLinearEquiv {
    toLinearMap := twistedLinear o
    invFun := fun f => twistedLinear o (twistedLinear o f)
    left_inv := twistedLinear_cube o
    right_inv := twistedLinear_cube o }
    (twistedLinear_one o) (twistedLinear_mul o)

theorem twistedEquiv_basis (o : Fin 12) (x : Lattice o) :
    twistedEquiv o (basisElement o x) =
      phase o x • basisElement o (latticeAction o x) := twistedLinear_basis o x

theorem twistedEquiv_cube (o : Fin 12) (f : TwistedAlgebra o) :
    twistedEquiv o (twistedEquiv o (twistedEquiv o f)) = f := twistedLinear_cube o f

theorem twistedEquiv_ne_one (o : Fin 12) : twistedEquiv o ≠ 1 := by
  intro h
  let x : Lattice o := ⟨CoxeterNeighbor.rootDifference o,
    CoxeterNeighbor.rootDifference o,
    CoxeterNeighbor.rootDifference_mem_kernel CoxeterNeighbor.wittCode o, 0, by simp⟩
  have hx : latticeAction o x ≠ x := by
    intro he
    have hv := congrArg (fun z : Lattice o => (z : CoxeterNeighbor.Space 12)) he
    change CoxeterNeighbor.action CoxeterNeighbor.wittOrientation
      (CoxeterNeighbor.rootDifference o) = CoxeterNeighbor.rootDifference o at hv
    exact CoxeterNeighbor.rootDifference_ne_zero o
      ((CoxeterNeighbor.action_fixed_iff _ _).mp hv)
  have he := congrArg (fun e : TwistedAlgebra o ≃ₐ[ℂ] TwistedAlgebra o =>
    e (basisElement o x)) h
  change twistedEquiv o (basisElement o x) = basisElement o x at he
  rw [twistedEquiv_basis] at he
  have hc := congrArg (fun f : Lattice o →₀ ℂ => f x) he
  change phase o x * (Finsupp.single (latticeAction o x) 1 x) =
    Finsupp.single x 1 x at hc
  simp only [Finsupp.single_apply, if_neg hx, if_pos rfl, mul_zero] at hc
  exact zero_ne_one hc

theorem twistedEquiv_order (o : Fin 12) : orderOf (twistedEquiv o) = 3 := by
  apply orderOf_eq_prime
  · apply AlgEquiv.ext
    intro f
    exact twistedEquiv_cube o f
  · exact twistedEquiv_ne_one o

/-- The same Coxeter acts simultaneously on the actual Fock and twisted
charge factors, with the phase correction retained on the latter. -/
def carrierEquiv (o : Fin 12) : LatticeCarrier o ≃ₗ[ℂ] LatticeCarrier o :=
  TensorProduct.congr (fockEquiv o).toLinearEquiv (twistedEquiv o).toLinearEquiv

theorem carrierEquiv_pure (o : Fin 12) (v : Fock o) (f : TwistedAlgebra o) :
    carrierEquiv o (v ⊗ₜ[ℂ] f) =
      fockEquiv o v ⊗ₜ[ℂ] twistedEquiv o f := TensorProduct.congr_tmul _ _ _ _

theorem carrierEquiv_charge (o : Fin 12) (v : Fock o) (x : Lattice o) :
    carrierEquiv o (v ⊗ₜ[ℂ] basisElement o x) =
      phase o x • (fockEquiv o v ⊗ₜ[ℂ] basisElement o (latticeAction o x)) := by
  rw [carrierEquiv_pure, twistedEquiv_basis, TensorProduct.tmul_smul]

theorem carrierEquiv_cube (o : Fin 12) (v : LatticeCarrier o) :
    carrierEquiv o (carrierEquiv o (carrierEquiv o v)) = v := by
  induction v using TensorProduct.induction_on with
  | zero => simp only [map_zero]
  | tmul v f =>
      simp only [carrierEquiv_pure, twistedEquiv_cube]
      change fockAction o (fockAction o (fockAction o v)) ⊗ₜ[ℂ] f = v ⊗ₜ[ℂ] f
      rw [fockAction_cube]
  | add u v hu hv => simp only [map_add, hu, hv]

theorem carrierEquiv_vacuum (o : Fin 12) : carrierEquiv o (vacuum o) = vacuum o := by
  simp only [vacuum, carrierEquiv_pure, map_one]

end HMT.IV.LatticeCoxeterTwistedLift
end

#print axioms HMT.IV.LatticeCoxeterTwistedLift.integer_choose_two_add
#print axioms HMT.IV.LatticeCoxeterTwistedLift.quadraticCochain_add
#print axioms HMT.IV.LatticeCoxeterTwistedLift.defectBilinear_symmetric
#print axioms HMT.IV.LatticeCoxeterTwistedLift.initialPhase_add
#print axioms HMT.IV.LatticeCoxeterTwistedLift.phaseExponent_coboundary
#print axioms HMT.IV.LatticeCoxeterTwistedLift.phaseExponent_orbit
#print axioms HMT.IV.LatticeCoxeterTwistedLift.phase_compatibility
#print axioms HMT.IV.LatticeCoxeterTwistedLift.phase_orbit
#print axioms HMT.IV.LatticeCoxeterTwistedLift.twistedLinear_cube
#print axioms HMT.IV.LatticeCoxeterTwistedLift.twistedLinear_mul
#print axioms HMT.IV.LatticeCoxeterTwistedLift.twistedEquiv
#print axioms HMT.IV.LatticeCoxeterTwistedLift.twistedEquiv_basis
#print axioms HMT.IV.LatticeCoxeterTwistedLift.twistedEquiv_cube
#print axioms HMT.IV.LatticeCoxeterTwistedLift.twistedEquiv_order
#print axioms HMT.IV.LatticeCoxeterTwistedLift.carrierEquiv
#print axioms HMT.IV.LatticeCoxeterTwistedLift.carrierEquiv_charge
#print axioms HMT.IV.LatticeCoxeterTwistedLift.carrierEquiv_cube
#print axioms HMT.IV.LatticeCoxeterTwistedLift.carrierEquiv_vacuum
