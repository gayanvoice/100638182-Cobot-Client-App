class ControlBoxModel(object):
    def __init__(self):
        self._voltage = None

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        control_box_model = ControlBoxModel()
        control_box_model.voltage = rtdl_model.data_row[rtdl_model.header_row.index("actual_main_voltage")]
        return control_box_model

    @staticmethod
    def get_from_parsed_data(parsed_data):
        control_box_model = ControlBoxModel()
        control_box_model.voltage = parsed_data["control_box_model"]["_voltage"]
        return control_box_model
