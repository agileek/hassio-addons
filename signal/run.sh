#!/bin/bash
set -e
set -x

CONFIG_PATH=/data/options.json

NUMBER=$(jq --raw-output ".phone_number" $CONFIG_PATH)

/signal-cli-0.6.2/bin/signal-cli --config /data/config/signal -u ${NUMBER} receive -t -1 --json
