#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Invalid number of arguments");
        return 1;
    }
    
    int cipherKey = atoi(argv[1]);
    int totalAlphabetChars = 'z'-'a' + 1;
    
    printf("plaintext: ");
    string plainText = get_string();
    
    printf("ciphertext: ");
    for(int i = 0, n = strlen(plainText); i < n; i++)
    {
        char plainChar = plainText[i];
        
        if(!isalpha(plainChar))
        {
            printf("%c", plainChar);
            continue;
        }
        
        char cipherChar;
        int offset = islower(plainChar) ? 'a' : 'A';

        cipherChar = (((plainChar + cipherKey) - offset) % totalAlphabetChars);
        printf("%c", cipherChar + offset);
    }
    printf("\n");
    return 0;
}