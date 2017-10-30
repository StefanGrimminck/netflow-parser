#!/usr/bin/env python
import csv
import sys


PORTLIST = [102,  110,  143,  1911,  20000,  21,  22,  23,  2323,  25,  443,  445,  465,  502,  7547,80 , 8080,  8888,  993,  995]

filename = 'FileName'
with open(filename, newline='') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            row[0] = row[0].strip()
            row[1] = row[1].strip()

            if float(row[1])in PORTLIST:
                with open(row[1] + '.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([row[0]])
    except:
        pass