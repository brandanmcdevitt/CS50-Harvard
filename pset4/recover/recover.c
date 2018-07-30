/*
 recover.c
 
 Brandan McDevitt
 Harvard Computer Science 50
 Week 4 Problem Set
 
 Implement a program that recovers JPEGs from a forensic image.
 */

#include <stdio.h>
 #include <stdint.h>

 int main()
 {
    int blockSize = 512;
    FILE *file;
    FILE *fw = NULL;
    uint8_t buffer[512];
    int count = 0;

    if ((file = fopen("card.raw", "r")) == NULL)
    {
        printf("Error opening file.");
        return 1;
    }

    // Iterate over file contents
    while (fread(buffer, blockSize, 1, file))
    {
        //check for jpg leading signature
        if (buffer[0] == 0xff
            && buffer[1] == 0xd8
            && buffer[2] == 0xff
            && (buffer[3] == 0xe0 || buffer[3] == 0xe1))
        {
            // Close the file, if it is opened
            if (fw != NULL)
                fclose(fw);

            char filename[8];
            sprintf(filename, "%03d.jpg", count);

            // Open a new JPEG file for writing
            fw = fopen(filename, "w");

            count++;
        }

        if (fw != NULL)
            fwrite(buffer, blockSize, 1, fw);
    }

    if (fw != NULL)
        fclose(fw);

    fclose(file);

    return 0;
 }
