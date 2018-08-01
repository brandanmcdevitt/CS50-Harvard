# vigenere.py

# Brandan McDevitt
# Harvard Computer Science 50
# Problem Set 6

# Port vigenere.c to python.

from cs50 import get_string
from sys import argv

# check input to make sure that the user entered a valid key
if len(argv) != 2:
    print("Incorrect usage. Try again. \ni.e. python vigenere.py <key>")
    exit(1)
else:
    for letter in range(len(argv[1])):
        if argv[1][letter].isalpha() == False:
            print("Incorrect usage. Try again. \n<key> must be alphabetical")
            exit(1)

key = []

# loop through the characters in the key and append them to the key[] list
for character in argv[1]:
    if character.isupper():
        character = (ord(character)) - (ord('A'))
        key.append(character)
    elif character.islower():
        character = (ord(character)) - (ord('a'))
        key.append(character)

# getting the length of the key
keyLength = len(key)

# prompt user for the message
message = get_string("Enter your message to be encrypted: ")

print("ciphertext: ", end="")

character = 0
i = 0

# loop through the characters in the message and replace the value dependent on the key
for character in message:

    # validate whether the character is alphabetical
    if character.isalpha():
        # check if the character is uppercase
        if character.isupper():
            character = ((ord(character) - ord('A') + (key[i])) % 26) + ord('A')
            print(chr(character), end = "")
        # check if the character is lowercase
        elif character.islower():
            character = ((ord(character) - ord('a') + (key[i])) % 26) + ord('a')
            print(chr(character), end = "")
    else:
        print(character, end="")

    i = (i + 1) % keyLength

print("")