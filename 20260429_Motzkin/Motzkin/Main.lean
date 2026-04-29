import Mathlib
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.Between

open Set
open Classical
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

lemma openSegment_split_at_point
    {u z v w : L}
    (hz : z ∈ openSegment ℝ u v)
    (hw : w ∈ openSegment ℝ u v) :
    w ∈ openSegment ℝ u z ∪ {z} ∪ openSegment ℝ z v := by
  rcases openSegment_t hz with ⟨A, hA0, hA1, hz_eq⟩
  rcases openSegment_t hw with ⟨c, hc0, hc1, hw_eq⟩

  by_cases hcA : c = A
  · subst hcA
    rw [← hz_eq] at hw_eq
    subst hw_eq
    simp

  by_cases hAc : A < c
  · left
    left
    let μ : ℝ := (c - A) / (1 - A)

    have hμ0 : 0 < μ := by
      subst μ
      exact div_pos (sub_pos.mpr hAc) (sub_pos.mpr hA1)

    have hμ1 : μ < 1 := by
      subst μ
      have hPos : 0 < 1 - A := by linarith
      rw [div_lt_one hPos]
      linarith

    apply openSegment_of_t hμ0 hμ1
    rw [hw_eq, hz_eq]
    subst μ
    have hAne : 1 - A ≠ 0 := (sub_pos.mpr hA1).ne'
    symm
    calc
      ((c - A) / (1 - A)) • u
          + (1 - (c - A) / (1 - A)) •
              (A • u + (1 - A) • v)
        = (((c - A) / (1 - A))
            + (1 - (c - A) / (1 - A)) * A) • u
            + ((1 - (c - A) / (1 - A)) * (1 - A)) • v := by
              module
      _ = c • u + (1 - c) • v := by
              ext i
              simp
              field_simp [hAne]
              ring

  · right
    have hcA_lt : c < A := lt_of_le_of_ne (le_of_not_gt hAc) hcA

    let μ : ℝ := c / A

    have hμ0 : 0 < μ := by
      subst μ
      exact div_pos hc0 hA0

    have hμ1 : μ < 1 := by
      subst μ
      rw [div_lt_one hA0]
      exact hcA_lt

    apply openSegment_of_t hμ0 hμ1
    rw [hw_eq, hz_eq]
    subst μ
    have hAne : A ≠ 0 := ne_of_gt hA0
    symm
    calc
      (c / A) • (A • u + (1 - A) • v)
          + (1 - c / A) • v
        = ((c / A) * A) • u
            + (((c / A) * (1 - A)) + (1 - c / A)) • v := by
              module
      _ = c • u + (1 - c) • v := by
              ext i
              simp
              field_simp [hAne]
              ring

