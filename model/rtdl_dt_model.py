from model.rtdl.base_model import BaseModel
from model.rtdl.cobot_model import CobotModel
from model.rtdl.control_box_model import ControlBoxModel
from model.rtdl.elbow_model import ElbowModel
from model.rtdl.payload_model import PayloadModel
from model.rtdl.shoulder_model import ShoulderModel
from model.rtdl.tool_model import ToolModel
from model.rtdl.wrist1_model import Wrist1Model
from model.rtdl.wrist2_model import Wrist2Model
from model.rtdl.wrist3_model import Wrist3Model


class RtdlDtModel(object):
    def __init__(self):
        self._cobot_model = None
        self._control_box_model = None
        self._payload_model = None
        self._base_model = None
        self._shoulder_model = None
        self._elbow_model = None
        self._wrist1_model = None
        self._wrist2_model = None
        self._wrist3_model = None
        self._tool_model = None

    @property
    def cobot_model(self):
        return self._cobot_model

    @property
    def control_box_model(self):
        return self._control_box_model

    @property
    def payload_model(self):
        return self._payload_model

    @property
    def base_model(self):
        return self._base_model

    @property
    def shoulder_model(self):
        return self._shoulder_model

    @property
    def elbow_model(self):
        return self._elbow_model

    @property
    def wrist1_model(self):
        return self._wrist1_model

    @property
    def wrist2_model(self):
        return self._wrist2_model

    @property
    def wrist3_model(self):
        return self._wrist3_model

    @property
    def tool_model(self):
        return self._tool_model

    @cobot_model.setter
    def cobot_model(self, value):
        self._cobot_model = value

    @control_box_model.setter
    def control_box_model(self, value):
        self._control_box_model = value

    @payload_model.setter
    def payload_model(self, value):
        self._payload_model = value

    @base_model.setter
    def base_model(self, value):
        self._base_model = value

    @shoulder_model.setter
    def shoulder_model(self, value):
        self._shoulder_model = value

    @elbow_model.setter
    def elbow_model(self, value):
        self._elbow_model = value

    @shoulder_model.setter
    def shoulder_model(self, value):
        self._shoulder_model = value

    @wrist1_model.setter
    def wrist1_model(self, value):
        self._wrist1_model = value

    @wrist2_model.setter
    def wrist2_model(self, value):
        self._wrist2_model = value

    @wrist3_model.setter
    def wrist3_model(self, value):
        self._wrist3_model = value

    @tool_model.setter
    def tool_model(self, value):
        self._tool_model = value

    @staticmethod
    def get_from_rtdl_model(rtdl_model):
        rtdl_dt_model = RtdlDtModel()
        rtdl_dt_model._cobot_model = CobotModel.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._control_box_model = ControlBoxModel.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._payload_model = PayloadModel.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._base_model = BaseModel.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._shoulder_model = ShoulderModel.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._elbow_model = ElbowModel.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._wrist1_model = Wrist1Model.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._wrist2_model = Wrist2Model.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._wrist3_model = Wrist3Model.get_from_rtdl_model(rtdl_model)
        rtdl_dt_model._tool_model = ToolModel.get_from_rtdl_model(rtdl_model)
        return rtdl_dt_model
