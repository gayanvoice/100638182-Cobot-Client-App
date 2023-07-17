import asyncio
import logging
import os
import xml.etree.ElementTree as ET
from asyncio import CancelledError
from os.path import exists

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

cobot_iot_configuration_path = "cobot_iot_configuration.xml"
cobot_client_configuration_path = "cobot_client_configuration.xml"
cobot_log_path = "cobot_log.log"

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename=cobot_log_path, encoding='utf-8', level=logging.INFO)


async def rtde_controller(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    rtde_configuration = config_element_tree.find('rtde')

    rtde_host = rtde_configuration.find('connection/host').text
    rtde_port = int(rtde_configuration.find('connection/port').text)
    iot_config = rtde_configuration.find('settings/iot_configuration_path').text
    frequency = int(rtde_configuration.find('settings/frequency').text)

    rtde_cntr = RtdeController(host=rtde_host,
                               port=rtde_port,
                               config=iot_config,
                               frequency=frequency,
                               cobot_client_configuration_path=cobot_client_configuration_path)
    await rtde_cntr.connect(queue)


async def cobot(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    cobot_configuration = config_element_tree.find('cobot')
    rtde_configuration = config_element_tree.find('rtde')

    rtde_host = rtde_configuration.find('connection/host').text
    rtde_port = int(rtde_configuration.find('connection/port').text)
    control_configuration_path = rtde_configuration.find('settings/control_configuration_path').text

    model_id = cobot_configuration.find('model_id').text
    provisioning_host = cobot_configuration.find('provisioning_host').text
    id_scope = cobot_configuration.find('id_scope').text
    registration_id = cobot_configuration.find('registration_id').text
    symmetric_key = cobot_configuration.find('symmetric_key').text

    cobot_device = Cobot(rtde_host=rtde_host,
                         rtde_port=rtde_port,
                         control_configuration_path=control_configuration_path,
                         cobot_client_configuration_path=cobot_client_configuration_path,
                         model_id=model_id,
                         provisioning_host=provisioning_host,
                         id_scope=id_scope,
                         registration_id=registration_id,
                         symmetric_key=symmetric_key)
    await cobot_device.connect_azure_iot(queue)


async def control_box(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    control_box_configuration = config_element_tree.find('control_box')

    model_id = control_box_configuration.find('model_id').text
    provisioning_host = control_box_configuration.find('provisioning_host').text
    id_scope = control_box_configuration.find('id_scope').text
    registration_id = control_box_configuration.find('registration_id').text
    symmetric_key = control_box_configuration.find('symmetric_key').text

    control_box_device = ControlBox(model_id=model_id,
                                    provisioning_host=provisioning_host,
                                    id_scope=id_scope,
                                    registration_id=registration_id,
                                    symmetric_key=symmetric_key,
                                    cobot_client_configuration_path=cobot_client_configuration_path)
    await control_box_device.connect_azure_iot(queue)


async def elbow(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    joint_load_configuration = config_element_tree.find('joint_load')

    model_id = joint_load_configuration.find('model_id').text
    provisioning_host = joint_load_configuration.find('provisioning_host').text
    id_scope = joint_load_configuration.find('id_scope').text
    registration_id = joint_load_configuration.find('registration_id').text
    symmetric_key = joint_load_configuration.find('symmetric_key').text

    elbow_device = Elbow(model_id=model_id,
                         provisioning_host=provisioning_host,
                         id_scope=id_scope,
                         registration_id=registration_id,
                         symmetric_key=symmetric_key,
                         cobot_client_configuration_path=cobot_client_configuration_path)
    await elbow_device.connect_azure_iot(queue)


async def payload(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    joint_load_configuration = config_element_tree.find('payload')

    model_id = joint_load_configuration.find('model_id').text
    provisioning_host = joint_load_configuration.find('provisioning_host').text
    id_scope = joint_load_configuration.find('id_scope').text
    registration_id = joint_load_configuration.find('registration_id').text
    symmetric_key = joint_load_configuration.find('symmetric_key').text

    payload_device = Payload(model_id=model_id,
                             provisioning_host=provisioning_host,
                             id_scope=id_scope,
                             registration_id=registration_id,
                             symmetric_key=symmetric_key,
                             cobot_client_configuration_path=cobot_client_configuration_path)
    await payload_device.connect_azure_iot(queue)


async def base(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    base_configuration = config_element_tree.find('base')

    model_id = base_configuration.find('model_id').text
    provisioning_host = base_configuration.find('provisioning_host').text
    id_scope = base_configuration.find('id_scope').text
    registration_id = base_configuration.find('registration_id').text
    symmetric_key = base_configuration.find('symmetric_key').text

    base_device = Base(model_id=model_id,
                       provisioning_host=provisioning_host,
                       id_scope=id_scope,
                       registration_id=registration_id,
                       symmetric_key=symmetric_key,
                       cobot_client_configuration_path=cobot_client_configuration_path)
    await base_device.connect_azure_iot(queue)


async def shoulder(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    shoulder_configuration = config_element_tree.find('shoulder')

    model_id = shoulder_configuration.find('model_id').text
    provisioning_host = shoulder_configuration.find('provisioning_host').text
    id_scope = shoulder_configuration.find('id_scope').text
    registration_id = shoulder_configuration.find('registration_id').text
    symmetric_key = shoulder_configuration.find('symmetric_key').text

    shoulder_device = Shoulder(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await shoulder_device.connect_azure_iot(queue)


async def tool(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    tool_configuration = config_element_tree.find('tool')

    model_id = tool_configuration.find('model_id').text
    provisioning_host = tool_configuration.find('provisioning_host').text
    id_scope = tool_configuration.find('id_scope').text
    registration_id = tool_configuration.find('registration_id').text
    symmetric_key = tool_configuration.find('symmetric_key').text

    tool_device = Tool(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await tool_device.connect_azure_iot(queue)


async def wrist1(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    wrist1_configuration = config_element_tree.find('wrist1')

    model_id = wrist1_configuration.find('model_id').text
    provisioning_host = wrist1_configuration.find('provisioning_host').text
    id_scope = wrist1_configuration.find('id_scope').text
    registration_id = wrist1_configuration.find('registration_id').text
    symmetric_key = wrist1_configuration.find('symmetric_key').text

    wrist1_device = Wrist1(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist1_device.connect_azure_iot(queue)


async def wrist2(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    wrist2_configuration = config_element_tree.find('wrist2')

    model_id = wrist2_configuration.find('model_id').text
    provisioning_host = wrist2_configuration.find('provisioning_host').text
    id_scope = wrist2_configuration.find('id_scope').text
    registration_id = wrist2_configuration.find('registration_id').text
    symmetric_key = wrist2_configuration.find('symmetric_key').text

    wrist2_device = Wrist2(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist2_device.connect_azure_iot(queue)


async def wrist3(queue):
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    wrist3_configuration = config_element_tree.find('wrist3')

    model_id = wrist3_configuration.find('model_id').text
    provisioning_host = wrist3_configuration.find('provisioning_host').text
    id_scope = wrist3_configuration.find('id_scope').text
    registration_id = wrist3_configuration.find('registration_id').text
    symmetric_key = wrist3_configuration.find('symmetric_key').text

    wrist3_device = Wrist3(model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    await wrist3_device.connect_azure_iot(queue)


async def main():
    config_element_tree = ET.parse(cobot_iot_configuration_path)
    rtde_configuration = config_element_tree.find('rtde')

    control_configuration_path = rtde_configuration.find('settings/control_configuration_path').text
    iot_configuration_path = rtde_configuration.find('settings/iot_configuration_path').text

    control_configuration_exists = exists(control_configuration_path)
    iot_configuration_exists = exists(iot_configuration_path)

    cobot_iot_configuration_path_exists = exists(cobot_iot_configuration_path)
    cobot_client_configuration_path_exists = exists(cobot_client_configuration_path)

    if control_configuration_exists \
            and iot_configuration_exists \
            and cobot_iot_configuration_path_exists \
            and cobot_client_configuration_path_exists:

        logging.info("main:Parsing cobot_client_configuration_path={cobot_client_configuration_path}"
                     .format(cobot_client_configuration_path=cobot_client_configuration_path))

        config_element = ET.Element("config")
        cobot_sub_element = ET.SubElement(config_element, "cobot")
        control_box_sub_element = ET.SubElement(config_element, "control_box")
        payload_sub_element = ET.SubElement(config_element, "payload")
        base_sub_element = ET.SubElement(config_element, "base")
        shoulder_sub_element = ET.SubElement(config_element, "shoulder")
        elbow_sub_element = ET.SubElement(config_element, "elbow")
        wrist1_sub_element = ET.SubElement(config_element, "wrist1")
        wrist2_sub_element = ET.SubElement(config_element, "wrist2")
        wrist3_sub_element = ET.SubElement(config_element, "wrist3")
        tool_sub_element = ET.SubElement(config_element, "tool")
        ET.SubElement(cobot_sub_element, "status").text = "True"
        ET.SubElement(control_box_sub_element, "status").text = "True"
        ET.SubElement(payload_sub_element, "status").text = "True"
        ET.SubElement(base_sub_element, "status").text = "True"
        ET.SubElement(shoulder_sub_element, "status").text = "True"
        ET.SubElement(elbow_sub_element, "status").text = "True"
        ET.SubElement(elbow_sub_element, "status").text = "True"
        ET.SubElement(wrist1_sub_element, "status").text = "True"
        ET.SubElement(wrist2_sub_element, "status").text = "True"
        ET.SubElement(wrist3_sub_element, "status").text = "True"
        ET.SubElement(tool_sub_element, "status").text = "True"
        cobot_client_configuration_element_tree = ET.ElementTree(config_element)
        cobot_client_configuration_element_tree.write(cobot_client_configuration_path)

        logging.info("main:Saved cobot_client_configuration_element_tree={cobot_client_configuration_element_tree}"
                     .format(cobot_client_configuration_element_tree=cobot_client_configuration_element_tree))

        try:
            queue = asyncio.Queue()
            # await asyncio.gather(rtde_controller(queue),
            #                      cobot(queue),
            #                      control_box(queue),
            #                      elbow(queue),
            #                      payload(queue),
            #                      base(queue),
            #                      shoulder(queue),
            #                      tool(queue),
            #                      wrist1(queue),
            #                      wrist2(queue),
            #                      wrist3(queue))
            await asyncio.gather(rtde_controller(queue),
                                 cobot(queue),
                                 control_box(queue),
                                 elbow(queue),
                                 base(queue),
                                 payload(queue))
        except asyncio.exceptions.CancelledError:
            logging.error("main:The execution of the thread was manually stopped due to a KeyboardInterrupt signal.")
        except SystemExit:
            logging.error("main:Cobot client was stopped.")


    else:
        logging.error("main:File does not exist cobot_iot_configuration.xml={cobot_iot_configuration_path_exists} "
                      "cobot_client_configuration.xml={cobot_client_configuration_path_exists} "
                      "control_configuration.xml={control_configuration_exists} "
                      "iot_configuration.xml={iot_configuration_exists}"
                      .format(cobot_iot_configuration_path_exists=cobot_iot_configuration_path_exists,
                              cobot_client_configuration_path_exists=cobot_client_configuration_path_exists,
                              control_configuration_exists=control_configuration_exists,
                              iot_configuration_exists=iot_configuration_exists))


if __name__ == '__main__':
    logging.info("main:Starting.")
    current_working_directory = os.getcwd()
    logging.info("main: current_working_directory={current_working_directory}"
                 .format(current_working_directory=current_working_directory))
    asyncio.run(main())
