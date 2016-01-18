import math
import sys
import random
from Crypto.Util import *

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def generatePrimeAndGenerator(k, t):
    prime = number.getPrime(k)
    g = random.randint(2, prime - 1)
    return prime, g

def keygen(k, t):
    p, g = generatePrimeAndGenerator(k, t)
    x = random.randint(1, p - 1)
    h = pow(g, x, p)
    return p, g, x, h

def rand(p):
    return random.randint(1, p - 1)

def main(args):
    p, g, x, y = keygen(256, 1) # t is neglected

    # Generate a random message
    m = rand(p)

    # Encryption
    k0, k1 = rand(p), rand(p) # r = (k0, k1)
    alpha0 = (m * pow(y, k0, p)) % p
    beta0 = pow(g, k0, p)
    alpha1 = pow(y, k1, p)
    beta1 = pow(g, k1, p)
    ct = [(alpha0, beta0), (alpha1, beta1)]

    # Decryption
    m0 = (alpha0 * modinv(pow(beta0, x, p), p)) % p
    m1 = (alpha1 * modinv(pow(beta1, x, p), p)) % p

    assert m1 == 1 # condition for decryption
    print >> sys.stderr, "Plaintext             %x" % (m)
    print >> sys.stderr, "Decrypted message #1: %x" % (m0)

    # Re-encryption (only source of randomness is r' = (k0', k1'))
    k0p, k1p = rand(p), rand(p)
    alpha0p = (alpha0 * pow(alpha1, k0p, p)) % p
    beta0p = (beta0 * pow(beta1, k0p, p)) % p
    alpha1p = pow(alpha1, k1p, p)
    beta1p = pow(beta1, k1p, p)

    m0p = (alpha0p * modinv(pow(beta0p, x, p), p)) % p
    m1p = (alpha1p * modinv(pow(beta1p, x, p), p)) % p
    assert m1p == 1
    print >> sys.stderr, "Decrypted message #2: %x" % (m0p)

if __name__ == "__main__":
    main(sys.argv[1:])
