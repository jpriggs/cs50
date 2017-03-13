#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Invalid number of arguments.\n Aborting program.\n");
        return 1;
    }
    int totalAlphabetChars = 'z'-'a' + 1;

    string cipherKey = argv[1];
    int cipherLength = strlen(cipherKey);
    //We need a separate cipher iterator if we want to properly ignore non-alpha characters.
    int cipherIterator = 0;
    
    //Check that all characters are valid, and make them lowercase if they aren't already (as per spec)
    for(int i = 0; i < cipherLength; i++)
    {
        if(!isalpha(cipherKey[i]))
        {
            printf("The string cannot contain non-alphabet characters.\n Aborting program.\n");
            return 1;
        }
        cipherKey[i] = tolower(cipherKey[i]);
    }
    
    printf("plaintext: ");
    string plainText = get_string();
    
    printf("ciphertext: ");
    for(int i = 0, n = strlen(plainText); i < n; i++)
    {
        char plainChar = plainText[i];
        
        //Ignore non alpha characters
        if(!isalpha(plainChar))
        {
            printf("%c", plainChar);
            continue;
        }
        //Using MODULO, iterate through the cipher key's entries
        char cipherChar = cipherKey[cipherIterator % cipherLength];
        
        //Cipher will all be lowercase, so we hardcode the offset in here as 'a'
        cipherChar = cipherChar - 'a';
        cipherIterator++;
        
        //The same offset as in caeser, keep track of the character being upper or lowercase.
        int offset = islower(plainChar) ? 'a' : 'A';

        //Convert the character by adding the cipher character to the current character (while taking into consideration the offset)
        char convertedChar = (((plainChar + cipherChar) - offset) % totalAlphabetChars) + offset;
        printf("%c", convertedChar);
    }
    printf("\n");
    return 0;
}