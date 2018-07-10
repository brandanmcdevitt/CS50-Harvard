#include <cs50.h>
#include <stdio.h>

float change;
float quarter = .25;
float dime = .10;
float nickel = .05;
float penny = .01;
int count = 0;

int main(void) {
 do {
     change = get_float("Enter change: ");
 } while(change < 0);

while(change >= quarter) {
    count++;
    change -= quarter;
}

while(change >= dime) {
    count++;
    change -= dime;
}

while(change >= nickel) {
    count++;
    change -= nickel;
}

while(change >= penny) {
    count++;
    change -= penny;
}

printf("Number of coins: %i\n", count);

}

