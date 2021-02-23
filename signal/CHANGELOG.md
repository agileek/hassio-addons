# Changelog

## 10.13.0

- Use file name when forwarding image 

## 10.12.1

- Embed native libsignal

## 10.12.0

- Upgrade to signal-cli 0.8.0

## 10.11.2

- remove deprecation messages

## 10.11.1

- fix zkgroup library
- if you use groups v2, you'll have to update the profile of your account
    - `/signal-cli/bin/signal-cli --config ${SIGNAL_CONFIG_PATH} -u ${PHONE_NUMBER} updateProfile --name "Name of the account"`

## 10.11.0

- update signal to 0.7.4
- update to latest JRE
- switch on debian based image
- image automatically built by github actions

## 10.10.0

- update signal to 0.6.11
- update to java 11

## 10.9.3

- installing jffi-native system-wide for aarch64 image

## 10.9.2

- reverting to 10.8.1 image for aarch64 image

## 10.9.1

- fix log levels

## 10.9.0

- signal cli updated to 0.6.8
  - No more libmatthew for dbus \o/

## 10.8.1

- added capacity to change log level
- added debug logs

## 10.8.0

- remotely build image
- fewer docker layers

## 10.7.1

- add hostname to startup logs

## 10.7.0

- Update signal-cli to 0.6.7
- Update docker base image to 5.1.0

## 10.6.0

- Add capacity to talk to home assistant

## 10.5.2

- Really fix compatibility problem with official signal integration

## 10.5.1

- Fix compatibility problem with official signal integration

## 10.5.0

- Compatible with official home assistant signal integration
- the url is http://4a36bbd1-signal:5000

## 10.4.1

- Refactor to make the application testable

## 10.4.0

- Dont launch flask anymore, use gunicorn

## 10.3.3

- Fix group sending: sendGroupMessage needs an array of byte, not a string
- Patch update hassioaddons/base-python 3.0.1 --> 3.0.2

## 10.3.2

- Fix python code

## 10.2.1

- Move changelog in own file

## 10.2.0

- Can retrieve groups

## 10.0.0

- Breaking change: update the application plugin
- Add attachments support
