""" galaxy_cloud_speak platform for notify component."""
import logging
import asyncio
import io

import aiohttp
import async_timeout

import requests
from requests.auth import HTTPBasicAuth
import voluptuous as vol

from homeassistant.components.notify import (
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import HTTP_OK
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SMARTTHINGS_API_URL = 'https://api.smartthings.com/v1/devices/{}/commands'
CONF_SMARTTHINGS_TOKEN = "token"
CONF_DEVICE_ID         = "device_id"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SMARTTHINGS_TOKEN): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
    }
)

def get_service(hass, config, discovery_info=None):
    """Get the Smartthings speechSynthesis Speak()  notification service."""
    return GalaxyCloudSpeechNotificationService(hass, config)


class GalaxyCloudSpeechNotificationService(BaseNotificationService):
    """Implementation of the notification service for Smartthings speechSynthesis Speak"""

    def __init__(self, hass, config):
        """Initialize the service."""
        self._hass = hass
        self._token     = config.get(CONF_SMARTTHINGS_TOKEN)
        self._device_id = config.get(CONF_DEVICE_ID)

        self._headers = {
            'Authorization' : 'Bearer {}'.format(self._token),
            'Content-Type' : 'application/json'
        }


    async def send_message(self, message="", **kwargs):
        """Send a message to specified target."""
        websession = async_get_clientsession(self.hass)

        if len(message) > 1000:
            message = 'Message max length is 1000.'

        try:

            with async_timeout.timeout(10):

                data = {
                    "commands": [
                        {
                            "component": "main",
                            "capability": "speechSynthesis",
                            "command": "speak",
                            "arguments": [
                                str(message)
                            ]
                        }
                    ]
                }

                url = SMARTTHINGS_API_URL.format(self._device_id)

                request = await websession.post(url, json=data, headers=self._headers)

                if request.status != HTTP_OK:
                    _LOGGER.error( "Error %d on load URL %s", request.status, request.url)
                else:
                    _LOGGER.debug("Galaxy Cloud Speak API send: %s", request.json())


        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for Galaxy Cloud Speech API")
