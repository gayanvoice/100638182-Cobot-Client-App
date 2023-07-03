import asyncio
import json
import logging
import sys
import time

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

from model.rtdl_dt_model import RtdlDtModel
from model.rtdl_model import RtdlModel
from twin_writer import TwinWriter


class RtdeController:
    def __init__(self, host, port, config, frequency):
        self.__host = host
        self.__port = port
        self.__config = config
        self.__frequency = frequency
        self.__rtde_connection = None
        self.__sync_running = True
        self.__connect_running = True
        self.__json_file = "cache.json"

    def terminate(self):
        self.__sync_running = False

    # async def connect(self):
    #     loop = asyncio.get_running_loop()
    #     user_finished = loop.run_in_executor(None, self.sync)
    #     await user_finished
    #
    #     while self.__connect_running:
    #         try:
    #             await self.sync()
    #         except Exception as ex:
    #             logging.error("rtde_controller.sync:error={error}".format(error=str(ex)))
    #             logging.info("rtde_controller.sync:retrying in 5 seconds")
    #             time.sleep(5)

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

            while self.__sync_running:
                try:
                    state = self.__rtde_connection.receive()
                    if state is not None:
                        data_row = twin_writer.get_data_row(state)
                        logging.info("rtde_controller.connect:data_row")
                        rtdl_model = RtdlModel.get_from_rows(header_row, data_row)
                        rtdl_dt_model = RtdlDtModel.get_from_rtdl_model(rtdl_model)
                        self.create_json(rtdl_dt_model.get_json())
                        await asyncio.sleep(5)

                except rtde.RTDEException as ex:
                    self.__rtde_connection.disconnect()
                    logging.error("rtde_controller.connect:while={error}".format(error=str(ex)))
                    self.terminate()

            await user_finished

            logging.debug("rtde_controller.connect:Complete")
            self.__rtde_connection.send_pause()
            self.__rtde_connection.disconnect()
            logging.info("rtde_controller.connect:queue.put")
            await queue.put(None)

        except Exception as ex:
            logging.error("rtde_controller.connect:exception={error}".format(error=str(ex)))
            logging.info("rtde_controller.connect:queue.put")
            await queue.put(None)


    def stdin_listener(self):
        while True:
            selection = input("Press R to quit Rtde Controller\n")
            if selection == "R" or selection == "r":
                print("Quitting Rtde Controller...")
                self.terminate()
                break


    def create_json(self, json_object):
        with open(self.__json_file, "w+") as f:
            logging.info("rtde_controller.create_json:{file} saved".format(file=self.__json_file))
            json.dump(json_object, f)
