#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
echo ExecStart="$DIR"/start_farmer.sh>>achifarm.service
echo WorkingDirectory="$DIR"/>>achifarm.service
cat achifarm.service
cp achifarm.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable achifarm
systemctl start achifarm
systemctl status achifarm
git checkout .