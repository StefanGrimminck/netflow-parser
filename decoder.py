import csv
import ast

reader = {}
with open(r"file", 'r') as f:
    reader = f.read()
    ipdict = ast.literal_eval(reader)


def checker(block1, block2, block3):
    print("Entered method")
    if (block3 in ipdict[block1][block2]):
        print("it works")
    else:
        print("It doesn't work")

checker("129", "125", "0")