import json
import logging
import sys
import asyncio
import json
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

from model.rtdl_dt_model import RtdlDtModel
from model.rtdl_model import RtdlModel
from twin_writer import TwinWriter


class CobotIotTask:

    def __init__(self, cobot_device):
        self.__cobot_device = cobot_device
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
            try:
                if self.__cache_json_content != self.load_json_content():
                    telemetry = {"ElapsedTime": self.__cache_json_content['cobot_model']['_elapsed_time']}
                    logging.info("cobot_iot_task.connect:" + str(telemetry))
                    await self.__cobot_device.send_telemetry(telemetry)
                    self.__cache_json_content = self.load_json_content()
                else:
                    await asyncio.sleep(1)
            except rtde.RTDEException as ex:
                await asyncio.sleep(5)
                logging.error("cobot_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("cobot_iot_task.connect:Complete")


