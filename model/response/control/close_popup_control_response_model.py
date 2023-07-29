__author__ = "100638182"
__copyright__ = "University of Derby"

from model.response.response_model import ResponseModel


class ClosePopupControlResponseModel(ResponseModel):
    def __init__(self):
        super().__init__()

    def get(self):
        super_result = super().get()
        return {
            "status": super_result.status,
            "log_text": super_result.log_text,
            "duration": super_result.duration
        }
