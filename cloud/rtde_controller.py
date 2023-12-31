__author__ = "100638182"
__copyright__ = "University of Derby"

import asyncio
import json
import logging
import sys
from jsondiff import diff
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from model.rtdl.rtdl_dt_model import RtdlDtModel
from model.rtdl.rtdl_model import RtdlModel
from twin_writer import TwinWriter
import xml.etree.ElementTree as ET


class RtdeController:
    def __init__(self, host, port, config, frequency, cobot_client_configuration_path):
        self.__host = host
        self.__port = port
        self.__config = config
        self.__frequency = frequency
        self.__cobot_client_configuration_path = cobot_client_configuration_path
        self.__rtde_connection = None
        self.__sync_running = True
        self.__connect_running = True
        self.__cache_json_file = "cache.json"

    def terminate(self):
        self.__sync_running = False

    async def connect(self, queue):
        logging.info("rtde_controller.connect:Starting")
        try:
            config_file = rtde_config.ConfigFile(self.__config)
            output_names, output_types = config_file.get_recipe("out")

            self.__rtde_connection = rtde.RTDE(self.__host, self.__port)
            self.__rtde_connection.connect()

            self.__rtde_connection.get_controller_version()

            if not self.__rtde_connection.send_output_setup(output_names, output_types, self.__frequency):
                logging.error("rtde_controller.connect:Unable to configure output")
                sys.exit()

            logging.info("rtde_controller.connect:Successfully configured output")

            if not self.__rtde_connection.send_start():
                logging.error("rtde_controller.connect:Unable to start synchronization")
                sys.exit()

            logging.info("rtde_controller.connect:Successfully started synchronization")

            twin_writer = TwinWriter(output_names, output_types)

            header_row = twin_writer.get_header_row()

            logging.info("rtde_controller.connect:header_row")

            loop = asyncio.get_running_loop()
            user_finished = loop.run_in_executor(None, self.stdin_listener)

            cache_json_content = self.load_json_content()

            while self.__sync_running:
                try:
                    state = self.__rtde_connection.receive()
                    if state is not None:
                        data_row = twin_writer.get_data_row(state)
                        logging.info("rtde_controller.connect:data_row")
                        rtdl_model = RtdlModel.get_from_rows(header_row, data_row)
                        rtdl_dt_model = RtdlDtModel.get_from_rtdl_model(rtdl_model)
                        self.create_json(rtdl_dt_model.get_json())
                        if cache_json_content != rtdl_dt_model.get_json():
                            changes = diff(cache_json_content, rtdl_dt_model.get_json())
                            logging.info("rtde_controller.connect:Modified json_object={changes}".format(changes=changes))
                            cache_json_content = rtdl_dt_model.get_json()
                        else:
                            logging.info("rtde_controller.connect:No changes in {cache_json_file}"
                                         .format(cache_json_file=self.__cache_json_file))
                        await asyncio.sleep(5)

                except rtde.RTDEException as ex:
                    self.__rtde_connection.disconnect()
                    logging.error("rtde_controller.connect:While={error}".format(error=str(ex)))
                    self.terminate()
                    sys.exit()

            await user_finished

            logging.debug("rtde_controller.connect:Complete")
            self.__rtde_connection.send_pause()
            self.__rtde_connection.disconnect()
            logging.info("rtde_controller.connect:queue.put")
            sys.exit()

        except Exception as ex:
            logging.error("rtde_controller.connect:exception={error}".format(error=str(ex)))
            logging.info("rtde_controller.connect:queue.put")
            sys.exit()


    def load_json_content(self):
        cache_json_file = open(self.__cache_json_file)
        json_content = json.load(cache_json_file)
        cache_json_file.close()
        return json_content


    def stdin_listener(self):
        while True:
            selection = input("Press Q to quit Cobot Client\n")
            if (selection == "Q" or selection == "q") or self.__connect_running:
                logging.info("rtde_controller.stdin_listener:Quitting Cobot Client...")
                logging.info("rtde_controller.stdin_listener:"
                             "Parsing cobot_client_configuration_path={cobot_client_configuration_path}"
                             .format(cobot_client_configuration_path=self.__cobot_client_configuration_path))

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
                ET.SubElement(cobot_sub_element, "status").text = "False"
                ET.SubElement(control_box_sub_element, "status").text = "False"
                ET.SubElement(payload_sub_element, "status").text = "False"
                ET.SubElement(base_sub_element, "status").text = "False"
                ET.SubElement(shoulder_sub_element, "status").text = "False"
                ET.SubElement(elbow_sub_element, "status").text = "False"
                ET.SubElement(elbow_sub_element, "status").text = "False"
                ET.SubElement(wrist1_sub_element, "status").text = "False"
                ET.SubElement(wrist2_sub_element, "status").text = "False"
                ET.SubElement(wrist3_sub_element, "status").text = "False"
                ET.SubElement(tool_sub_element, "status").text = "False"
                cobot_client_configuration_element_tree = ET.ElementTree(config_element)
                cobot_client_configuration_element_tree.write(self.__cobot_client_configuration_path)

                logging.info("rtde_controller.stdin_listener:"
                             "Saved cobot_client_configuration_element_tree={cobot_client_configuration_element_tree}"
                             .format(cobot_client_configuration_element_tree=cobot_client_configuration_element_tree))
                self.terminate()
                break

    def create_json(self, json_object):
        with open(self.__cache_json_file, "w+") as f:
            logging.info("rtde_controller.create_json:{file} saved".format(file=self.__cache_json_file))
            json.dump(json_object, f)
