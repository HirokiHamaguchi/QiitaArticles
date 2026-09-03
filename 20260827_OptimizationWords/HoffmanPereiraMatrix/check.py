import cvxpy as cp
import numpy as np

H = np.array([
    [ 1,-1, 1, 0, 0, 1,-1],
    [-1, 1,-1, 1, 0, 0, 1],
    [ 1,-1, 1,-1, 1, 0, 0],
    [ 0, 1,-1, 1,-1, 1, 0],
    [ 0, 0, 1,-1, 1,-1, 1],
    [ 1, 0, 0, 1,-1, 1,-1],
    [-1, 1, 0, 0, 1,-1, 1]
], dtype=float)

P = cp.Variable((7, 7), symmetric=True)
N = cp.Variable((7, 7), symmetric=True)

constraints = [
    H == P + N,
    P >> 0,      # P is PSD
    N >= 0       # entrywise nonnegative
]

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve()

print(prob.status)
