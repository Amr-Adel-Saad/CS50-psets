from cs50 import get_string
from sys import argv


def main():

    # Check if program was run with one command-line argument
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # open banned words file for reading
    banned = open(argv[1])
    # Initialize a list for banned words
    banned_words = []

    # Iterate through words in banned words file
    for word in banned:
        # Remove trailing \n
        word = word.strip()
        # Append each word to banned words list
        banned_words.append(word)

    # Print user for message
    message = get_string("What message would you like to censor?\n")

    # Iterate through words in message
    for word_in_message in message.split():
        lower_word_in_message = word_in_message.lower()

        # Check if lowered word is in banned words list and if yes, then replace each character with "*"
        if lower_word_in_message in banned_words:
            for c in word_in_message:
                print("*", end="")
            # Print "space" after word
            print(" ", end="")

        # If no, then print word
        else:
            print(word_in_message, end=" ")

    # Print a new line
    print()

    # Close file
    banned.close()


if __name__ == "__main__":
    main()

