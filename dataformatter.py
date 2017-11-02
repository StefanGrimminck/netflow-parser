#!/usr/bin/env python
import csv
import sys
import os
import argparse


def sortOnPorts(INFILE):
    PORTLIST = [102,  110,  143,  1911,  2000,  21,  22,  23,  2323,  25,  443,  445,  465,  502,  7547, 80 , 8080,  8888,  993,  995]
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

                    with open('/tmp/' + row[1] + '.csv', 'a', newline='') as csvfile: #files saved as /tmp/PORTNR.csv
                        writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([row[0]])
        except:
            pass

        foundPorts.sort()
    return foundPorts

def portToScanType(argument):
    switcher = {

        102: 'sudo zmap -p 102 --whitelist-file=/tmp/102.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/102.csv | zgrab --senders=2500 --timeout=10 --port=102 --s7 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/102-s7-szl-full_ipv4.json;',
        110: 'sudo zmap -p 110 --whitelist-file=/tmp/110.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/110.csv | zgrab --senders=2500 --timeout=5 --port=110 --starttls --banners --pop3 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/110-pop3-starttls-full_ipv4.json;',
        143: 'sudo zmap -p 143 --whitelist-file=/tmp/143.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/143.csv | zgrab --senders=2500 --timeout=5 --port=143 --starttls --banners --imap --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/143-imap-starttls-full_ipv4.json;',
        1911: 'sudo zmap -p 1911 --whitelist-file=/tmp/1911.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/1911.csv | zgrab --senders=2500 --timeout=5 --port=1911 --fox --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/1911-fox-device_id-full_ipv4.json;',
        2000: 'sudo zmap -p 2000 --whitelist-file=/tmp/2000.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/NAME.csv | zgrab --senders=2500 --timeout=15 --port=20000 --dnp3 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/20000-dnp3-status-full_ipv4.json;',
        21: 'sudo zmap -p 21 --whitelist-file=/tmp/21.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/21.csv | zgrab --senders=2500 --timeout=5 --port=21 --banners --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/21-ftp-banner-full_ipv4.json;',
        22: 'sudo zmap -p 22 --whitelist-file=/tmp/22.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/22.csv | zgrab --senders=2500 --timeout=5 --port=22 --xssh --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/22-ssh-v2-full_ipv4.json;',
        23: 'sudo zmap -p 23 --whitelist-file=/tmp/23.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/23.csv | zgrab --senders=2500 --timeout=5 --port=23 --telnet --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/23-telnet-banner-full_ipv4.json;',
        2323: 'sudo zmap -p 2323 --whitelist-file=/tmp/2323.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/2323.csv | zgrab --senders=2500 --timeout=5 --port=2323 --telnet --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/2323-telnet-banner-full_ipv4.json;',
        25: 'sudo zmap -p 25 --whitelist-file=/tmp/25.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/25.csv | zgrab --senders=2500 --timeout=5 --port=25 --starttls --banners --smtp --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/25-smtp-starttls-full_ipv4.json;',
        443: 'sudo zmap -p 443 --whitelist-file=/tmp/443.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/443.csv | zgrab --senders=2500 --timeout=5 --port=443 --tls --export-dhe-ciphers --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/443-https-dhe_export-full_ipv4.json; sudo zmap -p 443 --whitelist-file=/tmp/443.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/443_1.csv | zgrab --senders=2500 --timeout=5 --port=443 --tls --dhe-ciphers --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/443-https-dhe-full_ipv4.json; sudo zmap -p 443 --whitelist-file=/tmp/443.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/443_2.csv | zgrab --senders=2500 --timeout=5 --port=443 --tls --export-ciphers --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/443-https-rsa_export-full_ipv4.json; sudo zmap -p 443 --whitelist-file=/tmp/443.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/443_3.csv | zgrab --senders=2500 --timeout=5 --port=443 --tls --heartbleed --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/443-https-heartbleed-full_ipv4.json; sudo zmap -p 443 --whitelist-file=/tmp/443.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/443_4.csv | zgrab --senders=2500 --timeout=5 --ca-file=/etc/nss-root-store.pem --port=443 --tls --chrome-ciphers --tls-session-ticket --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/443-certificates-and-chrome-ciphers.json; sudo zmap -p 443 --whitelist-file=/tmp/443.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/443_5.csv | zgrab --senders=2500 --timeout=5 --tls-version=sslv3 --port=443 --tls --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/443-https-ssl_3-full_ipv4.json;',
        445: 'sudo zmap -p 445 --whitelist-file=/tmp/445.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/445_6.csv | zgrab --senders=2500 --timeout=5 --port=445 --smb --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/445-smb-banner-full_ipv4.json;',
        465: 'sudo zmap -p 465 --whitelist-file=/tmp/465.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/465_7.csv | zgrab --senders=2500 --timeout=5 --port=465 --tls --banners --smtp --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/465-smtps-tls-full_ipv4.json;',
        502: 'sudo zmap -p 502 --whitelist-file=/tmp/502.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/502.csv | zgrab --senders=2500 --timeout=5 --port=502 --modbus --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/502-modbus-device_id-full_ipv4.json;',
        7547: 'sudo zmap -p 7547 --whitelist-file=/tmp/7547.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/7547.csv | zgrab --http-max-size=64--http=/ --senders=2500 --timeout=5 --port=7547 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/7547-cwmp-get-full_ipv4.json;',
        80: 'sudo zmap -p 80 --whitelist-file=/tmp/80.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/80.csv | zgrab --http-max-size=64 --http=/ --http-max-redirects=5 --port=80 --timeout=5 --follow-localhost-redirects=False --senders=1000 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/80-http-get-full_ipv4.json;',
        8080: 'sudo zmap -p 8080 --whitelist-file=/tmp/8080.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/8080.csv | zgrab --http-max-size=64 --http=/ --http-max-redirects=5 --port=8080 --timeout=5 --follow-localhost-redirects=False --senders=1000 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/8080-http-get-full_ipv4.json;',
        8888: 'sudo zmap -p 8888 --whitelist-file=/tmp/8888.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/8888csv | zgrab --http-max-size=64--http=/ --http-max-redirects=5 --port=8888 --timeout=5 --follow-localhost-redirects=False --senders=1000 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/8888-http-get-full_ipv4.json;',
        993: 'sudo zmap -p 993 --whitelist-file=/tmp/993.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/993.csv | zgrab --senders=2500 --timeout=5 --port=993 --tls --banners --imap --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/993-imaps-tls-full_ipv4.json; sudo zmap -p 993 --whitelist-file=/tmp/993.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/993_2.csv | zgrab --senders=2500 --timeout=5 --port=993 --tls --export-dhe-ciphers --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/993-imaps-dhe_export-full_ipv4.json;',
        995: 'sudo zmap -p 995 --whitelist-file=/tmp/995.csv | sudo ztee /home/ubuntu/results-netflow/$(date +%Y%m%d)/995.csv | zgrab --senders=2500 --timeout=5 --port=995 --tls --banners --pop3 --output-file=/home/ubuntu/scanresults-netflow/$(date +%Y%m%d)/995-pop3s-tls-full_ipv4.json;',

    }
    return switcher.get(argument, "error")

def initScan(portlist):

    os.system('mkdir scanresults-netflow/$(date +%Y%m%d)/')
    os.system('mkdir results-netflow/$(date +%Y%m%d)/')
    os.system('ulimit -n 4096;')

    for port in portlist:
        os.system(portToScanType(port))






def main(arguments):
    parser = argparse.ArgumentParser( description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile',                  help="Input file",                  type=argparse.FileType('r'))


    args = parser.parse_args(arguments)
    INFILE = args.infile
    portlist = sortOnPorts(INFILE)
    initScan(portlist)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
