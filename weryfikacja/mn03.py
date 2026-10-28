"""Weryfikacja wyników z zestawu 3 (algebra dokładnie na ułamkach, reszta na float)."""
import math
import random
from fractions import Fraction as F

random.seed(3)


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def T(A):
    return [list(r) for r in zip(*A)]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def quad(A, x):
    return sum(x[i] * A[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))


def rand_matrix(n, lo=-5, hi=5):
    return [[F(random.randint(lo, hi)) for _ in range(n)] for _ in range(n)]


def ldlt(A):
    """Algorytm z zadania 3 (bez pierwiastków)."""
    n = len(A)
    L = [[F(0)] * n for _ in range(n)]
    d = [F(0)] * n
    for j in range(n):
        w = [L[j][k] * d[k] for k in range(j)]
        d[j] = A[j][j] - sum(L[j][k] * w[k] for k in range(j))
        L[j][j] = F(1)
        for i in range(j + 1, n):
            L[i][j] = (A[i][j] - sum(L[i][k] * w[k] for k in range(j))) / d[j]
    return L, d


def diag(d):
    return [[d[i] if i == j else F(0) for j in range(len(d))] for i in range(len(d))]


# ---------- Zadanie 1 ----------
for _ in range(200):
    n = random.randint(2, 4)
    M = rand_matrix(n)
    A = matmul(T(M), M)  # PD, jeśli M nieosobliwa
    A = [[A[i][j] + (n if i == j else 0) for j in range(n)] for i in range(n)]  # na pewno PD
    P = A
    for k in range(2, 6):
        P = matmul(P, A)
        x = [F(random.randint(-4, 4)) for _ in range(n)]
        if any(x):
            assert quad(P, x) > 0
# kontrprzykład dla parzystych k: A = -I
A = [[F(-1) if i == j else F(0) for j in range(3)] for i in range(3)]
x = [F(1), F(2), F(3)]
assert quad(matmul(A, A), x) > 0 and quad(A, x) < 0
# odwrotne dla k = 3: A^3 PD => A PD (sprawdzamy na losowych symetrycznych)
for _ in range(300):
    n = 2
    a, b, c = (F(random.randint(-4, 4)) for _ in range(3))
    A = [[a, b], [b, c]]
    if a * c - b * b == 0:
        continue
    A3 = matmul(matmul(A, A), A)
    pd = lambda M: M[0][0] > 0 and M[0][0] * M[1][1] - M[0][1] * M[1][0] > 0
    assert pd(A3) == pd(A)
print("Zadanie 1: A^k PD; A^3 PD <=> A PD; A=-I kontrprzykład dla parzystych  OK")

# ---------- Zadanie 2 ----------
for _ in range(2000):
    a = F(random.randint(1, 9), random.randint(1, 4))
    b = F(random.randint(-9, 9), random.randint(1, 4))
    c = F(random.randint(-9, 9), random.randint(1, 4))
    if a * c - b * b <= 0:
        continue
    x1, x2 = F(random.randint(-9, 9)), F(random.randint(-9, 9))
    q = a * x1 * x1 + 2 * b * x1 * x2 + c * x2 * x2
    assert q == a * (x1 + b / a * x2) ** 2 + (a * c - b * b) / a * x2 ** 2
    assert q > 0 or (x1 == 0 and x2 == 0)
A = [[F(1), F(2)], [F(2), F(1)]]
assert quad(A, [F(1), F(-1)]) == -2
print("Zadanie 2: dopełnienie do kwadratu, kontrprzykłady  OK")

# ---------- Zadanie 3 ----------
A = [[F(4), F(2), F(-2)], [F(2), F(10), F(2)], [F(-2), F(2), F(6)]]
L, d = ldlt(A)
assert L == [[1, 0, 0], [F(1, 2), 1, 0], [F(-1, 2), F(1, 3), 1]]
assert d == [4, 9, 4]
assert matmul(matmul(L, diag(d)), T(L)) == A
for _ in range(200):
    n = random.randint(1, 6)
    M = rand_matrix(n)
    A = matmul(T(M), M)
    A = [[A[i][j] + (1 if i == j else 0) for j in range(n)] for i in range(n)]
    L, d = ldlt(A)
    assert all(v > 0 for v in d)
    assert matmul(matmul(L, diag(d)), T(L)) == A
    # zgodność z Choleskym (float): d_j = g_jj^2
    G = [[0.0] * n for _ in range(n)]
    Af = [[float(v) for v in r] for r in A]
    for j in range(n):
        G[j][j] = math.sqrt(Af[j][j] - sum(G[j][k] ** 2 for k in range(j)))
        for i in range(j + 1, n):
            G[i][j] = (Af[i][j] - sum(G[i][k] * G[j][k] for k in range(j))) / G[j][j]
    for j in range(n):
        assert math.isclose(G[j][j] ** 2, float(d[j]), rel_tol=1e-9)
