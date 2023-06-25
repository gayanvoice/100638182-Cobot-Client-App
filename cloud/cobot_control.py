import asyncio
import logging
import json
import time
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from threading import Thread

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from datetime import timedelta, datetime

import cobot_control_async
from cloud.device import Device

logging.basicConfig(level=logging.ERROR)

model_id = "dtmi:com:example:Cobot;1"

max_temp = None
min_temp = None
avg_temp_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
moving_window_size = len(avg_temp_list)
target_temperature = None


def callback_a():
    event_loop_a = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop_a)
    asyncio.get_event_loop().call_soon(lambda: hello('a'))
    event_loop_a.run_forever()


def hello(thread_name):
    while True:
        time.sleep(1)
        print('hello from thread {}!'.format(thread_name))


async def start_command_handler(values):
    if values:
        thread_a = Thread(target=callback_a, daemon=True)
        thread_a.start()


def start_command_response_response(values):
    response_dict = {
        "elapsed_time": datetime.now().isoformat()
    }
    response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
    print(response_payload)
    return response_payload


def stdin_listener():
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break


async def main():
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Cobot"
    symmetric_key = "GQXiRV7rtQVOFCKZuSnHfj85arpbeQqAyhbov8zk7vNbaG/4mcXa06ETfH+C1Mr/IGPOCDawrqmfCR6lG0IyKA=="

    device = Device(model_id=model_id,
                    provisioning_host=provisioning_host,
                    id_scope=id_scope,
                    registration_id=registration_id,
                    symmetric_key=symmetric_key)

    await device.create_iot_hub_device_client()

    await device.iot_hub_device_client.connect()

    await device.iot_hub_device_client.patch_twin_reported_properties({"maxTempSinceLastReboot": 10.96})

    command_listeners = asyncio.gather(
        device.execute_command_listener(
            method_name="startCommand",
            user_command_handler=start_command_handler,
            create_user_response_handler=start_command_response_response,
        ),
        device.execute_property_listener(),
    )

    send_telemetry_task = asyncio.create_task(send_telemetry(device))

    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    await user_finished

    if not command_listeners.done():
        command_listeners.set_result(["Cobot done"])

    command_listeners.cancel()

    send_telemetry_task.cancel()

    await device.iot_hub_device_client.shutdown()


async def send_telemetry(iot_hub_device_client):
    print("Sending telemetry for elapsed time")

    while True:
        telemetry = {"elapsed_time": time.time()}
        await iot_hub_device_client.send_telemetry(telemetry)
        await asyncio.sleep(8)


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
