#!/usr/bin/env bash

readonly DIRNAME=$(readlink -f $(dirname $0))
SRC_FOLDER=${DIRNAME}/../../src
DATE=`date +%Y-%m-%d`
HOST='root@10.42.0.2'

scp ${HOST}:/usr/local/src/datacollector/* ${HOST}:/usr/local/src/datacollector-${DATE}
scp SRC_FOLDER/* ${HOST}:/usr/local/src/datacollector/*
