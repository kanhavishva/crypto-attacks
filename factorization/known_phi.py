from math import gcd
from random import randint

from sage.all import ZZ
from sage.all import is_prime


def factorize(n, phi):
    """
    Recovers the prime factors from a modulus if Euler's totient is known.
    This method only works for a modulus consisting of 2 primes!
    :param n: the modulus
    :param phi: Euler's totient, the order of the multiplicative group modulo n
    :return: a tuple containing the prime factors, or None if the factors were not found
    """
    s = n + 1 - phi
    x = ZZ["x"].gen()
    f = x ** 2 - s * x + n
    for p, _ in f.roots():
        p = int(p)
        if n % p == 0:
            return p, n // p


def factorize_multi_prime(n, phi):
    """
    Recovers the prime factors from a modulus if Euler's totient is known.
    This method works for a modulus consisting of any number of primes, but is considerably be slower than factorize.
    More information: Hinek M. J., Low M. K., Teske E., "On Some Attacks on Multi-prime RSA" (Section 3)
    :param n: the modulus
    :param phi: Euler's totient, the order of the multiplicative group modulo n
    :return: a tuple containing the prime factors
    """
    prime_factors = set()
    factors = [n]
    while len(factors) > 0:
        # Element to factorize.
        n = factors[0]

        w = randint(2, n - 2)
        i = 1
        while phi % (2 ** i) == 0:
            sqrt_1 = pow(w, phi // (2 ** i), n)
            if sqrt_1 > 1 and sqrt_1 != n - 1:
                # We can remove the element to factorize now, because we have a factorization.
                factors = factors[1:]

                p = gcd(n, sqrt_1 + 1)
                q = n // p

                if is_prime(p):
                    prime_factors.add(p)
                elif p > 1:
                    factors.append(p)

                if is_prime(q):
                    prime_factors.add(q)
                elif q > 1:
                    factors.append(q)

                # Continue in the outer loop
                break

            i += 1

    return tuple(prime_factors)
