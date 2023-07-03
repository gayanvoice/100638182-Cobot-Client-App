import logging
import asyncio
import json


class ControlBoxIotTask:

    def __init__(self, device):
        self.__device = device
        self.__json_file = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.info("control_box_iot_task.connect:starting")

        while self.__running:
            try:
                cache_json_file = open('cache.json')
                data_object = json.load(cache_json_file)
                # logging.info("cobot_iot_task.connect:data_object={data_object}".format(data_object=data_object))
                cache_json_file.close()
                telemetry = {"Voltage": data_object['control_box_model']['_voltage']}
                logging.info("control_box_iot_task.connect:" + str(telemetry))
                await self.__device.send_telemetry(telemetry)
                await asyncio.sleep(5)

            except Exception as ex:
                await asyncio.sleep(5)
                logging.error("control_box_iot_task.connect.while:error={error}".format(error=str(ex)))

        logging.debug("control_box_iot_task.connect:complete")


