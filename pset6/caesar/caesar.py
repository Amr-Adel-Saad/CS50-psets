from sys import argv
from cs50 import get_string

# Check if user ran the program with one command-line argument
if len(argv) != 2:
    print("Usage: python caesar.py k")
    exit(1)

# convert key into integer
k = int(argv[1])

p = get_string("plaintext: ")

print("ciphertext: ", end="")

# Iterate through chars in plaintext
for c in p:
    # Encrypt chars and print the encrypted
    if c.isupper():
        encrypted = 65 + ((ord(c) - 65) + k) % 26
        print(chr(encrypted), end="")

    elif c.islower():
        encrypted = 97 + ((ord(c) - 97) + k) % 26
        print(chr(encrypted), end="")

    else:
        print(c, end="")

print()