import logging
import asyncio
import json


class ElbowIotTask:

    def __init__(self, device):
        self.__device = device
        self.__json_file = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.info("elbow_iot_task.connect:starting")

        while self.__running:
            try:
                cache_json_file = open('cache.json')
                data_object = json.load(cache_json_file)
                cache_json_file.close()
                telemetry = {"position": data_object['elbow_model']['_position'],
                             "temperature": data_object['elbow_model']['_temperature'],
                             "voltage": data_object['elbow_model']['_voltage'],
                             "x": data_object['elbow_model']['_x'],
                             "y": data_object['elbow_model']['_y'],
                             "z": data_object['elbow_model']['_z']}
                logging.info("elbow_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except Exception as ex:
                await asyncio.sleep(5)
                logging.error("elbow_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("elbow_iot_task.connect:complete")


