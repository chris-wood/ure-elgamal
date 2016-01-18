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

class ElGamal(object):
    '''  See: http://crypto.stanford.edu/~pgolle/papers/univrenc.pdf
    '''
    def rand(p):
            return random.randint(1, p - 1)

    def generatePrimeAndGenerator(k):
        prime = number.getPrime(k)
        g = random.randint(2, prime - 1)
        return prime, g

    def keygen(k):
        p, g = ElGamal.generatePrimeAndGenerator(k)
        x = ElGamal.rand(p)
        h = pow(g, x, p)
        return p, g, x, h

    def __init__(self, k):
        self.p, self.g, self.x, self.y = ElGamal.keygen(k)

    def randomElement(self):
        return _rand(self.p)

    def encrypt(self, m, y):
        k0, k1 = _rand(self.p), _rand(self.p) # r = (k0, k1)
        alpha0 = (m * pow(y, k0, self.p)) % self.p
        beta0 = pow(self.g, k0, self.p)
        alpha1 = pow(y, k1, self.p)
        beta1 = pow(self.g, k1, self.p)
        ct = [(alpha0, beta0), (alpha1, beta1)]
        return ct

    def reencrypt(self, ct):
        [(alpha0, beta0), (alpha1, beta1)] = ct
        k0p, k1p = _rand(self.p), _rand(self.p)
        alpha0p = (alpha0 * pow(alpha1, k0p, self.p)) % self.p
        beta0p = (beta0 * pow(beta1, k0p, self.p)) % self.p
        alpha1p = pow(alpha1, k1p, self.p)
        beta1p = pow(beta1, k1p, self.p)
        ct = [(alpha0p, beta0p), (alpha1p, beta1p)]
        return ct

    def decrypt(self, ct, x):
        [(alpha0, beta0), (alpha1, beta1)] = ct
        m0 = (alpha0 * modinv(pow(beta0, x, self.p), self.p)) % self.p
        m1 = (alpha1 * modinv(pow(beta1, x, self.p), self.p)) % self.p
        assert m1 == 1 # condition for decryption
        return m0

def main(args):
    elgamal = ElGamal(int(args[0]))
    m = elgamal.randomElement()
    ct1 = elgamal.encrypt(m, elgamal.y)
    m1 = elgamal.decrypt(ct1, elgamal.x)
    ct2 = elgamal.reencrypt(ct1)
    m2 = elgamal.decrypt(ct2, elgamal.x)

    print >> sys.stderr, "%x" % (m)
    print >> sys.stderr, "%x" % (m1)
    print >> sys.stderr, "%x" % (m2)

if __name__ == "__main__":
    main(sys.argv[1:])
