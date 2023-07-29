__author__ = "100638182"
__copyright__ = "University of Derby"

import logging
import asyncio
import json


class CobotIotTask:

    def __init__(self, cobot_device):
        self.__device = cobot_device
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
        logging.info("cobot_iot_task.connect:Starting")

        self.__cache_json_content = self.load_json_content()

        while self.__running:
            if self.__cache_json_content != self.load_json_content():
                telemetry = {"ElapsedTime": self.__cache_json_content['cobot_model']['_elapsed_time']}
                logging.info("cobot_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                self.__cache_json_content = self.load_json_content()
            else:
                await asyncio.sleep(1)

        logging.debug("cobot_iot_task.connect:Complete")


