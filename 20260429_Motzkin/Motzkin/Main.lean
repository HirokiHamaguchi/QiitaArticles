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

def segmentPath (x z : L) : ℝ → L :=
  fun t => (1 - t) • x + t • z

def tailSet (K : Set L) (x z : L) : Set ℝ :=
  {t : ℝ | t ∈ Icc (0 : ℝ) 1 ∧ ∀ s ∈ Ioc t 1, segmentPath x z s ∈ K}

lemma continuous_segmentPath (x z : L) :
    Continuous (segmentPath x z) := by
  unfold segmentPath
  continuity

lemma exists_mem_tailSet_lt_one
    {K : Set L} (hK : IsOpen K) {x z : L} (hzK : z ∈ K) :
    ∃ t ∈ tailSet K x z, t < 1 := by
  let γ := segmentPath x z

  have hpre : {t : ℝ | γ t ∈ K} ∈ 𝓝 (1 : ℝ) := by
    have hz : γ 1 ∈ K := by
      simpa [γ, segmentPath] using hzK
    exact ((continuous_segmentPath x z).continuousAt (x := 1)).preimage_mem_nhds
      (hK.mem_nhds hz)

  rcases Metric.mem_nhds_iff.mp hpre with ⟨ε, hεpos, hεsub⟩

  let δ : ℝ := min (1 / 2) ε

  have hδpos : 0 < δ := by
    exact lt_min (by norm_num) (by linarith)

  have hδle_half : δ ≤ 1 / 2 := by
    exact min_le_left _ _

  refine ⟨1 - δ, ?_, by linarith [hδpos]⟩
  constructor
  · constructor <;> linarith [hδpos, hδle_half]
  · intro s ⟨hst, hsle⟩
    apply hεsub
    rw [Metric.mem_ball, Real.dist_eq]
    have h_nonpos : s - 1 ≤ 0 := by linarith
    rw [abs_of_nonpos h_nonpos]
    have hδleε : δ ≤ ε := by exact min_le_right _ _
    linarith

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

  have hxK : x ∉ K := by simpa using hx
  have hKint : interior K = K := hK.interior_eq
  have hzK : z ∈ K := by simpa [hKint] using hz
  have hγ_cont : Continuous γ := continuous_segmentPath x z

  rcases exists_mem_tailSet_lt_one hK (x := x) hzK with ⟨t₀, ht₀A, ht₀_lt_one⟩
  clear hzK

  have hAne : A.Nonempty := ⟨t₀, ht₀A⟩

  let a : ℝ := sInf A
  let u : L := γ a

  have hAbdd : BddBelow A := by
    refine ⟨0, ?_⟩
    intro t ht
    exact ht.1.1

  have haIco : a ∈ Ico (0 : ℝ) 1 := by
    constructor
    · exact le_csInf hAne fun t ht => ht.1.1
    · exact lt_of_le_of_lt (csInf_le hAbdd ht₀A) ht₀_lt_one

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
      exact lt_min (by linarith) (by linarith [haIco.2])

    have ht1 : t < 1 := by
      have hδle : δ ≤ (1 - a) / 2 := by
        exact min_le_right _ _
      dsimp [t]
      linarith

    have ht_ball : t ∈ Metric.ball a ε := by
      rw [Metric.mem_ball, Real.dist_eq]
      have ht_sub : t - a = δ := by ring
      rw [ht_sub, abs_of_nonneg (le_of_lt hδpos)]
      have hδle : δ ≤ ε / 2 := by exact min_le_left _ _
      linarith

    have hat : a < t := by linarith
    have hsInf_lt_t : sInf A < t := by simpa [a] using hat

    rcases (csInf_lt_iff hAbdd hAne).1 hsInf_lt_t with ⟨b, hbA, hbt⟩

    exact ⟨γ t, hεsub ht_ball, hbA.2 t ⟨hbt, le_of_lt ht1⟩⟩

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
        le_antisymm (le_of_not_gt hapos) haIco.1

      have hx_in_K : x ∈ K := by
        simpa [u, γ, segmentPath, ha0] using huK

      exact hxK hx_in_K

    let δ : ℝ := min a ε
    let b : ℝ := a - δ

    have hδpos : 0 < δ := by exact lt_min (by linarith) hεpos
    have hδle_a : δ ≤ a := by exact min_le_left _ _
    have hδleε : δ ≤ ε := by exact min_le_right _ _
    have hb_lt_a : b < a := by linarith [hδpos]

    have hbA : b ∈ A := by
      constructor
      · constructor
        · linarith [haIco.1, hδle_a]
        · linarith [haIco.2, hδpos]
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
    exact hu_not_int (by simpa [huz] using hz)

  have hu_frontier : u ∈ frontier K := by
    rw [frontier]
    exact ⟨hu_closure, hu_not_int⟩

  have hu_segment : u ∈ segment ℝ x z := by
    dsimp [u, γ, segmentPath]
    refine ⟨1 - a, a, by linarith [haIco.2], by exact haIco.1, by ring, rfl⟩

  have hopen : openSegment ℝ u z ⊆ interior K := by
    intro w hw

    rw [openSegment_eq_image'] at hw
    rcases hw with ⟨t, ⟨ht0, ht1⟩, rfl⟩
    simp

    let s : ℝ := (1 - t) * a + t * 1

    have hs : s ∈ Ioc a 1 := by
      constructor <;> nlinarith [ht0, ht1, haIco.2]

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
  rw [segment_eq_image_lineMap] at hu hv

  rcases hz with ⟨a, ⟨ha0, ha1⟩, rfl⟩
  rcases hu with ⟨b, ⟨hb0, hb1⟩, rfl⟩
  rcases hv with ⟨c, ⟨hc0, hc1⟩, rfl⟩

  let α : ℝ := b * a
  let β : ℝ := a + c * (1 - a)

  refine ⟨(a - α) / (β - α), ?_⟩

  have hden_ne : β - α ≠ 0 := by
    have hb_lt_one : b < 1 := by
      exact lt_of_le_of_ne hb1 fun hb_eq => huz (by simp [hb_eq])

    have hc_pos : 0 < c := by
      exact lt_of_le_of_ne hc0 fun hc_eq => hzv (by subst hc_eq; simp)

    exact ne_of_gt <| by
      dsimp [α, β]
      nlinarith

  calc
    lineMap
        (lineMap x (lineMap x y a) b)
        (lineMap (lineMap x y a) y c)
        ((a - α) / (β - α))
        =
        lineMap
          (lineMap x y α)
          (lineMap x y β)
          ((a - α) / (β - α)) := by
          dsimp [α]
          simp [lineMap_apply]
          module
    _ =
        lineMap x y
          ((1 - (a - α) / (β - α)) * α
            + ((a - α) / (β - α)) * β) := by
          simp [lineMap_apply]
          module
    _ = lineMap x y a := by
          congr 1
          field_simp [hden_ne]
          ring

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

  · intro w hw
    have hSubset := openSegment_subset_union u v hZInUV
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
