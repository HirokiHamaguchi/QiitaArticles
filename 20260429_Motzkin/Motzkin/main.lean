import Motzkin.Crosscut
import Motzkin.Motzkin

import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.Between
import Mathlib.Analysis.Convex.StrictConvexSpace
import Mathlib.Analysis.InnerProductSpace.Convex
import Mathlib.Analysis.InnerProductSpace.Basic

open Set AffineMap Metric
open scoped Topology
open scoped InnerProductSpace

variable {n : ℕ}

local notation "L" => EuclideanSpace ℝ (Fin n)

/-- `xy` is a crosscut of `K`. -/
def IsCrosscut (K : Set L) (x y : L) : Prop :=
  x ∈ frontier K ∧
  y ∈ frontier K ∧
  x ≠ y ∧
  openSegment ℝ x y ⊆ interior K

/-- `K` has no crosscut. -/
def HasNoCrosscut (K : Set L) : Prop :=
  ∀ x y : L, ¬ IsCrosscut K x y

lemma exists_frontier_point_segment_to_interior
    {K : Set L} (hK : IsOpen K) {x z : L}
    (hx : x ∈ compl K) (hz : z ∈ interior K) :
    ∃ u : L,
      u ≠ z ∧
      u ∈ frontier K ∧
      u ∈ segment ℝ x z ∧
      openSegment ℝ u z ⊆ interior K := by
  exact _exists_frontier_point_segment_to_interior hK hx hz

/--
`x` -- `u` -- `z` -- `v` -- `y`
-/
lemma openSegment_uv_ordered
    {x y z u v : L}
    (hNegUZ : u ≠ z)
    (hNegZV : z ≠ v)
    (hz : z ∈ openSegment ℝ x y)
    (hu : u ∈ segment ℝ x z)
    (hv : v ∈ segment ℝ z y) :
    u ≠ v ∧
      openSegment ℝ u v ⊆
        openSegment ℝ u z ∪ {z} ∪ openSegment ℝ z v := by
  exact _openSegment_uv_ordered hNegUZ hNegZV hz hu hv

/--
Theorem 4.2 in "Convex sets"
If an open set `K` has no crosscut, then its complement is convex.

Reference:
Valentine, F. A. (1964). Convex sets.
McGraw-Hill series in higher mathematics. McGraw-Hill Book Company.
-/
lemma thm_4_2 {K : Set L}
    (hKIsOpen : IsOpen K)
    (hK : HasNoCrosscut K) :
    Convex ℝ (compl K) := by
  apply convex_iff_openSegment_subset.mpr
  intro x hx y hy z hz_seg hzK

  have hz_int : z ∈ interior K := by
    simpa [hKIsOpen.interior_eq] using hzK

  obtain ⟨u, hNeqUZ, hu_frontier, hu_xz, hu_sub⟩ :=
    exists_frontier_point_segment_to_interior hKIsOpen hx hz_int

  obtain ⟨v, hNeqZV, hv_frontier, hv_yz_symm, hv_sub_symm⟩ :=
    exists_frontier_point_segment_to_interior hKIsOpen hy hz_int

  have hv_yz : v ∈ segment ℝ z y := by
    simpa [segment_symm] using hv_yz_symm

  obtain ⟨hNeqUV, hOpenSegUVDecomp⟩ := openSegment_uv_ordered hNeqUZ hNeqZV.symm hz_seg hu_xz hv_yz

  refine hK u v ⟨hu_frontier, hv_frontier, hNeqUV, ?_⟩

  intro w hw
  rcases hOpenSegUVDecomp hw with (hwuz | hwz) | hwzv
  · exact hu_sub hwuz
  · rw [hwz]
    exact hz_int
  · apply hv_sub_symm
    rw [openSegment_symm]
    exact hwzv

/--
`K` has the unique nearest-point property:
for every `x`, there exists a unique `q ∈ K` minimizing the distance from `x` to `K`.
-/
def HasUniqueNearestPointProperty (K : Set L) : Prop :=
  ∀ x : L, ∃! q : L, q ∈ K ∧ dist x q = infDist x K

def HasUniqueNearestPointProperty' (K : Set L) : Prop :=
  ∀ x : L, ∃! q : L, q ∈ K ∧ ∀ y : L, y ∈ K → dist x q ≤ dist x y

