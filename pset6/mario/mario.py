# mario.py

# Brandan McDevitt
# Harvard Computer Science 50
# Problem Set 6

# Port mario.c to python.

from cs50 import get_int

# continuous loop until broken out of
while True:
    height = get_int("Height of pyramid: ")

    # if user input is within 0-23 then break
    if height >= 0 and height <= 23:
        break

# counting backwards from given height to 0
for i in range(height, 0, -1):
    for n in range(0, height + 1):
        if n >= i - 1:
            print("#", end="")
        else:
            print(" ", end="")
    print("")