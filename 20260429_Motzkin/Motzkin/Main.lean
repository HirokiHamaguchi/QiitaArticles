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
  rcases openSegment_t hz_uv with ⟨A, hA0, hA1, hz_eq⟩
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

lemma exists_frontier_point_openSegment_to_interior
    {K : Set L} (hKIsOpen : IsOpen K)
    {a z : L}
    (ha : a ∈ compl K)
    (hz : z ∈ interior K) :
    ∃ u : L,
      u ∈ frontier K ∧
      u ∈ openSegment ℝ a z ∧
      openSegment ℝ u z ⊆ interior K := by
  sorry

lemma thm_4_2 {K : Set L}
    (hKIsOpen : IsOpen K)
    (hK : HasNoCrosscut K) :
    Convex ℝ (compl K) := by
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

    have hz_seg : z ∈ openSegment ℝ x y := hz_seg_K.1
    have hz_K : z ∈ K := hz_seg_K.2

    have hz_KInterior : z ∈ interior K := by
      rw [hKIsOpen.interior_eq]
      exact hz_K

    obtain ⟨u, hu_frontier, hu_xz, hu_sub⟩ :=
      exists_frontier_point_openSegment_to_interior hKIsOpen hXInKc hz_KInterior

    obtain ⟨v, hv_frontier, hv_yz, hv_sub_yz⟩ :=
      exists_frontier_point_openSegment_to_interior hKIsOpen hYInKc hz_KInterior

    have hv_zy : v ∈ openSegment ℝ z y := by
      rw [openSegment_symm]
      exact hv_yz

    have hv_sub : openSegment ℝ z v ⊆ interior K := by
      intro w hw
      apply hv_sub_yz
      rw [openSegment_symm]
      exact hw

    have huv :
        u ≠ v ∧
          openSegment ℝ u v ⊆
            openSegment ℝ u z ∪ {z} ∪ openSegment ℝ z v :=
      openSegment_uv_ordered hxy hz_seg hu_xz hv_zy

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
