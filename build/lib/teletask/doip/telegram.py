"""
Module for DoIP Telegrams.
"""
from enum import Enum
from teletask.exceptions import CouldNotParseTeletaskCommand

class TeletaskConst(Enum):
    START = 2
    CENTRAL = 1

class TelegramCommand(Enum):
    SET = 7
    GET = 6
    GROUPSET = 9
    LOG = 3
    EVENTREPORT = 0x10
    WRITEDISPLAY = 4
    KEEPALIVE = 11

class TelegramFunction(Enum):
    RELAY = 1
    DIMMER = 2
    MOTOR = 6
    LOCMOOD = 8
    GENMOOD = 10
    FLAG = 15
    SENSOR = 20
    AUDIO = 31
    PROCESS = 3
    REGIME = 14
    SERVICE = 53
    MESSAGE = 54
    CONDITION = 60

class TelegramSetting(Enum):
    ON = 255
    TOGGLE = 103
    OFF = 0

class Telegram:
    """Class for DoIP telegrams."""

    def __init__(self,command=None,function=None,address=None,setting=None):
        """Initialize Telegram class."""
        self.start = TeletaskConst.START.value
        self.length = 0
        self.command = None
        self.payload = {}

        if(str(command) == "TelegramCommand.LOG"):
            self.payload[0] = function.value
            self.payload[1] = 1
        elif(str(command) == "TelegramCommand.GET"):
            self.payload[0] = 1 # Central
            self.payload[1] = function.value
            self.payload[2] = 0
            self.payload[3] = address
        elif(str(command) == "TelegramCommand.SET"):
            self.payload[0] = 1
            self.payload[1] = None

            if(function!=None):
              self.payload[1] = function.value
        else:
            raise CouldNotParseTeletaskCommand

        if(command!=None):
            self.command = command.value

        if(setting!=None):
            self.payload[2] = 0
            self.payload[3] = address
            self.payload[4] = setting.value

        self.checksum = 0

    def to_teletask(self):
        print(str(self))
        return str(self)

    def __str__(self):
        """Return object as readable string."""
        self.calc_length()
        self.calc_checksum()

        payload_str = ','.join(("{!s}".format(val) for (key,val) in self.payload.items()))
        message = "s,{0},{1},{2},{3},".format(
                    self.length, self.command,
                    payload_str, self.checksum)
        return message

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__

    def calc_length(self):
        try:
            self.length = len(self.payload) + 3
        except Exception:
            self.length = 8


    def calc_checksum(self):
        packet_sum = 0
        for (key,val) in self.payload.items():
            packet_sum = packet_sum + val

        packet_sum = packet_sum + self.start + self.length + self.command
        self.checksum = (packet_sum % 256)


class TelegramHeartbeat:
    """Class for DoIP telegrams."""

    def __init__(self):
        """Initialize Telegram class."""

        self.content = TelegramCommand.KEEPALIVE

    def to_teletask(self):
        return str(self)

    def __str__(self):
        """Return object as readable string."""
        message = "s,3,{0},{1},".format(TelegramCommand.KEEPALIVE.value, (2+3+11 % 256))
        return message