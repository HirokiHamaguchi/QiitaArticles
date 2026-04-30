import Mathlib
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.Between

open Set AffineMap Classical
open scoped Pointwise

namespace Crosscut

variable {n : ℕ}

local notation "L" => EuclideanSpace ℝ (Fin n)

/-- Closed segment xy. -/
def closedSegment (x y: L) : Set (L) :=
  segment ℝ x y

/-- Open segment intv xy. -/
def intv (x y : L) : Set (L) :=
  openSegment ℝ x y

/-- `xy` is a crosscut of `S`. -/
def IsCrosscut (S : Set L) (x y : L) : Prop :=
  x ∈ frontier S ∧
  y ∈ frontier S ∧
  x ≠ y ∧
  openSegment ℝ x y ⊆ interior S

/-- S has no crosscut. -/
def HasNoCrosscut (S : Set L) : Prop :=
  ∀ x y : L, ¬ IsCrosscut S x y

lemma openSegment_self (x : L) : openSegment ℝ x x = {x} := by
  unfold openSegment
  ext z
  constructor
  · rintro ⟨a, b, ha, hb, hab, rfl⟩
    rw [← add_smul]
    rw [hab]
    simp
  · intro h
    subst h
    -- Provide witness: for example, a = 1/2 and b = 1/2
    use 1/2, 1/2
    refine ⟨by norm_num, by norm_num, by norm_num, ?_⟩
    rw [← add_smul]
    norm_num

