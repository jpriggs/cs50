#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(void)
{
    printf("plaintext: ");
    string plainText = get_string();
    
    for(int i = 0, n = strlen(plainText); i < n; i++)
    {
        printf("%c", plainText[i]);
    }
    printf("\n");
}