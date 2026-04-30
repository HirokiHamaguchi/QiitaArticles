# Motzkin's theorem

Def 1.1

topological linear space L

For S \subseteq L,
int S: interior of S
bd S: boundary of S
S^c: complement of S

Def 1.2

x, y \in L
line segment xy = { \alpha x + \beta y : alpha, beta >= 0, alpha + beta = 1 }

Def 1.3

S \subseteq L
S is convex iff for all x, y \in S, line segment xy \subseteq S

Def 1.8

x, y \in L
x \neq y
intv xy = { \alpha x + \beta y : alpha > 0, beta > 0, alpha + beta = 1 }

Def 1.10

S \subseteq L
S is convex body iff S is convex and has nonempty interior

Def 4.1

$S \subseteq L$
x,y \in bd S
closed segment xy is a crosscut of S iff intv xy \subseteq int S

Theorem 4.2

K: open set
If K has no crosscut, then K is the complement of a convex set.

Proof
x, y \in K^c, x \neq y

If xy \cap K \neq \emptyset, exists a,b \in xy \cap bd K, a \neq b, ab is a crosscut of K, contradiction.
    SubProof
        exists z \in xy \cap K = xy \cap int K.
        zx　= { tx + (1-t)z : t \in [0,1] }
        sup { t \in [0,1] : tx + (1-t)z \in bd K } = t_0
        a = t_0 x + (1-t_0) z (\in bd K, a \in [x,z), (a,z) \subseteq int K)
        zy = { ty + (1-t)z : t \in [0,1] }
        sup { t \in [0,1] : ty + (1-t)z \in bd K } = t_1
        b = t_1 y + (1-t_1) z (\in bd K, b \in (z,y], (z,b) \subseteq int K)
        closed segment ab can satisfy the conditions

Thus, xy \cap K = \emptyset
xy \cap K^c = xy

Thus, K^c is convex.

Def 7.5

smooth skip

Def 7.6
convex body S in L is strictly convex
iff
x, y \in S, x \neq y implies intv xy \subseteq int S


Thm 7.8
















hz : z ∈ segment ℝ x y ∩ K
hu_seg : u ∈ openSegment ℝ x z
hv_seg : v ∈ openSegment ℝ z y
heq : u = v
⊢ False











Yes. The key point: use the **last exit from the complement** along the segment, not the first entry into `K`, since `K` need not be convex.

Natural-language proof:

Let

[
\gamma(t) = (1-t)x + tz,\qquad t\in[0,1].
]

Then `γ 0 = x ∉ K` and `γ 1 = z ∈ interior K = K`, since `K` is open.

Consider the set of parameters near `1` for which the tail of the segment stays inside `K`:

[
A={t\in[0,1] : \forall s\in(t,1],\ \gamma(s)\in K}.
]

Because `z ∈ interior K` and `γ` is continuous, `A` is nonempty:

 all `t` sufficiently close to `1` belong to `A`.

Let

[
a = \inf A.
]

Set `u = γ a`.

Then:

1. For every `s ∈ (a,1]`, `γ s ∈ K`, by definition of `a` as the left endpoint of the final interval of membership in `K`.

2. Hence `openSegment ℝ u z ⊆ interior K`, because points of `openSegment ℝ u z` are exactly `γ s` with `s ∈ (a,1)`, and `K = interior K`.

3. We have `u ∈ closure K`, since `γ s ∈ K` for `s > a` and `γ s → γ a`.

4. We cannot have `u ∈ interior K`. If `u ∈ interior K`, then by openness and continuity of `γ`, parameters slightly less than `a` would also have their tails inside `K`, contradicting minimality of `a`.

So

[
u \in \overline K \setminus \operatorname{interior} K
= \operatorname{frontier} K.
]

Also `u ∈ segment ℝ x z` because `a ∈ [0,1]`. Finally, `u ≠ z`, since otherwise `z ∈ frontier K`, contradicting `z ∈ interior K`.

So the lemma is true. A Lean proof should formalize this via the connected component of `γ ⁻¹' K` containing `1`; that avoids manually proving the infimum/interval facts for `A`.
