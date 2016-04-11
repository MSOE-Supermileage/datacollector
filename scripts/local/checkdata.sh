#!/bin/bash

sudo mkdir -p /mnt/sdcard
sudo mount /dev/mmcblk0p2 /mnt/sdcard

sudo ranger /mnt/sdcard/daq_data

