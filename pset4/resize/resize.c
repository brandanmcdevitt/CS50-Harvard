/*
 resize.c
 
 Brandan McDevitt
 Harvard Computer Science 50
 Problem Set 4
 
 Implement a program that resizes BMPs
 */

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy scale infile outfile\n");
        return 1;
    }

    // remember filenames
    int scale = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if (scale < 1 || scale > 100)
    {
        fprintf(stderr, "Range must be within 1...100\n");
        return 5;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bfResized;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfResized = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, biResized;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    biResized = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    //setting the new sizes
    biResized.biWidth = bi.biWidth * scale;
    biResized.biHeight = bi.biHeight * scale;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddingResized = (4 - (biResized.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    biResized.biSizeImage = (biResized.biWidth * sizeof(RGBTRIPLE) + paddingResized) * abs(biResized.biHeight);
    bfResized.bfSize = bf.bfSize - bi.biSizeImage + biResized.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfResized, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biResized, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int j = 0; j < scale; j++)
        {
            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile
                for (int l = 0; l < scale; l++)
                {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // then add it back (to demonstrate how)
            for (int m = 0; m < paddingResized; m++)
            {
                fputc(0x00, outptr);
            }

            if (j < scale - 1)
            {
                fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
            }

        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
