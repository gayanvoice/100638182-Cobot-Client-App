import logging
import asyncio
import json


class PayloadIotTask:

    def __init__(self, device):
        self.__device = device
        self.__json_file = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.info("payload_iot_task.connect:starting")

        while self.__running:
            try:
                cache_json_file = open('cache.json')
                data_object = json.load(cache_json_file)
                cache_json_file.close()
                telemetry = {"Mass": data_object['payload_model']['_mass'],
                             "CogX": data_object['payload_model']['_cogx'],
                             "CogY": data_object['payload_model']['_cogy'],
                             "CogZ": data_object['payload_model']['_cogz']}
                logging.info("payload_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except Exception as ex:
                await asyncio.sleep(5)
                logging.error("payload_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("payload_iot_task.connect:complete")


