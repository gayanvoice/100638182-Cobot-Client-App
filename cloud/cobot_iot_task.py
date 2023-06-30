import json
import logging
import sys
import time

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

from model.rtdl_dt_model import RtdlDtModel
from model.rtdl_model import RtdlModel
from twin_writer import TwinWriter


class CobotIotTask:

    def __init__(self, host, port, config, frequency):
        self.__host = host
        self.__port = port
        self.__config = config
        self.__frequency = frequency
        self.__rtde_connection = None
        self.__running = True

    def terminate(self):
        self.__running = False

    async def connect(self):
        logging.error("cobot_iot_task.connect:Starting")
        logging.getLogger().setLevel(logging.INFO)

        config_file = rtde_config.ConfigFile(self.__config)
        output_names, output_types = config_file.get_recipe("out")

        self.__rtde_connection = rtde.RTDE(self.__host, self.__port)
        self.__rtde_connection.connect()

        self.__rtde_connection.get_controller_version()

        # setup recipes
        if not self.__rtde_connection.send_output_setup(output_names, output_types, self.__frequency):
            logging.error("cobot_iot_task.connect:Unable to configure output")
            sys.exit()

        logging.info("cobot_iot_task.connect:Successfully configured output")

        # start data synchronization
        if not self.__rtde_connection.send_start():
            logging.error("cobot_iot_task.connect:Unable to start synchronization")
            sys.exit()

        logging.info("cobot_iot_task.connect:Successfully started synchronization")

        twin_writer = TwinWriter(output_names, output_types)

        header_row = twin_writer.get_header_row()

        logging.info("cobot_iot_task.connect:header_row")

        while self.__running:
            try:
                state = self.__rtde_connection.receive()
                if state is not None:
                    data_row = twin_writer.get_data_row(state)
                    logging.info("cobot_iot_task.connect:data_row")
                    rtdl_model = RtdlModel.get_from_rows(header_row, data_row)
                    rtdl_dt_model = RtdlDtModel.get_from_rtdl_model(rtdl_model)

            except rtde.RTDEException:
                self.__rtde_connection.disconnect()
                sys.exit()

        logging.debug("cobot_iot_task.connect:Complete")
        self.__rtde_connection.send_pause()
        self.__rtde_connection.disconnect()
