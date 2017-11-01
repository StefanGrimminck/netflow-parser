#!/usr/bin/env python
import ast
import csv
import os
import sys
import argparse
import ipaddress


def nfdumpToCSV(IPRANGETREE, INFILE, OUTFILE, IPvTYPE, IPV6RNG):
    if (IPvTYPE == '6'):
        command = 'nfdump -6 -r ' + INFILE.name + \
                  ' -q -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)
    elif (IPvTYPE == '4'):
        command = 'nfdump -r  ' + INFILE.name + \
                  ' -q -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)

    cleanCSV(IPRANGETREE, OUTFILE, IPvTYPE, IPV6RNG)


def ownerChecker(ranges, block1, block2, block3):
    try:
        if (block3 in ranges[block1][block2]):
            return True
    except:
        return False


def cleanCSV(IPRANGETREE, OUTFILE, IPvTYPE, IPV6RNG):
    with open(OUTFILE.name + '.RAW', 'r') as inp, open(OUTFILE.name, 'w') as out:
        writer = csv.writer(out)

        if (IPvTYPE == '4'):

            rows = [] #list used to check for duplicates
            with open(IPRANGETREE.name, 'r') as f:
                reader = f.read()
                ranges = ast.literal_eval(reader)

                for row in csv.reader(inp, delimiter=','):
                    ip = row[0].strip()

                    portnr = row[1].strip()
                    # check if portnumber is lower than 1024
                    if 0 < float(portnr) <= 1024:
                        a, b, c, d = ip.split('.')

                        if ownerChecker(ranges, a, b, c):
                            if row not in rows:
                                rows.append(row)
                                writer.writerow(row)

        elif (IPvTYPE == '6'):
            for row in csv.reader(inp, delimiter=','):
                row[0] = row[0].strip()
                row[1] = row[1].strip()
                # check if portnumber is lower than 1024
                if 0 < float(row[1]) <= 1024:
                    if ipaddress.ip_address(row[0]) in ipaddress.ip_network(IPV6RNG):
                        writer.writerow(row)

    os.remove(OUTFILE.name + '.RAW')


def main(arguments):
    parser = argparse.ArgumentParser( description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile',                  help="Input file",                  type=argparse.FileType('r'))
    parser.add_argument('outfile',                 help="Output file",                 type=argparse.FileType('w'))
    parser.add_argument('--rangetree',             help="Range tree with addresses",   type=argparse.FileType('r'))
    parser.add_argument('--ipv6range',             help="IPv6 range",                  type=str)
    parser.add_argument('ipv', choices=['4', '6'], help='for IPv6 "6" for IPv4 "4"')

    args = parser.parse_args(arguments)
    INFILE = args.infile

    OUTFILE = args.outfile
    IPvTYPE = args.ipv
    IPRANGETREE = args.rangetree
    IPV6RNG = args.ipv6range

    nfdumpToCSV(IPRANGETREE, INFILE, OUTFILE, IPvTYPE, IPV6RNG)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
