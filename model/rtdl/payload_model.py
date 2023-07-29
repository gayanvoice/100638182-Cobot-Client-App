__author__ = "100638182"
__copyright__ = "University of Derby"


class PayloadModel(object):
    def __init__(self):
        self._mass = None
        self._cogx = None
        self._cogy = None
        self._cogz = None

    @property
    def mass(self):
        return self._mass

    @property
    def cogx(self):
        return self._cogx

    @property
    def cogy(self):
        return self._cogy

    @property
    def cogz(self):
        return self._cogz

    @mass.setter
    def mass(self, value):
        self._mass = value

    @cogx.setter
    def cogx(self, value):
        self._cogx = value

    @cogy.setter
    def cogy(self, value):
        self._cogy = value

    @cogz.setter
    def cogz(self, value):
        self._cogz = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        payload_model = PayloadModel()
        payload_model.mass = rtdl_model.data_row[rtdl_model.header_row.index("payload")]
        payload_model.cogx = rtdl_model.data_row[rtdl_model.header_row.index("payload_cog_0")]
        payload_model.cogy = rtdl_model.data_row[rtdl_model.header_row.index("payload_cog_1")]
        payload_model.cogz = rtdl_model.data_row[rtdl_model.header_row.index("payload_cog_2")]
        return payload_model

    @staticmethod
    def get_from_parsed_data(parsed_data):
        payload_model = PayloadModel()
        payload_model.mass = parsed_data["payload_model"]["_mass"]
        payload_model.cogx = parsed_data["payload_model"]["_cogx"]
        payload_model.cogy = parsed_data["payload_model"]["_cogy"]
        payload_model.cogz = parsed_data["payload_model"]["_cogz"]
        return payload_model
