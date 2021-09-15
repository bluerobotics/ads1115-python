#!/usr/bin/python3

import matplotlib.pyplot as plt

def generate_figures(log):
    footer = 'ads1115 test report'

    f, spec = log.figure(height_ratios=[1,1], suptitle='ads1115 data', footer=footer)
    plt.subplot(spec[0,0])
    log.channel0.pplot()

    plt.subplot(spec[0,1])
    log.channel1.pplot()

    plt.subplot(spec[1,0])
    log.channel2.pplot()

    plt.subplot(spec[1,1])
    log.channel3.pplot()

if __name__ == '__main__':
    import argparse
    from llog import LLogReader
    from matplotlib.backends.backend_pdf import PdfPages
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))

    defaultMeta = dir_path + '/ads1115.meta'
    parser = argparse.ArgumentParser(description='ads1115 test report')
    parser.add_argument('--input', action='store', type=str, required=True)
    parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
    parser.add_argument('--output', action='store', type=str)
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    log = LLogReader(args.input, args.meta)

    generate_figures(log)

    if args.output:
        # todo check if it exists!
        with PdfPages(args.output) as pdf:
            [pdf.savefig(n) for n in plt.get_fignums()]

    if args.show:
        plt.show()
