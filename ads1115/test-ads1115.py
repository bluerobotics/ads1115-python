#!/usr/bin/python3

from ads1115 import ADS1115
import argparse
from llog import LLogWriter
import time
from pathlib import Path

device = "ads1115"
defaultMeta = Path(__file__).resolve().parent / f"{device}.meta"

parser = argparse.ArgumentParser(description=f'{device} test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

with LLogWriter(args.meta, args.output) as log:
    ads = ADS1115()

    LLOG_CH0 = 100

    while True:
        for channel in range(4):
            log.log(LLOG_CH0 + channel, ads.read(channel))
            if args.frequency:
                time.sleep(1.0/args.frequency)
