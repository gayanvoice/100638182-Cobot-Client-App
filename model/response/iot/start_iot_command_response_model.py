from model.response.response_model import ResponseModel


class StartIotCommandRespondModel(ResponseModel):
    def __init__(self):
        super().__init__()

    def get(self):
        super_result = super().get()
        return {
            "status": super_result.status,
            "log_text": super_result.log_text,
            "duration": super_result.duration
        }

