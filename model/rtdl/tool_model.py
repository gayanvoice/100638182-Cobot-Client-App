class ToolModel:
    def __init__(self):
        self._temperature = None
        self._voltage = None
        self._x = None
        self._y = None
        self._z = None
        self._rx = None
        self._ry = None
        self._rz = None

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

    @property
    def rx(self):
        return self._rx

    @property
    def ry(self):
        return self._ry

    @property
    def rz(self):
        return self._rz

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

    @rx.setter
    def rx(self, value):
        self._rx = value

    @ry.setter
    def ry(self, value):
        self._ry = value

    @rz.setter
    def rz(self, value):
        self._rz = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        tool_model = ToolModel()
        tool_model.temperature = rtdl_model.data_row[rtdl_model.header_row.index("tool_temperature")]
        tool_model.voltage = rtdl_model.data_row[rtdl_model.header_row.index("tool_output_voltage")]
        tool_model.x = rtdl_model.data_row[rtdl_model.header_row.index("actual_TCP_pose_0")]
        tool_model.y = rtdl_model.data_row[rtdl_model.header_row.index("actual_TCP_pose_1")]
        tool_model.z = rtdl_model.data_row[rtdl_model.header_row.index("actual_TCP_pose_2")]
        tool_model.rx = rtdl_model.data_row[rtdl_model.header_row.index("actual_TCP_pose_3")]
        tool_model.ry = rtdl_model.data_row[rtdl_model.header_row.index("actual_TCP_pose_4")]
        tool_model.rz = rtdl_model.data_row[rtdl_model.header_row.index("actual_TCP_pose_5")]
        return tool_model

    @staticmethod
    def get_from_parsed_data(parsed_data):
        tool_model = ToolModel()
        tool_model.temperature = parsed_data["tool_model"]["_temperature"]
        tool_model.voltage = parsed_data["tool_model"]["_voltage"]
        tool_model.x = parsed_data["tool_model"]["_x"]
        tool_model.y = parsed_data["tool_model"]["_y"]
        tool_model.z = parsed_data["tool_model"]["_z"]
        tool_model.rx = parsed_data["tool_model"]["_rx"]
        tool_model.ry = parsed_data["tool_model"]["_ry"]
        tool_model.rz = parsed_data["tool_model"]["_rz"]
        return tool_model
