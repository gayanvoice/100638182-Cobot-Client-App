import asyncio
import inspect
import logging
import json
from threading import Thread
from datetime import datetime

from azure.iot.device.common.pipeline.pipeline_exceptions import PipelineNotRunning

from cloud.iot_task.control_box_iot_task import ControlBoxIotTask
from cloud.device import Device
import xml.etree.ElementTree as ET
import time

from helper.log_text_helper import LogTextHelper, LogTextStatus
from model.response.iot.start_iot_command_response_model import StartIotCommandRespondModel
from model.response.iot.stop_iot_command_response_model import StopIotCommandRespondModel
from model.response.response_model import Status


class ControlBox(object):
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
        self.__stop_iot_command_response_model = None
        self.__log_text_helper = LogTextHelper(class_name=self.__class__.__name__)
        self.__start_iot_command_response_model = None

    def stdin_listener(self):
        while True:
            config_element_tree = ET.parse(self.__cobot_client_configuration_path)
            control_box_configuration = config_element_tree.find('control_box')
            process_continue = control_box_configuration.find('status').text
            if process_continue == "False":
                logging.info("control_box.stdin_listener:break process_continue={process_continue}"
                             .format(process_continue=process_continue))
                break
            else:
                time.sleep(1)

    def iot_task_callback(self, values):
        try:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values
                })
            logging.info(log_text)

            self.__iot_lock = False
            self.__iot_task = ControlBoxIotTask(self.__device)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__iot_task.connect())
            loop.close()

        except PipelineNotRunning:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "exception": "PipelineNotRunning"
                })
            logging.error(log_text)
            self.__start_iot_command_response_model.set_response(status=Status.COBOT_CLIENT_ERROR,

                                                                 log_text=log_text)

    async def start_iot_command_handler(self, values):
        self.__start_iot_command_response_model = StartIotCommandRespondModel()
        if self.__iot_lock:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "iot_lock": self.__iot_lock
                })
            logging.info(log_text)
            self.__start_iot_command_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
            logging.info("control_box.start_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__iot_thread = Thread(target=self.iot_task_callback, args=(values,))
            self.__iot_thread.start()
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "iot_lock": self.__iot_lock
                })
            logging.error(log_text)
            self.__start_iot_command_response_model.set_response(status=Status.COMMAND_EXECUTION_SEQUENCE_ERROR,
                                                                 log_text=log_text)

    def start_iot_command_response_handler(self, values):
        response_payload = json.dumps(self.__start_iot_command_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def stop_iot_command_handler(self, values):
        self.__stop_iot_command_response_model = StopIotCommandRespondModel()
        if not self.__iot_lock:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "iot_lock": self.__iot_lock
                })
            logging.info(log_text)
            self.__stop_iot_command_response_model.set_response(status=Status.COBOT_CLIENT_EXECUTED,
                                                                log_text=log_text)
            self.__iot_lock = True
            self.__iot_task.terminate()
            self.__iot_thread.join()
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "iot_lock": self.__iot_lock
                })
            logging.error(log_text)
            self.__stop_iot_command_response_model.set_response(status=Status.COMMAND_EXECUTION_SEQUENCE_ERROR,
                                                                log_text=log_text)

    def stop_iot_command_response_handler(self, values):
        response_payload = json.dumps(self.__stop_iot_command_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload,
            }))
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
            command_listeners.set_result(["Control Box done"])

        command_listeners.cancel()

        await self.__device.iot_hub_device_client.shutdown()
        logging.info("control_box.connect_azure_iot:queue.put")
        await queue.put(None)
