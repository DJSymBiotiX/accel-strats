#!/bin/bash

tmux new-session -d -s accel
tmux send-keys -t accel:0 "bash" C-m
tmux send-keys -t accel:0 "cd /root/accel-strats/" C-m
tmux send-keys -t accel:0 "python accel.py" C-m


