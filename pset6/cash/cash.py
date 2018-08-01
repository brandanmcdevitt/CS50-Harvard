# cash.py

# Brandan McDevitt
# Harvard Computer Science 50
# Problem Set 6

# Port cash.c to python.

from cs50 import get_float

quarter = 25
dime = 10
nickel = 5
penny = 1
count = 0

while True:
    change = get_float("Enter change: ")

    if change > 0:
        break

change *= 100
change = round(change)

while change >= quarter:
    count += 1
    change -= quarter

while change >= dime:
    count += 1
    change -= dime

while change >= nickel:
    count += 1
    change -= nickel

while change >= penny:
    count += 1
    change -= penny

print(count)