from model.joint_load_model import JointLoadModel


class BaseModel(JointLoadModel):
    pass

    @staticmethod
    def get_from_rows(header_row, data_row):
        join_load_model = JointLoadModel()
        join_load_model.temperature = data_row[header_row.index("timestamp")]
        join_load_model.load = data_row[header_row.index("timestamp")]
        join_load_model.status = data_row[header_row.index("timestamp")]
        join_load_model.voltage = data_row[header_row.index("timestamp")]
        return join_load_model
