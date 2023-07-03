import asyncio
import logging
import json
from threading import Thread
from datetime import datetime
from cloud.cobot_control_task import CobotControlTask
from cloud.cobot_iot_task import CobotIotTask
from cloud.device import Device


class Cobot(object):
    def __init__(self, cobot_model_id, provisioning_host, id_scope, registration_id, symmetric_key):
        self.__cobot_model_id = cobot_model_id
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

    @staticmethod
    def stdin_listener():
        while True:
            selection = input("Press C to quit Cobot\n")
            if selection == "C" or selection == "c":
                print("Quitting Cobot...")
                break

    def cobot_control_task_callback(self, values):
        if self.__cobot_control_lock:
            self.__cobot_control_lock = False
            host = "localhost"
            port = 30004
            control_config = "control_configuration.xml"

            self.__cobot_control_task = CobotControlTask(host=host, port=port, config=control_config,
                                                         set_position_array=values)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__cobot_control_task.connect())
            loop.close()
        else:
            logging.error("cobot.cobot_control_task_callback:__cobot_control_lock={cobot_control_lock}"
                          .format(cobot_control_lock=self.__cobot_control_lock))

    def cobot_iot_task_callback(self, values):
        if self.__cobot_iot_lock:
            logging.info("cobot.cobot_iot_task_callback:__cobot_iot_lock={cobot_iot_lock}"
                         .format(cobot_iot_lock=self.__cobot_iot_lock))
            self.__cobot_iot_lock = False
            self.__cobot_iot_task = CobotIotTask(self.__cobot_device)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__cobot_iot_task.connect())
            loop.close()

        else:
            logging.error("cobot.cobot_iot_task_callback:__cobot_iot_lock={cobot_iot_lock}"
                          .format(cobot_iot_lock=self.__cobot_iot_lock))

    async def start_cobot_control_command_handler(self, values):
        if values:
            logging.info("cobot.start_cobot_control_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_control_thread = Thread(target=self.cobot_control_task_callback, args=(values,))
            self.__cobot_control_thread.start()

    @staticmethod
    def start_cobot_control_command_response_handler(values):
        response_dict = {
            "start_time": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def stop_cobot_control_command_handler(self, values):
        if values:
            self.__cobot_control_lock = True
            logging.info("cobot.stop_cobot_control_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_control_task.terminate()
            self.__cobot_control_thread.join()

    @staticmethod
    def stop_cobot_control_command_response_handler(values):
        response_dict = {
            "stop_time": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def start_cobot_iot_command_handler(self, values):
        if values:
            logging.info("cobot.start_cobot_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_iot_thread = Thread(target=self.cobot_iot_task_callback, args=(values,))
            self.__cobot_iot_thread.start()

    @staticmethod
    def start_cobot_iot_command_response_handler(values):
        response_dict = {
            "start_time": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def stop_cobot_iot_command_handler(self, values):
        if values:
            self.__cobot_iot_lock = True
            logging.info("cobot.stop_cobot_iot_command_handler:values={values} type={type}"
                         .format(values=values, type=str(type(values))))
            self.__cobot_iot_task.terminate()
            self.__cobot_iot_thread.join()

    @staticmethod
    def stop_cobot_iot_command_response_handler(values):
        response_dict = {
            "stop_time": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        return response_payload

    async def connect_azure_iot(self, queue):
        self.__cobot_device = Device(model_id=self.__cobot_model_id,
                                     provisioning_host=self.__provisioning_host,
                                     id_scope=self.__id_scope,
                                     registration_id=self.__registration_id,
                                     symmetric_key=self.__symmetric_key)

        await self.__cobot_device.create_iot_hub_device_client()


        await self.__cobot_device.iot_hub_device_client.connect()

        command_listeners = asyncio.gather(
            self.__cobot_device.execute_command_listener(
                method_name="startCobotCommand",
                user_command_handler=self.start_cobot_control_command_handler,
                create_user_response_handler=self.start_cobot_control_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="stopCobotCommand",
                user_command_handler=self.stop_cobot_control_command_handler,
                create_user_response_handler=self.stop_cobot_control_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="startIotCommand",
                user_command_handler=self.start_cobot_iot_command_handler,
                create_user_response_handler=self.start_cobot_iot_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="stopIotCommand",
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
