from random import randint

def is_prime(x: int) -> bool:
    d = 2
    while (d * d <= x):
        if (x % d == 0):
            return False
        d += 1
    return True

def gcd(a: int, b: int) -> int:
    while a:
        a, b = b % a, a
    return b

def deg(x: int, mod: int, deg: int) -> int:
    ans = 1
    cur = x
    while deg:
        if deg & 1:
            ans = (ans * cur) % mod
        cur = (cur * cur) % mod
        deg >>= 1
    return ans

p = 53
q = 101
n = p * q
phi = (p - 1) * (q - 1)
e = randint(2, phi - 1)
while gcd(e, phi) != 1:
    e = randint(2, phi - 1)
d = deg(e, phi, phi - 1)

print(f'p = {p}, q = {q}, n = {n}, phi = {phi}, e = {e}, d = {d}')
m = 155 % n
value = deg(m, n, e)
print(f'm = {m}, value = {value}')
c = deg(value, n, d)
print(f'c = {c}')
print(e * d % phi)
print(is_prime(n))