"""
TeletaskDoIPInterface manages Teletask/DoIP connections.
* It searches for available devices and connects with the corresponding connect method.
* It passes Teletask telegrams from the network and
* provides callbacks after having received a telegram from the network.
"""
from enum import Enum
from platform import system as get_os_name

from .client import Client

from teletask.exceptions import TeletaskException

class TeletaskDoIPInterface():
    """Class for managing Teletask/DoIP Tunneling or Routing connections."""

    def __init__(self, teletask):
        """Initialize TeletaskDoIPInterface class."""
        self.teletask = teletask

    async def start(self, host, port, auto_reconnect, auto_reconnect_wait):
        """Start Teletask/DoIP."""
        self.teletask.logger.debug("Starting to %s:%s ", host, port)
        self.interface = Client(self.teletask,host,port,telegram_received_callback=self.telegram_received)
        
        self.interface.register_callback(self.response_rec_callback)

        await self.interface.connect()

    def response_rec_callback(self, frame, _):
        """Verify and handle doipframe. Callback from internal client."""
        self.telegram_received(frame)

    async def stop(self):
        """Stop connected interfae."""
        if self.interface is not None:
            await self.interface.stop()
            self.interface = None

    def telegram_received(self, telegram):
        """Put received telegram into queue. Callback for having received telegram."""
        self.teletask.loop.create_task(self.teletask.telegrams.put(telegram))

    async def send_telegram(self, telegram):
        """Send telegram to connected device."""
        await self.interface.send_telegram(telegram)