__author__ = "100638182"
__copyright__ = "University of Derby"

import time


class Status:
    COMMAND_EXECUTION_SEQUENCE_ERROR = "COMMAND_EXECUTION_SEQUENCE_ERROR"
    COMMAND_SYNTAX_ERROR = "COMMAND_SYNTAX_ERROR"
    COBOT_CLIENT_ERROR = "COBOT_CLIENT_ERROR"
    AZURE_IOT_ERROR = "AZURE_IOT_ERROR"
    COBOT_CLIENT_EXECUTED = "COBOT_CLIENT_EXECUTED"
    AZURE_IOT_EXECUTED = "AZURE_IOT_EXECUTED"


class ResponseModel:
    def __init__(self):
        self._status = None
        self._log_text = None
        self._duration = None
        self._start_perf_counter = time.perf_counter()
        self._end_perf_counter = None

    @property
    def status(self):
        return self._status

    @property
    def log_text(self):
        return self._log_text

    @property
    def duration(self):
        return self._duration

    @status.setter
    def status(self, value):
        self._status = value

    @log_text.setter
    def log_text(self, value):
        self._log_text = value

    def set_response(self, status, log_text):
        self._status = status
        self._log_text = log_text
        return self

    def get(self):
        self._end_perf_counter = time.perf_counter()
        self._duration = self._end_perf_counter - self._start_perf_counter
        return self
