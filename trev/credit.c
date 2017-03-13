#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <math.h>
#include <string.h>

bool isValid(char* inputString, int length)
{
    char summationString[50];
    strcpy(summationString, "");
    int evensTotal = inputString[length - 1] - '0';
    //Get every other digit, starting from the second last
    for(int i = length - 2; i >= 0; i=i-2)
    {
        if(i > 0) 
        {
            evensTotal = evensTotal + inputString[i - 1] - '0';
        }
        char str[50];
        int cur = (inputString[i] - '0') * 2;
        //Multiply each of the above digits by 2
        sprintf(str, "%d", cur);
        //Append result to summation string
        strcat(summationString, str);
    }
    

    // Sum the remaining numbers from the input string
    //Once the summation string's components have been summed, add that total to the above remaining numbers total
    int summationTotal = 0;

    int lengthString = strlen(summationString);
    for(int i = 0; i < lengthString; i++)
    {
       summationTotal += (summationString[i] - '0');
    }
    
    //If the grand total mods to something of 10, it's good to go. 
    int grandTotal = summationTotal + evensTotal;
    return (grandTotal % 10 == 0);
}

const char * getType(char* inputString, int length)
{
    if(!isValid(inputString, length))
    {
        return "INVALID\n";
    }
    if(length == 15 && inputString[0] == '3')
    {
        return "AMEX\n";
    } 
    else if(length == 13 && inputString[0] == '4')
    {
        return "VISA\n";
    }
    else if(length == 16)
    {
        if(inputString[0] == '5')
        {
            return "MASTERCARD\n";
        }
        else 
        {
            return "VISA\n";
        }
    }
    return "INVALID\n";
}

int main(void)
{
    long user_input;
    int length;
    char user_input_string[50];
   
    //checks that user input is a non-negative number 
   do
    {
        printf("Enter credit card number \n");
        user_input = get_long_long();

        //Parse the integer into a string and record the length
        length = sprintf (user_input_string, "%ld", user_input);
    }
    while(user_input < 0.0 || length < 8);
    
    //Check validity of the credit card number

    printf("%s", getType(user_input_string, length));
    
}

