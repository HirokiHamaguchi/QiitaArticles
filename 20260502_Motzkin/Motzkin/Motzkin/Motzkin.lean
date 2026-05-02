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

  have hωK : ω ∈ K := by
    dsimp [ω]
    exact (convex_iff_add_mem.mp hK_convex)
      hpK hqK (by norm_num) (by norm_num) (by norm_num)

  have hinf_le : Metric.infDist x K ≤ dist x ω :=
    Metric.infDist_le_dist_of_mem hωK

  have hdist_lt : dist x ω < Metric.infDist x K := by
    rw [dist_comm]
    have hω_ball : ω ∈ Metric.ball x d := by
      dsimp [ω]
      have hp_ball : p ∈ Metric.closedBall x d := by
        rw [Metric.mem_closedBall, dist_comm]
        exact le_of_eq hpdist.symm
      have hq_ball : q ∈ Metric.closedBall x d := by
        rw [Metric.mem_closedBall, dist_comm]
        exact le_of_eq hqdist
      -- strict convexity of the ball is used here
      exact combo_mem_ball_of_ne hp_ball hq_ball hpq (by norm_num) (by norm_num) (by norm_num)
    simpa [Metric.mem_ball] using hω_ball

  exact not_lt_of_ge hinf_le hdist_lt
