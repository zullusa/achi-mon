#!/usr/bin/bash

{
  echo \#!/usr/bin/bash
  echo cd \"\$\(dirname \"\$0\"\)\" \|\| exit
  echo sudo -u $USER ./run_monitor.sh
} > start_monitor.sh

chmod 777 start_monitor.sh