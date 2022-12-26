"""Library for extracting device specific information common to entities."""


class GoProDeviceInfo:
    """Provide Device Info for a GoPro Camera."""

    def __init__(self, device) -> None:
        """Initialise the DeviceInfo."""
        self._device = device
