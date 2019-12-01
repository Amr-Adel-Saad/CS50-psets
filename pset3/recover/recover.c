#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check if user ran the program with one command line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image containing JPEGs\n");
        return 1;
    }
    
    char *file = argv[1];
    
    // check if user provided a valid readable file
    FILE *fptr = fopen(file, "r");
    if (fptr == NULL)
    {
        fclose(fptr);
        fprintf(stderr, "Could not open %s.\n", file);
        return 2;
    }
    
    // declare a character string that can contain 7 chars + NULL char
    char filename[8];
    
    // initialize jpgcount which tracks the number of created jpg files
    int jpgcount = 0;
    
    // declare buffer that represents a block of 512 bytes
    BYTE bytesarr[512];
    
    // initialize jpg's pointer to NULL value
    FILE *imgptr = NULL;
    
    // read blocks, each of 512 bytes, through user provided file until EOF
    while (fread(bytesarr, 512, 1, fptr) != 0)
    {
        // check if block is a start of a JPEG
        if (bytesarr[0] == 0xff && bytesarr[1] == 0xd8 && bytesarr[2] == 0xff && (bytesarr[3] & 0xf0) == 0xe0)
        {
            // check if we already found a JPEG
            if (jpgcount > 0)
            {
                // close jpg file
                fclose(imgptr);
            }
            // open new jpg file
            sprintf(filename, "%03i.jpg", jpgcount);
            imgptr = fopen(filename, "w");
            if (imgptr == NULL)
            {
                fclose(imgptr);
                return 3;
            }
            // write block into jpg file
            fwrite(bytesarr, 512, 1, imgptr);
            // increment jpgcount
            jpgcount++;
        }
        
        // block is not a start of a JPEG then check if we already found a JPEG
        else if (jpgcount > 0)
        {
            // write block into jpg file
            fwrite(bytesarr, 512, 1, imgptr);
        }
    }
    
    // close input file
    fclose(fptr);
    // close jpg file(ensuring jpg files are all closed)
    fclose(imgptr);
}
