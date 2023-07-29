__author__ = "100638182"
__copyright__ = "University of Derby"


class ElbowModel:
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
        elbow_model = ElbowModel()
        elbow_model.position = rtdl_model.data_row[rtdl_model.header_row.index("actual_q_2")]
        elbow_model.temperature = rtdl_model.data_row[rtdl_model.header_row.index("joint_temperatures_2")]
        elbow_model.voltage = rtdl_model.data_row[rtdl_model.header_row.index("actual_current_2")]
        elbow_model.x = rtdl_model.data_row[rtdl_model.header_row.index("elbow_position_0")]
        elbow_model.y = rtdl_model.data_row[rtdl_model.header_row.index("elbow_position_1")]
        elbow_model.z = rtdl_model.data_row[rtdl_model.header_row.index("elbow_position_2")]
        return elbow_model

    @staticmethod
    def get_from_parsed_data(parsed_data):
        elbow_model = ElbowModel()
        elbow_model.position = parsed_data["elbow_model"]["_position"]
        elbow_model.temperature = parsed_data["elbow_model"]["_temperature"]
        elbow_model.voltage = parsed_data["elbow_model"]["_voltage"]
        elbow_model.x = parsed_data["elbow_model"]["_x"]
        elbow_model.y = parsed_data["elbow_model"]["_y"]
        elbow_model.z = parsed_data["elbow_model"]["_z"]
        return elbow_model
