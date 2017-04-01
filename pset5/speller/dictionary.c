/**
 * Implements a dictionary's functionality.
 */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

#define ALPHABET 26
#define APOSTROPHY 26
#define OTHERCHARACTER 27

//global declarations
node *root;
node *travCursor;
unsigned int wordCounter;

//declaration of the free node prototype for recursive unloading
void freeNode(node *freeCursor);

//declaration of the indexing prototype
unsigned int setIndex(const char c);

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    //declarations
    travCursor = root;
    unsigned int textIndex;
    unsigned int wordLength = strlen(word);

    //iterates through each letter in the inputted word
    for(unsigned int i = 0; i < wordLength; i++)
    {
        //set the index value based on position in the alphabet or apostrophy index location
        textIndex = setIndex(tolower(word[i]));
        
        //checks if the index exists in the trie
        if(travCursor->children[textIndex] == NULL)
        {
            //if the index value is NULL, the word doesn't exist in the dictionary
            return false;
        }
        //checks if the index value exists, the cursor moves to the next letter in the word
        travCursor = travCursor->children[textIndex];
    }
    
    //checks if the end pointer is_word boolean value is set to true
    if(travCursor->is_word == true)
    {
        //if the boolean value is_word returns true, then the word exists in the dictionary
        return true;
    }
    
    //if the word is not found in the dictionary, the check boolean returns false
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    printf("THIS IS FUCKED UP CODE");
    // TODO
    //open a dictionary to be read and make sure it exists
    FILE *readptr = fopen(dictionary, "r");

    if(readptr == NULL)
    {
        printf("Could not open %s. \n", dictionary);
        unload();
        return false;
    }

    root = calloc(1, sizeof(node));
    travCursor = root;
    unsigned int dictIndex;
    
    //iterate through every character in the dictionary until the end of file
    for(unsigned int dictChar = tolower(fgetc(readptr)); dictChar != EOF; dictChar = fgetc(readptr))
    {
        //check if the line break has been reached
        if(dictChar == '\n')
        {
            if(travCursor != root)
            {
                //mark true as a complete word
                travCursor->is_word = true;
                
                //word counter is incremented by one
                wordCounter++;
                
                //reset the traversal pointer back to the root node
                travCursor = root;
            }
        }
        else
        {
            //set the index value based on position in the alphabet or apostrophy index location
            dictIndex = setIndex(dictChar);
            
            //check if a node already exists for a letter in a word
            if(travCursor->children[dictIndex] == NULL)
            {
                //create a new node
                travCursor->children[dictIndex] = calloc(1, sizeof(node));
            }
            //move onto the next node if a letter already exists
            travCursor = travCursor->children[dictIndex];
        
        }
    }
    //close the dictionary file
    fclose(readptr);
    
    //return true on successful dictionary load
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    //returns the number of words in the dictionary
    return wordCounter;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    //frees all nodes linked to the root node
    freeNode(root);

    //checks if the root node still exists
    if(root == NULL)
    {
        //if it does return false
        return false;
    }
    //return true if all nodes have been freed
    return true;
}

/**
 *  Creates a recursive function for deleting the nodes in the trie
 */
void freeNode(node *freeCursor)
{
    //loops through each index in each branch
    for(unsigned int i = 0; i < ALPHABET + 1; i++)
    {
        //looks for non-NULL nodes for deletion
        if(freeCursor->children[i] != NULL)
        {
            //clears all node branches recursively
            freeNode(freeCursor->children[i]);
        }
    }
    //frees the travCursor from memory
    free(freeCursor);
}

/**
 *  Determines the index value of each letter in the alphabet 0-25 and the apostrophy value at index location 26
 */
unsigned int setIndex(const char c)
{
    if(c == '\'')
    {
        //returns index location 26
        return APOSTROPHY;
    }
    else if(isalpha(c))
    {
        //returns a value of 0-25 based on the input letter
        return tolower(c - 'a');
    }
    else
    {
        //returns other characters such as '\n' to index location 27
        return OTHERCHARACTER;
    }
}
