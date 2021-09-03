#!/usr/bin/bash

echo ExecStart="$(dirname "$0")"/start_monitor.sh>>achimon.service
echo WorkingDirectory="$(dirname "$0")"/>>achimon.service
cat achimon.service
cp achimon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable achimon
systemctl start achimon
systemctl status achimon
git checkout .