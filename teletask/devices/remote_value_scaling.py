"""
Module for managing a Scaling remote value.
DPT 5.001.
"""
from .remote_value import RemoteValue


class RemoteValueScaling(RemoteValue):
    """Abstraction for remote value of Dimmer."""

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
        super(RemoteValueScaling, self).__init__(
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

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"