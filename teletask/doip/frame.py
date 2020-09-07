"""
Module for DoIP Responses.
"""
import re
from teletask.doip import Telegram, TelegramFunction, TelegramCommand

class FrameQueue:
    """Initialize Telegram class."""


    def __init__(self):
        """Initialize object."""


    def process_frames(self,raw):
        full_packet = ','.join(str(x) for x in raw)
        r1 = re.findall(r"(2,9,16,([0-9]*,?){7})",full_packet)

        result = []
        for packet in r1:
            frame = self.process_frame(packet[0])
            if(frame != None):
                result.append(frame)

        return result

    def process_frame(self,packet):
        event = packet.split(",")

        try:
            if(len(event) > 0):
                payload = [x for x in event]

                frame = Frame(payload=payload, doip_component=int(event[4]), group_address=int(event[6]), state=int(event[8]))
                return frame

        except Exception as e:
            print(e)

        return None

class Frame:
    command = None
    function = None
    group_address = None
    payload = None
    state = None
    doip_component = None
    event = None

    def __init__(self,command = None, function = None, group_address = None, payload = None, state = None, doip_component = None):
        self.command = command
        self.function = function
        self.group_address = group_address
        self.payload = payload
        self.state = state
        self.doip_component = doip_component

    def __str__(self):
        return '<{0} {1} {2} {3}/>' \
            .format(self.doip_component, self.group_address, \
                    self.payload, self.state, self.event)