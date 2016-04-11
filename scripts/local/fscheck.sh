#!/bin/bash

sudo mke2fs /dev/mmcblk0

sudo fsck -b 32768 /dev/mmcblk0
