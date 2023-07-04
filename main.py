import asyncio
import logging
import os

from cloud.cobot import Cobot
from cloud.control_box import ControlBox
from cloud.elbow import Elbow
from cloud.payload import Payload
from cloud.rtde_controller import RtdeController
from cloud.base import Base
from cloud.shoulder import Shoulder
from cloud.wrist1w import Wrist1w

# Get-Content ".\cobot-log.log" -Wait

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename="cobot-log.log", encoding='utf-8', level=logging.INFO)


async def rtde_controller(queue):
    host = "localhost"
    port = 30004
    iot_config = "iot_configuration.xml"
    frequency = 1

    rtde_cntr = RtdeController(host=host,
                               port=port,
                               config=iot_config,
                               frequency=frequency)
    await rtde_cntr.connect(queue)


async def cobot(queue):
    cobot_model_id = "dtmi:com:Cobot:Cobot;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Cobot"
    symmetric_key = "GQXiRV7rtQVOFCKZuSnHfj85arpbeQqAyhbov8zk7vNbaG/4mcXa06ETfH+C1Mr/IGPOCDawrqmfCR6lG0IyKA=="

    cobot_device = Cobot(cobot_model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await cobot_device.connect_azure_iot(queue)


async def control_box(queue):
    model_id = "dtmi:com:Cobot:ControlBox;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "ControlBox"
    symmetric_key = "Nr/tl5bwAyi1/9MUHpBE2QrW9x3unKqgO8G7wyvWsz0jYR6lpIeZw4w6B8M5fbw61oCoaQRiz9FaGpyN8WJmvg=="

    control_box_device = ControlBox(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await control_box_device.connect_azure_iot(queue)


async def elbow(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Elbow;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Elbow"
    symmetric_key = "Mu5iJnFpJAOjU7F6LuQtpgGSLQNsNGJIDKcDM8Y9m8fCMK/o05VY+llkBd6NyhITmbWtOmz1eHpgkntv2YXriw=="

    elbow_device = Elbow(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await elbow_device.connect_azure_iot(queue)


async def payload(queue):
    model_id = "dtmi:com:Cobot:Payload;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Payload"
    symmetric_key = "yKEbtMdipsxgsqajuUp/4oQtu0nEXxxrM1wbOvWZheiJKn3AQqa/fDyTxCp9yXyK3VUrHDZ8SV7HQyUy97hUXQ=="

    payload_device = Payload(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await payload_device.connect_azure_iot(queue)


async def base(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Base;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Base"
    symmetric_key = "LglN6zKwdTTKcoZlGwpSpEN9OP9UjV2ad0ajGLpx19gZYWVcQN2bT3OQFh/jjTuJuP4pmXsqpWDYN5S/0A6W2A=="

    base_device = Base(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await base_device.connect_azure_iot(queue)


async def shoulder(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Shoulder;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Shoulder"
    symmetric_key = "X+LqHs7T67/h3iZNp3KQ3hqLUobJNB4fBU3fSUx5iEG90raxoPGfl2A2McxyQsFkPz6KUeRH7v0Em+Rnpg1mWA=="

    shoulder_device = Shoulder(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await shoulder_device.connect_azure_iot(queue)


async def wrist1w(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Wrist1w;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Wrist1w"
    symmetric_key = "YTbbDTY4Br5XnKjLJiCLi/fghSWQvD33jKHcK5uoWK8GaD4+UaASrINI93oMu6uinnjsLbbrszmaEyc7jJcvhA=="

    wrist1w_device = Wrist1w(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist1w_device.connect_azure_iot(queue)


async def main():
    queue = asyncio.Queue()
    # await asyncio.gather(rtde_controller(queue),
    #                      cobot(queue),
    #                      control_box(queue),
    #                      elbow(queue),
    #                      payload(queue),
    #                      base(queue))
    await asyncio.gather(rtde_controller(queue), wrist1w(queue))


if __name__ == '__main__':
    current_working_directory = os.getcwd()
    logging.info("main: current_working_directory={current_working_directory}"
                 .format(current_working_directory=current_working_directory))
    asyncio.run(main())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.run_until_complete(loop.shutdown_asyncgens())
    # loop.close()
