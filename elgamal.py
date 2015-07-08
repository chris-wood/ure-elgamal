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

def millerRabin(n, t):
    if n < 2 or n % 2 == 0:
        return False

    # find r s.t. n-1=(2^s)r
    s = 0
    r = n - 1
    while r % 2 == 0:
        s += 1
        r //= 2

    for i in range(1, t + 1):
        a = random.randint(2, n - 2)
        exp = pow(a, r, n)
        if exp != 1 and exp != (n - 1):
            j = 1
            while j <= (s - 1) and y != (n - 1):
                y = pow(y, 2, n)
                if y == 1:
                    return False
                j += 1
            if y != (n - 1):
                return False
    return True

def randomPrime(k, t):
    n = random.getrandbits(k)
    while not millerRabin(n, t):
        n = random.getrandbits(k)
    return n

def generatePrimeAndGenerator(k, t):
    #p = randomPrime(k, t)
    #pp = p - 1
    # factor pp (= p - 1)

    prime = number.getPrime(k)
    g = random.randint(2, prime - 1)

    return prime, g

def keygen(k, t):
    p, g = generatePrimeAndGenerator(k, t)
    x = random.randint(1, p - 1)
    h = pow(g, x, p)
    return p, g, x, h

def main(args):
    p, g, x, h = keygen(256, 1) # t is neglected

    # Generate a random message
    m = random.randint(1, p - 1)

    # Encrypt
    y = random.randint(1, p - 1)
    c1 = pow(g, y, p)
    ss = pow(h, y, p)
    c2 = (m * ss) % p
    ct = (c1, c2)

    # Decrypt
    s = pow(c1, x, p)
    mm = (c2 * modinv(s, p)) % p

    print >> sys.stderr, "Plaintext          %x" % (m)
    print >> sys.stderr, "Decrypted message: %x" % (mm)
    assert m == mm

if __name__ == "__main__":
    main(sys.argv[1:])
