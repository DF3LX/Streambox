#!/usr/bin/bash

# create a symlink of this script under /etc/init.d/

# installation directory of the git repo
install_dir=/home/pi/Streambox

# compose name of log file
logfile=$install_dir/logs/$(date +%F_%T).txt

echo "called startup.sh" > $logfile


# Run main script in an infinite loop, this is because if a
# new version is detected, the script downloads the new version
# and exists. Then it will be restarted by this loop.
while true; do

  # run main script
  $install_dir/streambox.py 2>&1 | tee -a $logfile

  # only if exist status was "2", exit infinite loop
  if [ "$?$" = "2" ]; then
    echo "script terminated with exit status 2, now quit startup script"
    exit
  fi

  echo "script terminated with exit status $?, restarting in 1s"
  sleep 1

done
