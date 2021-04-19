#!/usr/bin/python3

import argparse
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='ads1115 test')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--output', action='store', type=str, required=True)
args = parser.parse_args()

data = pd.read_csv(args.input, header=None, sep=' ')
data.rename(columns={0:"Timestamp", 1:"Log_Type"}, inplace=True)
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
print(data.head())

measurements = pd.DataFrame(data=data.query('Log_Type == 1'))
measurements.rename(columns={2: "Channel", 3: "Voltage"}, inplace=True)
ch0 = pd.DataFrame(data=measurements.query('Channel == 0'))
ch1 = pd.DataFrame(data=measurements.query('Channel == 1'))
ch2 = pd.DataFrame(data=measurements.query('Channel == 2'))
ch3 = pd.DataFrame(data=measurements.query('Channel == 3'))
ch0['Voltage'] *= 2
ch1['Voltage'] *= 2
ch3['Voltage'] *= 11
ch2.rename(columns={3:'Current'}, inplace=True)
ch2['Current'] -= 0.33
ch2['Current'] *= 37.8788
print(ch0.head())
print(ch1.head())
print(ch2.head())
print(ch3.head())




