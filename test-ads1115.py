#!/usr/bin/python3

from ads1115 import ADS1115
import argparse
import time

parser = argparse.ArgumentParser(description='ads1115 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

ads = ADS1115()

if args.output:
    outfile = open(args.output, "w")

while True:
    for channel in range(4):
        output = f"{time.time()} 1 {channel} {ads.read(channel)}"
        print(output)
        if args.output:
            outfile.write(output)
            outfile.write('\n')
        if args.frequency:
            time.sleep(1.0/args.frequency)

# this is never reached, but works anyway in practice
# todo handle KeyboardInterrupt for ctrl+c
if args.output:
    outfile.close()
