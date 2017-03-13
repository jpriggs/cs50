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
    
    string key = argv[1];
    int keyConverted = atoi(key);
    
    if(keyConverted < 1)
    {
        //returns an error message and ends the program with an error code
        printf("No negative integers please.\n");
        return 1;
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

    //iterate over the characters in the plainText input
    printf("ciphertext: ");
    for(int i = 0, n = strlen(plainText); i < n; i++)
    {
        //check if characters in plainText are alphanumeric characters
        if(isalpha(plainText[i]))
        {
            //check if character is upper or lower case
            if(islower(plainText[i]))
            {
                //execute lowercase cipher conversion
                char lowercaseChar = plainText[i];
                char cipherChar;
                int lowerCharOffset = 97;
                
                cipherChar = (((lowercaseChar + keyConverted) - lowerCharOffset)%26);
                printf("%c", cipherChar + lowerCharOffset);            
            }
            else
            {
                //execute uppercase cipher conversion
                char uppercaseChar = plainText[i];
                char cipherChar;
                int upperCharOffset = 65;
                
                cipherChar = (((uppercaseChar + keyConverted) - upperCharOffset)%26);
                printf("%c", cipherChar + upperCharOffset); 
            }
        }
        else
        {
            //print non-alpha numeric characters without change
            printf("%c", plainText[i]);
        }
    }
    printf("\n");
    return 0;
}
