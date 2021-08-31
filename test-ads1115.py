#!/usr/bin/python3

from ads1115 import ADS1115
import argparse
from llog import LLogWriter
import signal
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

defaultMeta = dir_path + '/ads1115.meta'

parser = argparse.ArgumentParser(description='ads1115 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

log = LLogWriter(args.meta, args.output)

def cleanup(_signo, _stack):
    log.close()
    exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

ads = ADS1115()

LLOG_CH0 = 100

while True:
    for channel in range(4):
        log.log(LLOG_CH0 + channel, ads.read(channel))
        if args.frequency:
            time.sleep(1.0/args.frequency)
