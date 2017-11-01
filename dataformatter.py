#!/usr/bin/env python
import csv
import sys
import argparse


def sortOnPorts(INFILE):
    PORTLIST = [102,  110,  143,  1911,  20000,  21,  22,  23,  2323,  25,  443,  445,  465,  502,  7547,80 , 8080,  8888,  993,  995]
    foundPorts = []

    filename = INFILE.name
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                row[0] = row[0].strip()
                row[1] = row[1].strip()
                portnr = float(row[1]) #float because of the outputfile containing 0.0 as a port

                if portnr in PORTLIST:

                    if portnr not in foundPorts:
                        foundPorts.append(int(portnr))

                    with open(row[1] + '.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([row[0]])
        except:
            pass
    return foundPorts



def main(arguments):
    parser = argparse.ArgumentParser( description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile',                  help="Input file",                  type=argparse.FileType('r'))


    args = parser.parse_args(arguments)
    INFILE = args.infile
    portlist = sortOnPorts(INFILE)

    portlist.sort()
    print(portlist)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
