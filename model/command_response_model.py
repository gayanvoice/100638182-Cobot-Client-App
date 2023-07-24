import time


class Status:
    COMMAND_EXECUTION_SEQUENCE_ERROR = "COMMAND_EXECUTION_SEQUENCE_ERROR"
    COMMAND_SYNTAX_ERROR = "COMMAND_SYNTAX_ERROR"
    COBOT_CLIENT_ERROR = "COBOT_CLIENT_ERROR"
    AZURE_IOT_ERROR = "AZURE_IOT_ERROR"
    COBOT_CLIENT_EXECUTED = "COBOT_CLIENT_EXECUTED"
    AZURE_IOT_EXECUTED = "AZURE_IOT_EXECUTED"


class CommandResponseModel:
    def __init__(self):
        self._status = None
        self._message = None
        self._duration = None
        self._start_perf_counter = time.perf_counter()
        self._end_perf_counter = None

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value

    def set_response(self, status, message):
        self._status = status
        self._message = message
        return self

    def get(self):
        self._end_perf_counter = time.perf_counter()
        self._duration = self._end_perf_counter - self._start_perf_counter
        return {
            "_status": self._status,
            "_message": self._message,
            "_duration": self._duration
        }
