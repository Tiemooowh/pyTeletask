"""
Device is the base class for all implemented devices (e.g. Lights/Switches/Sensors).
It provides basis functionality for reading the state from the Teletask bus.
"""
from teletask.exceptions import TeletaskException
from teletask.doip import Telegram#, TelegramType


class Device:
    """Base class for devices."""

    def __init__(self, teletask, name, device_updated_cb=None):
        """Initialize Device class."""
        self.teletask = teletask
        self.doip_component = "UNKOWN"
        self.name = name
        self.device_updated_cbs = []
        if device_updated_cb is not None:
            self.register_device_updated_cb(device_updated_cb)

    def register_device_updated_cb(self, device_updated_cb):
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb):
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def after_update(self):
        """Execute callbacks after internal state has been changed."""
        for device_updated_cb in self.device_updated_cbs:
            await device_updated_cb(self)

    async def sync(self, wait_for_result=True):
        """Read state of device from Teletask bus."""
        try:
            await self._sync_impl(wait_for_result)
        except TeletaskException as ex:
            self.teletask.logger.error("Error while syncing device: %s", ex)

    async def _sync_impl(self, wait_for_result=True):
        self.teletask.logger.debug("Sync %s", self.name)
        for group_address in self.state_addresses():
            from teletask.core import ValueReader
            value_reader = ValueReader(self.teletask, group_address)
            if wait_for_result:
                telegram = await value_reader.read()
                if telegram is not None:
                    await self.process(telegram)
                else:
                    self.teletask.logger.warning("Could not read value of %s %s", self, group_address)
            else:
                await value_reader.send_group_read()

    async def send(self, group_address, payload=None, response=False):
        """Send payload as telegram to Teletask bus."""
        telegram = Telegram()
        telegram.group_address = group_address
        telegram.payload = payload
        telegram.telegramtype = TelegramType.GROUP_RESPONSE \
            if response else TelegramType.GROUP_WRITE
        await  self.teletask.telegrams.put(telegram)

    def state_addresses(self):
        """Return group addresses which should be requested to sync state."""
        # pylint: disable=no-self-use
        return []

    async def process(self, telegram):
        """Process incoming telegram."""
        pass
        # 
        # if telegram.telegramtype == TelegramType.GROUP_WRITE:
        #     await self.process_group_write(telegram)
        # elif telegram.telegramtype == TelegramType.GROUP_RESPONSE:
        #     await self.process_group_response(telegram)
        # elif telegram.telegramtype == TelegramType.GROUP_READ:
        #     await self.process_group_read(telegram)

    async def process_group_read(self, telegram):
        """Process incoming GROUP RESPONSE telegram."""
        # The dafault is, that devices dont answer to group reads
        pass

    async def process_group_response(self, telegram):
        """Process incoming GROUP RESPONSE telegram."""
        # Per default mapped to group write.
        await self.process_group_write(telegram)

    async def process_group_write(self, telegram):
        """Process incoming GROUP WRITE telegram."""
        # The dafault is, that devices dont answer to group reads
        pass

    def get_name(self):
        """Return name of device."""
        return self.name

    async def do(self, action):
        """Execute 'do' commands."""
        # pylint: disable=invalid-name
        self.teletask.logger.info("Do not implemented action '%s' for %s", action, self.__class__.__name__)