import logging
import asyncio
import json

from rtde import rtde


class ControlBoxIotTask:

    def __init__(self, device):
        self.__device = device
        self.__cache_json_path = "cache.json"
        self.__cache_json_content = None
        self.__running = True

    def terminate(self):
        self.__running = False


    def load_json_content(self):
        cache_json_file = open(self.__cache_json_path)
        json_content = json.load(cache_json_file)
        cache_json_file.close()
        return json_content


    async def connect(self):
        logging.info("control_box_iot_task.connect:Starting")
        self.__cache_json_content \
            = self.load_json_content()

        while self.__running:
            if self.__cache_json_content != self.load_json_content():
                telemetry = {"Voltage": self.__cache_json_content['control_box_model']['_voltage']}
                logging.info("control_box_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                self.__cache_json_content = self.load_json_content()
            else:
                await asyncio.sleep(1)


        logging.debug("control_box_iot_task.connect:Complete")


