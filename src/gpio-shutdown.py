#!/usr/bin/env python3

import RPIO
import subprocess
import time

PIN_MODE = RPIO.BCM
SHUTDOWN_BTN_PIN = 4
PIN_PULL = RPIO.PUD_DOWN
EDGE_DETECT = 'rising'


def main():
    RPIO.setmode(PIN_MODE)
    RPIO.setup(SHUTDOWN_BTN_PIN, RPIO.IN, pull_up_down=PIN_PULL)
    RPIO.add_interrupt_callback(SHUTDOWN_BTN_PIN,
                                shutdown_callback,
                                edge=EDGE_DETECT,
                                pull_up_down=PIN_PULL,
                                debounce_timeout_ms=33)


def shutdown_callback(gpio_id, value):
    subprocess.call('shutdown now')


if __name__ == '__main__':
    main()

    # do an efficient spin-lock here so that we can continue waiting for an
    # interrupt
    while True:
        # this sleep() is an attempt to prevent the CPU from staying at 100%
        time.sleep(10)

