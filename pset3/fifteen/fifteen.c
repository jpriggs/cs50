/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();
        
        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }

        // sleep thread for animation's sake
        usleep(500000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
 
void init(void)
{
    // TODO
    int currentTileValue = (d * d) - 1;

    //fill values of the max tile value to 0 in descending order
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            board[i][j] = currentTileValue;
            currentTileValue--;
        }
    }

    int evenCheck = d % 2;

    if(evenCheck == 0)
    {
         //execute swap of values 1 and 2 in the array if d is an even number
         board[d - 1][d - 3] = 1;
         board[d - 1][d - 2] = 2;
    }
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
    // TODO
    //print values from the array into the game board
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            //if a value of zero is encountered in the array, replace it with an underscore _
            if(board[i][j] == 0)
            {
                printf(" _\t");
                continue;
            }
            printf("%2i\t", board[i][j]);
        }
        printf("\n\n");
    }
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    // TODO
    int tileXPosition;
    int tileYPosition;
    int blankXPosition;
    int blankYPosition;
    
    //linear search for the user inputted tile number and blank array locations
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            if(board[i][j] == tile)
            {
                tileXPosition = i;
                tileYPosition = j;
            }
            
            if(board[i][j] == 0)
            {
                blankXPosition = i;
                blankYPosition = j;
            }
        }
    }
    
    //check if both the blank and tile number's X and Y positions have both changed
    if(blankXPosition != tileXPosition && blankYPosition != tileYPosition)
    {
        return false;
    }
    
    int compareX = abs(blankXPosition - tileXPosition);
    int compareY = abs(blankYPosition - tileYPosition);
    
    //check if either the blank or tile number's X and Y position have moved more than 1 index
    if(compareX > 1 || compareY > 1)
    {
        return false;
    }
    
    //swap the values at the blank and tile number array positions
    board[blankXPosition][blankYPosition] = tile;
    board[tileXPosition][tileYPosition] = 0;
    
    return true;
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    // TODO
    int singleArray[d * d];
    int currentValue;
    int singleArrayEndIndex = d * d - 2;
    
    //fill a single dimensional array with values from the two dimensional array
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            currentValue = board[i][j];
            singleArray[d * i + j] = currentValue;
        }
    }
    
    //iterate through the values in the single dimensional array ignoring the final value, the blank tile
    for(int i = 0; i < singleArrayEndIndex; i++)
    {
        int leftIndexValue = singleArray[i];
        int rightIndexValue = singleArray[i + 1];

        //checks if the left index value is larger than the right index value
        if(leftIndexValue > rightIndexValue)
        {
            return false;
        }
    }
    return true;
}
