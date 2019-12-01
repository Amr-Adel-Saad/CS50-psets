#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Checking that program was run with one command line argument
    if (argc == 2)
    {
        // Iterating through characters in argv
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            // Checking if every character is a decimal number and
            // terminating program if it is not
            if (isdigit(argv[1][i]) == false)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        // Converting argv into an integer
        int key = atoi(argv[1]);
        // Prompting user for Plaintext
        string plaintext = get_string("Plaintext: ");
        printf("Ciphertext: ");
        // Iterating through each character in Plaintext and converting it into its
        // encrypted from if it is an alphabetical character 
        for (int i = 0; i < strlen(plaintext); i++)
        {
            char c;
            if (islower(plaintext[i]))
            {
                c = 97 + (((plaintext[i] - 97) + key) % 26);
            }
            else if (isupper(plaintext[i]))
            {
                c = 65 + (((plaintext[i] - 65) + key) % 26);
            }
            // Printing same character in plaintext if it is not an alphabetical character
            else
            {
                c = plaintext[i];
            }
            printf("%c", c);
        }
        printf("\n");
    }
    // Terminating program if the user didn't provide one command line argument
    else
    {    
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
