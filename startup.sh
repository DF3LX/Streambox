#!/usr/bin/bash

# create a symlink of this script under /etc/init.d/

# installation directory of the git repo
install_dir=/home/pi/Streambox

# compose name of log file
logfile=$install_dir/logs/$(date +%F_%T).txt

# start main script
while true; do

$install_dir/streambox.py | tee -a $logfile
echo "script terminated with exit status $?, restarting in 1s"
sleep 1

done
