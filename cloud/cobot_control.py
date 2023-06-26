import asyncio
import logging
import json
import sys
import time
from threading import Thread

from datetime import datetime

from cloud import cobot_control_async
from cloud.cobot_control_async import CobotControlAsync
from cloud.device import Device
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

logging.basicConfig(level=logging.ERROR)


class CobotControlTask:

    def __init__(self, host, port, config):
        self.__host = host
        self.__port = port
        self.__config = config
        self.__set_position_array = None
        self.__rtde_connection = None
        self.__running = True

    def terminate(self):
        self.__running = False


    async def connect(self):
        print("connect")

        set_position_1 = [-0.12, -0.43, 0.14, 0, 3.11, 0.14]
        set_position_2 = [-0.52, -0.71, 0.21, 0, 3.11, 0.24]
        set_position_3 = [-0.82, -0.81, 0.31, 0, 3.21, 0.34]
        set_position_4 = [-0.62, -0.91, 0.41, 0, 3.31, 0.54]
        set_position_array = [set_position_1, set_position_2, set_position_3, set_position_4]

        logging.getLogger().setLevel(logging.INFO)

        config_file = rtde_config.ConfigFile(self.__config)
        state_names, state_types = config_file.get_recipe("state")
        setp_names, setp_types = config_file.get_recipe("setp")
        watchdog_names, watchdog_types = config_file.get_recipe("watchdog")

        self.__rtde_connection = rtde.RTDE(self.__host, self.__port)
        self.__rtde_connection.connect()

        # get controller version
        self.__rtde_connection.get_controller_version()

        # setup recipes
        self.__rtde_connection.send_output_setup(state_names, state_types)
        set_position = self.__rtde_connection.send_input_setup(setp_names, setp_types)
        watchdog = self.__rtde_connection.send_input_setup(watchdog_names, watchdog_types)

        watchdog.input_int_register_0 = 0

        if not self.__rtde_connection.send_start():
            sys.exit()

        # control_task = asyncio.create_task(self.control_cobot(watchdog, set_position_array, set_position))

        await self.control_cobot(watchdog, set_position_array, set_position)

        # loop = asyncio.get_running_loop()
        #
        # user_finished = loop.run_in_executor(None, self.stdin_listener)
        # await user_finished

        # control_task.cancel()

        self.__rtde_connection.send_pause()
        self.__rtde_connection.disconnect()

    async def control_cobot(self, watchdog, set_position_array, set_position):
        set_position.input_double_register_0 = 0
        set_position.input_double_register_1 = 0
        set_position.input_double_register_2 = 0
        set_position.input_double_register_3 = 0
        set_position.input_double_register_4 = 0
        set_position.input_double_register_5 = 0

        self.__running = True
        move_completed = True
        set_position_index = 0
        start_time = None
        end_time = None
        while self.__running:
            if set_position_index >= len(set_position_array):
                set_position_index = 0

            current_set_position = set_position_array[set_position_index]

            state = self.__rtde_connection.receive()

            if state is None:
                break

            if move_completed and state.output_int_register_0 == 1:
                start_time = datetime.now()
                move_completed = False
                await self.list_to_setp(set_position, current_set_position)
                print(str(set_position_index) + "/" + str(len(set_position_array)) + ": " + str(start_time) + " New pose = "
                      + str(current_set_position))
                self.__rtde_connection.send(set_position)
                watchdog.input_int_register_0 = 1
            elif not move_completed and state.output_int_register_0 == 0:
                end_time = datetime.now()
                elapsed_time = self.calculate_time_difference(start_time, end_time)
                print(str(set_position_index) + "/" + str(len(set_position_array)) + ": " + str(start_time) + "Move to "
                                                                                                              "confirmed "
                                                                                                              "pose = " +
                      str(state.target_q))
                print(str(set_position_index) + "/" + str(len(set_position_array)) + ": " + "Time Elapsed = "
                      + str(elapsed_time))
                move_completed = True
                watchdog.input_int_register_0 = 0
                time.sleep(1)
            self.__rtde_connection.send(watchdog)
            set_position_index += 1

    def setp_to_list(self, sp):
        sp_list = []
        for i in range(0, 6):
            sp_list.append(sp.__dict__["input_double_register_%i" % i])
        return sp_list

    async def list_to_setp(self, sp, list):
        for i in range(0, 6):
            sp.__dict__["input_double_register_%i" % i] = list[i]
        return sp

    def calculate_time_difference(self, start, end):
        duration = end - start
        return duration



def stdin_listener():
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break





class CobotControl(object):
    def __init__(self, cobot_model_id, provisioning_host, id_scope, registration_id, symmetric_key):
        self.__cobot_model_id = cobot_model_id
        self.__provisioning_host = provisioning_host
        self.__id_scope = id_scope
        self.__registration_id = registration_id
        self.__symmetric_key = symmetric_key
        self.__cobot_control_task = None
        self.__thread = None

    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        host = "localhost"
        port = 30004
        config = "control_configuration.xml"
        self.__cobot_control_task = CobotControlTask(host=host, port=port, config=config)
        loop.run_until_complete(self.__cobot_control_task.connect())
        loop.close()

    async def start_command_handler(self, values):
        if values:
            self.__thread = Thread(target=self.between_callback)
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


    async def connect_iot(self):
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
        user_finished = loop.run_in_executor(None, stdin_listener)

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


def run():
    cobot_model_id = "dtmi:com:example:Cobot;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Cobot"
    symmetric_key = "GQXiRV7rtQVOFCKZuSnHfj85arpbeQqAyhbov8zk7vNbaG/4mcXa06ETfH+C1Mr/IGPOCDawrqmfCR6lG0IyKA=="

    # host = "localhost"
    # port = 30004
    # config = "control_configuration.xml"
    # set_position_1 = [-0.12, -0.43, 0.14, 0, 3.11, 0.14]
    # set_position_2 = [-0.52, -0.71, 0.21, 0, 3.11, 0.24]
    # set_position_3 = [-0.82, -0.81, 0.31, 0, 3.21, 0.34]
    # set_position_4 = [-0.62, -0.91, 0.41, 0, 3.31, 0.54]
    # payload = [set_position_1, set_position_2, set_position_3, set_position_4]

    cobot_control = CobotControl(cobot_model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    # cobot_control_async = CobotControlAsync(host, port, config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(cobot_control.connect_iot())
    # loop.run_until_complete(cobot_control_async.connect(payload))
    loop.close()
