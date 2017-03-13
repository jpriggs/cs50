#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string userInput = get_string();
    
    //checks if the string entered is a valid string
    if(userInput != NULL)
    {
        
        //prints the first initial of the first word inputted
        printf("%c", toupper(userInput[0]));
        
        //loops through each strings characters
        for(int i = 1, n = strlen(userInput); i < n; i++)
        {
            
            //checks if the previous character inputted was a space character
            char currentChar = userInput[i];
            char previousChar = userInput[i - 1];
            if(previousChar == ' ')
            {
                //outputs the current character in the loop as a capital letter
                printf("%c", toupper(currentChar));
            }
        }
    }
    printf("\n");
}