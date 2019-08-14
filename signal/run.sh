#!/bin/bash

CONFIG_PATH=/data/options.json

export PHONE_NUMBER=$(jq --raw-output ".phone_number" ${CONFIG_PATH})
export SIGNAL_CLI_PATH=$(jq --raw-output ".signal_cli_path" ${CONFIG_PATH})
export SIGNAL_CONFIG_PATH=$(jq --raw-output ".signal_config_path" ${CONFIG_PATH})

export FLASK_APP=app.py
cd /app
flask run --host=0.0.0.0