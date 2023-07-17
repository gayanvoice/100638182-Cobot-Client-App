import asyncio
import logging
import json
from threading import Thread
from datetime import datetime

from azure.iot.device.common.pipeline.pipeline_exceptions import PipelineNotRunning

from cloud.control_task.cobot_control_task import CobotControlTask
from cloud.iot_task.cobot_iot_task import CobotIotTask
from cloud.device import Device
import xml.etree.ElementTree as ET
import time


class Cobot(object):
    def __init__(self,
                 rtde_host,
                 rtde_port,
                 control_configuration_path,
                 cobot_client_configuration_path,
                 model_id,
                 provisioning_host,
                 id_scope,
                 registration_id,
                 symmetric_key):
        self.__rtde_host = rtde_host
        self.__rtde_port = rtde_port
        self.__control_configuration_path = control_configuration_path
        self.__cobot_client_configuration_path = cobot_client_configuration_path
        self.__model_id = model_id
        self.__provisioning_host = provisioning_host
        self.__id_scope = id_scope
        self.__registration_id = registration_id
        self.__symmetric_key = symmetric_key
        self.__cobot_device = None
        self.__cobot_control_task = None
        self.__cobot_iot_task = None
        self.__cobot_control_thread = None
        self.__cobot_iot_thread = None
        self.__cobot_control_lock = True
        self.__cobot_iot_lock = True

    def stdin_listener(self):
        while True:
            config_element_tree = ET.parse(self.__cobot_client_configuration_path)
            cobot_configuration = config_element_tree.find('cobot')
            process_continue = cobot_configuration.find('status').text
            if process_continue == "False":
                logging.info("cobot.stdin_listener:break process_continue={process_continue}"
                             .format(process_continue=process_continue))
                break
            else:
                logging.info("cobot.stdin_listener:sleeping process_continue={process_continue}"
                             .format(process_continue=process_continue))
                time.sleep(1)

    def cobot_control_task_callback(self, values):
        if self.__cobot_control_lock:
            logging.info("cobot.cobot_control_task_callback:__cobot_control_lock={cobot_control_lock}"
                         .format(cobot_control_lock=self.__cobot_control_lock))
            self.__cobot_control_lock = False

            self.__cobot_control_task = CobotControlTask(rtde_host=self.__rtde_host,
                                                         rtde_port=self.__rtde_port,
                                                         control_configuration_path=self.__control_configuration_path,
                                                         set_position_array=values)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__cobot_control_task.connect())
            loop.close()
        else:
            logging.error("cobot.cobot_control_task_callback:__cobot_control_lock={cobot_control_lock}"
                          .format(cobot_control_lock=self.__cobot_control_lock))

    def start_cobot_iot_task_callback(self, values):
        if self.__cobot_iot_lock:
            try:
                logging.info("cobot.cobot_iot_task_callback:__cobot_iot_lock={cobot_iot_lock}"
                             .format(cobot_iot_lock=self.__cobot_iot_lock))
                self.__cobot_iot_lock = False
                self.__cobot_iot_task = CobotIotTask(self.__cobot_device)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.__cobot_iot_task.connect())
                loop.close()
            except PipelineNotRunning:
                logging.error("cobot.cobot_iot_task_callback:PipelineNotRunning")


        else:
            logging.error("cobot.cobot_iot_task_callback:__cobot_iot_lock={cobot_iot_lock}"
                          .format(cobot_iot_lock=self.__cobot_iot_lock))

    async def start_cobot_control_command_handler(self, values):
        if self.is_input_array_valid(values):
            logging.info("cobot.start_cobot_control_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_control_thread = Thread(target=self.cobot_control_task_callback, args=(values,))
            self.__cobot_control_thread.start()
        else:
            logging.info("cobot.start_cobot_control_command_handler:invalid values={values} type={type}"
                         .format(values=values, type=str(type(values))))

    @staticmethod
    def start_cobot_control_command_response_handler(values):
        response_dict = {
            "StartTime": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def stop_cobot_control_command_handler(self, values):
        if values:
            logging.info("cobot.stop_cobot_control_command_handler:cobot_control_lock={cobot_control_lock}"
                         .format(cobot_control_lock=self.__cobot_control_lock))
            self.__cobot_control_lock = True
            logging.info("cobot.stop_cobot_control_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_control_task.terminate()
            self.__cobot_control_thread.join()

    @staticmethod
    def stop_cobot_control_command_response_handler(values):
        response_dict = {
            "StopTime": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def start_cobot_iot_command_handler(self, values):
        if values:
            logging.info("cobot.start_cobot_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_iot_thread = Thread(target=self.start_cobot_iot_task_callback, args=(values,))
            self.__cobot_iot_thread.start()

    @staticmethod
    def start_cobot_iot_command_response_handler(values):
        response_dict = {
            "StartTime": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def stop_cobot_iot_command_handler(self, values):
        if not self.__cobot_iot_lock:
            self.__cobot_iot_lock = True
            logging.info("cobot.stop_cobot_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_iot_task.terminate()
            self.__cobot_iot_thread.join()

    @staticmethod
    def stop_cobot_iot_command_response_handler(values):
        response_dict = {
            "StopTime": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def connect_azure_iot(self, queue):
        self.__cobot_device = Device(model_id=self.__model_id,
                                     provisioning_host=self.__provisioning_host,
                                     id_scope=self.__id_scope,
                                     registration_id=self.__registration_id,
                                     symmetric_key=self.__symmetric_key)

        await self.__cobot_device.create_iot_hub_device_client()

        await self.__cobot_device.iot_hub_device_client.connect()

        command_listeners = asyncio.gather(
            self.__cobot_device.execute_command_listener(
                method_name="StartCobotCommand",
                user_command_handler=self.start_cobot_control_command_handler,
                create_user_response_handler=self.start_cobot_control_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StopCobotCommand",
                user_command_handler=self.stop_cobot_control_command_handler,
                create_user_response_handler=self.stop_cobot_control_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StartIotCommand",
                user_command_handler=self.start_cobot_iot_command_handler,
                create_user_response_handler=self.start_cobot_iot_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StopIotCommand",
                user_command_handler=self.stop_cobot_iot_command_handler,
                create_user_response_handler=self.stop_cobot_iot_command_response_handler,
            ),
            self.__cobot_device.execute_property_listener(),
        )

        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)

        await user_finished

        if not command_listeners.done():
            command_listeners.set_result(["Cobot done"])

        command_listeners.cancel()

        await self.__cobot_device.iot_hub_device_client.shutdown()
        logging.info("cobot.connect_azure_iot:queue.put")
        await queue.put(None)

    @staticmethod
    def is_input_array_valid(input_array):
        if not isinstance(input_array, list) or not all(isinstance(row, list) for row in input_array):
            return False
        num_elements = len(input_array[0])
        if not all(len(row) == num_elements for row in input_array):
            return False
        if not all(isinstance(element, (int, float)) for row in input_array for element in row):
            return False
        return True
