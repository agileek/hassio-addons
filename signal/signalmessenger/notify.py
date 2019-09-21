"""
Signal Messenger for notify component.
Place this in `<confdir>/custom_components/signalmessenger/notify.py`
"""
from urllib import request
import json
import logging
from homeassistant.components.notify import (
    ATTR_DATA, ATTR_TITLE, ATTR_TITLE_DEFAULT, PLATFORM_SCHEMA,
    BaseNotificationService)

REQUIREMENTS = []

_LOGGER = logging.getLogger("signalmessenger")

CONF_DESTINATON_NUMBERS = 'destinations'


def get_service(hass, config, discovery_info=None):
    """Get the Join notification service."""
    destination_numbers = config.get(CONF_DESTINATON_NUMBERS)

    if destination_numbers is None:
        _LOGGER.error("destinations is required")
        return False

    _LOGGER.info("Signal Service initialized")
    return SignalNotificationService(destination_numbers)


class SignalNotificationService(BaseNotificationService):
    """Implement the notification service for Join."""

    def __init__(self, destination_numbers):
        """Initialize the service."""
        self.destination_numbers = destination_numbers

    def send_message(self, message="", target=None, **kwargs):
        destinations = self.destination_numbers
        if target is not None:
            destinations = target

        for destination in destinations:
            params = json.dumps({"number": destination, "content": message}).encode('utf8')
            _LOGGER.info(f'Sending message "{message}" to "{destination}"')
            req = request.Request("http://4a36bbd1-signal:5000/message",
                                  data=params,
                                  headers={'content-type': 'application/json'})
            resp = request.urlopen(req)
            _LOGGER.info(resp)
