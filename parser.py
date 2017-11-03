# --------------------------------------------------------------------------------------------
# Copyright (c) 2017 Stefan Grimminck & Jeroen Janssen. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

#!/usr/bin/env python3

"""A script which uses nfdump to obtain IPadresses and ports.
These are then filtered using a tree with IPadresses to check if it falls in a desired range.
The IPadresses are then written to a file."""
# Imports
import argparse
import ast
import csv
import ipaddress
import os
import sys

def nfdumptocsv(iprangetree, infile, outfile, ipvtype, ipv6rng):
    """executes a nfdump command on the system and saves the results in a .RAW file.

    Note:
        if ipvtype == 4: The iprangetree must be used.
        if ipvtype == 6: The ipv6rng must be used.

    Args:
        iprangetree (Dictonary, optional): A dictonary containing a dictonary containing an array.
            This 'Tree' contains IPv4 adresses that should be saved
        infile (ncap file): A ncap file containing the data to read.
        outfile (file): The file to place the final data in.
        ipvtype (int): An integer determining if the infile contains IPv4 or IPv6 adresses.
            Only allows 4 or 6 as entries.
        ipv6rng (string, optional): A string containing the IPv6 adresses that should be saved."""

    # Depending on the ipvtype change the command to execute on the system.
    if ipvtype == "4":
        command = "nfdump -r  " + infile.name + \
                  " -q -o 'fmt:%da,%dp' > " + outfile.name + ".RAW"
        os.system(command)
    elif ipvtype == "6":
        command = "nfdump -6 -r " + infile.name + \
                  " -q -o 'fmt:%da,%dp' > " + outfile.name + ".RAW"
        os.system(command)

    cleancsv(iprangetree, outfile, ipvtype, ipv6rng)


def ownerchecker(ranges, block1, block2, block3):
    """Check if the IPv4 adress is a member of the IPv4 adresses provided in the tree.

    Note:
        This method is only called for IPv64 adresses.

    Args:
        ranges (Dictonary): A dictonary containing a dictonary containing an array.
            This 'Tree' contains IPv4 adresses that should be saved
        block1 (int): The first block of a IPv4 adress.
        block2 (int): The second block of a IPv4 adress.
        block3 (int): The third block of a IPv4 adress.

    Returns:
        True if it should be saved, False otherwise."""
    # Checks if the IPv4 adress is contained within the tree.
    try:
        # If you do not own all adresses in the fourth block, update this method to also check for a fourth block.
        if block3 in ranges[block1][block2]:
            return True
    # A KeyError is thrown when the IPv4 adress doesn't match an adress in the tree.
    except KeyError:
        return False


def cleancsv(iprangetree, outfile, ipvtype, ipv6rng):
    """Asses for every IP if it should be saved, and if so write it to a file.

    Args:
        iprangetree (Dictonary, optional): A dictonary containing a dictonary containing an array.
            This 'Tree' contains IPv4 adresses that should be saved
        outfile (file): The file to place the final data in.
        ipvtype (int): An integer determining if the infile contains IPv4 or IPv6 adresses.
            Only allows 4 or 6 as entries.
        ipv6rng (string, optional): A string containing the IPv6 adresses that should be saved."""
    # Open the .RAW file created in the nfdumptocsv method and write the final data to the output file.
    with open(outfile.name + ".RAW", "r") as inp, open(outfile.name, "w") as out:
        writer = csv.writer(out)

        # Execute this statement only when processing IPv4 adresses.
        if ipvtype == "4":
            # list used to check for duplicates
            rows = []
            with open(iprangetree.name, "r") as tree:
                reader = tree.read()
                ranges = ast.literal_eval(reader)

                for row in csv.reader(inp, delimiter=","):
                    ip4 = row[0].strip()

                    portnr = row[1].strip()
                    # check if portnumber is lower than 1024
                    if 0 < float(portnr) <= 1024:
                        # Only save the first three integers of the IPv4. The fourth one isn't neccessary if you own everything in the fourth block.
                        block1, block2, block3 = ip4.split(".")

                        if ownerchecker(ranges, block1, block2, block3):
                            if row not in rows:
                                rows.append(row)
                                writer.writerow(row)

        # Execute this statement only when processing IPv6 adresses.
        elif ipvtype == "6":
            for row in csv.reader(inp, delimiter=","):
                row[0] = row[0].strip()
                row[1] = row[1].strip()
                # check if portnumber is lower than 1024
                if 0 < float(row[1]) <= 1024:
                    if ipaddress.ip_address(row[0]) in ipaddress.ip_network(ipv6rng):
                        writer.writerow(row)

    # Delete the RAW file since it's no longer neccessary.
    os.remove(outfile.name + ".RAW")


def main(arguments):
    """Main method containing the argumentparser and initial setup.

    Args:
        arguments(list): Contains all the arguments added on the start of the script."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("infile", help="Input file", type=argparse.FileType("r"))
    parser.add_argument("outfile", help="Output file", type=argparse.FileType("w"))
    parser.add_argument("--rangetree", help="Range tree with addresses", type=argparse.FileType("r"))
    parser.add_argument("--ipv6range", help="IPv6 range", type=str)
    parser.add_argument("ipv", choices=["4", "6"], help="for IPv6 '6' for IPv4 '4'")

    args = parser.parse_args(arguments)
    infile = args.infile
    outfile = args.outfile
    ipvtype = args.ipv
    iprangetree = args.rangetree
    ipv6rng = args.ipv6range

    nfdumptocsv(iprangetree, infile, outfile, ipvtype, ipv6rng)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
