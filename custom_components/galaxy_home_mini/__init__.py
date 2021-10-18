import requests
import logging
import asyncio
import aiohttp
import json
import base64

import voluptuous as vol

import homeassistant.loader as loader
from homeassistant.const import (STATE_UNKNOWN, EVENT_STATE_CHANGED)
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.helpers import discovery

from .const import DOMAIN, CONF_ACCESS_TOKEN, CONF_DEVICE_ID

_LOGGER = logging.getLogger(__name__)


def base_config_schema(config: dict = {}) -> dict:
    """Return a shcema configuration dict for Galaxy Home Mini."""
    if not config:
        config = {
            CONF_ACCESS_TOKEN: "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    return {
        vol.Required(CONF_ACCESS_TOKEN, default=config.get(CONF_ACCESS_TOKEN)): str,
    }


def config_combined() -> dict:
    """Combine the configuration options."""
    base = base_config_schema()

    return base

CONFIG_SCHEMA = vol.Schema({DOMAIN: config_combined()}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):

    if DOMAIN not in config:
        return True

    return True


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""

    if hass.data.get(DOMAIN) is not None:
        return False

    if config_entry.source == config_entries.SOURCE_IMPORT:
        hass.async_create_task(hass.config_entries.async_remove(config_entry.entry_id))
        return False

    access_token = config_entry.data[CONF_ACCESS_TOKEN]
    device_id    = config_entry.data[CONF_DEVICE_ID]

    hdr = {
        'Authorization' : 'Bearer {}'.format(access_token),
        'Content-Type'  : 'application/json'
    }

    session = async_get_clientsession(hass)

    # speak add service
    async def speak(service):
        message = service.data["message"]

        if len(message) > 1000:
            message = 'Message max length is 1000.'
            _LOGGER.error(f'[{DOMAIN}] speak() Error, %s', message)

        try:
            with async_timeout.timeout(90):
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

                url = SMARTTHINGS_API_CALL_URL.format(device_id)

                request = await websession.post(url, json=data, headers=hdr)

                if request.status != HTTP_OK:
                    _LOGGER.error( "Error %d on load URL %s", request.status, request.url)
                else:
                    _LOGGER.debug("Galaxy Home Mini Serivce Speak()  send: %s", request.json())

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for Galaxy Home Mini speak() API")


    hass.services.async_register(DOMAIN, "speak", speak)

    # bixbi_command add service
    async def bixbi_command(service):
        message = service.data["message"]

        if len(message) > 1000:
            message = 'Message max length is 1000.'
            _LOGGER.error(f'[{DOMAIN}] bixbi_command() Error, %s', message)

        try:
            with async_timeout.timeout(90):
                data = {
                    "commands": [
                        {
                            "component": "main",
                            "capability": "samsungim.bixbyContent",
                            "command": "bixbyCommand",
                            "arguments": [
                                "search_all",
                                str(message)
                            ]
                        }
                    ]
                }

                url = SMARTTHINGS_API_CALL_URL.format(device_id)

                request = await websession.post(url, json=data, headers=hdr)

                if request.status != HTTP_OK:
                    _LOGGER.error(f"[{DOMAIN}] Error %d on load URL %s", request.status, request.url)
                else:
                    _LOGGER.debug(f"[{DOMAIN}] Bixby Command API send: %s", request.json())


        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for Galaxy Home Mini Bixbi Command API")

    hass.services.async_register(DOMAIN, "bixbi_command", bixbi_command)

    return True
