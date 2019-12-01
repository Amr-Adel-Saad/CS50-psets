#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c);

int main(int argc, string argv[])
{
    // Check if program was run with one command line argument
    if (argc == 2)
    {
        // Iterate over argument and checking each character if its an alphabet or not
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (isalpha(argv[1][i]) == false)
            {
                printf("Usage: ./Vigenere keyword\n");
                // Terminate program if argument contains a non-alphabet
                return 1;
            }
        }
        // prompt user for plaintext
        string plaintext = get_string("Plaintext: ");
        printf("Ciphertext: ");
        // Declare (Key) which represents the shift value
        int key;
        // Declare (Ci) which represent character in ciphertext
        char ci;
        // Declare (k) to account for punctuation marks in plaintext
        int k = 0;
        // Iterate over plaintext
        for (int i = 0; i < strlen(plaintext); i++)
        {
            // Increment k if character is a punctuation mark
            if (ispunct(plaintext[i]))
            {
                k++;
            }
            // Declare (j) which represents index of character in argument to be used in key
            int j = (i + k) % strlen(argv[1]);
            // Get the shift value using (shift)
            key = shift(argv[1][j]);
            // Get the character in ciphertext
            if (islower(plaintext[i]))
            {
                ci = 97 + (((plaintext[i] - 97) + key) % 26);
            }
            else if (isupper(plaintext[i]))
            {
                ci = 65 + (((plaintext[i] - 65) + key) % 26);
            }
            else
            {
                ci = plaintext[i];
            }
            // Print that character
            printf("%c", ci);
        }
        // Print a newline
        printf("\n");
    }
    // Inform user how to use program if user didn't run it with one command line argument
    else
    {    
        printf("Usage: ./Vigenere keyword\n");
        return 1;
    }
}

// Declare shift function which converts an alphabet character into an integer
int shift(char c)
{
    int key = c;
    if (isupper(key))
    {
        key = c - 65;
    }
    if (islower(key))
    {
        key = c - 97;
    }
    return key;
}
