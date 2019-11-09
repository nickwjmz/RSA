#!/usr/bin/env python3
"""A module for computing the private and public keys of the RSA algorithm.

Functions:
    gcd(a, b):
        Returns the greatest common denominator of arguments a and b.
    egcd(a, b):
        computes the Extended Euclidean Algorithm of arguments a and b.
    encrypt_message():
        Encrypts random integer m Based on inputs p, q, and which are currently
        randomly generated without primality tests.
    decrypt_message():
        Decryption of cipher text c currently relies on encrypt_message() to
        pass the same values of p, q.

Usage:
    python3 rsa.py
"""
import random


def gcd(a, b):
    if b > a:
        x, y = b, a
    else:
        x, y = a, b
    r = x % y
    while r != 0:
        x, y = y, r
        r = x % y
    return y


def egcd(A, B):
    """Calculates x, y in the Extended Euclidean Algorithm (EEA) for integers a & b.
    Creates two lists--Xn and Yn--that represent the programs steps thru the EEA.
    The for loop then checks the calculations of the while loop by creating another
    value EE, and iterates thru the two lists doing the same calculations, and returning the
    values needed to produce the gcd(a,b).
    """
    a, b = A, B
    d = gcd(A, B)
    xone, xtwo = 1, 0
    yone, ytwo = 0, 1
    Xn = []                             # Creates a list for all x-values
    Yn = []                             # Creates a list for all y-values
    while b != 0:                       # WHILE LOOP
        q = a // b                      # Calculates q(i)
        r = a % b                       # remainder r(i)
        a, b = b, r                     # Basic gcd
        x = xone-q*xtwo                 # While loop for finding x(n)
        Xn.append(x)                    # Appends each value x to the list
        xone, xtwo = xtwo, x            # Adjusting values for the loop
        y = yone-q*ytwo                 # While loop for finding y(n)
        Yn.append(y)                    # Appends each value y to the list
        yone, ytwo, = ytwo, y           # Adjusting values for the loop.
    for f, g in zip(Xn, Yn):            # Pairing the arrays to allow vector Calc.
        EE = (A*f + B*g)
        if d == EE:
            # print(A," * ",f," + ",B," * ",g," = ",EE)                 
            return (f, d)               # Returns the x-value & the gcd of the 2 integers

def Modular_Inverse(a, n):
    """'Calculates the inverse of a (mod n) using the Extended Euclidean Algorithm."""
    inverse, d = egcd(a, n)
    if d != 1:
        print('Modular inverse does not exist. The gcd(a,n) must be equal to one')
    else:
        return inverse % n


def Modular_Exponentiation(m, e, n):
    """Calculates m^e (mod n) by the successive squares algorithm."""
    a, b, c = e, 1, m
    while a != 0:    
        if a % 2 == 0:
            a, b, c = a//2, b, c**2 % n
        else:
            a, b, c = a-1, b*c % n, c
    return b


def find_n():
    """p and q are generated randomly and not checked for primality."""
    p = random.randint(1*10**100, 1*10**200)
    q = random.randint(1*10**100, 1*10**200)
    n = p*q
    return p, q, n


def find_e():
    """e is currently generated randomly depending on the
    results of the find_n() function.
    """
    p, q, n = find_n()
    pq = (p-1) * (q-1)
    e = random.randint(1*10**100, 1*10**200)
    while gcd(e, pq) != 1:
        e = random.randint(1*10**100, 1*10**200)
    return e, pq, n, p, q


def find_d():
    e, pq, n, p, q = find_e()
    d = Modular_Inverse(e, pq)
    return d, e, pq, n, p, q


def encrypt_message():
    """Randomizing m in function instead of as an argument allows this fuction
    to easily be passed off to decrypt_message().
    """
    d, e, pq, n, p, q = find_d()
    c = Modular_Exponentiation(random.randint(1*10**100, 1*10**200), e, n)
    print("PUBLIC KEY:")
    print("e = ", e)
    print("n = ", n)
    print("PRIVATE KEY: KEEP SECRET")
    print("p = ", p)
    print("q = ", q)
    print("d = ", d)
    print("*****************************")
    print("m^e = c (mod n)")
    print("c = ", c)
    return c, d, n


def decrypt_message():
    c, d, n = encrypt_message()
    M = Modular_Exponentiation(c, d, n)
    print("c^d = m (mod n)")
    print("m = ", M)
    return M, c, d, n


if __name__ == '__main__':
    decrypt_message()
