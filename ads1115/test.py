#!/usr/bin/python3

def main():
    from ads1115 import ADS1115
    from llog import LLogWriter
    import time

    device = "ads1115"
    parser = LLogWriter.create_default_parser(__file__, device)
    args = parser.parse_args()

    with LLogWriter(args.meta, args.output, console=args.console) as log:
        ads = ADS1115()

        # requires custom channel setup - doesn't use standard data logging
        LLOG_CH0 = 100

        start_time = time.time()
        while time.time() < start_time + args.duration:
            for channel in range(4):
                try:
                    log.log(LLOG_CH0 + channel, ads.read(channel))
                except Exception as e:
                    log.log_error(f'"e"')
                    if args.stop_on_error:
                        return

                if args.frequency:
                    time.sleep(1.0 / args.frequency)

if __name__ == '__main__':
    main()