lemma isIffHasUniqueNearestPointProperty
    (K : Set L) :
    HasUniqueNearestPointProperty K ↔ HasUniqueNearestPointProperty' K := by
  constructor
  · intro h x
    rcases h x with ⟨q, ⟨hqK, hqdist⟩, hquniq⟩
    refine ⟨q, ⟨hqK, ?_⟩, ?_⟩
    · intro y hyK
      rw [hqdist]
      exact Metric.infDist_le_dist_of_mem hyK
    · intro q' ⟨hq'K, hq'min⟩
      apply hquniq
      refine ⟨hq'K, le_antisymm ?_ ?_⟩
      · rw [← hqdist]
        exact hq'min q hqK
      · exact (Metric.infDist_le_dist_of_mem hq'K)
  · intro h x
    rcases h x with ⟨q, ⟨hqK, hqmin⟩, hquniq⟩
    refine ⟨q, ⟨hqK, ?_⟩, ?_⟩
    · refine le_antisymm ?_ ?_
      · by_cases hK_nonempty : K.Nonempty
        · apply (Metric.le_infDist hK_nonempty).mpr
          exact hqmin
        · have hK_empty : K.Nonempty := ⟨q, hqK⟩
          contradiction
      · exact (Metric.infDist_le_dist_of_mem hqK)
    · intro q' ⟨hq'K, hq'dist⟩
      apply hquniq
      refine ⟨hq'K, ?_⟩
      intro y hyK
      rw [hq'dist]
      exact Metric.infDist_le_dist_of_mem hyK

lemma Motzkin_only_if
    {K : Set L}
    (hK_nonempty : K.Nonempty)
    (hK_closed : IsClosed K) :
    Convex ℝ K → HasUniqueNearestPointProperty K := by
  intro hK_convex x
  obtain ⟨p, hpK, hpdist⟩ :=
    hK_closed.exists_infDist_eq_dist hK_nonempty x

  refine ⟨p, ⟨hpK, hpdist.symm⟩, ?_⟩
  intro q ⟨hqK, hqdist⟩
  by_contra hqp
  have hpq : p ≠ q := by
    apply Ne.symm
    exact hqp

  let ω : L := (1 / 2 : ℝ) • p + (1 / 2 : ℝ) • q
  let d := Metric.infDist x K

  have hω_ball : ω ∈ Metric.ball x d := by
    dsimp [ω]
    have hp_ball : p ∈ Metric.closedBall x d := by
      rw [Metric.mem_closedBall, dist_comm]
      exact le_of_eq hpdist.symm
    have hq_ball : q ∈ Metric.closedBall x d := by
      rw [Metric.mem_closedBall, dist_comm]
      exact le_of_eq hqdist
    exact combo_mem_ball_of_ne hp_ball hq_ball hpq (by norm_num) (by norm_num) (by norm_num)

  have hωK : ω ∈ K := by
    dsimp [ω]
    exact (convex_iff_add_mem.mp hK_convex)
      hpK hqK (by norm_num) (by norm_num) (by norm_num)

  have hinf_le : Metric.infDist x K ≤ dist x ω :=
    Metric.infDist_le_dist_of_mem hωK

  have hdist_lt : dist x ω < Metric.infDist x K := by
    rw [dist_comm]
    simpa [Metric.mem_ball] using hω_ball

  exact not_lt_of_ge hinf_le hdist_lt

lemma Motzkin_if
    {K : Set L}
    (hK_nonempty : K.Nonempty)
    (hK_closed : IsClosed K) :
    HasUniqueNearestPointProperty K → Convex ℝ K := by
  intro hUnique
  by_contra hK_not_convex

  have exists_crosscut : ∃ x y : L, IsCrosscut Kᶜ x y := by
    by_contra h_no_crosscut_exists

    have h_no_crosscut : HasNoCrosscut Kᶜ := by
      intro x y hxy
      exact h_no_crosscut_exists ⟨x, y, hxy⟩

    have hS_convex : Convex ℝ K := compl_compl K ▸ thm_4_2 hK_closed.isOpen_compl h_no_crosscut

    contradiction

  rcases exists_crosscut with ⟨x, y, hxFront, hyFront, hNeqXY, hOpenSegInInt⟩

  let z : L := (1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y

  have hz_int_compl : z ∈ interior Kᶜ := by
    apply hOpenSegInInt
    unfold openSegment
    use (1 / 2 : ℝ), (1 / 2 : ℝ)
    refine ⟨by norm_num, by norm_num, by norm_num, rfl⟩

  rcases hUnique z with ⟨p, ⟨hpK, hpdist⟩, hpuniq⟩
  clear hOpenSegInInt

  have hz_ne_p : z ≠ p := by
    rintro rfl
    have hz_mem_compl : z ∈ Kᶜ := interior_subset hz_int_compl
    exact hz_mem_compl hpK

  have hxK : x ∈ K := by
    apply hK_closed.frontier_subset
    simpa [frontier_compl] using hxFront

  have hyK : y ∈ K := by
    apply hK_closed.frontier_subset
    simpa [frontier_compl] using hyFront

  obtain ⟨w, hwpos, hwK, hw_ne_p⟩ :
      ∃ w : L, 0 < ⟪z - p, w - p⟫_ℝ ∧ w ∈ K ∧ w ≠ p := by
    have hinner_sum_pos :
        0 < ⟪z - p, x - p⟫_ℝ + ⟪z - p, y - p⟫_ℝ := by
      have hzmp : z - p ≠ 0 := sub_ne_zero.mpr hz_ne_p
      calc
        0 < 2 * ‖z - p‖ ^ 2 := by
          nlinarith [sq_pos_iff.mpr (norm_ne_zero_iff.mpr hzmp)]
        _ = ⟪z - p, x - p⟫_ℝ + ⟪z - p, y - p⟫_ℝ := by
          rw [← inner_add_right]
          rw [show (x - p) + (y - p) = (2 : ℝ) • (z - p) by
            dsimp [z]
            module]
          simp [inner_smul_right]
    by_cases hxpos : 0 < ⟪z - p, x - p⟫_ℝ
    · refine ⟨x, hxpos, hxK, ?_⟩
      rintro rfl
      simp at hxpos
    · have hypos : 0 < ⟪z - p, y - p⟫_ℝ := by
        linarith
      refine ⟨y, hypos, hyK, ?_⟩
      rintro rfl
      simp at hypos
  clear hxK hyK hxFront hyFront hNeqXY

  sorry

  -- let R : ℝ := ‖w - p‖ ^ 2 / (2 * ⟪z - p, w - p⟫_ℝ)
  -- let z' : L := z + R • (z - p)
  -- let r' : ℝ := (1 + R) * dist z p

  -- have hR1_nonneg : 0 ≤ 1 + R := by
  --   have hR_nonneg : 0 ≤ R := by positivity
  --   linarith

  -- have hp_in_expanding_ball : dist z' p = r' := by
  --   calc dist z' p
  --       = ‖(1 + R) • (z - p)‖ := by
  --         rw [dist_eq_norm]
  --         congr 1
  --         module
  --     _ = ‖1 + R‖ * ‖z - p‖ := by rw [norm_smul]
  --     _ = (1 + R) * dist z p := by
  --         rw [Real.norm_of_nonneg hR1_nonneg]
  --         rw [dist_eq_norm]

  -- have hw_in_expanding_ball : dist z' w ≤ r' := by
  --   have hR_mul : R * (2 * ⟪z - p, w - p⟫_ℝ) = ‖w - p‖ ^ 2 := by
  --     dsimp [R]
  --     field_simp

  --   have hsq : dist z' w ^ 2 ≤ r' ^ 2 := by
  --     rw [dist_eq_norm]
  --     calc
  --       ‖(z + R • (z - p)) - w‖ ^ 2
  --         = ‖(1 + R) • (z - p) - (w - p)‖ ^ 2 := by
  --               congr 2
  --               module
  --       _ = ((1 + R) * ‖z - p‖) ^ 2
  --             - 2 * (1 + R) * ⟪z - p, w - p⟫_ℝ
  --             + ‖w - p‖ ^ 2 := by
  --               rw [norm_sub_sq_real]
  --               rw [inner_smul_left]
  --               rw [norm_smul]
  --               rw [Real.norm_of_nonneg hR1_nonneg]
  --               simp
  --               ring
  --       _ ≤ ((1 + R) * ‖z - p‖) ^ 2 := by nlinarith

  --   have hrad_nonneg : 0 ≤ r' :=
  --     mul_nonneg hR1_nonneg dist_nonneg

  --   simpa [
  --     abs_of_nonneg dist_nonneg,
  --     abs_of_nonneg hrad_nonneg
  --   ] using sq_le_sq.mp hsq

  -- have hInfDistOfZDash : infDist z' K = r' := by
  --   sorry

  -- have hw_eq_p : w = p := by
  --   have hp_nearest : p ∈ K ∧ dist z' p = infDist z' K := by
  --     refine ⟨hpK, ?_⟩
  --     rw [hp_in_expanding_ball, hInfDistOfZDash]

  --   have hw_nearest : w ∈ K ∧ dist z' w = infDist z' K := by
  --     refine ⟨hwK, ?_⟩
  --     rw [hInfDistOfZDash.symm] at hw_in_expanding_ball
  --     exact le_antisymm hw_in_expanding_ball (infDist_le_dist_of_mem hwK)

  --   rcases hUnique z' with ⟨q, hq, hquniq⟩
  --   exact (hquniq w hw_nearest).trans (hquniq p hp_nearest).symm

  -- contradiction

theorem Motzkin
    {K : Set L}
    (hK_nonempty : K.Nonempty)
    (hK_closed : IsClosed K) :
    Convex ℝ K ↔ HasUniqueNearestPointProperty K := by
  exact ⟨Motzkin_only_if hK_nonempty hK_closed, Motzkin_if hK_nonempty hK_closed⟩
