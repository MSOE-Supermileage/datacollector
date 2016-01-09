#!/usr/bin/env bash

function install_dependencies {
  apt-get update
  [[ which python3 ]] && apt-get install -y python3
  [[ which git ]] && apt-get install -y git
  [[ which adb ]] && apt-get install -y android-tools-adb
  [[ which arduino ]] && apt-get install -y arduino
}

function copy_files {
  [[ ! -d /usr/local/src/datacollector ]] && mkdir -p /usr/local/src/datacollector
  ln -vis src/adb.py /usr/local/src/datacollector/adb.py
}

function install_service {
  cp -vf datacollector.service /etc/systemd/service/datacollector.service
  systemctl daemon-restart
  systemctl enable datacollector.service
}

function main {
  install_dependencies
  copy_files
  install_service
}

main
