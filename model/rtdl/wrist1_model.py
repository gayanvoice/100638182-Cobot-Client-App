class Wrist1Model:
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
        wrist1_model = Wrist1Model()
        wrist1_model.position = rtdl_model.data_row[rtdl_model.header_row.index("actual_q_3")]
        wrist1_model.temperature = rtdl_model.data_row[rtdl_model.header_row.index("joint_temperatures_3")]
        wrist1_model.voltage = rtdl_model.data_row[rtdl_model.header_row.index("actual_current_3")]
        return wrist1_model
