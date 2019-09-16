"""
Signal Messenger for notify component.
Place this in `<confdir>/custom_components/signalmessenger/notify.py`
"""
from urllib import request
import json
import logging
import voluptuous as vol
from homeassistant.components.notify import (
    ATTR_DATA, ATTR_TITLE, ATTR_TITLE_DEFAULT, PLATFORM_SCHEMA,
    BaseNotificationService)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = []

_LOGGER = logging.getLogger("signalmessenger")

CONF_RECEIVER_NUMBER = 'receiver'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_RECEIVER_NUMBER): cv.string,
})


def get_service(hass, config, discovery_info=None):
    """Get the Join notification service."""
    receiver_number = config.get(CONF_RECEIVER_NUMBER)

    if receiver_number is None:
        _LOGGER.error("receiver_number is required")
        return False

    _LOGGER.info("Service initialized")
    return SignalNotificationService(receiver_number)


class SignalNotificationService(BaseNotificationService):
    """Implement the notification service for Join."""

    def __init__(self, receiver_number):
        """Initialize the service."""
        self.receiver_number = receiver_number

    def send_message(self, message="", **kwargs):
        _LOGGER.info("Calling with message")
        """Send a message to a user."""
        params = json.dumps({"number": self.receiver_number, "content": message}).encode('utf8')
        req = request.Request("http://4a36bbd1-signal:5000/message",
                              data=params,
                              headers={'content-type': 'application/json'})
        resp = request.urlopen(req)
        _LOGGER.info(resp)
