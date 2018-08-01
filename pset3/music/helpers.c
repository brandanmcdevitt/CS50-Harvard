/*
 helpers.c
 
 Brandan McDevitt
 Harvard Computer Science 50
 Problem Set 3
 
 Convert musical notes to frequencies.
 */

#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include "helpers.h"
#include <math.h>

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator = fraction[0] - '0'; //'top' number
    int denominator = fraction[2] - '0'; //'bottom' number

    return 8 * numerator / denominator;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int octave;
    int n = 0;

    if (strlen(note) == 3)
    {
        octave = atoi(&note[2]);
        char accidental = note[1];

        switch (accidental) //switch statement for raising or lowering the pitch depending on sharp/flat
        {
            case '#':
            n += 1;
            break;
            case 'b':
            n -= 1;
            break;
        }
    }
    else
    {
        octave = atoi(&note[1]);
    }

    char letter = note[0];

    switch (letter)
    {
        case 'A':
        n += 0;
        break;
        case 'B':
        n += 2;
        break;
        case 'C':
        n -= 9;
        break;
        case 'D':
        n -= 7;
        break;
        case 'E':
        n -= 5;
        break;
        case 'F':
        n -= 4;
        break;
        case 'G':
        n -= 2;
        break;
    }

    n += (octave-4) * 12;

    float power = n/12.;
    float f = round(pow(2, power)*440);

    return f;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strcmp(s, "") == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }

}