lemma openSegment_uv_ordered
    {x y z u v : L}
    (hNegXY : x ≠ y)
    (hz : z ∈ openSegment ℝ x y)
    (hu : u ∈ openSegment ℝ x z)
    (hv : v ∈ openSegment ℝ z y) :
    u ≠ v ∧
      openSegment ℝ u v ⊆
        openSegment ℝ u z ∪ {z} ∪ openSegment ℝ z v := by
  rcases openSegment_t hz with ⟨t, ht0, ht1, hz_xy⟩
  rcases openSegment_t hu with ⟨s, hs0, hs1, hu_xz⟩
  rcases openSegment_t hv with ⟨r, hr0, hr1, hv_zy⟩
  clear hz hu hv

  let α : ℝ := s + (1 - s) * t
  let β : ℝ := r * t

  have hu_xy : u = α • x + (1 - α) • y := by
    subst α
    rw [hu_xz, hz_xy]
    ext i
    simp
    ring
  clear hu_xz

  have hv_xy : v = β • x + (1 - β) • y := by
    subst β
    rw [hv_zy, hz_xy]
    ext i
    simp
    ring
  clear hv_zy

  have hβ_lt_t : β < t := by
    subst β
    nlinarith [ht0, ht1, hr0, hr1]

  have ht_lt_α : t < α := by
    subst α
    nlinarith [ht0, ht1, hs0, hs1]

  have hβ_lt_α : β < α := by
    linarith

  have huv_ne : u ≠ v := by
    intro huv
    have hProd : (α - β) • (x - y) = (0 : L) := by
      calc
        (α - β) • (x - y)
            = (α • x + (1 - α) • y)
                - (β • x + (1 - β) • y) := by module
        _ = 0 := by rw [← hu_xy, ← hv_xy, huv, sub_self]
    have hαβ : α - β ≠ 0 := by linarith
    have hxy : x - y = (0 : L) := by simpa [smul_eq_zero, hαβ] using hProd
    apply hNegXY
    ext i
    have hi := congrArg (fun p : L => p i) hxy
    simp at hi
    linarith

  refine ⟨huv_ne, ?_⟩
  clear hNegXY hs0 hs1 hr0 hr1

  have hz_uv : z ∈ openSegment ℝ u v := by
    let A : ℝ := (t - β) / (α - β)

    have hA0 : 0 < A := by
      subst A
      exact div_pos (sub_pos.mpr hβ_lt_t) (sub_pos.mpr hβ_lt_α)

    have hA1 : A < 1 := by
      subst A
      have hPos : 0 < α - β := by linarith
      rw [div_lt_one hPos]
      linarith

    apply openSegment_of_t hA0 hA1
    rw [hu_xy, hv_xy, hz_xy]
    subst A
    ext i
    simp
    field_simp [sub_ne_zero.mpr (ne_of_gt hβ_lt_α)]
    ring

  intro w hw
  exact openSegment_split_at_point hz_uv hw

lemma thm_4_2 {K : Set L} (hKIsOpen : IsOpen K) (hK : HasNoCrosscut K) : Convex ℝ (compl K) := by
  -- We show the convexity by proving xy ⊆ Kᶜ
  apply convex_iff_openSegment_subset.mpr
  intro x hXInKc y hYInKc

  rcases eq_or_ne x y with rfl | hxy

  · rw [openSegment_self]
    intro x xInX
    simp at xInX
    subst xInX
    exact hXInKc

  -- Show xy ∩ K = ∅ by contradiction
  have hXYCapKIsEmpty : openSegment ℝ x y ∩ K = ∅ := by
    by_contra hNot

    have ⟨z, hz_seg_K⟩ : ∃ z, z ∈ openSegment ℝ x y ∩ K := Set.nonempty_iff_ne_empty.mpr hNot

    have hz_KInterior : z ∈ interior K := by
      apply Set.inter_subset_right at hz_seg_K
      rw [hKIsOpen.interior_eq]
      exact hz_seg_K

    have hu: ∃ u: L, u ∈ frontier K ∧ u ∈ openSegment ℝ x z ∧ openSegment ℝ u z ⊆ interior K := by
      sorry
    have hv: ∃ v: L, v ∈ frontier K ∧ v ∈ openSegment ℝ z y ∧ openSegment ℝ z v ⊆ interior K := by
      sorry
    obtain ⟨u, hu_front, hu_seg, hu_int⟩ := hu
    obtain ⟨v, hv_front, hv_seg, hv_int⟩ := hv

    have hOrder :=
      openSegment_uv_ordered hxy hz_seg_K.1 hu_seg hv_seg

    rcases hOrder with ⟨huv_ne, huv_subset⟩

    have huv_crosscut : IsCrosscut K u v := by
      refine ⟨hu_front, hv_front, huv_ne, ?_⟩
      intro w hw
      have hw' := huv_subset hw
      rcases hw' with hwuz_or_hwz | hwzv
      · rcases hwuz_or_hwz with hwuz | hwz
        · exact hu_int hwuz
        · rw [hwz]
          exact hz_KInterior
      · exact hv_int hwzv

    exact hK u v huv_crosscut

  -- xy ∩ K = ∅ implies xy ⊆ Kᶜ
  replace hXYAndKIsDisjoint := disjoint_iff_inter_eq_empty.mpr hXYCapKIsEmpty
  rw [Set.subset_compl_iff_disjoint_right]
  exact hXYAndKIsDisjoint
