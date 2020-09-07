"""
Module for managing a remote value Teletask.

Remote value can either be a group address for reading
and and one group address for writing a Teletask value
or a group address for both.
"""
# from teletask.exceptions import CouldNotParseTelegram
from teletask.doip import Telegram, TeletaskConst, TelegramCommand, TelegramFunction, TelegramSetting#, TelegramType
import asyncio

class RemoteValue():
    """Class for managing remote teletask value."""

    def __init__(self,
                 teletask,
                 group_address=None,
                 device_name=None,
                 after_update_cb=None,
                 doip_component=None):
        """Initialize RemoteValue class."""
        self.teletask = teletask

        self.doip_component = doip_component
        self.group_address = group_address
        self.brightness_val = 0
        self.after_update_cb = after_update_cb
        self.device_name = "Unknown" \
            if device_name is None else device_name
        self.payload = None

    @property
    def initialized(self):
        """Evaluate if remote value is initialized with group address."""
        return bool(self.group_address)

    def has_group_address(self, group_address):
        """Test if device has given group address."""
        return (self.group_address == group_address)

    def state_addresses(self):
        """Return group addresses which should be requested to sync state."""
        if self.group_address:
            return [self.group_address, ]
        return []

    def payload_valid(self, payload):
        """Test if telegram payload may be parsed - to be implemented in derived class.."""
        # pylint: disable=unused-argument
        self.teletask.logger.warning("payload_valid not implemented for %s", self.__class__.__name__)
        return True

    def from_teletask(self, payload):
        """Convert current payload to value - to be implemented in derived class."""
        # pylint: disable=unused-argument
        self.teletask.logger.warning("from_teletask not implemented for %s", self.__class__.__name__)
        return None

    def to_teletask(self, value):
        """Convert value to payload - to be implemented in derived class."""
        # pylint: disable=unused-argument
        self.teletask.logger.warning("to_teletask not implemented for %s", self.__class__.__name__)
        return None

    async def process(self, telegram):
        """Process incoming telegram."""
        if not self.has_group_address(telegram.group_address):
            return False
        if not self.payload_valid(telegram.payload):
            raise Exception("payload invalid",
                                        payload=telegram.payload,
                                        group_address=telegram.group_address,
                                        device_name=self.device_name)
        if self.payload != telegram.payload or self.payload is None:
            self.payload = telegram.payload
            if self.after_update_cb is not None:
                await self.after_update_cb()
        return True

    @property
    def value(self):
        """Return current value ."""
        if self.payload is None:
            return None
        return self.from_teletask(self.payload)

    async def current_state(self):
        """Send payload as telegram to Teletask bus."""
        function = TelegramFunction[self.doip_component]
        telegram = Telegram(command=TelegramCommand.GET, address=int(self.group_address), function=function)
        await self.teletask.telegrams.put(telegram)

    async def send(self, receivedSetting=TelegramSetting.TOGGLE.value, response=False):
        """Send payload as telegram to Teletask bus."""
        function = TelegramFunction[self.doip_component]
        if self.doip_component == "DIMMER":
            ttvalue = TeletaskValue()
            ttvalue.value  = self.brightness_val
            setting = ttvalue
        else:
            ttvalue = TeletaskValue()
            ttvalue.value = receivedSetting
            setting = ttvalue

        telegram = Telegram(command=TelegramCommand.SET, function=function,  address=int(self.group_address), setting=setting)
        await self.teletask.telegrams.put(telegram)

    async def set(self, value):
        """Set new value."""
        if not self.initialized:
            self.teletask.logger.info("Setting value of uninitialized device %s (value %s)", self.device_name, value)
            return

        payload = self.to_teletask(value)
        updated = False
        if self.payload is None or payload != self.payload:
            self.payload = payload
            updated = True

        if value != None:
            self.brightness_val  = value

        await self.send(receivedSetting=value)
        if updated and self.after_update_cb is not None:
            await self.after_update_cb()

    async def state(self, raw_value):
        """Set new value."""
        if int(raw_value) == TelegramSetting.ON.value:
            value = self.Value.ON
        else:
            value = self.Value.OFF

        updated = False
        if self.payload is None or self.payload != value:
            self.payload = value
            updated = True
        if updated and self.after_update_cb is not None:
            await self.after_update_cb()

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    def group_addr_str(self):
        """Return object as readable string."""
        return '{0}/{1}/{2}/{3}' \
            .format(self.group_address.__repr__(),
                    self.group_address_state.__repr__(),
                    self.payload,
                    self.value)

    def __str__(self):
        """Return object as string representation."""
        return '<{} device_name="{}" {}/>'.format(
            self.__class__.__name__,
            self.device_name,
            self.group_addr_str())

    def __eq__(self, other):
        """Equal operator."""
        for key, value in self.__dict__.items():
            if key == "after_update_cb":
                continue
            if key not in other.__dict__:
                return False
            if other.__dict__[key] != value:
                return False
        for key, value in other.__dict__.items():
            if key == "after_update_cb":
                continue
            if key not in self.__dict__:
                return False
        return True

class TeletaskValue():
    def __init__(self):
        self.value = 0