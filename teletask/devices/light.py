"""
Module for managing a light via Teletask.
It provides functionality for
* switching light 'on' and 'off'.
"""
from .device import Device
from .remote_value_switch import RemoteValueSwitch

class Light(Device):
    """Class for managing a light."""

    def __init__(self,
                 teletask,
                 name,
                 group_address_switch=None,
                 group_address_switch_state=None,
                 doip_component="relay",
                 device_updated_cb=None):
        """Initialize Light class."""
        # pylint: disable=too-many-arguments
        super(Light, self).__init__(teletask, name, device_updated_cb)

        self.doip_component = str(doip_component).upper()
        self.teletask = teletask
        self.light_state = False
        self.switch = RemoteValueSwitch(
            teletask,
            group_address_switch,
            group_address_switch_state,
            device_name=self.name,
            after_update_cb=self.after_update,
            doip_component=self.doip_component)
        self.teletask.register_device(self)

    def __str__(self):
        """Return object as readable string."""

        return '<Light name="{0}" ' \
            'switch="{1}" />' \
            .format(
                self.name,
                self.switch.group_address)

    @property
    def state(self):
        """Return the current switch state of the device."""
        return self.switch.value == RemoteValueSwitch.Value.ON

    async def set_on(self):
        """Switch light on."""
        await self.switch.on()

    async def set_off(self):
        """Switch light off."""
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