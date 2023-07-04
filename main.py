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
from cloud.tool import Tool
from cloud.wrist1 import Wrist1
from cloud.wrist2 import Wrist2
from cloud.wrist3 import Wrist3

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


async def tool(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Tool;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Tool"
    symmetric_key = "qCL1QAg9XZ9K2fx7yl0xBnRBCC47l6Bs+zTnAYgSbGVcn62yKox5OdrCJTNqd10XwcehcRRV4jejRdtBhpttRQ=="

    tool_device = Tool(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await tool_device.connect_azure_iot(queue)


async def wrist1(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Wrist1;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Wrist1"
    symmetric_key = "NlhP/P6RonODZMde3PkRaJmSm+hDsyyu0V84gWJabMl923J7tTZkdRlBF4WBRlDj+WyiOuShZnjhy0OAjBd1RA=="

    wrist1_device = Wrist1(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist1_device.connect_azure_iot(queue)


async def wrist2(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Wrist2;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Wrist2"
    symmetric_key = "3r7qgEn8BND2TQRutb178cvQuIpM+GEx2M3vJvbuWaQVyzO6ZkiY/c9fXS0Zs+bMMwiGIrRuhao9y/xCCxymSg=="

    wrist2_device = Wrist2(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist2_device.connect_azure_iot(queue)


async def wrist3(queue):
    model_id = "dtmi:com:Cobot:JointLoad:Wrist3;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Wrist3"
    symmetric_key = "vTo1dkvIHtOGYPQakKv4KpmN8QTQnBZcqLW2glLb6rJP+WS2ZnCyYRYhrnGv8aOgVqXhc+/WHgtFigidDnFcTQ=="

    wrist3_device = Wrist3(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist3_device.connect_azure_iot(queue)


async def main():
    queue = asyncio.Queue()
    await asyncio.gather(rtde_controller(queue),
                         cobot(queue),
                         control_box(queue),
                         payload(queue),
                         base(queue),
                         shoulder(queue),
                         elbow(queue),
                         tool(queue),
                         wrist1(queue),
                         wrist2(queue),
                         wrist3(queue))


if __name__ == '__main__':
    current_working_directory = os.getcwd()
    logging.info("main: current_working_directory={current_working_directory}"
                 .format(current_working_directory=current_working_directory))
    asyncio.run(main())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.run_until_complete(loop.shutdown_asyncgens())
    # loop.close()
