# Changelog

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
