#!/bin/bash

sudo mkdir -p /mnt/sdcard
sudo mount /dev/mmcblk0p2 /mnt/sdcard

sudo cp /mnt/sdcard/daq_data/* .

sudo umount /dev/mmcblk0p2

