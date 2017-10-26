#!/usr/bin/env python
import csv
import os
import sys
import argparse
from netaddr import IPNetwork, IPAddress

CIDRLIST = set()

CIDRLIST = {'0.0.0.0/0'}


def nfdumpToCSV(INFILE, OUTFILE, IPvTYPE):
    if (IPvTYPE == '6'):
        command = 'nfdump -6 -r ' + INFILE.name + \
            ' -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)
    elif (IPvTYPE == '4'):
        command = 'nfdump -r  ' + INFILE.name + \
            ' -q -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)

    cleanCSV(OUTFILE)


def cleanCSV(OUTFILE):
    with open(OUTFILE.name + '.RAW', 'r') as inp, open(OUTFILE.name, 'w') as out:
        writer = csv.writer(out)

        for row in csv.reader(inp, delimiter=','):
            ip = row[0].strip()

            portnr = row[1].strip()
                # check if portnumber is lower than 1024
            if 0 < float(portnr) <= 1024:
                a, b, c, d= ip.split('.')

                # if a in a
                    # then if a as key and b in b
                        # then if a s key and b as value in c = c
                print(a +"."+  b +"."+ c +"."+ d)
                ifchecker(a,b,c)
                    writer.writerow(row)


                    #for CIDR in CIDRLIST:
                    #    if IPAddress(row[0]) in IPNetwork(CIDR):
                    #        writer.writerow(row)

    os.remove(OUTFILE.name + '.RAW')


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Input file",
                        type=argparse.FileType('r'))
    parser.add_argument('outfile', help="Output file",
                        type=argparse.FileType('w'))
    parser.add_argument(
        'ipv', choices=['4', '6'], help='for IPv6 "6" for IPv4 "4"')

    args = parser.parse_args(arguments)
    INFILE = args.infile
    OUTFILE = args.outfile
    IPvTYPE = args.ipv

    nfdumpToCSV(INFILE, OUTFILE, IPvTYPE)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
