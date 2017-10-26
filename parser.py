#!/usr/bin/env python
import ast
import csv
import os
import sys
import argparse

def nfdumpToCSV(IPRANGETREE, INFILE, OUTFILE, IPvTYPE):
    if (IPvTYPE == '6'):
        command = 'nfdump -6 -r ' + INFILE.name + \
            ' -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)
    elif (IPvTYPE == '4'):
        command = 'nfdump -r  ' + INFILE.name + \
            ' -q -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)

    cleanCSV(IPRANGETREE, OUTFILE)

def ownerChecker(ranges, block1, block2, block3):
    try:
        if (block3 in ranges[block1][block2]):
            return True
    except:
        return False

def cleanCSV(IPRANGETREE, OUTFILE):
    with open(OUTFILE.name + '.RAW', 'r') as inp, open(OUTFILE.name, 'w') as out:
        writer = csv.writer(out)

        reader = {}
        with open(IPRANGETREE.name, 'r') as f:
            reader = f.read()
            ranges = ast.literal_eval(reader)

            for row in csv.reader(inp, delimiter=','):
                row[0] = row[0].strip()

                row[1] = row[1].strip()
                # check if portnumber is lower than 1024
                if 0 < float(row[1]) <= 1024:
                    a, b, c, d = row[0].split('.')

                    if ownerChecker(ranges, a, b, c):
                        writer.writerow(row)

    os.remove(OUTFILE.name + '.RAW')


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Input file",
                        type=argparse.FileType('r'))
    parser.add_argument('outfile', help="Output file",
                        type=argparse.FileType('w'))
    parser.add_argument('rangetree', help="Range tree with addresses",
                        type=argparse.FileType('r'))
    parser.add_argument(
        'ipv', choices=['4', '6'], help='for IPv6 "6" for IPv4 "4"')

    args = parser.parse_args(arguments)
    INFILE = args.infile
    OUTFILE = args.outfile
    IPvTYPE = args.ipv
    IPRANGETREE = args.rangetree

    nfdumpToCSV(IPRANGETREE, INFILE, OUTFILE, IPvTYPE)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
