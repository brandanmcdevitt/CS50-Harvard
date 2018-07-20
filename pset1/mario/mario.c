#include <stdio.h>
#include <cs50.h>

int height; //user input variable

int main(void)
{
do
{
height = get_int("Height of pyramid: "); //prompting the user for input
}
while (height < 0 || height > 23); //validation for input

for (int i = height; i >= 1; i--)
{
    for (int n = 0; n <= height; n++)
        {
            if (n >= i - 1)
            {
                printf("#"); //print the hashes
            }
            else
            {
                printf(" "); //print the spaces
            }

        }
        printf("\n"); //print newline
    }

}