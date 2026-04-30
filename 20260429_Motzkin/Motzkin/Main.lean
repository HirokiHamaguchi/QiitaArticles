import Mathlib
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.Between

open Set AffineMap Classical
open Metric
open scoped Pointwise
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

private def segmentPath (x z : L) : ℝ → L :=
  fun t => (1 - t) • x + t • z

private def tailSet (K : Set L) (x z : L) : Set ℝ :=
  {t : ℝ | t ∈ Icc (0 : ℝ) 1 ∧ ∀ s ∈ Ioc t 1, segmentPath x z s ∈ K}

private lemma continuous_segmentPath (x z : L) :
    Continuous (segmentPath x z) := by
  unfold segmentPath
  continuity

private lemma exists_mem_tailSet_lt_one
    {K : Set L} (hK : IsOpen K) {x z : L}
    (hzK : z ∈ K) :
    ∃ t ∈ tailSet K x z, t < 1 := by
  let γ := segmentPath x z

  have hpre : {t : ℝ | γ t ∈ K} ∈ 𝓝 (1 : ℝ) := by
    have hz : γ 1 ∈ K := by
      simpa [γ, segmentPath] using hzK
    exact ((continuous_segmentPath x z).continuousAt (x := 1)).preimage_mem_nhds
      (hK.mem_nhds hz)

  rcases Metric.mem_nhds_iff.mp hpre with ⟨ε, hεpos, hεsub⟩

  let δ : ℝ := min (1 / 2 : ℝ) (ε / 2)

  have hδpos : 0 < δ := by
    dsimp [δ]
    exact lt_min (by norm_num) (by linarith)

  have hδle_half : δ ≤ (1 / 2 : ℝ) := by
    dsimp [δ]
    exact min_le_left _ _

  have hδleε : δ ≤ ε := by
    dsimp [δ]
    calc
      min (1 / 2 : ℝ) (ε / 2) ≤ ε / 2 := min_le_right _ _
      _ ≤ ε := by linarith

  refine ⟨1 - δ, ?_, by linarith [hδpos]⟩
  constructor
  · constructor <;> linarith [hδpos, hδle_half]
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

lemma existence_of_A
    {K : Set L} (hK : IsOpen K) {x z : L}
    (hx : x ∈ Kᶜ) (hz : z ∈ interior K) :
    let γ : ℝ → L := fun t => (1 - t) • x + t • z
    γ 0 = x ∧
    γ 1 = z ∧
    x ∉ K ∧
    z ∈ K ∧
    ({t : ℝ | t ∈ Icc (0 : ℝ) 1 ∧
      ∀ s ∈ Ioc t 1, γ s ∈ K}).Nonempty := by
  intro γ

  have hzK : z ∈ K := by
    simpa [hK.interior_eq] using hz

  rcases exists_mem_tailSet_lt_one hK hzK with ⟨t, ht, -⟩

  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simp [γ]
  · simp [γ]
  · simpa using hx
  · exact hzK
  · exact ⟨t, by simpa [tailSet, segmentPath, γ] using ht⟩

