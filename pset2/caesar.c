/*
 caesar.c
 
 Brandan McDevitt
 Harvard Computer Science 50
 Week 2 Problem Set
 
 Implement a program that encrypts messages using Caesar’s cipher.
 */

#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

//declaring variables
int key;
string message;

int main(int argc, string argv[])
{
    //if input count == 2 then run this code block
    if (argc == 2)
    {
        //converting the key to an int
        key = atoi(argv[1]);

        do
        {
            //prompting the user for a message
            message = get_string("Enter your message: ");
        }

        while (message < 0);

        printf("ciphertext: ");

        for (int i = 0; i < strlen(message); i++)
        {
            //if the character is alphabetical, enter this block
            if (isalpha(message[i]))
            {
                //if the character is uppercase
                if (isupper(message[i]))
                {
                    printf("%c", (((message[i] + key) - 65) % 26) + 65);
                }
                //else if the character is lowercase
                else if (islower(message[i]))
                {
                    printf("%c", (((message[i] + key) - 97) % 26) + 97);
                }
            }
            //if the character is non alphabetical, print the character
            else
            {
                printf("%c", message[i]);
            }

        }

        printf("\n");
    }
    //if the user entered more than 1 key
    else
    {
        printf("You may only enter 1 key.\n");
        return 1;
    }
}
