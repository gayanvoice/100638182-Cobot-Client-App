class BaseModel:
    def __init__(self):
        self._position = None
        self._temperature = None
        self._voltage = None
        self._x = None
        self._y = None
        self._z = None

    @property
    def position(self):
        return self._position

    @property
    def temperature(self):
        return self._temperature

    @property
    def voltage(self):
        return self._voltage

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @position.setter
    def position(self, value):
        self._position = value

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @voltage.setter
    def voltage(self, value):
        self._voltage = value

    @x.setter
    def x(self, value):
        self._x = value

    @x.setter
    def y(self, value):
        self._y = value

    @x.setter
    def z(self, value):
        self._z = value

    @staticmethod
    def get_from_rows(header_row, data_row):
        join_load_model = JointLoadModel()
        join_load_model.temperature = data_row[header_row.index("timestamp")]
        join_load_model.load = data_row[header_row.index("timestamp")]
        join_load_model.status = data_row[header_row.index("timestamp")]
        join_load_model.voltage = data_row[header_row.index("timestamp")]
        return join_load_model