lemma exists_frontier_point_segment_to_interior
    {K : Set L} (hK : IsOpen K) {x z : L}
    (hx : x ∈ compl K) (hz : z ∈ interior K) :
    ∃ u : L,
      u ≠ z ∧
      u ∈ frontier K ∧
      u ∈ segment ℝ x z ∧
      openSegment ℝ u z ⊆ interior K := by
  let γ := segmentPath x z
  let A : Set ℝ := tailSet K x z

  have hxK : x ∉ K := by
    simpa using hx

  have hKint : interior K = K :=
    hK.interior_eq

  have hzK : z ∈ K := by
    simpa [hKint] using hz

  have hγ_cont : Continuous γ :=
    continuous_segmentPath x z

  rcases exists_mem_tailSet_lt_one hK (x := x) hzK with
    ⟨t₀, ht₀A, ht₀_lt_one⟩

  have hAne : A.Nonempty :=
    ⟨t₀, ht₀A⟩

  have hAlt : ∃ t ∈ A, t < 1 :=
    ⟨t₀, ht₀A, ht₀_lt_one⟩

  let a : ℝ := sInf A
  let u : L := γ a

  have hAbdd : BddBelow A := by
    refine ⟨0, ?_⟩
    intro t ht
    exact ht.1.1

  have haIcc : a ∈ Icc (0 : ℝ) 1 := by
    constructor
    · exact le_csInf hAne fun t ht => ht.1.1
    · rcases hAlt with ⟨t, htA, htlt⟩
      exact le_trans (csInf_le hAbdd htA) (le_of_lt htlt)

  have ha_lt_one : a < 1 := by
    rcases hAlt with ⟨t, htA, htlt⟩
    exact lt_of_le_of_lt (csInf_le hAbdd htA) htlt

  have htail : ∀ s ∈ Ioc a 1, γ s ∈ K := by
    intro s hs

    have hex : ∃ t ∈ A, t < s := by
      by_contra hnone
      push Not at hnone

      have hsle : s ≤ a := by
        refine le_csInf hAne ?_
        intro t ht
        exact hnone t ht

      linarith [hs.1]

    rcases hex with ⟨t, htA, hts⟩
    exact htA.2 s ⟨hts, hs.2⟩

  have hu_closure : u ∈ closure K := by
    rw [mem_closure_iff_nhds]
    intro V hV

    have hpre : γ ⁻¹' V ∈ 𝓝 a := by
      simpa [u] using hγ_cont.continuousAt hV

    rcases Metric.mem_nhds_iff.mp hpre with ⟨ε, hεpos, hεsub⟩

    let δ : ℝ := min (ε / 2) ((1 - a) / 2)
    let t : ℝ := a + δ

    have hδpos : 0 < δ := by
      dsimp [δ]
      exact lt_min (by linarith) (by linarith [ha_lt_one])

    have hat : a < t := by
      dsimp [t]
      linarith

    have ht1 : t < 1 := by
      have hδle : δ ≤ (1 - a) / 2 := by
        dsimp [δ]
        exact min_le_right _ _
      dsimp [t]
      linarith

    have ht_ball : t ∈ Metric.ball a ε := by
      rw [Metric.mem_ball, Real.dist_eq]

      have ht_sub : t - a = δ := by
        dsimp [t]
        ring

      rw [ht_sub, abs_of_nonneg (le_of_lt hδpos)]

      have hδle : δ ≤ ε / 2 := by
        dsimp [δ]
        exact min_le_left _ _

      linarith

    have htV : γ t ∈ V :=
      hεsub ht_ball

    have hsInf_lt_t : sInf A < t := by
      simpa [a] using hat

    rcases (csInf_lt_iff hAbdd hAne).1 hsInf_lt_t with
      ⟨b, hbA, hbt⟩

    have htK : γ t ∈ K :=
      hbA.2 t ⟨hbt, le_of_lt ht1⟩

    exact ⟨γ t, htV, htK⟩

  have hu_not_int : u ∉ interior K := by
    intro hu_int

    have huK : u ∈ K := by
      simpa [hKint] using hu_int

    have hprea : {t : ℝ | γ t ∈ K} ∈ 𝓝 a := by
      have hK_nhds_u : K ∈ 𝓝 (γ a) := by
        simpa [u] using hK.mem_nhds huK
      exact hγ_cont.continuousAt.preimage_mem_nhds hK_nhds_u

    rcases Metric.mem_nhds_iff.mp hprea with ⟨ε, hεpos, hεsub⟩

    have ha_pos : 0 < a := by
      by_contra hapos

      have ha0 : a = 0 :=
        le_antisymm (le_of_not_gt hapos) haIcc.1

      have hx_in_K : x ∈ K := by
        simpa [u, γ, segmentPath, ha0] using huK

      exact hxK hx_in_K

    let δ : ℝ := min (a / 2) (ε / 2)
    let b : ℝ := a - δ

    have hδpos : 0 < δ := by
      dsimp [δ]
      exact lt_min (by linarith) (by linarith)

    have hδle_a : δ ≤ a := by
      dsimp [δ]
      calc
        min (a / 2) (ε / 2) ≤ a / 2 := min_le_left _ _
        _ ≤ a := by linarith

    have hδleε : δ ≤ ε := by
      dsimp [δ]
      calc
        min (a / 2) (ε / 2) ≤ ε / 2 := min_le_right _ _
        _ ≤ ε := by linarith

    have hb_lt_a : b < a := by
      dsimp [b]
      linarith [hδpos]

    have hbA : b ∈ A := by
      constructor
      · constructor
        · dsimp [b]
          linarith [haIcc.1, hδle_a]
        · dsimp [b]
          linarith [haIcc.2, hδpos]
      · intro s hs
        by_cases hsa : s ≤ a
        · apply hεsub
          rw [Metric.mem_ball, Real.dist_eq]

          have habs : |s - a| = a - s := by
            have h_nonpos : s - a ≤ 0 := by linarith
            rw [abs_of_nonpos h_nonpos]
            linarith

          rw [habs]

          have h_as_lt_delta : a - s < δ := by
            dsimp [b] at hs
            linarith [hs.1]

          linarith [h_as_lt_delta, hδleε]
        · exact htail s ⟨lt_of_not_ge hsa, hs.2⟩

    have ha_le_b : a ≤ b :=
      csInf_le hAbdd hbA

    linarith [hb_lt_a, ha_le_b]

  have hu_ne_z : u ≠ z := by
    intro huz
    exact hu_not_int (by
      simpa [huz] using hz)

  have hu_frontier : u ∈ frontier K := by
    rw [frontier]
    exact ⟨hu_closure, hu_not_int⟩

  have hu_segment : u ∈ segment ℝ x z := by
    dsimp [u, γ, segmentPath]
    refine ⟨1 - a, a, ?_, ?_, ?_, rfl⟩
    · linarith
    · exact haIcc.1
    · ring

  have hopen : openSegment ℝ u z ⊆ interior K := by
    intro w hw

    rw [openSegment_eq_image'] at hw
    rcases hw with ⟨t, ⟨ht0, ht1⟩, rfl⟩
    simp

    let s : ℝ := (1 - t) * a + t * 1

    have hs : s ∈ Ioc a 1 := by
      constructor
      · dsimp [s]
        nlinarith [ht0, ht1, ha_lt_one]
      · dsimp [s]
        nlinarith [ht0, ht1, haIcc.2]

    have hγs : (1 - t) • u + t • z = γ s := by
      ext i
      simp [u, γ, segmentPath, s]
      ring

    have hγsInt : γ s ∈ interior K := by
      rw [hKint]
      exact htail s hs

    have h_eq : u + t • (z - u) = (1 - t) • u + t • z := by
      rw [smul_sub, sub_smul, one_smul]
      abel

    rw [h_eq, hγs]
    exact hγsInt

  exact ⟨u, hu_ne_z, hu_frontier, hu_segment, hopen⟩


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

  have hb_lt_one : b < 1 := by
    refine lt_of_le_of_ne hb.2 ?_
    intro hb1
    apply huz
    simp [hb1]

  have hc_pos : 0 < c := by
    refine lt_of_le_of_ne hc.1 ?_
    intro hc0
    apply hzv
    subst hc0
    simp

  let α : ℝ := b * a
  let β : ℝ := a + c * (1 - a)

  have hα_lt_a : α < a := by
    dsimp [α]
    nlinarith [mul_lt_mul_of_pos_right hb_lt_one ha0]

  have ha_lt_β : a < β := by
    dsimp [β]
    nlinarith [hc_pos, ha1]

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
  have hZInUV : z ∈ range (lineMap u v : ℝ → L) :=
    lineMap_mem_range_of_mem_segment_left_right hNegUZ hNegZV hz hu hv

  constructor
  · intro hUV
    subst v
    simp at hZInUV
    exact hNegUZ hZInUV

  · have hSubset := openSegment_subset_union u v hZInUV
    intro w hw
    rcases hSubset hw with rfl | hWInUZ | hWInZV
    · simp
    · tauto
    · tauto

lemma thm_4_2 {K : Set L}
    (hKIsOpen : IsOpen K)
    (hK : HasNoCrosscut K) :
    Convex ℝ (compl K) := by
  apply convex_iff_openSegment_subset.mpr
  intro x hx y hy z hz_seg hzK

  have hz_int : z ∈ interior K := by
    rw [hKIsOpen.interior_eq]
    exact hzK

  obtain ⟨u, hNeqUZ, hu_frontier, hu_xz, hu_sub⟩ :=
    exists_frontier_point_segment_to_interior hKIsOpen hx hz_int

  obtain ⟨v, hNeqZV, hv_frontier, hv_yz_symm, hv_sub_symm⟩ :=
    exists_frontier_point_segment_to_interior hKIsOpen hy hz_int

  have hv_yz : v ∈ segment ℝ z y := by
    rw [segment_symm]
    exact hv_yz_symm

  obtain ⟨hNeqUV, hOpenSegUVDecomp⟩ := openSegment_uv_ordered hNeqUZ hNeqZV.symm hz_seg hu_xz hv_yz

  have hCross : IsCrosscut K u v := by
    have hOpenUVInIntK : openSegment ℝ u v ⊆ interior K := by
      intro w hw
      rcases hOpenSegUVDecomp hw with (hwuz | hwz) | hwzv
      · exact hu_sub hwuz
      · rw [hwz]
        exact hz_int
      · apply hv_sub_symm
        rw [openSegment_symm]
        exact hwzv

    exact ⟨hu_frontier, hv_frontier, hNeqUV, hOpenUVInIntK⟩

  exact hK u v hCross
