#!/usr/bin/env bash

sudo mount /dev/mmcblk0p2 /mnt/sdcard

readonly DIRNAME=$(readlink -f $(dirname $0))
SRC_FOLDER=${DIRNAME}/../../src
DATE=`date +%Y-%m-%d`
NEW_DIR=/mnt/sdcard/usr/local/src/datacollector-${DATE}

sudo rsync -rva /mnt/sdcard/usr/local/src/datacollector/* ${NEW_DIR}/
sudo rsync -rva ${SRC_FOLDER}/* /mnt/sdcard/usr/local/src/datacollector/
