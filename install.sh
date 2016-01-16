#!/usr/bin/env bash

readonly DIRNAME=$(dirname $0)
readonly INSTALL_DIR=/usr/local/src/datacollector

if [ "$(id -u)" != "0" ]; then
  echo "Please run $0 as root" 1>&2
  exit 1
fi

function install_dependencies {
  apt-get update
  [ `which python3` ] && apt-get install -y python3
  [ `which git` ] && apt-get install -y git
  [ `which adb` ] && apt-get install -y android-tools-adb
  [ `which arduino` ] && apt-get install -y arduino
}

function copy_files {
  [ ! -d $INSTALL_DIR ] && mkdir -p $INSTALL_DIR
  ln -vfs $DIRNAME/src/adb.py $INSTALL_DIR/adb.py
}

function install_service {
  cp -vf $DIRNAME/datacollector.service /etc/systemd/system/datacollector.service
  systemctl daemon-reload
  systemctl enable datacollector.service
}

function main {
  install_dependencies
  copy_files
  install_service
}

main
