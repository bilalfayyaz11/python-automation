#!/bin/bash
set -e

echo "Triggering CPU spike incident..."

for i in 1 2 3 4; do
  timeout 300 bash -c 'while true; do :; done' &
  echo $! >> /tmp/cpu-spike-pids.txt
done

echo "CPU spike incident triggered"
cat /tmp/cpu-spike-pids.txt
