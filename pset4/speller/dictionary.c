// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

int size_of_dict = 0;
// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        // create new node for new word
        node *new_node = malloc(sizeof(node));
        
        // check if there is no memory
        if (new_node == NULL)
        {
            // unload dictionary if there is no memory
            unload();
            return false;
        }
        // insert word into new node
        strcpy(new_node->word, word);
        // hash the word
        int i = hash(word);
        // check if there is any node in this index of hashtable
        if (hashtable[i] == NULL)
        {
            // insert new node into index of hashtable
            hashtable[i] = new_node;
            new_node->next = NULL;
        }
        else
        {
            // point new node next to the pointer that HEAD's pointing to
            new_node->next = hashtable[i];
            // reassign head to new node
            hashtable[i] = new_node;
        }
        // increment size_of_dict
        size_of_dict++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return size_of_dict;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int i = hash(word);
    node *cursor = hashtable[i];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < 26; i++)
    {
        node *cursor = hashtable[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
