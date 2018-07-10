#include <cs50.h>
#include <stdio.h>
#include <math.h>

//declaring variables for change, coins and coin count
float change;
float quarter = 25;
float dime = 10;
float nickel = 5;
float penny = 1;
int count = 0;

int main(void)
{
    do
    {
        change = get_float("Enter change: ");
    }
    while (change < 0); //if change is less than 0 then repeat prompt

    change *= 100; //converting my float to an int to avoid tiny errors along the decimal place
    change = round(change); //round the change to the decimal place

    while (change >= quarter) //check if the quarter can be used
    {
        count++;
        change -= quarter;
    }

    while (change >= dime) //check if the dime can be used
    {
        count++;
        change -= dime;
    }

    while (change >= nickel) //check if the nickel can be used
    {
        count++;
        change -= nickel;
    }

    while (change >= penny) //check if the penny can be used
    {
        count++;
        change -= penny;
    }

    printf("Number of coins: %i\n", count); //print the count

}

