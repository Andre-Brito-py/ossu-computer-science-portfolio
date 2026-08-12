import random
from math import gcd

# Cryptography - RSA Cryptosystem Implementation
# Implementing key generation, encryption, and decryption from scratch

def is_prime(num, test_count=40):
    # Miller-Rabin primality test
    if num == 2 or num == 3:
        return True
    if num <= 1 or num % 2 == 0:
        return False
        
    s = 0
    d = num - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
        
    for _ in range(test_count):
        a = random.randrange(2, num - 1)
        x = pow(a, d, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        # Ensure it's odd and has the correct bit length
        num |= (1 << bits - 1) | 1
        if is_prime(num):
            return num

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits):
    print("Generating primes (this may take a moment)...")
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

if __name__ == '__main__':
    print("--- RSA Cryptosystem ---")
    public, private = generate_keypair(128) # 128-bit for demonstration speed
    print(f"Public key (e, n):\n  e={public[0]}\n  n={public[1]}")
    print(f"Private key (d, n):\n  d={private[0]}\n  n={private[1]}\n")
    
    msg = "Cryptography is the ultimate defense."
    print(f"Original Message: {msg}")
    
    encrypted_msg = encrypt(public, msg)
    print(f"\nEncrypted (array of ints):\n{encrypted_msg}")
    
    decrypted_msg = decrypt(private, encrypted_msg)
    print(f"\nDecrypted Message: {decrypted_msg}")
