import math
import sys
import random

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
    p = randomPrime(k, t)
    pp = p - 1
    # factor pp (= p - 1)
    

def keygen(k, t):
    p, alpha = generatePrimeAndGenerator(k, t)

def main(args):
    pass

if __name__ == "__main__":
    main(sys.argv[1:])

