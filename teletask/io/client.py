"""
Client is an abstraction for handling the complete UDP io.
The module is build upon asyncio udp functions.
Due to lame support of UDP multicast within asyncio some special treatment for multicast is necessary.
"""
import asyncio
import socket
import binascii
import time

#from teletask.exceptions import CouldNotParseTeletaskIP, XTeletaskException
from teletask.doip import Frame, FrameQueue


class Client:
    """Class for handling (sending and receiving) TCP packets."""

    # pylint: disable=too-few-public-methods

    class Callback:
        """Callback class for handling callbacks for different 'service types' of received packets."""

        def __init__(self, callback, service_types=None):
            """Initialize Callback class."""
            self.callback = callback
            self.service_types = service_types or []

        def has_service(self, service_type):
            """Test if callback is listening for given service type."""
            return \
                len(self.service_types) == 0 or \
                service_type in self.service_types

    class ClientFactory(asyncio.Protocol):
        """Abstraction for managing the asyncio-tcp transports."""

        def __init__(self,
                     host, port,
                     data_received_callback=None,teletask=None):
            """Initialize ClientFactory class."""
            self.host = host
            self.port = port
            self.data_received_callback = data_received_callback
            self.teletask = teletask

        def connection_made(self, transport):
            """Assign transport. Callback after TCP connection was made."""
            self.transport = transport

        def data_received(self, data):
            """Call assigned callback. Callback for datagram received."""
            if self.data_received_callback is not None:
                self.data_received_callback(data)

        def error_received(self, exc):
            """Handle errors. Callback for error received."""
            if hasattr(self, 'teletask'):
                self.teletask.logger.warning('Error received: %s', exc)

        def connection_lost(self, exc):
            """Log error. Callback for connection lost."""
            if hasattr(self, 'teletask'):
                self.teletask.logger.info('closing transport %s', exc)
        
        def send(self,msg):
            self.transport.write(msg)

    def __init__(self, teletask, host, port, telegram_received_callback=None):
        """Initialize Client class."""
        self.teletask = teletask
        self.host = host
        self.port = port
        self.callbacks = []

    def data_received_callback(self, raw):
        """Parse and process Teletask frame. Callback for having received an TCP packet."""
        if raw:
            try:
                frame_queue = FrameQueue()
                frames = frame_queue.process_frames(raw)
                for frame in frames:
                    self.teletask.logger.info("Received: %s", frame)
                    self.handle_teletaskframe(frame)

            except Exception as ex:
                self.teletask.logger.exception(ex)

    def handle_teletaskframe(self, frame):
        """Handle Frame and call all callbacks which watch for the service type ident."""
        handled = False
        for callback in self.callbacks:
            callback.callback(frame, self)
            handled = True
        if not handled:
            self.teletask.logger.debug("UNHANDLED: %s", frame)

    def register_callback(self, callback):
        """Register callback."""
        callb = Client.Callback(callback)
        self.callbacks.append(callb)
        return callb

    def unregister_callback(self, callb):
        """Unregister callback."""
        self.callbacks.remove(callb)

    async def connect(self):
        """Connect TCP socket. Open UDP port and build mulitcast socket if necessary."""
        client_factory = Client.ClientFactory(host=self.host, port=self.port, data_received_callback=self.data_received_callback, teletask=self.teletask)
        
        (reader, writer) = await self.teletask.loop.create_connection(
            lambda: client_factory,
            host=self.host,
            port=self.port)

        self.reader = reader
        self.writer = writer
        

    async def send_telegram(self,frame):
        self.send(frame)

    def send(self, frame):
        """Send Frame to socket."""
        self.teletask.logger.info("Sending: %s", frame)
        self.writer.send(frame.to_teletask().encode())
        #time.sleep(0.2)

    async def stop(self):
        """Stop TCP socket."""
        self.reader.close()
        self.reader.writer()
        