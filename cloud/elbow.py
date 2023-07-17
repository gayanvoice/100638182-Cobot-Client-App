import asyncio
import logging
import json
from threading import Thread
from datetime import datetime
from cloud.device import Device
from cloud.iot_task.elbow_iot_task import ElbowIotTask
import xml.etree.ElementTree as ET
import time


class Elbow(object):
    def __init__(self,
                 model_id,
                 provisioning_host,
                 id_scope,
                 registration_id,
                 symmetric_key,
                 cobot_client_configuration_path):
        self.__model_id = model_id
        self.__provisioning_host = provisioning_host
        self.__id_scope = id_scope
        self.__registration_id = registration_id
        self.__symmetric_key = symmetric_key
        self.__cobot_client_configuration_path = cobot_client_configuration_path
        self.__device = None
        self.__iot_task = None
        self.__iot_thread = None
        self.__iot_lock = True

    def stdin_listener(self):
        while True:
            config_element_tree = ET.parse(self.__cobot_client_configuration_path)
            elbow_configuration = config_element_tree.find('elbow')
            process_continue = elbow_configuration.find('status').text
            if process_continue == "False":
                logging.info("elbow.stdin_listener:break process_continue={process_continue}"
                             .format(process_continue=process_continue))
                break
            else:
                time.sleep(1)

    def iot_task_callback(self, values):
        if self.__iot_lock:
            logging.info("elbow.iot_task_callback:__iot_lock={iot_lock}"
                         .format(iot_lock=self.__iot_lock))
            self.__iot_lock = False
            self.__iot_task = ElbowIotTask(self.__device)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__iot_task.connect())
            loop.close()

        else:
            logging.error("elbow.iot_task_callback:__iot_lock={iot_lock}"
                          .format(iot_lock=self.__iot_lock))

    async def start_iot_command_handler(self, values):
        if values:
            logging.info("elbow.start_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__iot_thread = Thread(target=self.iot_task_callback, args=(values,))
            self.__iot_thread.start()

    @staticmethod
    def start_iot_command_response_handler(values):
        response_dict = {
            "StartTime": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def stop_iot_command_handler(self, values):
        if values:
            self.__iot_lock = True
            logging.info("elbow.stop_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__iot_task.terminate()
            self.__iot_thread.join()

    @staticmethod
    def stop_iot_command_response_handler(values):
        response_dict = {
            "StopTime": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def connect_azure_iot(self, queue):
        self.__device = Device(model_id=self.__model_id,
                               provisioning_host=self.__provisioning_host,
                               id_scope=self.__id_scope,
                               registration_id=self.__registration_id,
                               symmetric_key=self.__symmetric_key)

        await self.__device.create_iot_hub_device_client()

        await self.__device.iot_hub_device_client.connect()

        command_listeners = asyncio.gather(
            self.__device.execute_command_listener(
                method_name="StartIotCommand",
                user_command_handler=self.start_iot_command_handler,
                create_user_response_handler=self.start_iot_command_response_handler,
            ),
            self.__device.execute_command_listener(
                method_name="StopIotCommand",
                user_command_handler=self.stop_iot_command_handler,
                create_user_response_handler=self.stop_iot_command_response_handler,
            ),
            self.__device.execute_property_listener(),
        )

        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)

        await user_finished

        if not command_listeners.done():
            command_listeners.set_result(["Elbow done"])

        command_listeners.cancel()

        await self.__device.iot_hub_device_client.shutdown()
        logging.info("elbow.connect_azure_iot:queue.put")
        await queue.put(None)
