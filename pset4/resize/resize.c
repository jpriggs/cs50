/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    //remember command line argument values
    char *number = argv[1];
    char *infile = argv[2];
    char *outfile = argv[3];
    
    //convert char n to an integer
    int n = atoi(number);

    //check if n is a valid positive integer
    if(n <= 0 || n > 100)
    {
        fprintf(stderr, "%i is not a valid number, please enter a value between 1 - 100.\n", n);
        return 1;
    }
    
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 1;
    }

    //determine the read padding for scanlines
    int readPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    int sourceImageWidth = bi.biWidth;
    int sourceImageHeight = bi.biHeight;
    
    //change the width and height values based on the user inputted n value
    bi.biWidth = bi.biWidth *= n;
    bi.biHeight = bi.biHeight *= n;
    
    // determine the write padding for scanlines
    int writePadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    //change the image data size and the total size for the file based on the user inputted n value
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + writePadding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    int resetCursor = sizeof(RGBTRIPLE) * sourceImageWidth;
    
    // iterate over source file's scanlines
    for (int i = 0; i < abs(sourceImageHeight); i++)
    {
        // temporary storage
        RGBTRIPLE triple;
        
        // copy n number of scanlines for each source file row
        for (int m = 0; m < n - 1; m++)
        {
            // iterate over each pixel in the source file's scanline
            for (int j = 0; j < sourceImageWidth; j++)
            {
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
                // write each pixel from the source file's scanline to the output file
                for (int k = 0; k < n; k++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            
            // add padding to the output file if necessary to the end of each scanline
            for (int l = 0; l < writePadding; l++)
            {
                fputc(0x00, outptr);
            }
            
            // reset the source file's cursor position to the beginning of the current row
            fseek(inptr, -resetCursor, SEEK_CUR);
        }
        
        // iterate over each pixel in the source file's scanline
        for (int j = 0; j < sourceImageWidth; j++)
        {
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
              // write each pixel from the source file's scanline to the output file
            for (int k = 0; k < n; k++)
            {
                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }
        
        /// add padding to the output file if necessary to the end of each scanline
        for (int l = 0; l < writePadding; l++)
        {
            fputc(0x00, outptr);
        }
        
        // skip over padding in each scanline in the source file if there is any
        fseek(inptr, readPadding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
