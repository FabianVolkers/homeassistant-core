"""The GoPro Camera integration."""
from __future__ import annotations

import logging

from goprocam import GoProCamera

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, GOPRO, GOPRO_INFO

PLATFORMS: list[Platform] = [Platform.CAMERA]

_LOGGER = logging.getLogger(__name__)


def _init_gopro_device(device):
    return device.getStatus("status", "31"), device.infoCamera()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GoPro Camera from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    gopro_config = entry.data

    device_ip = gopro_config["ip"]

    device = await hass.async_add_executor_job(GoProCamera.GoPro, device_ip)

    status, info = await hass.async_add_executor_job(_init_gopro_device, device)

    if status is None:
        _LOGGER.error("Could not connect to GoPro at %s", device_ip)
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = {GOPRO: device, GOPRO_INFO: info}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
