#!/bin/bash

CONFIG_PATH=/data/options.json
PHONE_NUMBER=$(jq --raw-output ".phone_number" ${CONFIG_PATH})
SIGNAL_CONFIG_PATH=$(jq --raw-output ".signal_config_path" ${CONFIG_PATH})
SIGNAL_LOG_LEVEL=$(jq --raw-output ".log_level" ${CONFIG_PATH})

export PHONE_NUMBER
export SIGNAL_CONFIG_PATH
export SIGNAL_LOG_LEVEL

dbus-uuidgen --ensure=/etc/machine-id
mkdir /var/run/dbus
dbus-daemon --system --nopidfile
cd /app || exit
source ~/.python_signal/bin/activate
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app