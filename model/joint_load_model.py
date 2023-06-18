class JointLoadModel(object):
    def __init__(self):
        self._temperature = None
        self._load = None
        self._status = None
        self._voltage = None

    @property
    def temperature(self):
        return self._temperature

    @property
    def load(self):
        return self._load

    @property
    def status(self):
        return self._status

    @property
    def voltage(self):
        return self.voltage

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @load.setter
    def load(self, value):
        self._load = value

    @status.setter
    def status(self, value):
        self._status = value

    @voltage.setter
    def voltage(self, value):
        self._voltage = value

