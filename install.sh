#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
echo ExecStart="$DIR"/start_monitor.sh>>achimon.service
echo WorkingDirectory="$DIR"/>>achimon.service
cat achimon.service
cp achimon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable achimon
systemctl start achimon
systemctl status achimon
git checkout .