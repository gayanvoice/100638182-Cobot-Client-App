from model.response.response_model import ResponseModel


class EnableControlResponseModel(ResponseModel):
    def __init__(self):
        super().__init__()
        self._elapsed_time = None

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        self._elapsed_time = value

    def get(self):
        super_result = super().get()
        return {
            "status": super_result.status,
            "log_text": super_result.log_text,
            "duration": super_result.duration,
            "elapsed_time": self.elapsed_time
        }
