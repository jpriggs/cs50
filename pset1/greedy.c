#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float user_input;
    int counter = 0;
    int remainder;

   
    //checks that user input is a non-negative number 
   do
    {
        printf("O hai! How much change is owed? \n");
        user_input = get_float();
    }
    while(user_input < 0.00);
    
    //convert and calculate the user's input
    remainder = round(user_input * 100);
    
    if(remainder > 0)
    {
        //count the number of coins the remainder gets divided into
        for(counter = 0; remainder > 0; counter++)
        
            if(remainder > 24)
            {
                
                remainder = remainder - 25;
            
            }    
            else if(remainder > 9 && remainder < 25)
            {
                
                remainder = remainder - 10;
                
            }
            else if(remainder > 4 && remainder < 10)
            {
                
                remainder = remainder - 5;
                
            }
            else
            {
                
                remainder = remainder - 1;
                
            }
    }  
    
   //output the resulting number of coins
    printf("%i\n", counter);

}