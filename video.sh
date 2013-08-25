#!/bin/sh
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
raspivid -t 5000 -o ./videos/$current_time.h264
