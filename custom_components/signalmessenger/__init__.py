"""Signal Messenger integration using signal-cli.
Place this in `<confdir>/custom_components/signalmessenger/__init__.py`
"""
import logging
import requests
from .const import signal_url

DOMAIN = 'signalmessenger'
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    def get_groups(call):
        response = requests.get(f'{signal_url}/group')
        _LOGGER.info('retrieve groups (status: %d), %s', response.status_code, response.json())
    hass.services.register(DOMAIN, 'get_groups', get_groups)
    return True
