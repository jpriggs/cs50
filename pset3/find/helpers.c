/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */

//binary search algorithm
bool search(int value, int values[], int n)
{
    //checks if there are any values in the array
    if(n < 1)
    {
        return false;
    }
    
    int indexLower = 0;
    int indexUpper = n - 1;
    int indexPosition;
    
    //loops as long as the last index in the array is larger than the start position in the array on each iteration
    while(indexUpper >= indexLower)
    {
        //sets the index position to the middle index of the array
        indexPosition = indexLower + (int)((indexUpper - indexLower) / 2);
        
        //returns true if a specific value in the array matches the search criteria else changes the search index range
        if(value == values[indexPosition])
        {
            return true;
        }
        else if(value > values[indexPosition])
        {
            indexLower = indexPosition + 1;
        }
        else
        {
            indexUpper = indexPosition - 1;
        }
    }
    return false;
}

/**
 * Sorts array of n values.
 */

//bubble sort
void sort(int values[], int n)
{
    // TODO: implement an O(n^2) sorting algorithm
    
    int endIndex = n - 1;
    int swapCounter;
    //loop while swaps still need to occur
    do
    {
        swapCounter = 0;

        //iterate through the values in the array
        for(int i = 0; i < endIndex; i++)
        {
            int leftIndexValue = values[i];
            int rightIndexValue = values[i + 1];

            //check if the current index position and the position right of it need swapping
            if(rightIndexValue < leftIndexValue)
            {
                values[i] = rightIndexValue;
                values[i + 1] = leftIndexValue;
                swapCounter++;
            }
        }
    }
    while(swapCounter > 0);

    return;
} 
