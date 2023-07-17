import asyncio
import logging
import json
from threading import Thread
from datetime import datetime
from cloud.device import Device
from cloud.iot_task.wrist3_iot_task import Wrist3IotTask


class Wrist3(object):
    def __init__(self, model_id, provisioning_host, id_scope, registration_id, symmetric_key):
        self.__model_id = model_id
        self.__provisioning_host = provisioning_host
        self.__id_scope = id_scope
        self.__registration_id = registration_id
        self.__symmetric_key = symmetric_key
        self.__device = None
        self.__iot_task = None
        self.__iot_thread = None
        self.__iot_lock = True

    @staticmethod
    def stdin_listener():
        while True:
            selection = input("Press C to quit Wrist3\n")
            if selection == "C" or selection == "c":
                print("Quitting Wrist3...")
                break

    def iot_task_callback(self, values):
        if self.__iot_lock:
            logging.info("wrist3.iot_task_callback:__iot_lock={iot_lock}"
                         .format(iot_lock=self.__iot_lock))
            self.__iot_lock = False
            self.__iot_task = Wrist3IotTask(self.__device)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__iot_task.connect())
            loop.close()

        else:
            logging.error("wrist3.iot_task_callback:__iot_lock={iot_lock}"
                          .format(iot_lock=self.__iot_lock))

    async def start_iot_command_handler(self, values):
        if values:
            logging.info("wrist3.start_iot_command_handler:values={values} type={type}"
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
            logging.info("wrist3.stop_iot_command_handler:values={values} type={type}"
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
            command_listeners.set_result(["Wrist3 done"])

        command_listeners.cancel()

        await self.__device.iot_hub_device_client.shutdown()
        logging.info("wrist3.connect_azure_iot:queue.put")
        await queue.put(None)
