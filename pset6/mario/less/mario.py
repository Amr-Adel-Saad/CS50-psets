from cs50 import get_int

# Prompt user for height, and if user didn't provide a valid height reprompt user again
while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(height):

    # Print spaces
    print(" " * (height - (i + 1)), end="")

    # Print hashes
    print("#" * (i + 1), end="")

    # Print new line
    print()