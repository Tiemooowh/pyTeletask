"""Teletask is an Asynchronous Python module for reading and writing Teletask/DoIP packets."""
import asyncio
import logging
import signal

from sys import platform

import time
from concurrent.futures import ProcessPoolExecutor

from teletask.core import TelegramQueue
from teletask.devices import Devices
from teletask.io import TeletaskDoIPInterface
from teletask.doip import Telegram, TeletaskConst, TelegramCommand, TelegramFunction, TelegramSetting, TelegramHeartbeat

class Teletask:
    """Class for reading and writing Teletask/DoIP packets."""
    DEFAULT_ADDRESS = ''

    def __init__(self,
                 config=None,
                 loop=None,
                 telegram_received_cb=None):

        """Initialize Teletask class."""
        self.devices = Devices()
        self.telegrams = asyncio.Queue()
        self.loop = loop or asyncio.get_event_loop()
        self.sigint_received = asyncio.Event()
        self.telegram_queue = TelegramQueue(self)
        self.state_updater = None
        self.teletaskip_interface = None
        self.started = False
        self.executors = ProcessPoolExecutor(2)
        self.registered_devices = {}
        self.logger = logging.getLogger('teletask.log')
        self.teletask_logger = logging.getLogger('teletask.teletask')
        self.telegram_logger = logging.getLogger('teletask.telegram')

        if telegram_received_cb is not None:
            self.telegram_queue.register_telegram_received_cb(telegram_received_cb)


    def __del__(self):
        """Destructor. Cleaning up if this was not done before."""
        if self.started:
            try:
                task = self.loop.create_task(self.stop())
                self.loop.run_until_complete(task)
            except RuntimeError as exp:
                self.logger.warning("Could not close loop, reason: %s", exp)

    async def start(self,
                    host=None,
                    port=None,
                    daemon_mode=False):
        """Start Teletask module. Connect to Teletask/DoIP devices and start state updater."""
        self.teletaskip_interface = TeletaskDoIPInterface(self)
        await self.teletaskip_interface.start(host,port,True,60)
        await self.telegram_queue.start()


        if daemon_mode:
            await self.loop_until_sigint()

        self.started = True

    async def join(self):
        """Wait until all telegrams were processed."""
        await self.telegrams.join()

    async def _stop_teletaskip_interface_if_exists(self):
        """Stop TeletaskIPInterface if initialized."""
        if self.teletaskip_interface is not None:
            await self.teletaskip_interface.stop()
            self.teletaskip_interface = None

    async def stop(self):
        """Stop Teletask module."""
        await self.join()
        await self.telegram_queue.stop()
        await self._stop_teletaskip_interface_if_exists()
        self.started = False

    async def loop_until_sigint(self):
        """Loop until Crtl-C was pressed."""
        def sigint_handler():
            """End loop."""
            self.sigint_received.set()
        if platform == "win32":
            self.logger.warning('Windows does not support signals')
        else:
            self.loop.add_signal_handler(signal.SIGINT, sigint_handler)
        self.logger.warning('Press Ctrl+C to stop')
        await self.sigint_received.wait()

    async def register_feedback(self):
        telegram = Telegram(command=TelegramCommand.LOG, function=TelegramFunction.RELAY)
        self.registered_devices["RELAY"] = {}
        await self.telegrams.put(telegram)
        await asyncio.sleep(1)

        telegram = Telegram(command=TelegramCommand.LOG, function=TelegramFunction.DIMMER)
        self.registered_devices["DIMMER"] = {}
        await self.telegrams.put(telegram)
        await asyncio.sleep(1)

        telegram = Telegram(command=TelegramCommand.LOG, function=TelegramFunction.LOCMOOD)
        self.registered_devices["LOCMOOD"] = {}
        await self.telegrams.put(telegram)
        await asyncio.sleep(1)

        telegram = Telegram(command=TelegramCommand.LOG, function=TelegramFunction.GENMOOD)
        self.registered_devices["GENMOOD"] = {}
        await self.telegrams.put(telegram)
        await asyncio.sleep(1)

        telegram = Telegram(command=TelegramCommand.LOG, function=TelegramFunction.FLAG)
        self.registered_devices["FLAG"] = {}
        await self.telegrams.put(telegram)
        await asyncio.sleep(1)


    def register_device(self, device):
        if device.doip_component in self.registered_devices:
            self.registered_devices[device.doip_component][device.switch.group_address] = device