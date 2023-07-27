class LogTextStatus:
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"


class LogTextHelper:

    def __init__(self, class_name):
        self.__class_name = class_name

    def get_log_text(self, status, command_name, input_dictionary):
        log_text = "{class_name}.{command_name}:{status} ".format(
            status=status,
            class_name=self.__class_name,
            command_name=command_name)
        for key, value in input_dictionary.items():
            log_text += f"{key}={value} "
        return log_text
