import GeneratedN69Rows

/-!
All-depth joint regional bands and their existing N69 signature.
The three rational publication procedures generate each block; the stored
600-trit prefixes are a posterior finite comparison, not constructor inputs.
This records the joint signature/carry component, not an identification with
nine complete enriched Sel/Tra/Upd updates.
-/

noncomputable section
namespace HMT.I.JointRegionalFrontier

open HMT.N69RegionalSignature
open HMT.I.GeneratedN69Rows HMT.I.RegionalPublicationComposition

def blockGenerated (t : Nat) (i : Fin 3) : Nat :=
  publish (channelOfIndex i) 729 (by decide) (t + 1) % 729

def bandsGenerated (t : Nat) : Bands :=
  fun i => bandFromWord (blockGenerated t i)

def signatureGenerated (t : Nat) : Signature := readSignature (bandsGenerated t)

theorem publish_base729_eq_base3 (c : Channel) (n : Nat) :
    publish c 729 (by decide) n = publish c 3 (by decide) (6 * n) := by
  simp only [publish_eq_prefix, RadixCellSelection.positionalPrefix]
  congr 2
  rw [pow_mul]
  norm_num

theorem regionalPrefix_eq_base729 (i : Fin 3) :
    regionalPrefixes i = publish (channelOfIndex i) 729 (by decide) 100 := by
  rw [regionalPrefixes_are_publications, publish_base729_eq_base3]

/-- Any sufficiently long publication recovers the same earlier block. -/
theorem generated_block_from_longer_prefix (t n : Nat) (i : Fin 3) (h : t < n) :
    blockGenerated t i =
      (publish (channelOfIndex i) 729 (by decide) n / 729 ^ (n - (t + 1))) % 729 := by
  have hn : (t + 1) + (n - (t + 1)) = n := by omega
  have hc := publications_compatible (channelOfIndex i) 729 (by decide)
    (t + 1) (n - (t + 1))
  rw [hn] at hc
  unfold blockGenerated
  rw [hc]

theorem generated_block_eq_finite (t : Nat) (i : Fin 3) (h : t < 100) :
    blockGenerated t i = blockFromPrefix (regionalPrefixes i) t := by
  rw [generated_block_from_longer_prefix t 100 i h, regionalPrefix_eq_base729]
  unfold blockFromPrefix
  have hn : 100 - (t + 1) = 99 - t := by omega
  rw [hn]

theorem bandsGenerated_eq_finite (t : Nat) (h : t < 100) :
    bandsGenerated t = bandsFromPrefixes regionalPrefixes t := by
  funext i
  unfold bandsGenerated bandsFromPrefixes
  rw [generated_block_eq_finite t i h]

theorem signatureGenerated_eq_finite (t : Nat) (h : t < 100) :
    signatureGenerated t = readSignature (bandsFromPrefixes regionalPrefixes t) := by
  unfold signatureGenerated
  rw [bandsGenerated_eq_finite t h]

theorem generated_block_lt (t : Nat) (i : Fin 3) : blockGenerated t i < 729 :=
  Nat.mod_lt _ (by decide)

/-- Exact residue and carry retain the unreduced sum of the three regions. -/
theorem generated_column_reconstruction (t : Nat) (j : Fin 6) :
    (signatureGenerated t).q j + 3 * (signatureGenerated t).c j =
      columnTotal (bandsGenerated t) j :=
  signature_reconstructs_columns (bandsGenerated t) j

theorem generated_signed_axial (t : Nat) (j : Fin 6) :
    ((signatureGenerated t).a j : Int) =
      ((bandsGenerated t 0 j).val + (bandsGenerated t 1 j).val -
        (bandsGenerated t 2 j).val : Int) % 3 :=
  a_is_signed_residue (bandsGenerated t) j

/-- q and a recover the auto-scale axis; no terminal row is supplied. -/
theorem signature_recovers_axis (B : Bands) (j : Fin 6) :
    (B 2 j).val = (2 * (q B j + 3 - a B j)) % 3 := by
  have h0 := (B 0 j).isLt
  have h1 := (B 1 j).isLt
  have h2 := (B 2 j).isLt
  unfold q a columnTotal
  omega

theorem generated_axis_reconstruction (t : Nat) (j : Fin 6) :
    (bandsGenerated t 2 j).val =
      (2 * ((signatureGenerated t).q j + 3 - (signatureGenerated t).a j)) % 3 :=
  signature_recovers_axis (bandsGenerated t) j

theorem generated_signature_bounds (t : Nat) (j : Fin 6) :
    (signatureGenerated t).q j < 3 ∧ (signatureGenerated t).a j < 3 ∧
      (signatureGenerated t).c j ≤ 2 ∧ (signatureGenerated t).colw j ≤ 3 ∧
      (signatureGenerated t).colwMod j < 3 :=
  ⟨q_lt_three _ _, a_lt_three _ _, carry_le_two _ _, columnWeight_le_three _ _,
    columnWeightMod_lt_three _ _⟩

theorem generated_dual_charge (t : Nat) (i : Fin 3) :
    (signatureGenerated t).wittDual i =
      (∑ j : Fin 6, wittResidue (bandsGenerated t) i j) % 3 :=
  wittDualCharge_residue_sum (bandsGenerated t) i

end HMT.I.JointRegionalFrontier
end

#print axioms HMT.I.JointRegionalFrontier.publish_base729_eq_base3
#print axioms HMT.I.JointRegionalFrontier.regionalPrefix_eq_base729
#print axioms HMT.I.JointRegionalFrontier.generated_block_from_longer_prefix
#print axioms HMT.I.JointRegionalFrontier.generated_block_eq_finite
#print axioms HMT.I.JointRegionalFrontier.bandsGenerated_eq_finite
#print axioms HMT.I.JointRegionalFrontier.signatureGenerated_eq_finite
#print axioms HMT.I.JointRegionalFrontier.generated_block_lt
#print axioms HMT.I.JointRegionalFrontier.generated_column_reconstruction
#print axioms HMT.I.JointRegionalFrontier.generated_signed_axial
#print axioms HMT.I.JointRegionalFrontier.signature_recovers_axis
#print axioms HMT.I.JointRegionalFrontier.generated_axis_reconstruction
#print axioms HMT.I.JointRegionalFrontier.generated_signature_bounds
#print axioms HMT.I.JointRegionalFrontier.generated_dual_charge
