class ControlBoxModel(object):
    def __init__(self):
        self._controller_temperature = None
        self._main_voltage = None
        self._average_robot_power = None
        self._current = None
        self._io_current = None
        self._tool_current = None

    @property
    def controller_temperature(self):
        return self._controller_temperature

    @property
    def main_voltage(self):
        return self._main_voltage

    @property
    def average_robot_power(self):
        return self._average_robot_power

    @property
    def current(self):
        return self.current

    @property
    def io_current(self):
        return self._io_current

    @property
    def tool_current(self):
        return self._tool_current

    @controller_temperature.setter
    def controller_temperature(self, value):
        self._controller_temperature = value

    @main_voltage.setter
    def main_voltage(self, value):
        self._main_voltage = value

    @average_robot_power.setter
    def average_robot_power(self, value):
        self._average_robot_power = value

    @current.setter
    def current(self, value):
        self._current = value

    @io_current.setter
    def io_current(self, value):
        self._io_current = value

    @tool_current.setter
    def tool_current(self, value):
        self._tool_current = value
