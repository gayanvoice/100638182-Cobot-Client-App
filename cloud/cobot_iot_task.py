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
        print("connect")
        logging.getLogger().setLevel(logging.INFO)

        config_file = rtde_config.ConfigFile(self.__config)
        output_names, output_types = config_file.get_recipe("out")

        self.__rtde_connection = rtde.RTDE(self.__host, self.__port)
        self.__rtde_connection.connect()

        self.__rtde_connection.get_controller_version()

        # setup recipes
        if not self.__rtde_connection.send_output_setup(output_names, output_types, self.__frequency):
            logging.error("Unable to configure output")
            sys.exit()

        # start data synchronization
        if not self.__rtde_connection.send_start():
            logging.error("Unable to start synchronization")
            sys.exit()

        twin_writer = TwinWriter(output_names, output_types)

        header_row = twin_writer.get_header_row()

        while self.__running:
            try:
                state = self.__rtde_connection.receive()
                if state is not None:
                    data_row = twin_writer.get_data_row(state)
                    rtdl_model = RtdlModel.get_from_rows(header_row, data_row)
                    rtdl_dt_model = RtdlDtModel.get_from_rtdl_model(rtdl_model)
                    print(str(rtdl_dt_model.cobot_model.elapsed_time))

            except rtde.RTDEException:
                self.__rtde_connection.disconnect()
                sys.exit()

        sys.stdout.write("\rComplete!\n")
        self.__rtde_connection.send_pause()
        self.__rtde_connection.disconnect()
