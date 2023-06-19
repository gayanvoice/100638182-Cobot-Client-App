class RtdlModel:
    def __init__(self):
        self._header_row = None
        self._data_row = None

    @property
    def header_row(self):
        return self._header_row

    @property
    def data_row(self):
        return self._data_row

    @header_row.setter
    def header_row(self, value):
        self._header_row = value

    @data_row.setter
    def data_row(self, value):
        self._data_row = value

    @staticmethod
    def get_from_rows(header_row, data_row):
        rtdl_model = RtdlModel()
        rtdl_model.header_row = header_row
        rtdl_model.data_row = data_row
        return rtdl_model
