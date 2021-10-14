"""Config flow for K-Weather."""
import logging
import json

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (CONF_SCAN_INTERVAL)
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import DOMAIN, CONF_ACCESS_TOKEN, CONF_DEVICE_ID, SMARTTHINGS_API_URL

_LOGGER = logging.getLogger(__name__)

async def get_devices(session, token):
    headers = {
        'Authorization' : 'Bearer {}'.format(token)
    }

    url = SMARTTHINGS_API_URL

    response = await session.get(url, headers = headers)

    rescode = response.status

    if ( rescode == 200 ):
        response_body = response.content
    else:
        _LOGGER.error(f'[{DOMAIN}] Error Code: {rescode}')

    items = await response.json()

    devices = {}

    for item in items['items']:
        devices[item['deviceId']] = '{} - {}'.format(item['name'], item['label'])

    #_LOGGER.error(f'[{DOMAIN}] Smartthins Devices, %s', devices)

    return devices

class GalaxyHomeMiniConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Galaxy Home Mini."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._device_id: Required[str]    = None
        self._access_token: Required[str] = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._access_token    = user_input[CONF_ACCESS_TOKEN]

            return await self.async_step_device()

#        if self._async_current_entries():
#            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            schema = vol.Schema(
                {
                    vol.Required(CONF_ACCESS_TOKEN, default=None): str
                }
            )

            return self.async_show_form(step_id='user', data_schema=schema)


    async def async_step_import(self, import_info):
        """Handle import from config file."""
        return await self.async_step_user(import_info)

    @callback
    async def async_step_device(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # device 목록 가져오기
        session = async_create_clientsession(self.hass)

        devices = await get_devices(session, self._access_token)

        # device 목록이 없는 경우, 취소처리
        if not devices:
            _LOGGER.error(f'[{DOMAIN}] async_step_device() not exists devices.')
            return self.async_abort(reason="not_exists_device")

        _DEVICES = devices

        if user_input is not None:

            user_input[CONF_ACCESS_TOKEN] = self._access_token

            uniqid = 'galay-home-mini-{}'.format(user_input[CONF_DEVICE_ID])
            await self.async_set_unique_id(uniqid)

            tit = devices[user_input[CONF_DEVICE_ID]]

            return self.async_create_entry(title=tit, data=user_input)


        if user_input is None:
            return self.async_show_form(
                step_id='device',
                data_schema=vol.Schema({ vol.Required(CONF_DEVICE_ID, default=None): vol.In(_DEVICES) })
                )

