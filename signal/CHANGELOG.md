# Changelog

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
