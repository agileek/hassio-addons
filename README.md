## Hass.io plugins

[![Build Status](https://travis-ci.org/agileek/hassio-addons.svg?branch=master)](https://travis-ci.org/agileek/hassio-addons)

## Pre-built images

## [Signal](/signal)

Signal cli wrapper

## [Syncthing](/syncthing)

Forked from https://github.com/bestlibre/hassio-addons



That's to be compatible with armv7 arch on signal.

Build on rpi manually

docker build -t local_signal .
docker tag local_signal:latest agileek/hassio-armv7-signal:10.10.0
docker push agileek/hassio-armv7-signal:10.10.0
