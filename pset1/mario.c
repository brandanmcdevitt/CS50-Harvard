#include <stdio.h>
#include <cs50.h>

int height;

int main(void) {

do {
    height = get_int("Height of pyramid: ");
} while (height < 0 || height > 23);

for(int i = height; i >= 1; i--) {
        for(int n = 0; n <= height; n++)
            if(n >= i - 1)
                printf("#");
            else
                printf(" ");

        printf("\n");
    }

}