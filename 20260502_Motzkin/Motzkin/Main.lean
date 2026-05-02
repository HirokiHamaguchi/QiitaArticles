import Motzkin.Crosscut

variable {n : ℕ}

local notation "L" => EuclideanSpace ℝ (Fin n)

/-- `xy` is a crosscut of `K`. -/
def IsCrosscut (K : Set L) (x y : L) : Prop :=
  x ∈ frontier K ∧ -- frontier K is the boundary of K
  y ∈ frontier K ∧
  x ≠ y ∧
  openSegment ℝ x y ⊆ interior K

/-- `K` has no crosscuts. -/
def HasNoCrosscut (K : Set L) : Prop :=
  ∀ x y : L, ¬ IsCrosscut K x y

/-- Lemma asserting the existence of a frontier point `u`. -/
lemma exists_frontier_point_segment_to_interior
    {K : Set L} (hK : IsOpen K) {x z : L}
    (hx : x ∈ compl K) (hz : z ∈ interior K) :
    ∃ u : L,
      u ≠ z ∧
      u ∈ frontier K ∧
      u ∈ segment ℝ x z ∧
      openSegment ℝ u z ⊆ interior K := by
  -- The proof is provided in `Crosscut.lean`.
  exact _exists_frontier_point_segment_to_interior hK hx hz

/--
Lemma asserting the intv uv ⊆ intv uz ∪ {z} ∪ intv zv.
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

  -- By the definition of convexity, we need to show that
  -- `z ∈ Kᶜ` when
  -- `x` : a point in `L`
  -- `hx` : x ∈ Kᶜ
  -- `y` : a point in `L`
  -- `hy` : y ∈ Kᶜ
  -- `z` : a point in `L`
  -- `hz_seg` : z ∈ openSegment ℝ x y
  apply convex_iff_openSegment_subset.mpr
  intro x hx y hy z hz_seg

  -- By the definition of the complement,
  -- we have to show `False` when `hz` : z ∈ K.
  by_contra hzK
  simp at hzK

  -- Since `K` is open, we have `z ∈ interior K`.
  have hz_int : z ∈ interior K := by
    simpa [hKIsOpen.interior_eq] using hzK

  -- Obtain `u` and `v` in the frontier of `K` such that
  -- `u` : L
  -- `hNeqUZ` : u ≠ z
  -- `hu_frontier` : u ∈ frontier K
  -- `hu_xz` : u ∈ segment ℝ x z
  -- `hu_sub` : openSegment ℝ u z ⊆ interior K
  obtain ⟨u, hNeqUZ, hu_frontier, hu_xz, hu_sub⟩ :=
    exists_frontier_point_segment_to_interior hKIsOpen hx hz_int

  -- Similarly, we can obtain `v`.
  obtain ⟨v, hNeqZV, hv_frontier, hv_yz_symm, hv_sub_symm⟩ :=
    exists_frontier_point_segment_to_interior hKIsOpen hy hz_int

  -- Convert `v ∈ segment ℝ y z` to `v ∈ segment ℝ z y`
  have hv_yz : v ∈ segment ℝ z y := by
    simpa [segment_symm] using hv_yz_symm

  -- From the above, we can derive that
  -- `hNeqUV` : u ≠ v
  -- `hOpenSegUVDecomp` : openSegment ℝ u v ⊆ openSegment ℝ u z ∪ {z} ∪ openSegment ℝ z v
  obtain ⟨hNeqUV, hOpenSegUVDecomp⟩ := openSegment_uv_ordered hNeqUZ hNeqZV.symm hz_seg hu_xz hv_yz

  -- Finally, we show the contradiction by showing
  -- `uv` is a crosscut of `K`, which contradicts the assumption `hK`.
  -- Now, the goal changes to show that `openSegment ℝ u v ⊆ interior K`,
  -- which is the last condition for `uv` to be a crosscut of `K`.
  refine hK u v ⟨hu_frontier, hv_frontier, hNeqUV, ?_⟩

  -- We show it by saying that `w ∈ openSegment ℝ u v` implies `w ∈ interior K`.
  intro w hw
  -- By the decomposition of `openSegment ℝ u v`, we have three cases:
  rcases hOpenSegUVDecomp hw with (hwuz | hwz) | hwzv
  · -- w ∈ openSegment ℝ u z
    exact hu_sub hwuz
  · -- w ∈ {z}
    rw [hwz]
    exact hz_int
  · -- w ∈ openSegment ℝ z v
    apply hv_sub_symm
    rw [openSegment_symm]
    exact hwzv
