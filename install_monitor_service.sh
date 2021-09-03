#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
echo ExecStart="$DIR"/start_monitor.sh>>./daemons/achimon/achimon.service
echo WorkingDirectory="$DIR"/>>./daemons/achimon/achimon.service
cat ./daemons/achimon/achimon.service
cp ./daemons/achimon/achimon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable achimon
systemctl start achimon
systemctl status achimon
git checkout .