"""Numeryczna weryfikacja wyników z zestawu 2 (dokładnie, na ułamkach)."""
import random
from fractions import Fraction as F

random.seed(2)


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def gauss(A, b=None, pivoting=False):
    """Eliminacja Gaussa. Zwraca (L, U, perm, liczba_zamian, pivoty, b')."""
    n = len(A)
    U = [[F(x) for x in row] for row in A]
    b = [F(x) for x in b] if b is not None else [F(0)] * n
    L = eye(n)
    perm = list(range(n))
    swaps = 0
    for k in range(n - 1):
        if pivoting:
            p = max(range(k, n), key=lambda i: abs(U[i][k]))
            if abs(U[p][k]) > abs(U[k][k]):  # zamieniamy tylko, gdy diagonalny nie jest największy
                U[k], U[p] = U[p], U[k]
                b[k], b[p] = b[p], b[k]
                perm[k], perm[p] = perm[p], perm[k]
                L[k][:k], L[p][:k] = L[p][:k], L[k][:k]
                swaps += 1
        if U[k][k] == 0:
            raise ZeroDivisionError(k)
        for i in range(k + 1, n):
            l = U[i][k] / U[k][k]
            L[i][k] = l
            for j in range(k, n):
                U[i][j] -= l * U[k][j]
            b[i] -= l * b[k]
    return L, U, perm, swaps, [U[k][k] for k in range(n)], b


def back_subst(U, y):
    n = len(U)
    x = [F(0)] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))) / U[i][i]
    return x


def det(A):
    try:
        _, U, perm, swaps, piv, _ = gauss(A, pivoting=True)
    except ZeroDivisionError:
        return F(0)
    d = F((-1) ** swaps)
    for p in piv:
        d *= p
    return d


# Zadanie 1: interpolacja przez układ Vandermonde'a, Gauss bez permutacji
for n in range(0, 12):
    for _ in range(10):
        xs = random.sample(range(-30, 31), n + 1)
        coef = [F(random.randint(-9, 9), random.randint(1, 5)) for _ in range(n + 1)]
        ys = [sum(c * F(x) ** j for j, c in enumerate(coef)) for x in xs]
        V = [[F(x) ** j for j in range(n + 1)] for x in xs]
        _, U, _, _, piv, y = gauss(V, ys)  # bez pivotingu: nie może się wyłożyć
        assert all(p != 0 for p in piv)
        assert back_subst(U, y) == coef
print("ok  zad1")

# Zadanie 2: brak LU dla [[0,1],[1,1]] (sprawdzamy też, że Gauss staje)
try:
    gauss([[0, 1], [1, 1]])
    raise AssertionError("Gauss nie powinien przejść")
except ZeroDivisionError:
    pass
L, U, perm, swaps, _, _ = gauss([[0, 1], [1, 1]], pivoting=True)
assert perm == [1, 0] and U == [[1, 1], [0, 1]] and L == eye(2)
print("ok  zad2")


# Zadanie 3: odwrotność górnotrójkątnej jest górnotrójkątna, przekątna 1/u_ii
def inverse_upper(U):
    n = len(U)
    cols = [back_subst(U, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


for n in range(1, 9):
    for _ in range(20):
        U = [[F(random.randint(-9, 9)) if i <= j else F(0) for j in range(n)] for i in range(n)]
        for i in range(n):
            U[i][i] = F(random.choice([-3, -2, -1, 1, 2, 3, 7]))
        Ui = inverse_upper(U)
        assert matmul(U, Ui) == eye(n)
        assert all(Ui[i][j] == 0 for i in range(n) for j in range(i))
        assert all(Ui[i][i] == 1 / U[i][i] for i in range(n))
print("ok  zad3")

# Zadanie 4: jednoznaczność Doolittle'a + kontrprzykład dla osobliwej
for n in range(1, 8):
    for _ in range(20):
        Lr = [[F(random.randint(-5, 5)) if i > j else F(int(i == j)) for j in range(n)] for i in range(n)]
        Ur = [[F(random.randint(-5, 5)) if i <= j else F(0) for j in range(n)] for i in range(n)]
        for i in range(n):
            Ur[i][i] = F(random.choice([-2, -1, 1, 3]))
        A = matmul(Lr, Ur)
        L, U, _, _, _, _ = gauss(A)  # Gauss odtwarza dokładnie ten sam rozkład
        assert L == Lr and U == Ur
for t in range(-5, 6):
    assert matmul([[1, 0], [t, 1]], [[0, 0], [0, 1]]) == [[0, 0], [0, 1]]
print("ok  zad4")


# Zadanie 5: dominacja kolumnowa => brak zamian, pivoty != 0, det != 0
def dominujaca(n):
    A = [[F(random.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
    for j in range(n):
        s = sum(abs(A[i][j]) for i in range(n) if i != j)
        A[j][j] = (s + F(random.randint(1, 3), random.randint(1, 4))) * random.choice([-1, 1])
    return A


def kolumnowo_dominujaca(A):
    n = len(A)
    return all(abs(A[j][j]) > sum(abs(A[i][j]) for i in range(n) if i != j) for j in range(n))


for n in range(1, 10):
    for _ in range(40):
        A = dominujaca(n)
        L, U, perm, swaps, piv, _ = gauss(A, pivoting=True)
        assert swaps == 0 and all(p != 0 for p in piv)
        assert all(abs(L[i][j]) < 1 for i in range(n) for j in range(i))
        assert det(A) != 0
        if n >= 2:  # lemat: podmacierz po jednym kroku nadal dominująca
            a = [[F(x) for x in r] for r in A]
            sub = [[a[i][j] - a[i][0] / a[0][0] * a[0][j] for j in range(1, n)] for i in range(1, n)]
            assert kolumnowo_dominujaca(sub)
# dominacja wierszowa nie wystarcza
assert gauss([[1, 0], [3, 4]], pivoting=True)[3] == 1
print("ok  zad5")

# Przykłady w teorii
A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]]
L, U, perm, zamiany, piv, _ = gauss(A)
assert L == [[1, 0, 0], [2, 1, 0], [4, 3, 1]] and U == [[2, 1, 1], [0, 1, 1], [0, 0, 2]]
assert matmul(L, U) == A and piv == [2, 1, 2]
assert [det([r[:k] for r in A[:k]]) for k in (1, 2, 3)] == [2, 2, 4]
assert matmul(A, [[1], [1], [2]]) == [[5], [13], [33]]
assert matmul(U, [[1], [1], [2]]) == [[5], [3], [4]] and matmul(L, [[5], [3], [4]]) == [[5], [13], [33]]
V = [[1, 0, 0], [1, 1, 1], [1, 2, 4]]
assert matmul(V, [[1], [1], [1]]) == [[1], [3], [7]]
assert matmul([[1, 2], [0, 3]], [[4, 5], [0, 6]]) == [[4, 17], [0, 18]]
assert kolumnowo_dominujaca([[4, 1, -1], [1, -5, 2], [2, 3, 6]])
assert not kolumnowo_dominujaca([[1, 2], [3, 4]])
# pivoting: [[eps,1],[1,1]] x = [1,2] w double
e = 1e-20
l = 1 / e
u22 = 1 - l
x2 = (2 - l * 1) / u22
x1 = (1 - x2) / e
assert u22 == -1e20 and (x1, x2) == (0.0, 1.0)
u22 = 1 - e * 1
x2 = (1 - e * 2) / u22
x1 = (2 - x2) / 1
assert u22 == 1.0 and (x1, x2) == (1.0, 1.0)
print("ok  przykłady z teorii")
