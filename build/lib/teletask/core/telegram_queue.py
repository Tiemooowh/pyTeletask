"""
Module for queing telegrams.
When a device wants to sends a telegram to the Teletask bus, it has to queue it to the TelegramQueue within XTeletask.
The underlaying TeletaskIPInterface will poll the queue and send the packets to the correct Teletask/IP abstraction (Tunneling or Routing).
You may register callbacks to be notified if a telegram was pushed to the queue.
"""
import asyncio

from teletask.doip import Telegram, TelegramFunction, TelegramCommand, TelegramHeartbeat
from teletask.exceptions import TeletaskException


class TelegramQueue():
    """Class for telegram queue."""

    class Callback:
        """Callback class for handling telegram received callbacks."""
        def __init__(self, callback):
            """Initialize Callback class."""
            self.callback = callback


    def __init__(self, teletask):
        """Initialize TelegramQueue class."""
        self.teletask = teletask
        self.telegram_received_cbs = []
        self.queue_stopped = asyncio.Event()

    def register_telegram_received_cb(self, telegram_received_cb):
        """Register callback for a telegram beeing received from Teletask bus."""
        callback = TelegramQueue.Callback(telegram_received_cb)
        self.telegram_received_cbs.append(callback)
        return callback

    def unregister_telegram_received_cb(self, telegram_received_cb):
        """Unregister callback for a telegram beeing received from Teletask bus."""
        self.telegram_received_cbs.remove(telegram_received_cb)

    async def start(self):
        """Start telegram queue."""
        self.teletask.loop.create_task(self.run())
        asyncio.ensure_future(self.start_heartbeat())
        

    async def start_heartbeat(self):
        # your infinite loop here, for example:
        while True:
            telegram = TelegramHeartbeat()
            await self.teletask.telegrams.put(telegram)
            await asyncio.sleep(10)

    async def run(self):
        """Endless loop for processing telegrams."""
        while True:
            telegram = await self.teletask.telegrams.get()
            #asyncio.ensure_future(self.start())



            # Breaking up queue if None is pushed to the queue
            if telegram is None:
                break

            await self.process_telegram(telegram)
            self.teletask.telegrams.task_done()

        self.queue_stopped.set()

    async def stop(self):
        """Stop telegram queue."""
        self.teletask.logger.debug("Stopping TelegramQueue")
        # If a None object is pushed to the queue, the queue stops
        await self.teletask.telegrams.put(None)
        await self.queue_stopped.wait()

    async def process_all_telegrams(self):
        """Process all telegrams being queued."""
        while not self.teletask.telegrams.empty():
            telegram = self.teletask.telegrams.get_nowait()
            await self.process_telegram(telegram)
            self.teletask.telegrams.task_done()

    async def process_telegram(self, telegram):
        """Process telegram."""
        try:
            if str(type(telegram)) == "<class 'teletask.doip.frame.Frame'>":
                await self.process_telegram_incoming(telegram)
            else: 
                await self.process_telegram_outgoing(telegram)
        except Exception as ex:
           self.teletask.logger.error("Error while processing telegram %s", ex)

    async def process_telegram_outgoing(self, telegram):
        """Process outgoing telegram."""
        if self.teletask.teletaskip_interface is not None:
            await self.teletask.teletaskip_interface.send_telegram(telegram)
        else:
            self.teletask.logger.warning("No TeletaskIP interface defined")

    async def process_telegram_incoming(self, telegram):
        """Process incoming telegram."""
        processed = False
        for telegram_received_cb in self.telegram_received_cbs:
            if(telegram.doip_component != None):
                await self.update_component_state(doip_component=telegram.doip_component, group_address=telegram.group_address, state=telegram.state)
                ret = await telegram_received_cb.callback(telegram)
                if ret:
                    processed = True
        
    async def update_component_state(self, doip_component, group_address, state):
        doip_component_name = (TelegramFunction(doip_component).name)

        if(doip_component_name != 'None'):
            if(doip_component_name in self.teletask.registered_devices and group_address != None):
                try:
                    remote = self.teletask.registered_devices[doip_component_name][str(group_address)]
                    await remote.change_state(state)
                except:
                    self.teletask.logger.warning("No TeletaskIP Callback not defined That was no valid number.  Try again...")