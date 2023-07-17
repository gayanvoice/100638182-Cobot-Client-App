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
                telemetry = {"Position": data_object['elbow_model']['_position'],
                             "Temperature": data_object['elbow_model']['_temperature'],
                             "Voltage": data_object['elbow_model']['_voltage'],
                             "X": data_object['elbow_model']['_x'],
                             "Y": data_object['elbow_model']['_y'],
                             "Z": data_object['elbow_model']['_z']}
                logging.info("elbow_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except Exception as ex:
                await asyncio.sleep(5)
                logging.error("elbow_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("elbow_iot_task.connect:complete")


