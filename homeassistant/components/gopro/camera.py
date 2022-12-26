"""Support for GoPro Cameras."""

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, GOPRO


def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GoPro Camera."""
    config_entry_id = config_entry.entry_id
    config_data = hass.data[DOMAIN][config_entry_id]
    gopro = config_data[GOPRO]
    async_add_entities([GoProCameraEntity(gopro)])


class GoProCameraEntity(Camera):
    """The GoPro Camera Entity."""

    def __init__(self, device) -> None:
        """Initialise the Camera on a GoPro."""
        super().__init__()
        self._device = device
        # self._device_info = device.infoCamera()

    # @property
    # def unique_id(self) -> str:
    #     return f"camera-{self._device_info['serial_number']}"

    # @property
    # def device_info(self) -> DeviceInfo:
    #     """Return device specific attributes."""
    #     return self._device_info
