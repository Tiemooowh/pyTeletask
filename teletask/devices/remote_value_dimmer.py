"""
Module for managing a Scaling remote value.
DPT 5.001.
"""
from enum import Enum

from .remote_value import RemoteValue
from teletask.doip import TelegramSetting

class RemoteValueDimmer(RemoteValue):
    class Value(Enum):
        """Enum for indicating the direction."""
        OFF = 0
        ON = 255

    def __init__(self,
                 teletask,
                 group_address=None,
                 device_name=None,
                 after_update_cb=None,
                 range_from=100,
                 range_to=0,
                 doip_component="DIMMER"):
        """Abstraction for remote value of Dimmer."""
        # pylint: disable=too-many-arguments
        super(RemoteValueDimmer, self).__init__(
            teletask, group_address=group_address,
            device_name=device_name, after_update_cb=after_update_cb,
            doip_component=doip_component)

        self.range_from = range_from
        self.range_to = range_to

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

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"