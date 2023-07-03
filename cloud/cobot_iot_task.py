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
        self.__json_file = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.info("cobot_iot_task.connect:Starting")

        while self.__running:
            try:
                cache_json_file = open('cache.json')
                data_object = json.load(cache_json_file)
                # logging.info("cobot_iot_task.connect:data_object={data_object}".format(data_object=data_object))
                cache_json_file.close()
                telemetry = {"ElapsedTime": data_object['cobot_model']['_elapsed_time']}
                logging.info("cobot_iot_task.connect:" + str(telemetry))
                await self.__cobot_device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except rtde.RTDEException as ex:
                await asyncio.sleep(5)
                logging.error("cobot_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("cobot_iot_task.connect:Complete")


