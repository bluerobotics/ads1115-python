import smbus2
import time

# Navigator ADS1115 is on i2c1 address 0x48
_address = 0x48

POINTER_CONVERSION = 0x00
POINTER_CONFIG = 0x01

# conversion in progress flag
CONFIG_OS = 1 << 15

# single shot mode is to be used for multiple channels
CONFIG_MODE = 1 << 8 # single shot mode

# 860 samples per second data rate (highest available), not sure if this matters in single shot mode
CONFIG_DR = 0b111 << 5

# configure PGA to +/-4.096V range for best resolution
# on Navigator (0~3.3V inputs)
CONFIG_PGA_4096 = 0b001 << 9

# channel selection
CONFIG_MUX_AIN0 = 0b100 << 12
CONFIG_MUX_AIN1 = 0b101 << 12
CONFIG_MUX_AIN2 = 0b110 << 12
CONFIG_MUX_AIN3 = 0b111 << 12

_mux = {
    0: CONFIG_MUX_AIN0,
    1: CONFIG_MUX_AIN1,
    2: CONFIG_MUX_AIN2,
    3: CONFIG_MUX_AIN3
}

DELAY_MEASURE = 1.0/860

class ADS1115:

    # Navigator ADS1115 is on i2c1 address 0x48
    def __init__(self, bus=1):
        self._bus = smbus2.SMBus(bus)

    # channel: integer channel to read [0,3]
    # return: floating point voltage of requested channel
    def read(self, channel):
        config = CONFIG_OS | CONFIG_PGA_4096 | CONFIG_MODE | CONFIG_DR
        config = config | _mux[channel]
        # request conversion on selected channel
        self._write_config(config)

        # wait for conversion to complete (860 conversions/second)
        time.sleep(DELAY_MEASURE)
        while int.from_bytes(self._bus.read_i2c_block_data(_address, POINTER_CONVERSION, 2), 'big', signed=True) & (1 << 15):
            continue

        # read conversion register data
        data = self._read_data()
        # convert to voltage
        return 2*data*4.096/0xffff

    # write the configuration register
    # config: byte of data to write to configuration register
    # return: None
    def _write_config(self, config):
        # data is sent MSB first
        data = list(config.to_bytes(2, 'big'))
        self._bus.write_i2c_block_data(_address, POINTER_CONFIG, data)

    # read the conversion data register
    # return: conversion register data as signed 16 bit integer
    def _read_data(self):
        data = self._bus.read_i2c_block_data(_address, POINTER_CONVERSION, 2)
        # convert 2 byte data into signed 16 bit integer
        return int.from_bytes(data, 'big', signed=True)
