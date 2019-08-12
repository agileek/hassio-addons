#!/bin/bash

#CONFIG_PATH=/data/options.json
#
#NUMBER=$(jq --raw-output ".phone_number" $CONFIG_PATH)
#
#/signal-cli-0.6.2/bin/signal-cli --config /data/config/signal -u ${NUMBER} receive -t -1 --json
export FLASK_APP=app.py
cd /app
flask run --host=0.0.0.0