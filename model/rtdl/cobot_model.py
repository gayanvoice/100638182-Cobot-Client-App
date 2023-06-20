class CobotModel(object):
    def __init__(self):
        self._elapsed_time = None

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        self._elapsed_time = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        cobot_model = CobotModel()
        cobot_model.elapsed_time = rtdl_model.data_row[rtdl_model.header_row.index("timestamp")]
        return cobot_model
