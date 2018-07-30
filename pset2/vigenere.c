/*
 vigenere.c
 
 Brandan McDevitt
 Harvard Computer Science 50
 Week 2 Problem Set
 
 Implement a program that encrypts messages using Vigenère’s cipher.
 */

#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

//declaring variables
string key;
string message;
int kLength;

int main(int argc, string argv[])
{
    //if the input count is not equal to 2 then inform the user and end
    if (argc != 2)
    {
        printf("Incorrect usage. Try again.\n");
        printf("./vigenere key\n");
        return 1;
    }
    //else if the count is equal to 2 but there are non alphabetical letters, inform the user and end
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (isalpha(argv[1][i]) == false)
            {
                printf("Incorrect usage. Try again.\n");
                printf("Key must be alphabetical.\n");
                return 1;
            }
        }
    }

    //assigning the key and length of the key to variables
    key = argv[1];
    kLength = strlen(key);

    //storing the message from the user
    message = get_string("Enter your message to be encrypted: ");

    printf("ciphertext: ");

    //a loop for going through each character and replacing it with the encrypted letter
    for (int i = 0, j = 0; i < strlen(message); i++)
    {
        int letterKey = tolower(key[j % kLength]) - 'a';

        if (isupper(message[i]))
        {
            printf("%c", 'A' + (message[i] - 'A' + letterKey) % 26);

            j++;
        }
        else if (islower(message[i]))
        {
            printf("%c", 'a' + (message[i] - 'a' + letterKey) % 26);
            j++;
        }
        else
        {
            printf("%c", message[i]);
        }
    }

    printf("\n");

    return 0;

}
