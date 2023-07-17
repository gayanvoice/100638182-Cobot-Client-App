import logging
import asyncio
import json


class Wrist3IotTask:

    def __init__(self, device):
        self.__device = device
        self.__json_file = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.info("wrist3_iot_task.connect:starting")

        while self.__running:
            try:
                cache_json_file = open('cache.json')
                data_object = json.load(cache_json_file)
                cache_json_file.close()
                telemetry = {"Position": data_object['base_model']['_position'],
                             "Temperature": data_object['base_model']['_temperature'],
                             "Voltage": data_object['base_model']['_voltage']}
                logging.info("wrist3_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except Exception as ex:
                await asyncio.sleep(5)
                logging.error("wrist3_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("wrist3_iot_task.connect:complete")


