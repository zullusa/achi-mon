#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
PARENT_DIR="$( cd "$( dirname "$DIR" )" >/dev/null && pwd )"
{
  echo "[Unit]"
  echo Description=Achi Monitoring Service
  echo "[Install]"
  echo WantedBy=multi-user.target
  echo "[Service]"
  echo Type=simple
  echo Restart=always
  echo ExecStart="$PARENT_DIR"/start_monitor.sh
  echo WorkingDirectory="$PARENT_DIR/"
} > achimon.service

cat achimon.service
mv achimon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable achimon
systemctl start achimon
systemctl status achimon