#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>


int main(void)
{
    printf("plaintext: ");
    //string plainText = get_string();
    string plainText = "ABCDE";
    string secondText = "ABC";
    int secondStringLength = strlen(secondText);

    //Print out AaBcCeDdEf
    // Assume A = 0
    //Loops through user string and prints out each character.
    int offset = 'A';
    for(int i = 0, n = strlen(plainText); i < n; i++)
    {
        int secondTextIndex = i % secondStringLength;
        printf("%c%c", plainText[i], tolower(plainText[i] + (secondText[secondTextIndex] - offset);
    }
    // A + 0 = A ==> A + (A - A) = A
    // B + 1 = C ==> B + (B - A) = C
    // C + 2 = E ==> C + (C - A) = E
    // D + 0 = D ==> D + (A - A) = D
    // E + 1 = F ==> E + (B - A) = F
    // plainText[i] + (secondText[secondTextIndex] - offset) = appendLetter
    
    printf("\n");
}