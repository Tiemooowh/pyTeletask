"""
Module for DoIP Responses.
"""
from teletask.doip import Telegram, TelegramFunction, TelegramCommand

class Frame:
    """Initialize Telegram class."""
    command = None
    function = None
    group_address = None
    payload = None
    state = None
    doip_component = None
    
    def __init__(self, raw):
        """Initialize object."""
        self.raw = raw
        event = None

        print([x for x in raw])
        
        for i in range(len(raw)):
            b = raw[i]
            
            if(b == 2):
                frame_length = int(raw[i+1]) + 1
                event = [None] * frame_length

                if((i + frame_length) <= len(raw)):
                    event = raw[i+1:frame_length]

        if(event != None):
            self.payload = [x for x in event]
            self.doip_component = self.payload[3]
            self.group_address = self.payload[5]
            self.state = self.payload[7]
            
            