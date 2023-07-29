
__author__ = "100638182"
__copyright__ = "University of Derby"


class Wrist3Model:
    def __init__(self):
        self._position = None
        self._temperature = None
        self._voltage = None

    @property
    def position(self):
        return self._position

    @property
    def temperature(self):
        return self._temperature

    @property
    def voltage(self):
        return self._voltage

    @position.setter
    def position(self, value):
        self._position = value

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @voltage.setter
    def voltage(self, value):
        self._voltage = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        wrist3_model = Wrist3Model()
        wrist3_model.position = rtdl_model.data_row[rtdl_model.header_row.index("actual_q_5")]
        wrist3_model.temperature = rtdl_model.data_row[rtdl_model.header_row.index("joint_temperatures_5")]
        wrist3_model.voltage = rtdl_model.data_row[rtdl_model.header_row.index("actual_current_5")]
        return wrist3_model

    @staticmethod
    def get_from_parsed_data(parsed_data):
        wrist3_model = Wrist3Model()
        wrist3_model.position = parsed_data["wrist3_model"]["_position"]
        wrist3_model.temperature = parsed_data["wrist3_model"]["_temperature"]
        wrist3_model.voltage = parsed_data["wrist3_model"]["_voltage"]
        return wrist3_model
