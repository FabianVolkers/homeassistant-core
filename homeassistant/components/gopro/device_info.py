"""Library for extracting device specific information common to entities."""


from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


class GoProDeviceInfo:
    """Provide Device Info for a GoPro Camera."""

    device_brand = "GoPro"

    def __init__(self, device, device_info) -> None:
        """Initialise the DeviceInfo."""
        self._device = device
        self._device_info = device_info

    @property
    def device_info(self) -> DeviceInfo:
        """Return device specific attributes."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info["serial_number"])},
            manufacturer=self.device_brand,
            model=self.device_model,
            name=self.device_name,
        )

    @property
    def device_model(self) -> str:
        """Return device model."""
        return self._device_info["model_name"]

    @property
    def device_name(self) -> str:
        """Return device name."""
        return self._device_info["ap_ssid"]
