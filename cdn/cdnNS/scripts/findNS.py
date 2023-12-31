 # To run, pyhton dns.py list1m.csv > filetowriteIn

import os
import sys
import subprocess
import time
import tldextract


def main():

    filename = sys.argv[1]
    output = sys.argv[2]

    start = int(sys.argv[3])
    entries = int (sys.argv[4])
    f = open(filename, 'r')
    of = open(output,"w")
    count = 0
    for line in f:
        result = "" 
        try:
            print(count)
            if count >= start + entries:
                break
            if count >= start:
                line = line.strip('\n').split(",")
                cdn = line[0]
                cnames = line[1].split(" ")
                for line in cnames:
                    output = subprocess.check_output(['dig', line])
                    output = str(output,"utf-8")
                    if("NXDOMAIN" in output):
                        of.write((f"{cdn},{line},NXDOMAIN\n"))
                    elif("SERVFAIL" in output):
                        # print (f"{line},SERVFAIL")
                        output = subprocess.check_output(['dig', "@8.8.8.8",line])
                        output = str(output,"utf-8")
                        if("NXDOMAIN" in output):
                            of.write((f"{cdn},{line},NXDOMAIN\n"))
                        if("SERVFAIL" in output):
                            of.write(f"{cdn},{line},SERVFAIL\n")
                    else:
                        output = subprocess.check_output(['dig', "ns","@8.8.8.8",line])
                        output = str(output,"utf-8")

                        if("ANSWER: 0" in output):
                            tld = tldextract.extract(line)
                            domain = tld.domain + "." + tld.suffix
                            output = subprocess.check_output(['dig', "ns","@8.8.8.8",domain])
                            output = str(output,"utf-8")
                                                    
                        of.write(cdn + " " + line + " " + output.replace("\n"," ") + "\n")


                    
                    
            count += 1
        except subprocess.CalledProcessError as e:
            pass



if __name__ == "__main__":
    main()
