"""
Module for managing an DPT Switch remote value.
DPT 1.001.
"""
from enum import Enum

from .remote_value import RemoteValue
from teletask.doip import TelegramSetting

class RemoteValueSwitch(RemoteValue):
    class Value(Enum):
        """Enum for indicating the direction."""
        OFF = 0
        ON = 255

    def __init__(self,
                 teletask,
                 group_address=None,
                 device_name=None,
                 after_update_cb=None,
                 doip_component=None,
                 invert=False):
        """Initialize remote value of Teletask """
        super(RemoteValueSwitch, self).__init__(
            teletask, group_address,
            device_name=device_name, after_update_cb=after_update_cb,
            doip_component=doip_component)
        self.invert = invert

    def to_teletask(self, value):
        """Convert value to payload."""
        return value

    def from_teletask(self, value):
        """Convert current payload to value."""
        return value

    async def off(self):
        """Set value to down."""
        await self.set(self.Value.OFF.value)

    async def on(self):
        """Set value to UP."""
        await self.set(self.Value.ON.value)