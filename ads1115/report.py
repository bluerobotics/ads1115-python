#!/usr/bin/python3

import matplotlib.pyplot as plt

DEVICE = 'ads1115'

def generate_figures(log):
    footer = f'{DEVICE} test report'

    f, spec = log.figure(height_ratios=[1,1], suptitle=f'{DEVICE} data', footer=footer)
    plt.subplot(spec[0,0])
    log.channel0.pplot()

    plt.subplot(spec[0,1])
    log.channel1.pplot()

    plt.subplot(spec[1,0])
    log.channel2.pplot()

    plt.subplot(spec[1,1])
    log.channel3.pplot()

def main():
    from llog import LLogReader
    from matplotlib.backends.backend_pdf import PdfPages

    parser = LLogReader.create_default_parser(__file__, DEVICE)
    args = parser.parse_args()

    log = LLogReader(args.input, args.meta)

    generate_figures(log)

    if args.output:
        # todo check if it exists!
        with PdfPages(args.output) as pdf:
            [pdf.savefig(n) for n in plt.get_fignums()]

    if args.show:
        plt.show()

if __name__ == '__main__':
    main()
