import json


class OpenPopupControlRequestModel:
    def __init__(self):
        self._popup_text = None

    @property
    def popup_text(self):
        return self._popup_text

    @popup_text.setter
    def popup_text(self, value):
        self._popup_text = value

    @staticmethod
    def get_open_popup_control_request_model_from_values(values):
        data = json.loads(values)
        open_popup_control_request_model = OpenPopupControlRequestModel()
        open_popup_control_request_model.popup_text = data["popup_text"]
        return open_popup_control_request_model
