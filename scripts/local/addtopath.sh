#!/usr/bin/env bash

readonly DIRNAME=$(readlink -f $(dirname $0))

sudo rsync -rva ${DIRNAME}/* ~/bin/