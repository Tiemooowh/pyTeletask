"""
Module for managing a Switch via Teletask.
It provides functionality for
* switching a switch 'on' and 'off'.
"""
from .device import Device
from .remote_value_switch import RemoteValueSwitch

class Switch(Device):
    """Class for managing a Switch."""

    def __init__(self,
                 teletask,
                 name,
                 group_address_switch=None,
                 group_address_switch_state=None,
                 device_updated_cb=None,
                 doip_component="relay"):
        """Initialize Switch class."""
        # pylint: disable=too-many-arguments
        super(Switch, self).__init__(teletask, name, device_updated_cb)

        self.doip_component = str(doip_component).upper()
        self.teletask = teletask
        self.Switch_state = False
        self.switch = RemoteValueSwitch(
            teletask,
            group_address=group_address_switch,
            device_name=self.name,
            after_update_cb=self.after_update,
            doip_component=self.doip_component)
        self.teletask.register_device(self)

    def __str__(self):
        """Return object as readable string."""

        return '<Switch name="{0}" ' \
            'switch="{1}" />' \
            .format(
                self.name,
                self.switch.group_address)

    @property
    def state(self):
        """Return the current switch state of the device."""
        return self.switch.value == RemoteValueSwitch.Value.ON

    async def set_on(self):
        """Switch Switch on."""
        await self.switch.on()

    async def set_off(self):
        """Switch Switch off."""
        await self.switch.off()

    async def change_state(self,value):
        await self.switch.state(value)

    async def current_state(self):
        await self.switch.current_state()

    async def do(self, action):
        """Execute 'do' commands."""
        if action == "on":
            await self.set_on()
        elif action == "off":
            await self.set_off()
        else:
            self.teletask.logger.debug("Could not understand action %s for device %s", action, self.get_name())

    def has_group_address(self, var):
        return False

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__