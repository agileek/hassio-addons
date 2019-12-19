#!/bin/bash

CONFIG_PATH=/data/options.json
PHONE_NUMBER=$(jq --raw-output ".phone_number" ${CONFIG_PATH})
SIGNAL_CONFIG_PATH=$(jq --raw-output ".signal_config_path" ${CONFIG_PATH})
export PHONE_NUMBER
export SIGNAL_CONFIG_PATH

cd /app || exit
dbus-daemon --system --nopidfile
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app