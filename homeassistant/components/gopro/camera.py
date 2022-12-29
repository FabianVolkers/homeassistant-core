"""Support for GoPro Cameras."""

from goprocam.GoProCamera import GoPro

from homeassistant.components.camera import CameraEntityFeature
from homeassistant.components.ffmpeg.camera import FFmpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, GOPRO
from .device_info import GoProDeviceInfo


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GoPro Camera."""
    config_entry_id = config_entry.entry_id
    config_data = hass.data[DOMAIN][config_entry_id]
    gopro: GoPro = config_data[GOPRO]
    gopro_info = await hass.async_add_executor_job(gopro.infoCamera)
    async_add_entities([GoProCameraEntity(hass, config_entry.data, gopro, gopro_info)])


class GoProCameraEntity(FFmpegCamera):
    """The GoPro Camera Entity."""

    def __init__(self, hass, config, device, device_info) -> None:
        """Initialise the Camera on a GoPro."""
        super().__init__(hass, config)
        self._device: GoPro = device
        self._serial_number: str = device_info["serial_number"]
        self._device_info: GoProDeviceInfo = GoProDeviceInfo(device, device_info)
        self._input = config["stream_address"]

    @property
    def unique_id(self) -> str:
        """Return a unique id for the device."""
        return f"{self._serial_number}-camera"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device specific attributes."""
        return self._device_info.device_info

    @property
    def brand(self) -> str:
        """Return the camera brand."""
        return self._device_info.device_brand

    @property
    def model(self) -> str:
        """Return the camera model."""
        return self._device_info.device_model

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Flag supported features."""
        supported_features = CameraEntityFeature(0)
        return supported_features

    # @property
    # def frontend_stream_type(self) -> StreamType:
    #     return super().frontend_stream_type
