"""Module for Teletask Exceptions."""


class TeletaskException(Exception):
    """Default Teletask Exception."""

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__

    def __hash__(self):
        """Hash function."""
        return 0


class CouldNotParseTelegram(TeletaskException):
    """Could not parse telegram error."""

    def __init__(self, description, **kwargs):
        """Initialize CouldNotParseTelegram class."""
        super(CouldNotParseTelegram, self).__init__("Could not parse Telegram")
        self.description = description
        self.parameter = kwargs

    def _format_parameter(self):
        return " ".join(['%s="%s"' % (key, value) for (key, value) in sorted(self.parameter.items())])

    def __str__(self):
        """Return object as readable string."""
        return '<CouldNotParseTelegram description="{0}" {1}/>' \
            .format(self.description, self._format_parameter())

class CouldNotParseTeletaskCommand(TeletaskException):
    """Exception fails for wrong Teletask Command data."""

    def __init__(self, description=""):
        """Initialize CouldNotParseTeletaskCommand class."""
        super(CouldNotParseTeletaskIP, self).__init__("Could not parse Teletask Command")
        self.description = description

    def __str__(self):
        """Return object as readable string."""
        return '<CouldNotParseTeletaskCommand description="{0}" />' \
            .format(self.description)

class CouldNotParseTeletaskIP(TeletaskException):
    """Exception falss for worong TeletaskIP data."""

    def __init__(self, description=""):
        """Initialize CouldNotParseTelegram class."""
        super(CouldNotParseTeletaskIP, self).__init__("Could not parse TeletaskIP")
        self.description = description

    def __str__(self):
        """Return object as readable string."""
        return '<CouldNotParseTeletaskIP description="{0}" />' \
            .format(self.description)


class ConversionError(TeletaskException):
    """Exception class for error while converting one type to another."""

    def __init__(self, description, **kwargs):
        """Initialize ConversionError class."""
        super(ConversionError, self).__init__("Conversion Error")
        self.description = description
        self.parameter = kwargs

    def _format_parameter(self):
        return " ".join(['%s="%s"' % (key, value) for (key, value) in sorted(self.parameter.items())])

    def __str__(self):
        """Return object as readable string."""
        return '<ConversionError description="{0}" {1}/>'.format(self.description, self._format_parameter())


class CouldNotParseAddress(TeletaskException):
    """Exception class for wrong address format."""

    def __init__(self, address=None):
        """Initialize CouldNotParseAddress class."""
        super(CouldNotParseAddress, self).__init__("Could not parse address")
        self.address = address

    def __str__(self):
        """Return object as readable string."""
        return '<CouldNotParseAddress address="{0}" />'.format(self.address)


class DeviceIllegalValue(TeletaskException):
    """Exception class for setting a value of a device with an illegal value."""

    def __init__(self, value, description):
        """Initialize DeviceIllegalValue class."""
        super(DeviceIllegalValue, self).__init__("Illegal value for device")
        self.value = value
        self.description = description

    def __str__(self):
        """Return object as readable string."""
        return '<DeviceIllegalValue description="{0}" value="{1}" />'.format(
            self.value,
            self.description)