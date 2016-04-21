#!/bin/bash

fdisk -lu /dev/mmcblk0

mount /dev/mmcblk0p2 /mnt/sdcard/
mount /dev/mmcblk0p1 /mnt/sdcard/boot

