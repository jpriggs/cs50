#include <cs50.h>
#include <stdio.h>

int main(void)
{
    
    int i, j, k;
    int height;
    
    do
    {
    
    //checks if used entered number is valid
     printf("Enter a height: ");
     height = get_int();
     
    }
     while(height > 23 || height < 0); 
    
    //loop the user height input
    for(i = 0; i < height; i++)
    {
        //output space characters left side
        for(j = 0; j < height - 1 - i; j++)
        {
            
            printf(" ");
            
        }    
        
        //output hash characters left side
        for(k = 0; k < i + 1; k++)
        {
            
            printf("#");
            
        }    
        
        //output space characters between pyramids
        printf("  ");
        
        //output hash characters right side
        for(k = 0; k < i + 1; k++)
        {
            
            printf("#");
            
        }    
    
        printf("\n");
    }
}