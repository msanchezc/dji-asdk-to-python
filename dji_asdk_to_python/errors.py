class CustomError:
    pass


class DJIError(CustomError):
    ERROR_CODE = "errorCode"
    DESCRIPTION = "description"

    def __init__(self, errorCode, description):
        self.errorCode = errorCode
        self.description = description

    def __str__(self):
        return "DJIError instance with data: %s" % str(
            {"ERROR_CODE": self.errorCode, "DESCRIPTION": self.description}
        )


class SocketError(CustomError):
    def __init__(self, message_error):
        self.message_error = message_error

    def __str__(self):
        return "SocketError instance with data: %s" % self.message_error


class JsonError(CustomError):
    def __init__(self, message_error):
        self.message_error = message_error

    def __str__(self):
        return "JsonError instance with data: %s" % self.message_error


class ModuleNotAvailableError(CustomError):
    def __init__(self, message_error):
        self.message_error = message_error

    def __str__(self):
        return "ModuleNotAvailableError instance with data: %s" % (
            self.message_error
        )


class BridgeIOError(CustomError):
    def __init__(self, message_error):
        self.message_error = message_error

    def __str__(self):
        return "BridgeIOError instance with data: %s" % self.message_error


class CommunicationError(CustomError):
    def __init__(self, message_error):
        self.message_error = message_error

    def __str__(self):
        return "CommunicationError instance with data: %s" % self.message_error
