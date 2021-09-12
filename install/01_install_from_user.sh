#!/usr/bin/bash

{
  echo \#!/usr/bin/bash
  echo cd \"\$\(dirname \"\$0\"\)\" \|\| exit
  echo sudo -u $USER git pull
  echo sudo -u $USER ./install/run_monitor.sh
} > ./start_monitor.sh

chmod 777 ./start_monitor.sh
