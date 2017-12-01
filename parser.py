# --------------------------------------------------------------------------------------------
# Copyright (c) 2017 Stefan Grimminck & Jeroen Janssen. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

#!/usr/bin/env python3

"""A script loads a text file containing IPaddresses and ports.
These are then filtered using a tree with IPaddresses to check if it falls in a desired range.
The IPaddresses and ports are then written to a file."""

# Imports
import argparse
import ast
import csv
import ipaddress
import sys


def ownerchecker(ranges, block1, block2, block3, block4):
    """Function to check if an IPV4 address is found inside the rangetree

    Note:
        This method is only called for IPv4 addresses.

    Args:
        ranges (Dictionary): A dictionary containing a dictionary containing an array.
            This "Tree" contains IPv4 addresses that should be saved
        block1 (int): The first block of a IPv4 address.
        block2 (int): The second block of a IPv4 address.
        block3 (int): The third block of a IPv4 address.
        block4 (int): The fourth block of a IPv4 address.

     Returns:
         True if it should be saved, False otherwise."""
    # This is only used to comply with the Pylint standard, which doesn't allow unused variables.
    block4 = block4
    try:
        # If you don't own all the IPv4 addresses in the fourth block you can update the following line of code to:
        # if block 4 in ranges[block1][block2][block3]:
        if block3 in ranges[block1][block2]:
            return True
    # The KeyError is raised if the IPv4 address isn't found in the tree.
    except KeyError:
        return False


def cleancsv4(rangetree, inputfile, outputfile):
    """Assess for every IPv4 address if it should be saved, and if so write it to a file.

    Args:
        rangetree (Dictionary): A dictionary containing a dictionary containing an array.
            This 'Tree' contains IPv4 addresses that should be saved
        inputfile (file): An input file containing the IPv4 addresses.
        outputfile (file): The file to place the final data in."""
    with open(inputfile, "r") as inp, open(outputfile, "w") as out, open(rangetree, "r") as tree:
        writer = csv.writer(out)
        reader = tree.read()
        ranges = ast.literal_eval(reader)

        for row in csv.reader(inp, delimiter=","):
            row[0] = row[0].strip()
            row[1] = row[1].strip()

            try:
                if 0 < float(row[1]) <= 1024:
                    block1, block2, block3, block4 = row[0].split(".")

                    if ownerchecker(ranges, block1, block2, block3, block4):
                        rows = []

                        if row not in rows:
                            rows.append(row)
                            writer.writerow(row)
            except ValueError:
                pass


def cleancsv6(inputfile, outputfile, iprange):
    with open(inputfile, "r") as inp, open(outputfile, "w") as out:
        writer = csv.writer(out)

        for row in csv.reader(inp, delimiter=","):
            row[0] = row[0].strip()
            row[1] = row[1].strip()
            # check if portnumber is lower than 1024
            if 0 < float(row[1]) <= 1024:
                if ipaddress.ip_address(row[0]) in ipaddress.ip_network(iprange):
                    writer.writerow(row)


def main(arguments):
    # Specify required arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("infile", help="Input file", type=argparse.FileType("r"))
    parser.add_argument("outfile", help="Output file", type=argparse.FileType("w"))
    parser.add_argument("--rangetree", help="Range tree with addresses", type=argparse.FileType("r"))
    parser.add_argument("--ipv6range", help="IPv6 range", type=str)
    parser.add_argument("ipv", choices=["4", "6"], help="for IPv6 '6' for IPv4 '4'")

    # Convert args to usable variables
    args = parser.parse_args(arguments)
    infile = args.infile
    outfile = args.outfile
    ipvtype = args.ipv
    ipv4rangetree = args.rangetree
    ipv6range = args.ipv6range

    # Check if all the correct parameters have been given
    if ipvtype == "4" and infile is not None and outfile is not None and ipv4rangetree is not None:
        cleancsv4(ipv4rangetree.name, infile.name, outfile.name)
    elif ipvtype == "6" and infile is not None and outfile is not None and ipv6range is not None:
        cleancsv6(infile.name, outfile.name, ipv6range)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
