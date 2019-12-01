// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: positive_resize_number infile outfile\n");
        return 1;
    }
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            fprintf(stderr, "Usage: positive_resize_number infile outfile\n");
            return 1;
        }
    }
    int n = atoi(argv[1]);
    if (n <= 0 || n > 100)
    {
        fprintf(stderr, "Usage: positive_resize_number infile outfile\n");
        return 1;
    }
    
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

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
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    int inWidth = bi.biWidth;
    int inHeight = bi.biHeight;
    int inpadding = (4 - (inWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int outWidth = inWidth * n;
    int outHeight = inHeight * n;
    bi.biWidth *= n;
    bi.biHeight *= n;

    // determine padding for scanlines
    int outpadding = (4 - (outWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // change size of image
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * outWidth) + outpadding) * abs(outHeight);
    // change total size of file
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(inHeight); i < biHeight; i++)
    {
        RGBTRIPLE triple;
        RGBTRIPLE pixelarr[outWidth];
        // iterate over pixels in scanline
        for (int j = 0; j < inWidth; j++)
        {
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            // write RGB triple to pixelarr n times
            for (int k = 0; k < n; k++)
            {
                pixelarr[k + (n * j)] = triple;
            }
        }
        // write pixelarr n times into outfile
        for (int x = 0; x < n; x++)
        {
            fwrite(pixelarr, sizeof(RGBTRIPLE) * outWidth, 1, outptr);
            // write outfile's padding
            for (int p = 0; p < outpadding; p++)
            {
                fputc(0x00, outptr);
            }
        }
        // skip over infile's padding if any
        fseek(inptr, inpadding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