print("Zadanie 3: LDL^T (przykład + 200 losowych), d_j = g_jj^2  OK")

# ---------- Zadanie 4 ----------
for _ in range(100):
    n = random.randint(1, 5)
    v = [random.uniform(-3, 3) for _ in range(n)]
    nv = math.sqrt(sum(t * t for t in v))
    v = [t / nv for t in v]
    H = [[(i == j) - 2 * v[i] * v[j] for j in range(n)] for i in range(n)]
    H2 = matmul(H, H)
    assert all(abs(H2[i][j] - (i == j)) < 1e-12 for i in range(n) for j in range(n))
# na ułamkach: v = (3/5, 4/5)
v = [F(3, 5), F(4, 5)]
H = [[F(int(i == j)) - 2 * v[i] * v[j] for j in range(2)] for i in range(2)]
assert matmul(H, H) == eye(2)
# bez normalizacji: H^2 = I + 4(v^T v - 1) v v^T
v = [F(1), F(2)]
H = [[F(int(i == j)) - 2 * v[i] * v[j] for j in range(2)] for i in range(2)]
vv = sum(t * t for t in v)
assert matmul(H, H) == [[F(int(i == j)) + 4 * (vv - 1) * v[i] * v[j] for j in range(2)] for i in range(2)]
print("Zadanie 4: H^2 = I  OK")

# ---------- Zadanie 5 ----------
s2 = math.sqrt(2)
G2 = [[1 / s2, 0, 1 / s2], [0, 1, 0], [-1 / s2, 0, 1 / s2]]
G1 = [[2 * s2 / 3, 1 / 3, 0], [-1 / 3, 2 * s2 / 3, 0], [0, 0, 1]]
x = [[2], [1], [2]]
y = matmul(G2, x)
assert all(math.isclose(a[0], b, abs_tol=1e-14) for a, b in zip(y, [2 * s2, 1, 0]))
z = matmul(G1, y)
assert all(math.isclose(a[0], b, abs_tol=1e-14) for a, b in zip(z, [3, 0, 0]))
for G, (i, j), th in ((G2, (0, 2), -math.pi / 4), (G1, (0, 1), -math.asin(1 / 3))):
    R = [[float(r == c) for c in range(3)] for r in range(3)]
    R[i][i], R[i][j], R[j][i], R[j][j] = math.cos(th), -math.sin(th), math.sin(th), math.cos(th)
    assert all(math.isclose(R[r][c], G[r][c], abs_tol=1e-14) for r in range(3) for c in range(3))
# dokładnie: wyrazy (2 sqrt2/3)^2 + (1/3)^2 = 1, (1/sqrt2)^2 * 2 = 1
assert F(8, 9) + F(1, 9) == 1
print("Zadanie 5: G1 G2 (2,1,2) = (3,0,0), kąty -pi/4 i -arcsin(1/3)  OK")

# ---------- Zadanie 6 ----------
# Kwadratura prostokątów na pełnym okresie jest dokładna dla wielomianów
# trygonometrycznych stopnia < N, więc to sprawdza całki (prawie) dokładnie.
N = 256
xs = [-math.pi + 2 * math.pi * k / N for k in range(N)]


def inner(f, g):
    return (2 * math.pi / N) * sum(f(t) * g(t) for t in xs) / math.pi


funs = [("1", lambda t: 1.0)]
for n in range(1, 11):
    funs.append((f"cos {n}x", lambda t, n=n: math.cos(n * t)))
    funs.append((f"sin {n}x", lambda t, n=n: math.sin(n * t)))
for a, (na, f) in enumerate(funs):
    for b, (nb, g) in enumerate(funs):
        val = inner(f, g)
        if a != b:
            assert abs(val) < 1e-12, (na, nb, val)
        else:
            assert math.isclose(val, 2.0 if na == "1" else 1.0, rel_tol=1e-12), (na, val)
print("Zadanie 6: ortogonalność, ||1|| = sqrt 2, pozostałe normy 1  OK")
