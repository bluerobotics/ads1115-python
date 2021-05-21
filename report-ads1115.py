#!/usr/bin/python3

import argparse
from datetime import datetime
from fpdf import FPDF
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

WIDTH = 210
HEIGHT = 297

file_path = './tmp/'
if not os.path.exists(file_path):
    os.makedirs(file_path)

# TODO Can I put this into a function?
parser = argparse.ArgumentParser(description='ads1115 test')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--output', action='store', type=str, required=True)
args = parser.parse_args()

data = pd.read_csv(args.input, header=None, sep=' ')
data.rename(columns={0: "Timestamp", 1: "Log_Type"}, inplace=True)
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
ch2.rename(columns={'Voltage': 'Current'}, inplace=True)
ch2['Current'] -= 0.33
ch2['Current'] *= 37.8788
print(ch0.head())
print(ch1.head())
print(ch2.head())
print(ch3.head())

configuration = pd.DataFrame(data=data.query('Log_Type == 2'))
configuration.rename(columns={2: 'PGA Gain', 3: 'ODR'}, inplace=True)

errors = pd.DataFrame(data=data.query('Log_Type == 0'))
errors.rename(columns={2: 'Error Message'}, inplace=True)


def generate_table():
    # Calib and errors
    gain_const = None
    odr_const = None
    gain = None
    odr = None
    error_list = None
    ts_list = None

    # TODO - make this simpler?
    if not configuration.empty:
        first_last_config = configuration.iloc[[0, -1]]
        if first_last_config['PGA Gain'].iloc[0] == first_last_config['PGA Gain'].iloc[1]:
            # gain settings unchanged during test
            gain_const = True
            gain = first_last_config['PGA Gain'].iloc[0]
        if first_last_config['ORD'].iloc[0] == first_last_config['ORD'].iloc[1]:
            # odr settings unchanged during test
            odr_const = True
            odr = first_last_config['ORD'].iloc[0]
        else:
            gain_const = False
            odr_const = False

    if not errors.empty:
        error_list = errors['Error Message'].tolist()
        ts_list = errors['Timestamps'].to_list()

    # Measurement table
    mean_3 = round(ch0['Voltage'].mean(), 3)
    mean_5 = round(ch1['Voltage'].mean(), 3)

    min_3 = round(ch0['Voltage'].min(), 3)
    min_5 = round(ch1['Voltage'].min(), 3)

    max_3 = round(ch0['Voltage'].max(), 3)
    max_5 = round(ch1['Voltage'].max(), 3)

    std_3 = round(ch0['Voltage'].std(), 3)
    std_5 = round(ch1['Voltage'].std(), 3)

    return mean_3, mean_5, min_3, min_5, max_3, max_5, std_3, std_5, gain_const, gain, odr_const, odr, error_list, ts_list


def generate_figures(filename=args.output):
    # Plot current vs voltage
    ch3.plot(kind='line', x='Timestamp', y='Voltage', color='#FFA630')
    ax2 = plt.twinx()
    ch2.plot(kind='line', x='Timestamp', y='Current', color='#4DA1A9', ax=ax2)
    ax2.legend(loc="upper left")
    label_fig('Timestamp', 'Current and Voltage', 'Battery Current and Voltage vs Time')

    plt.savefig(fname=file_path+'ads_0.png')
    plt.close()

    # Plot 5V bus
    ch1.plot(kind='line', x='Timestamp', y='Voltage', color='#FFA630')
    label_fig('Timestamp', '5V ', '5V ADC')

    plt.savefig(fname=file_path+'ads_1.png')
    plt.close()

    # Plot 3.3V bus
    ch0.plot(kind='line', x='Timestamp', y='Voltage', color='#FFA630')
    label_fig('Timestamp', '3.3V ', '3.3V ADC')

    plt.savefig(fname=file_path+'ads_2.png')
    plt.close()


def label_fig(x, y, title):
    # TODO - create dict for columns to X and Y axis labels
    plt.title(f"{title}")
    plt.ylabel(f"{y}")
    plt.xlabel(f"{x}")


def table_helper(pdf, epw, th, table_data, col_num):
    for row in table_data:
        for datum in row:
            # Enter data in columns
            pdf.cell(epw/col_num, 2 * th, str(datum), border=1)
        pdf.ln(2 * th)


def init_report(filename=args.output):
    mean_3, mean_5, min_3, min_5, max_3, max_5, std_3, std_5, gain_const, gain, odr_const, odr, error_list, \
        timestamp_list = generate_table()

    config_data = [['', 'PGA Gain', 'ODR'], ['Value', gain, odr], ['Constant Config', gain_const, odr_const]]
    error_data = [timestamp_list, error_list]

    table_data = [['Voltage [V]', 'Mean', 'Min', 'Max', 'Std'], ['3', mean_3, min_3, max_3, std_3],
                  ['5', mean_5, min_5, max_5, std_5]]

    result_data = [[None]] # TODO add the required pass/fails for 9.6 in nav
    pdf = FPDF()
    epw = pdf.w - 2*pdf.l_margin
    pdf.add_page()

    pdf.set_font('Helvetica', '', 10.0)
    th = pdf.font_size

    if None not in result_data:
        pdf.set_font('Helvetica', '', 14.0)
        pdf.cell(WIDTH, 0.0, 'Summary of ADC Test', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, result_data, 3)

    if None not in config_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of ADC Test Configurations', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, config_data, 3)

    pdf.ln(5)

    if None not in error_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of ADC Test Errors', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, error_data, len(error_list))

    pdf.ln(5)

    if None not in table_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of ADC Test Measurements', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, table_data, 5)

    # Add images
    pdf.image("./tmp/ads_2.png", 5, 85, WIDTH/2-10)
    pdf.image("./tmp/ads_1.png", WIDTH/2, 85, WIDTH/2-10)
    pdf.image("./tmp/ads_0.png", 5, 150, WIDTH - 10)

    pdf.output(filename, 'F')


if __name__ == '__main__':
    print("Post-Processing Script")
    generate_table()
    generate_figures()
    init_report()
