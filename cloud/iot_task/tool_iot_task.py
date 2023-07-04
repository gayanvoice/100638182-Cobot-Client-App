import logging
import asyncio
import json


class ToolIotTask:

    def __init__(self, device):
        self.__device = device
        self.__json_file = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.info("tool_iot_task.connect:starting")

        while self.__running:
            try:
                cache_json_file = open('cache.json')
                data_object = json.load(cache_json_file)
                cache_json_file.close()
                telemetry = {"temperature": data_object['tool_model']['_temperature'],
                             "voltage": data_object['tool_model']['_voltage'],
                             "x": data_object['tool_model']['_x'],
                             "y": data_object['tool_model']['_y'],
                             "z": data_object['tool_model']['_z'],
                             "rx": data_object['tool_model']['_rx'],
                             "ry": data_object['tool_model']['_ry'],
                             "rz": data_object['tool_model']['_rz']
                             }
                logging.info("tool_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except Exception as ex:
                await asyncio.sleep(5)
                logging.error("tool_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("tool_iot_task.connect:complete")


