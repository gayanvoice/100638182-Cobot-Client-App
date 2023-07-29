__author__ = "100638182"
__copyright__ = "University of Derby"

from model.response.response_model import ResponseModel


class PowerOffControlResponseModel(ResponseModel):
    def __init__(self):
        super().__init__()
        self._robot_mode = None
        self._robot_status = None

    @property
    def robot_mode(self):
        return self._robot_mode

    @property
    def robot_status(self):
        return self._robot_status

    @robot_mode.setter
    def robot_mode(self, value):
        self._robot_mode = value

    @robot_status.setter
    def robot_status(self, value):
        self._robot_status = value

    def get(self):
        super_result = super().get()
        return {
            "status": super_result.status,
            "log_text": super_result.log_text,
            "duration": super_result.duration,
            "robot_mode": self._robot_mode,
            "robot_status": self._robot_status
        }