lemma openSegment_t {x y z : L} (hz : z ∈ openSegment ℝ x y) : ∃ t : ℝ , 0 < t ∧ t < 1 ∧ z = t • x + (1-t) • y := by
  rw [openSegment_eq_image'] at hz
  rcases hz with ⟨θ, hθ, rfl⟩
  exact ⟨1 - θ, by linarith [hθ.2], by linarith [hθ.1], by ext n; simp; ring⟩

lemma openSegment_of_t {x y z : L} {t : ℝ}
    (ht0 : 0 < t) (ht1 : t < 1)
    (hz : z = t • x + (1 - t) • y) :
    z ∈ openSegment ℝ x y := by
  use t, 1 - t
  exact ⟨ht0, by linarith, by ring, hz.symm⟩

lemma lineMap_mem_range_of_mem_segment_left_right
    {x y z u v : L}
    (huz : u ≠ z)
    (hzv : z ≠ v)
    (hz : z ∈ openSegment ℝ x y)
    (hu : u ∈ segment ℝ x z)
    (hv : v ∈ segment ℝ z y) :
    z ∈ range (lineMap u v : ℝ → L) := by
  rw [openSegment_eq_image_lineMap] at hz
  rcases hz with ⟨a, ha, rfl⟩

  rw [segment_eq_image_lineMap] at hu hv
  rcases hu with ⟨b, hb, rfl⟩
  rcases hv with ⟨c, hc, rfl⟩

  have ha0 : 0 < a := ha.1
  have ha1 : a < 1 := ha.2

  have hb_ne_one : b ≠ 1 := by
    intro hb1
    apply huz
    simp [hb1]

  have hb_lt_one : b < 1 :=
    lt_of_le_of_ne hb.2 hb_ne_one

  have hc_ne_zero : c ≠ 0 := by
    intro hc0
    apply hzv
    simp [hc0]

  have hc_pos : 0 < c :=
    lt_of_le_of_ne hc.1 (Ne.symm hc_ne_zero)

  let α : ℝ := b * a
  let β : ℝ := a + c * (1 - a)

  have hα_lt_a : α < a := by
    dsimp [α]
    nlinarith [mul_lt_mul_of_pos_right hb_lt_one ha0]

  have ha_lt_β : a < β := by
    dsimp [β]
    have h1a : 0 < 1 - a := sub_pos.mpr ha1
    have hpos : 0 < c * (1 - a) := mul_pos hc_pos h1a
    linarith

  have hden_pos : 0 < β - α := by
    linarith

  have hden_ne : β - α ≠ 0 :=
    ne_of_gt hden_pos

  refine ⟨(a - α) / (β - α), ?_⟩

  have hu_eq :
      lineMap x (lineMap x y a) b = lineMap x y α := by
    dsimp [α]
    simp [lineMap_apply]
    module

  have hv_eq :
      lineMap (lineMap x y a) y c = lineMap x y β := by
    dsimp [β]
    simp [lineMap_apply]
    module

  rw [hu_eq, hv_eq]

  have hparam :
      (1 - (a - α) / (β - α)) * α +
        ((a - α) / (β - α)) * β = a := by
    field_simp [hden_ne]
    ring

  have hline :
      lineMap (lineMap x y α) (lineMap x y β)
          ((a - α) / (β - α))
        =
      lineMap x y
        ((1 - (a - α) / (β - α)) * α +
          ((a - α) / (β - α)) * β) := by
    simp [lineMap_apply]
    module

  rw [hline, hparam]

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
  have hZInUV : z ∈ range (lineMap u v : ℝ → L) := by
    exact lineMap_mem_range_of_mem_segment_left_right hNegUZ hNegZV hz hu hv

  constructor
  · intro hUV
    subst v
    simp at hZInUV
    exact hNegUZ hZInUV

  · have hSubset := openSegment_subset_union (𝕜 := ℝ) u v hZInUV

    intro w hw
    have hw' : w ∈ insert z (openSegment ℝ u z ∪ openSegment ℝ z v) := hSubset hw

    rcases hw' with rfl | hw'
    · left
      right
      simp
    · rcases hw' with hWInUZ | hWInZV
      · left
        left
        exact hWInUZ
      · right
        exact hWInZV

noncomputable section

open Set Metric
open scoped Topology

example {K : Set L} (hKIsOpen : IsOpen K) {x z : L}
    (hx : x ∈ Kᶜ) (hz : z ∈ interior K) :
    let γ : ℝ → L := fun t => (1 - t) • x + t • z
    γ 0 = x ∧
    γ 1 = z ∧
    x ∉ K ∧
    z ∈ K ∧
    ({t : ℝ | t ∈ Icc (0 : ℝ) 1 ∧ ∀ s ∈ Ioc t 1, γ s ∈ K}).Nonempty := by
  intro γ

  have hγ0 : γ 0 = x := by
    simp [γ]

  have hγ1 : γ 1 = z := by
    simp [γ]

  have hx_not_mem : x ∉ K := by
    simpa using hx

  have hInterior : interior K = K := hKIsOpen.interior_eq

  have hzK : z ∈ K := by
    simpa [hInterior] using hz

  have hγ_cont : Continuous γ := by
    dsimp [γ]
    continuity

  have hK_nhds : K ∈ 𝓝 (γ 1) := by
    simpa [hγ1] using hKIsOpen.mem_nhds hzK

  have hpre : {t : ℝ | γ t ∈ K} ∈ 𝓝 (1 : ℝ) :=
    (hγ_cont.continuousAt (x := 1)).preimage_mem_nhds hK_nhds

  rcases Metric.mem_nhds_iff.mp hpre with ⟨ε, hεpos, hεsub⟩

  let δ : ℝ := min (1 / 2 : ℝ) (ε / 2)

  have hδpos : 0 < δ := by
    dsimp [δ]
    exact lt_min (by norm_num) (by linarith)

  have hδleε : δ ≤ ε := by
    dsimp [δ]
    calc
      min (1 / 2 : ℝ) (ε / 2) ≤ ε / 2 := min_le_right _ _
      _ ≤ ε := by linarith

  have hA_nonempty :
      ({t : ℝ | t ∈ Icc (0 : ℝ) 1 ∧ ∀ s ∈ Ioc t 1, γ s ∈ K}).Nonempty := by
    refine ⟨1 - δ, ?_⟩
    constructor
    · constructor
      · have hδle_half : δ ≤ (1 / 2 : ℝ) := by
          dsimp [δ]
          exact min_le_left _ _
        linarith
      · linarith [hδpos]
    · intro s hs
      apply hεsub
      rw [Metric.mem_ball, Real.dist_eq]
      have hsle : s ≤ 1 := hs.2
      have hst : 1 - δ < s := hs.1
      have habs : |s - 1| = 1 - s := by
        have h_nonpos : s - 1 ≤ 0 := by linarith
        rw [abs_of_nonpos h_nonpos]
        linarith
      rw [habs]
      linarith

  exact ⟨hγ0, hγ1, hx_not_mem, hzK, hA_nonempty⟩

lemma exists_frontier_point_segment_to_interior
    {K : Set L} (hKIsOpen : IsOpen K) {x z : L}
    (hx : x ∈ compl K) (hz : z ∈ interior K) :
    ∃ u : L,
      u ≠ z ∧
      u ∈ frontier K ∧
      u ∈ segment ℝ x z ∧
      openSegment ℝ u z ⊆ interior K := by
  classical

  -- Parameterize the segment from `x` to `z`.
  let γ : ℝ → L := fun t => (1 - t) • x + t • z

  sorry


-- lemma exists_frontier_point_segment_to_interior {K : Set L} (hKIsOpen : IsOpen K) {x z : L} (hx : x ∈ compl K) (hz : z ∈ interior K) : ∃ u : L, u ≠ z ∧  u ∈ frontier K ∧ u ∈ segment ℝ x z ∧ openSegment ℝ u z ⊆ interior K := by
--   classical
--   -- 「z に一番近い frontier point」を取る補題。
--   sorry

lemma thm_4_2 {K : Set L}
    (hKIsOpen : IsOpen K)
    (hK : HasNoCrosscut K) :
    Convex ℝ (compl K) := by
  apply convex_iff_openSegment_subset.mpr
  intro x hXInKc y hYInKc

  -- Show xy ∩ K = ∅ by contradiction
  have hXYCapKIsEmpty : openSegment ℝ x y ∩ K = ∅ := by
    by_contra hNot
    have ⟨z, hz_seg, hz_K⟩ : ∃ z, z ∈ openSegment ℝ x y ∩ K := Set.nonempty_iff_ne_empty.mpr hNot
    clear hNot

    have hz_KInterior : z ∈ interior K := by
      rw [hKIsOpen.interior_eq]
      exact hz_K

    have hNeqXZ : x ≠ z := by
      intro hxz
      subst hxz
      contradiction

    have hNeqYZ : y ≠ z := by
      intro hyz
      subst hyz
      contradiction

    obtain ⟨u, hNeqUZ, hu_frontier, hu_xz, hu_sub⟩ :=
      exists_frontier_point_segment_to_interior hKIsOpen hXInKc hz_KInterior

    obtain ⟨v, hNeqZV, hv_frontier, hv_yz_symm, hv_sub_symm⟩ :=
      exists_frontier_point_segment_to_interior hKIsOpen hYInKc hz_KInterior

    have hv_yz : v ∈ segment ℝ z y := by
      rw [segment_symm]
      exact hv_yz_symm

    have hv_sub : openSegment ℝ z v ⊆ interior K := by
      intro w hw
      apply hv_sub_symm
      rw [openSegment_symm]
      exact hw
    clear hv_sub_symm

    have huv :
        u ≠ v ∧
          openSegment ℝ u v ⊆
            openSegment ℝ u z ∪ {z} ∪ openSegment ℝ z v :=
      openSegment_uv_ordered hNeqUZ hNeqZV.symm hz_seg hu_xz hv_yz

    have hCross : IsCrosscut K u v := by
      refine ⟨hu_frontier, hv_frontier, huv.left, ?_⟩
      intro w hw
      have hw' := huv.right hw
      rcases hw' with hwuz_or_hwz | hwzv
      · rcases hwuz_or_hwz with hwuz | hwz
        · exact hu_sub hwuz
        · rw [hwz]
          exact hz_KInterior
      · exact hv_sub hwzv

    exact hK u v hCross

  -- xy ∩ K = ∅ implies xy ⊆ Kᶜ
  intro z hz_seg hz_K
  have hz_inter : z ∈ openSegment ℝ x y ∩ K := ⟨hz_seg, hz_K⟩
  rw [hXYCapKIsEmpty] at hz_inter
  exact hz_inter
