import socket
import argparse
import csv
import sys
from multiprocessing import Pool

def getHostName(ipaddress):
    # Get reverse DNS results and convert tuple to list
    try:
        DNSList = list(socket.gethostbyaddr(ipaddress))
    except:
        return None
        pass

    # Remove empty entries in list
    if DNSList:
        return list(filter(None, DNSList))

def formatOutput(results, ipaddress):
    results = results[:-1]
    results.insert(0, "{\"ip\": \"" + ipaddress + "\",")
    results.insert(1, "\"hostname\": \"" + results[1] + "\"}")
    results.pop(2)

    results = " ".join(str(x) for x in results)
    return results

def csvHandler(inputfile, outputfile):
    with open(inputfile, newline='') as f:
        reader = csv.reader(f)

        try:
            for row in reader:
                ipaddress = row[0].strip()
                results = getHostName(ipaddress)
                if results:
                    with open(outputfile, "a") as outfile:
                        outfile.write(formatOutput(results, ipaddress))
        except:
            pass



def main(arguments):
    parser = argparse.ArgumentParser(description='Program for bulk DNS lookup')
    parser.add_argument('inputfile', help="input file, CSV", type=argparse.FileType('r'))
    parser.add_argument('outputfile', help="output file, JSON", type=argparse.FileType('w'))

    args = parser.parse_args(arguments)
    inputfile = args.inputfile
    outputfile = args.outputfile

    csvHandler(inputfile.name, outputfile.name)



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
