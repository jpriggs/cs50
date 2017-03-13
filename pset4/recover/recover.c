#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t  BYTE;

// defines the size in bytes of each block
#define BLOCK 512

int main(int argc, char *argv[])
{
    // ensure correct number of command line arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // remember input file name
    char *inputFile = argv[1];
    
    // open input file
    FILE *inptr = fopen(inputFile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", inputFile);
        return 2;
    }

    BYTE buffer[BLOCK];
    FILE *outputFile = NULL;
    char ouputFileName[8];
    int outputFileCounter = 0;
    
    // loop through each 512 byte block until a block less 512 bytes is reached, that is the end of file marker
    while (fread(buffer, BLOCK, 1, inptr) == 1)
    {
        // if a JPEG signature is read, print each block until the next JPEG signature is read
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if a file is already open, close it
            if (outputFile != NULL)
            {
                fclose(outputFile);
                outputFile = NULL;
            }
            
            // create a file name from 000.jpg and increment the file number on each loop
            sprintf(ouputFileName, "%03i.jpg", outputFileCounter++);
            
            // opens the output file for writing
            outputFile = fopen(ouputFileName, "w");
            
            // writes each block read to an output file
            fwrite(buffer, BLOCK, 1, outputFile);
        }
        else
        {
            // if the end of file block is detected, add the data to the final JPEG file
            if (outputFile != NULL)
            {
                fwrite(buffer, BLOCK, 1, outputFile);
            }
        }
    }
    // close the input and output files
    fclose(outputFile);
    fclose(inptr);
    
    // return a successful run to the terminal
    return 0;
}