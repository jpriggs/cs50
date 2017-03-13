#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //ask user for minutes input
    printf("Enter the length of your shower in minutes: ");
    int showerMinutes = get_int();
    
    //output the number of bottles used
    printf("Bottles: %i\n", showerMinutes * 12);
    
}
