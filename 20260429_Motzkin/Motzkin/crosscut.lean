import Motzkin.Basic

import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.Between

open Set AffineMap Metric
open scoped Topology

variable {n : ℕ}

local notation "L" => EuclideanSpace ℝ (Fin n)

/-- `xy` is a crosscut of `S`. -/
def IsCrosscut (S : Set L) (x y : L) : Prop :=
  x ∈ frontier S ∧
  y ∈ frontier S ∧
  x ≠ y ∧
  openSegment ℝ x y ⊆ interior S

/-- `S` has no crosscut. -/
def HasNoCrosscut (S : Set L) : Prop :=
  ∀ x y : L, ¬ IsCrosscut S x y

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
Main theorem: if an open set `K` has no crosscut,
              then its complement is convex.
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
