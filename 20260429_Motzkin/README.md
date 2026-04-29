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

If xy \cap K \neq \emptyset,
exists a,b \in xy \cap bd K, a \neq b, ab is a crosscut of K, contradiction.
    SubProof
        exists z \in xy \cap K.
        zx　= { tx + (1-t)z : t \in [0,1] }
        sup { t \in [0,1] : tx + (1-t)z \in bd K } = t_0
        a = t_0 x + (1-t_0) z
        zy = { ty + (1-t)z : t \in [0,1] }
        sup { t \in [0,1] : ty + (1-t)z \in bd K } = t_1
        b = t_1 y + (1-t_1) z
        ab can satisfy the conditions

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
