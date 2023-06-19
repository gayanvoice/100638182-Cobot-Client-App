from model.rtdl_model import RtdlModel


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

    @y.setter
    def y(self, value):
        self._y = value

    @z.setter
    def z(self, value):
        self._z = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        base_model = BaseModel()
        base_model.position = rtdl_model.data_row[rtdl_model.header_row.index("timestamp")]  # Assuming position is the first element in the header_row
        base_model.temperature = rtdl_model.header_row[1]  # Assuming temperature is the second element in the header_row
        base_model.voltage = rtdl_model.header_row[2]  # Assuming voltage is the third element in the header_row
        base_model.x = rtdl_model.data_row[0]  # Assuming x is the first element in the data_row
        base_model.y = rtdl_model.data_row[1]  # Assuming y is the second element in the data_row
        base_model.z = rtdl_model.data_row[2]  # Assuming z is the third element in the data_row
        return base_model
