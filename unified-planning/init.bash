#!/bin/bash

tmux new -d -s "init"

while [ ! -f "/tmp/quit" ]; do
  sleep 60
done

