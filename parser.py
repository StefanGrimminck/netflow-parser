#!/usr/bin/env python
import csv
import os
import sys
import argparse
import ipaddress
from netaddr import IPNetwork, IPAddress

CIDRLIST = set()

CIDRLIST = {'IPLIST'}


def nfdumpToCSV(INFILE, OUTFILE, IPvTYPE):
    if (IPvTYPE == '6'):
        command = 'nfdump -6 -r ' + INFILE.name + \
            ' -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)
    elif (IPvTYPE == '4'):
        command = 'nfdump -r ' + INFILE.name + \
            ' -o "fmt:%da,%dp" > ' + OUTFILE.name + '.RAW'
        os.system(command)

    cleanCSV(OUTFILE)


def cleanCSV(OUTFILE):
    with open(OUTFILE.name + '.RAW', 'r') as inp, open(OUTFILE.name, 'w') as out:
        writer = csv.writer(out)

        for row in csv.reader(inp, delimiter=','):
            row[0] = row[0].strip()

            try:
                # check for valid IP address
                ipaddress.ip_address(row[0])
                row[1] = row[1].strip()
                # check if portnumber is lower than 1024
                if 0 < float(row[1]) <= 1024:
                    for CIDR in CIDRLIST:
                        if IPAddress(row[0]) in IPNetwork(CIDR):
                            writer.writerow(row)
            except:
                pass
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
