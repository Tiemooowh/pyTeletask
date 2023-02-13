"""
Module for managing a dimmer via Teletask.
It provides functionality for
* switching dimmer 'on' and 'off'.
"""
from .device import Device
from .remote_value_dimmer import RemoteValueDimmer


class Dimmer(Device):
    """Class for managing a Dimmer."""

    def __init__(self,
                 teletask,
                 name,
                 group_address_brightness=None,
                 doip_component="dimmer",
                 device_updated_cb=None):
        """Initialize Dimmer class."""
        # pylint: disable=too-many-arguments
        super(Dimmer, self).__init__(teletask, name, device_updated_cb)

        self.doip_component = str(doip_component).upper()
        self.teletask = teletask
        self.light_state = False

        self.dimmer = RemoteValueDimmer(
            teletask,
            group_address=group_address_brightness,
            device_name=self.name,
            after_update_cb=self.after_update,
            range_from=0,
            range_to=100,
            doip_component="DIMMER")

        self.teletask.register_device(self)

    def __str__(self):
        """Return object as readable string."""
        str_brightness = '' if not self.supports_brightness else \
            ' brightness="{0}"'.format(
                self.dimmer.group_addr_str())

        return '<Light name="{0}" ' \
            'switch="{1}" {2} />' \
            .format(
                self.name,
                self.dimmer.group_address,
                str_brightness)

    @property
    def supports_brightness(self):
        """Return if light supports brightness."""
        return self.dimmer.initialized

    @property
    def state(self):
        """Return the current switch state of the device."""
        return self.dimmer.value != RemoteValueDimmer.Value.OFF

    async def set_on(self):
        """Switch light on."""
        await self.dimmer.on()

    async def set_off(self):
        """Switch light off."""
        await self.dimmer.off()

    @property
    def current_brightness(self):
        """Return current brightness of light."""
        return self.dimmer.value

    async def set_brightness(self, brightness):
        """Set brightness of light."""
        if not self.supports_brightness:
            self.teletask.logger.warning("Dimming not supported for device %s", self.get_name())
            return
        await self.dimmer.set(brightness)

    async def change_state(self,value):
        await self.dimmer.state(value)

    async def current_state(self):
        await self.dimmer.current_state()

    async def do(self, action):
        """Execute 'do' commands."""
        if action == "on":
            await self.set_on()
        elif action == "off":
            await self.set_off()
        elif action.startswith("brightness:"):
            await self.set_brightness(int(action[11:]))
        else:
            self.teletask.logger.debug("Could not understand action %s for device %s", action, self.get_name())

    def has_group_address(self, var):
        return False

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__