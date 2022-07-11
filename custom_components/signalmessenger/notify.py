"""
Signal Messenger for notify component.
Place this in `<confdir>/custom_components/signalmessenger/notify.py`
"""
import requests
import logging
import json
from homeassistant.components.notify import (ATTR_DATA, BaseNotificationService)

from .const import signal_url

ATTR_FILE = "file"

REQUIREMENTS = ["requests==2.28.1"]

_LOGGER = logging.getLogger("signalmessenger")

CONF_DESTINATON_NUMBERS = 'destinations'


def get_service(hass, config, discovery_info=None):
    """Get the Join notification service."""
    destination_numbers = config.get(CONF_DESTINATON_NUMBERS)

    if destination_numbers is None:
        _LOGGER.error("destinations is required")
        return False

    _LOGGER.info("Signal Service initialized")
    return SignalNotificationService(destination_numbers=destination_numbers, url=f'{signal_url}/message')


class SignalNotificationService(BaseNotificationService):
    """Implement the notification service for Join."""

    def __init__(self, destination_numbers, url):
        """Initialize the service."""
        self.destination_numbers = destination_numbers
        self.url = url

    def send_message(self, message="", target=None, **kwargs):
        destinations = self.destination_numbers
        if target is not None:
            destinations = target
        data = kwargs.get(ATTR_DATA)

        for destination in destinations:
            if destination.startswith("+"):
                key = "number"
            else:
                key = "group"
            files = {'json': ('data.json', json.dumps({key: destination, "content": message}), 'application/json')}
            if data is not None and ATTR_FILE in data:
                files['file'] = (data.get(ATTR_FILE), open(data.get(ATTR_FILE), 'rb'), 'application/octet-stream')
            _LOGGER.info(f'Sending message "{message}" to "{destination}"')
            response = requests.post(self.url, files=files)
            _LOGGER.info(response)
