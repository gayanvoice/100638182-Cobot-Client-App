import asyncio
import logging
import json
import time
from threading import Thread

from datetime import datetime

from cloud.cobot_control_task import CobotControlTask
from cloud.device import Device

logging.basicConfig(level=logging.ERROR)


class Cobot(object):
    def __init__(self, cobot_model_id, provisioning_host, id_scope, registration_id, symmetric_key):
        self.__cobot_model_id = cobot_model_id
        self.__provisioning_host = provisioning_host
        self.__id_scope = id_scope
        self.__registration_id = registration_id
        self.__symmetric_key = symmetric_key
        self.__cobot_control_task = None
        self.__thread = None

    def stdin_listener(self):
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break

    def between_callback(self, values):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        host = "localhost"
        port = 30004
        config = "control_configuration.xml"


        self.__cobot_control_task = CobotControlTask(host=host, port=port, config=config, set_position_array=values)
        loop.run_until_complete(self.__cobot_control_task.connect())
        loop.close()

    async def start_command_handler(self, values):
        if values:
            self.__thread = Thread(target=self.between_callback, args=(values,))
            self.__thread.start()

    def start_command_response_response(self, values):
        response_dict = {
            "start_time": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        print(response_payload)
        return response_payload

    async def stop_command_handler(self, values):
        if values:
            print("stop command")
            self.__cobot_control_task.terminate()
            self.__thread.join()

    def stop_command_response_response(self, values):
        response_dict = {
            "stop_time": datetime.now().isoformat()
        }
        response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
        print(response_payload)
        return response_payload

    async def connect_azure_iot(self):
        device = Device(model_id=self.__cobot_model_id,
                        provisioning_host=self.__provisioning_host,
                        id_scope=self.__id_scope,
                        registration_id=self.__registration_id,
                        symmetric_key=self.__symmetric_key)

        await device.create_iot_hub_device_client()

        await device.iot_hub_device_client.connect()

        await device.iot_hub_device_client.patch_twin_reported_properties({"maxTempSinceLastReboot": 10.96})

        command_listeners = asyncio.gather(
            device.execute_command_listener(
                method_name="startCommand",
                user_command_handler=self.start_command_handler,
                create_user_response_handler=self.start_command_response_response,
            ),
            device.execute_command_listener(
                method_name="stopCommand",
                user_command_handler=self.stop_command_handler,
                create_user_response_handler=self.stop_command_response_response,
            ),
            device.execute_property_listener(),
        )

        # send_telemetry_task = asyncio.create_task(self.send_telemetry(device))

        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)

        await user_finished

        if not command_listeners.done():
            command_listeners.set_result(["Cobot done"])

        command_listeners.cancel()

        # send_telemetry_task.cancel()

        await device.iot_hub_device_client.shutdown()

    async def send_telemetry(self, iot_hub_device_client):
        print("Sending telemetry for elapsed time")

        while True:
            telemetry = {"elapsed_time": time.time()}
            await iot_hub_device_client.send_telemetry(telemetry)
            await asyncio.sleep(8)

