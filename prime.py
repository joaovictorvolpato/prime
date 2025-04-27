

import random

#O teste de Miller-Rabin é um teste probabilístico de primalidade. 
#Ele verifica se um número é provavelmente primo com base em propriedades
# dos números primos sob a aritmética modular.
#A ideia básica é decompor n-1 = 2^r * d com d impar então verificar
#para uma base aleatoria alpha se a^d mod n = 1
#ou alpha^(2^j)*d mod n = n - 1 para algum 0 <= j < r 
#Referencia : Koblitz, N. A Course in Number Theory and Cryptography, Springer, 1994
#           https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
def miller_rabin(n, k=10):
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Escreve n-1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Testa k vezes com bases aleatórias
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # x = a^d mod n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)  # x = x^2 mod n
            if x == n - 1:
                break
        else:
            return False  # composto
    return True  # provavelmente primo


# Based on fermat's theorem, that says that if p is prime and a is an integer that
# 1 < a < p so: a^{p-1} congruent 1 mod p.
#Reference: https://en.wikipedia.org/wiki/Fermat_primality_test

def fermat_test(n, k=10):
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randrange(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False  
    return True 
