#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //checks that the user command-line is only 2 arguments
    if(argc != 2)
    {
        //returns an error message and ends the program with an error code
        printf("missing command-line argument\n");
        return 1;
    }
    string cipherKey = argv[1];
    int cipherKeyLength = strlen(cipherKey);
    int uppercaseOffset = 'A';
    int lowercaseOffset = 'a';
    int cipherKeyIterator = 0;
    
    //Loops through user string and checks that each character is valid
    for(int i = 0; i < cipherKeyLength; i++)
    {
        if(!isalpha(cipherKey[i]))
        {
        //returns an error message and ends the program with an error code
        printf("Please enter alphanumeric characters only\n");
        return 1;
        } 
    }
    //prompt the user for a plaintext string
    printf("plaintext: ");
    string plainText = get_string();
    
    //checks that the user inputted plaintext is a string
    if(plainText == NULL)
    {
        //returns an error message and ends the program with an error code
        printf("Enter a string please.\n");
        return 1;
    }
    printf("ciphertext: ");
    for(int i = 0, n = strlen(plainText); i < n; i++)
    {
        //check if characters in plainText are alphanumeric characters
        if(isalpha(plainText[i]))
        {
            //check if character is upper or lower case
            if(islower(plainText[i]))
            {
                int cipherKeyIndex = cipherKeyIterator % cipherKeyLength; 
                char cipherKeyChar = tolower(cipherKey[cipherKeyIndex]) - lowercaseOffset;
                char convertedChar = (((plainText[i] + cipherKeyChar) - lowercaseOffset) % 26) + lowercaseOffset; 
                
                //prints lowercase converted characters
                printf("%c", convertedChar);
            }
            else
            {
                int cipherKeyIndex = cipherKeyIterator % cipherKeyLength; 
                char cipherKeyChar = tolower(cipherKey[cipherKeyIndex]) - lowercaseOffset;
                char convertedChar = (((plainText[i] + cipherKeyChar) - uppercaseOffset) % 26) + uppercaseOffset; 
                
                //prints uppercase converted characters
                printf("%c", convertedChar);
            }
            cipherKeyIterator++;
        }
         else
        {
            //print non-alphanumeric characters without change
            printf("%c", plainText[i]);
        }
    }
    printf("\n");
}