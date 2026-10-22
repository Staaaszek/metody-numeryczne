"""Numeryczna weryfikacja wyników z zestawu 1 (Python float = IEEE 754 double)."""
import cmath
import math
import random
from fractions import Fraction as F

# Zadanie 1: (a+b)+c != a+(b+c)
a, b, c = 1.0, 2.0**-53, 2.0**-53
assert (a + b) + c == 1.0
assert a + (b + c) == 1.0 + 2.0**-52
assert F(a) + F(b) + F(c) == F(a + (b + c))  # prawa strona jest nawet dokładna
a, b, c = 2.0**53, 1.0, 1.0
assert (a + b) + c == 2.0**53 and a + (b + c) == 2.0**53 + 2
print("ok  zad1")

# Zadanie 2: a(b+c) != ab+ac
a, b, c = 3.0, 1.0, 2.0**-53
assert a * (b + c) == 3.0
assert a * b + a * c == 3.0 + 2.0**-51
assert a * c == 3 * 2.0**-53  # iloczyn ac jest dokładny
print("ok  zad2")


# Zadanie 3: algorytm bez catastrophic cancellation vs szkolny wzór
def stabilny(A, B, C):
    d = B * B - 4 * A * C
    if d >= 0:
        q = -(B + math.sqrt(d)) / 2
        x2 = C / q
        return [x2] if A == 0 else [q / A, x2]
    r, s = -B / (2 * A), math.sqrt(-d) / (2 * A)
    return [complex(r, s), complex(r, -s)]


def szkolny(A, B, C):
    d = math.sqrt(B * B - 4 * A * C)
    return [(-B - d) / (2 * A), (-B + d) / (2 * A)]


def dokladne(A, B, C):
    """Pierwiastki z dużą precyzją (Fraction + Newton dla sqrt)."""
    A, B, C = F(A), F(B), F(C)
    d = B * B - 4 * A * C
    s = F(math.sqrt(float(d)))
    for _ in range(6):  # Newton: kwadratowa zbieżność, ~ setki cyfr
        s = (s + d / s) / 2
    if A == 0:
        return [-C / B]
    return [(-B - s) / (2 * A), (-B + s) / (2 * A)]


def blad(x, y):
    return abs(F(x) - y) / abs(y) if y != 0 else abs(F(x))


# przykład z intuicji
assert szkolny(1e-9, 20.0, 1e-9)[1] == 0.0
x1, x2 = stabilny(1e-9, 20.0, 1e-9)
e1, e2 = dokladne(1e-9, 20.0, 1e-9)
assert blad(x1, e1) < 1e-15 and blad(x2, e2) < 1e-15

random.seed(1)
gorsze = 0
for _ in range(3000):
    A = random.choice([random.uniform(0, 20), 10 ** random.uniform(-15, 1), 0.0])
    B = random.uniform(10, 20) + 1e-9
    C = random.choice([random.uniform(0, 20), 10 ** random.uniform(-15, 1), 0.0])
    d = F(B) ** 2 - 4 * F(A) * F(C)
    if d < 0:
        for z in stabilny(A, B, C):
            assert abs(A * z * z + B * z + C) < 1e-12 * (B * abs(z) + C)
        continue
    if d < F(B) ** 2 / 10:  # prawie podwójny pierwiastek: źle uwarunkowane, pomijamy
        continue
    got = sorted(stabilny(A, B, C))
    ex = sorted(dokladne(A, B, C))
    for g, e in zip(got, ex):
        assert blad(g, e) < 4 * 2.0**-53, (A, B, C, g, float(e))
    if A > 0 and C > 0:
        gorsze += blad(szkolny(A, B, C)[1], ex[1]) > 1e-10
assert gorsze > 100  # szkolny wzór regularnie traci cyfry
print(f"ok  zad3 (szkolny wzór stracił >6 cyfr w {gorsze} przypadkach, stabilny nigdy)")

# Zadanie 4: ||A|| = 3, ||Ax||^2 = 5 + 4 sin 2t
best = 0
for k in range(100000):
    t = 2 * math.pi * k / 100000
    x, y = math.cos(t), math.sin(t)
    n2 = (2 * x + y) ** 2 + (x + 2 * y) ** 2
    assert math.isclose(n2, 5 + 4 * math.sin(2 * t), abs_tol=1e-12)
    assert n2 <= 9 + 1e-12
    best = max(best, n2)
assert math.isclose(math.sqrt(best), 3)
print("ok  zad4")
