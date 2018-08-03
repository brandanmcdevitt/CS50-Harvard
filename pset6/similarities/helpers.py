# helpers.py

# Brandan McDevitt
# Harvard Computer Science 50
# Problem Set 6

# Implement a program that compares two files for similarities.

from nltk.tokenize import sent_tokenize


def similar(a, b):
    """Return similar data from both a and b, passing over duplicate items"""
    stored = []

    for i in range(len(a)):
        for j in range(len(b)):
            # if a at index i equals b at index j
            if a[i] == b[j]:
                # and if stored does not contain a[i]
                if a[i] not in stored:
                    # append a[i] to stored
                    stored.append(a[i])
    return stored


def extractSub(a, n, arr):
    """Extract the substring from the input and append them to a list"""
    for i in range(len(a)):
        # if the length of a equals n, append to arr
        if len(a) == n:
            arr.append(a[i:n + i])
            break
        elif len(a) <= n:
            break
        elif len(a[i:n + i]) < n:
            break
        else:
            arr.append(a[i:n + i])
    return arr


def lines(a, b):
    """Return lines in both a and b"""

    # split the file by lines
    file1 = a.splitlines()
    file2 = b.splitlines()

    # TODO
    return similar(file1, file2)


def sentences(a, b):
    """Return sentences in both a and b"""

    # split the file by natural language sentences
    file1 = sent_tokenize(a)
    file2 = sent_tokenize(b)

    # TODO
    return similar(file1, file2)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # create lists to append the substrings to
    temp1 = []
    temp2 = []
    sub1 = []
    sub2 = []

    sub1 = extractSub(a, n, temp1)
    sub2 = extractSub(b, n, temp2)

    # TODO
    return similar(sub1, sub2)