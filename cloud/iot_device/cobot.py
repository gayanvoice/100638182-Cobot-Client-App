__author__ = "100638182"
__copyright__ = "University of Derby"

import ast
import asyncio
import inspect
import logging
import json
import URBasic
import xml.etree.ElementTree as ET
import time
from azure.iot.device.common.pipeline.pipeline_exceptions import PipelineNotRunning
from json import JSONDecodeError
from threading import Thread
from cloud.control_task.cobot_control_task import CobotControlTask
from cloud.device import Device
from cloud.iot_task.cobot_iot_task import CobotIotTask
from helper.log_text_helper import LogTextHelper, LogTextStatus
from model.response.control.close_popup_control_response_model import ClosePopupControlResponseModel
from model.response.control.close_safety_popup_control_response_model import CloseSafetyPopupControlResponseModel
from model.response.control.open_popup_control_response_model import OpenPopupControlResponseModel
from model.response.control.pause_control_response_model import PauseControlResponseModel
from model.response.control.play_control_response_model import PlayControlResponseModel
from model.response.control.power_off_control_response_model import PowerOffControlResponseModel
from model.response.control.power_on_control_response_model import PowerOnControlResponseModel
from model.response.control.start_free_drive_control_response_model import StartFreeDriveControlResponseModel
from model.response.control.stop_free_drive_control_response_model import StopFreeDriveControlResponseModel
from model.response.control.unlock_protective_stop_control_response_model import \
    UnlockProtectiveStopControlResponseModel
from model.response.control.move_j_control_response_model import MoveJControlResponseModel
from model.response.control.move_l_control_response_model import MoveLControlResponseModel
from model.response.control.move_p_control_response_model import MovePControlResponseModel
from model.response.response_model import Status
from model.response.iot.start_iot_command_response_model import StartIotCommandRespondModel
from model.response.iot.stop_iot_command_response_model import StopIotCommandRespondModel
from model.response.control.enable_control_response_model import EnableControlResponseModel
from model.response.control.disable_control_response_model import DisableControlResponseModel
from model.request.move_j_control_request_model import MoveJControlRequestModel
from model.request.move_l_control_request_model import MoveLControlRequestModel
from model.request.move_p_control_request_model import MovePControlRequestModel
from model.request.open_popup_control_request_model import OpenPopupControlRequestModel
from model.rtdl.rtdl_dt_model import RtdlDtModel


class Cobot(object):
    def __init__(self,
                 rtde_host,
                 rtde_port,
                 control_configuration_path,
                 cobot_client_configuration_path,
                 model_id,
                 provisioning_host,
                 id_scope,
                 registration_id,
                 symmetric_key,
                 cache_json_path):
        self.__rtde_host = rtde_host
        self.__rtde_port = rtde_port
        self.__control_configuration_path = control_configuration_path
        self.__cobot_client_configuration_path = cobot_client_configuration_path
        self.__model_id = model_id
        self.__provisioning_host = provisioning_host
        self.__id_scope = id_scope
        self.__registration_id = registration_id
        self.__symmetric_key = symmetric_key
        self.__cache_json_path = cache_json_path
        self.__cobot_device = None
        self.__ur_script_ext = None
        self.__cobot_control_task = None
        self.__cobot_iot_task = None
        self.__cobot_control_thread = None
        self.__cobot_iot_thread = None
        self.__is_ur_basic_running = False
        self.__cobot_control_lock = True
        self.__cobot_iot_lock = True
        self.__enable_control_response_model = None
        self.__disable_control_response_model = None
        self.__move_j_control_response_model = None
        self.__move_l_control_response_model = None
        self.__move_p_control_response_model = None
        self.__pause_control_response_model = None
        self.__play_control_response_model = None
        self.__power_on_control_response_model = None
        self.__power_off_control_response_model = None
        self.__unlock_protective_stop_control_response_model = None
        self.__close_safety_popup_control_response_model = None
        self.__open_popup_control_response_model = None
        self.__close_popup_control_response_model = None
        self.__start_free_drive_control_response_model = None
        self.__stop_free_drive_control_response_model = None
        self.__start_iot_command_response_model = None
        self.__stop_iot_command_response_model = None
        self.__log_text_helper = LogTextHelper(class_name=self.__class__.__name__)

    def stdin_listener(self):
        while True:
            config_element_tree = ET.parse(self.__cobot_client_configuration_path)
            cobot_configuration = config_element_tree.find('cobot')
            process_continue = cobot_configuration.find('status').text
            if process_continue == "False":
                try:
                    self.__ur_script_ext.close()
                    self.__cobot_control_lock = True
                except AttributeError:
                    logging.error("cobot.stdin_listener:No UR Script Ext error=AttributeError")
                logging.info("cobot.stdin_listener:break process_continue={process_continue}"
                             .format(process_continue=process_continue))
                break
            else:
                time.sleep(1)

    def move_j_control_task_callback(self, move_j_control_model):
        if not self.__cobot_control_lock:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.info(log_text)

            self.__cobot_control_lock = True
            self.__cobot_control_task = CobotControlTask(robot=self.__ur_script_ext)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(self.__cobot_control_task.move_j(move_j_control_model=move_j_control_model))

                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.COMPLETED,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "cobot_control_lock": self.__cobot_control_lock
                    })
                logging.info(log_text)
            except RuntimeError:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.ERROR,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "error": RuntimeError.__dict__
                    })
                logging.error(log_text)

            loop.close()
            self.__cobot_control_lock = False

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.info(log_text)
        else:
            self.__cobot_control_lock = True

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.error(log_text)

    async def move_j_control_command_handler(self, values):
        self.__move_j_control_response_model = MoveJControlResponseModel()
        if self.__is_ur_basic_running:
            try:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.STARTING,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running
                    })
                logging.info(log_text)

                move_j_control_request_model = MoveJControlRequestModel\
                    .get_move_j_control_request_model_from_values(values)
                self.__cobot_control_thread = Thread(target=self.move_j_control_task_callback,
                                                     args=(move_j_control_request_model,))
                self.__cobot_control_thread.start()

                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.COMPLETED,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running,
                        "move_j_control_request_model": move_j_control_request_model.__dict__,
                        "move_j_control_request_model_type": str(type(move_j_control_request_model))
                    })
                logging.info(log_text)
                self.__move_j_control_response_model \
                    .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)

            except JSONDecodeError:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.ERROR,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running,
                        "error": "JSONDecodeError"
                    })
                logging.info(log_text)
                self.__move_j_control_response_model \
                    .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__move_j_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def move_j_control_response_handler(self, values):
        response_payload = json.dumps(self.__move_j_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    def move_p_control_task_callback(self, move_p_control_model):
        if not self.__cobot_control_lock:
            logging.info("cobot.move_p_control_task_callback:__cobot_control_lock={cobot_control_lock}"
                         .format(cobot_control_lock=self.__cobot_control_lock))
            self.__cobot_control_lock = True
            logging.info("cobot.move_p_control_task_callback:Robot initialised")

            self.__cobot_control_task = CobotControlTask(robot=self.__ur_script_ext)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(self.__cobot_control_task.move_p(move_p_control_model=move_p_control_model))

                logging.info('cobot.move_p_control_task_callback:Thread completed')
            except RuntimeError:
                logging.error('cobot.move_p_control_task_callback:Thread failed runtime_error={runtime_error}'
                              .format(runtime_error=RuntimeError.__dict__))
            logging.info('cobot.move_p_control_task_callback:Close')

            loop.close()
            self.__cobot_control_lock = False

        else:
            logging.error("cobot.move_p_control_task_callback:__cobot_control_lock={cobot_control_lock}"
                          .format(cobot_control_lock=self.__cobot_control_lock))
            self.__cobot_control_lock = True

    async def move_p_control_command_handler(self, values):
        self.__move_p_control_response_model = MovePControlResponseModel()
        if self.__is_ur_basic_running:
            try:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.STARTING,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running
                    })
                logging.info(log_text)

                move_p_control_request_model = MovePControlRequestModel\
                    .get_move_p_control_request_model_from_values(values)
                self.__cobot_control_thread = Thread(target=self.move_p_control_task_callback,
                                                     args=(move_p_control_request_model,))
                self.__cobot_control_thread.start()

                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.COMPLETED,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running,
                        "move_p_control_request_model": move_p_control_request_model.__dict__,
                        "move_p_control_request_model_type": str(type(move_p_control_request_model))
                    })
                logging.info(log_text)
                self.__move_p_control_response_model \
                    .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
            except JSONDecodeError:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.ERROR,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running,
                        "error": "JSONDecodeError"
                    })
                logging.info(log_text)
                self.__move_p_control_response_model \
                    .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__move_p_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def move_p_control_response_handler(self, values):
        response_payload = json.dumps(self.__move_p_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    def move_l_control_task_callback(self, move_l_control_model):
        if not self.__cobot_control_lock:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.info(log_text)

            self.__cobot_control_lock = True
            self.__cobot_control_task = CobotControlTask(robot=self.__ur_script_ext)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.__cobot_control_task.move_l(move_l_control_model=move_l_control_model))
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.COMPLETED,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "cobot_control_lock": self.__cobot_control_lock
                    })
                logging.info(log_text)
            except RuntimeError:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.ERROR,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "error": RuntimeError.__dict__
                    })
                logging.error(log_text)

            loop.close()
            self.__cobot_control_lock = False

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.info(log_text)
        else:
            self.__cobot_control_lock = True
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.error(log_text)

    async def move_l_control_command_handler(self, values):
        self.__move_l_control_response_model = MoveLControlResponseModel()
        if self.__is_ur_basic_running:
            try:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.STARTING,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running
                    })
                logging.info(log_text)

                move_l_control_request_model = MoveLControlRequestModel\
                    .get_move_l_control_request_model_from_values(values)
                self.__cobot_control_thread = Thread(target=self.move_l_control_task_callback,
                                                     args=(move_l_control_request_model,))
                self.__cobot_control_thread.start()

                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.COMPLETED,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running,
                        "move_l_control_model": move_l_control_request_model.__dict__,
                        "move_l_control_model_type": str(type(move_l_control_request_model))
                    })
                logging.info(log_text)
                self.__move_l_control_response_model \
                    .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)

            except JSONDecodeError:
                log_text = self.__log_text_helper.get_log_text(
                    status=LogTextStatus.ERROR,
                    command_name=inspect.currentframe().f_code.co_name,
                    input_dictionary={
                        "values": values,
                        "is_ur_basic_running": self.__is_ur_basic_running,
                        "error": "JSONDecodeError"
                    })
                logging.info(log_text)
                self.__move_l_control_response_model \
                    .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__move_l_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def move_l_control_response_handler(self, values):
        response_payload = json.dumps(self.__move_l_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def enable_control_command_handler(self, values):
        self.__enable_control_response_model = EnableControlResponseModel()
        if not self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "rtde_host": self.__rtde_host,
                    "cobot_control_lock": self.__cobot_control_lock,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            robotModel = URBasic.robotModel.RobotModel()
            self.__ur_script_ext = URBasic.urScriptExt.UrScriptExt(host=self.__rtde_host, robotModel=robotModel)
            self.__ur_script_ext.reset_error()
            self.__cobot_control_lock = False
            self.__is_ur_basic_running = True
            self.__enable_control_response_model.elapsed_time = self.__ur_script_ext.get_elapsed_time()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "rtde_host": self.__rtde_host,
                    "cobot_control_lock": self.__cobot_control_lock,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__enable_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "rtde_host": self.__rtde_host,
                    "cobot_control_lock": self.__cobot_control_lock,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__enable_control_response_model.elapsed_time = self.__ur_script_ext.get_elapsed_time()
            self.__enable_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def enable_control_response_handler(self, values):
        response_payload = json.dumps(self.__enable_control_response_model.get(),
                                      default=lambda o: o.__dict__,
                                      sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def disable_control_command_handler(self, values):
        self.__disable_control_response_model = DisableControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values
                })
            logging.info(log_text)

            self.__ur_script_ext.close()
            self.__cobot_control_lock = True
            self.__is_ur_basic_running = False

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "cobot_control_lock": self.__cobot_control_lock,
                })
            self.__disable_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "rtde_host": self.__rtde_host,
                    "cobot_control_lock": self.__cobot_control_lock,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__disable_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def disable_control_response_handler(self, values):
        response_payload = json.dumps(self.__disable_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def pause_control_command_handler(self, values):
        self.__pause_control_response_model = PauseControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.pause()
            time.sleep(5)
            self.__pause_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__pause_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()
            self.__cobot_control_lock = True

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running,
                    "cobot_control_lock": self.__cobot_control_lock
                })
            logging.info(log_text)
            self.__pause_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__pause_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def pause_control_response_handler(self, values):
        response_payload = json.dumps(self.__pause_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def play_control_command_handler(self, values):
        self.__play_control_response_model = PlayControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.play()
            self.__cobot_control_lock = False
            time.sleep(5)
            self.__play_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__play_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__play_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__play_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def play_control_response_handler(self, values):
        response_payload = json.dumps(self.__play_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def unlock_protective_stop_control_command_handler(self, values):
        self.__unlock_protective_stop_control_response_model = UnlockProtectiveStopControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.unlock_protective_stop()
            self.__cobot_control_lock = False
            time.sleep(5)
            self.__unlock_protective_stop_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__unlock_protective_stop_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()
            self.__unlock_protective_stop_control_response_model.robot_safety_status \
                = self.__ur_script_ext.get_robot_safety_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__unlock_protective_stop_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__unlock_protective_stop_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def unlock_protective_stop_control_response_handler(self, values):
        response_payload = json.dumps(self.__unlock_protective_stop_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    async def close_safety_popup_control_command_handler(self, values):
        self.__close_safety_popup_control_response_model = CloseSafetyPopupControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.close_safety_popup()
            self.__cobot_control_lock = False
            time.sleep(5)

            self.__close_safety_popup_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__close_safety_popup_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()
            self.__close_safety_popup_control_response_model.robot_safety_status \
                = self.__ur_script_ext.get_robot_safety_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__close_safety_popup_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__close_safety_popup_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def close_safety_popup_control_response_handler(self, values):
        response_payload = json.dumps(self.__close_safety_popup_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    async def open_popup_control_command_handler(self, values):
        self.__open_popup_control_response_model = OpenPopupControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            open_popup_control_request_model = OpenPopupControlRequestModel\
                .get_open_popup_control_request_model_from_values(values)
            logging.info(open_popup_control_request_model.popup_text)
            self.__ur_script_ext.open_popup(popup_text=open_popup_control_request_model.popup_text)

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__open_popup_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__open_popup_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def open_popup_control_response_handler(self, values):
        response_payload = json.dumps(self.__open_popup_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    async def close_popup_control_command_handler(self, values):
        self.__close_popup_control_response_model = ClosePopupControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.close_popup()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__close_popup_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__close_popup_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def close_popup_control_response_handler(self, values):
        response_payload = json.dumps(self.__close_popup_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    async def power_on_control_command_handler(self, values):
        self.__power_on_control_response_model = PowerOnControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.power_on()
            time.sleep(5)
            self.__power_on_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__power_on_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__power_on_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__power_on_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def power_on_control_response_handler(self, values):
        response_payload = json.dumps(self.__power_on_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def power_off_control_command_handler(self, values):
        self.__power_off_control_response_model = PowerOffControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.power_off()
            time.sleep(5)
            self.__power_off_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__power_off_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__power_off_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__power_off_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def power_off_control_response_handler(self, values):
        response_payload = json.dumps(self.__power_off_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload
            }))
        return response_payload

    async def start_free_drive_control_command_handler(self, values):
        self.__start_free_drive_control_response_model = StartFreeDriveControlResponseModel()
        if self.__is_ur_basic_running:

            self.__ur_script_ext.freedrive_mode()
            time.sleep(5)
            self.__start_free_drive_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__start_free_drive_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()
            self.__start_free_drive_control_response_model.robot_safety_status \
                = self.__ur_script_ext.get_robot_safety_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__start_free_drive_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__start_free_drive_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def start_free_drive_control_response_handler(self, values):
        response_payload = json.dumps(self.__start_free_drive_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    async def stop_free_drive_control_command_handler(self, values):
        self.__stop_free_drive_control_response_model = StopFreeDriveControlResponseModel()
        if self.__is_ur_basic_running:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.STARTING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)

            self.__ur_script_ext.end_freedrive_mode()
            time.sleep(5)
            self.__stop_free_drive_control_response_model.robot_mode = self.__ur_script_ext.get_robot_mode()
            self.__stop_free_drive_control_response_model.robot_status = self.__ur_script_ext.get_robot_status()
            self.__stop_free_drive_control_response_model.robot_safety_status \
                = self.__ur_script_ext.get_robot_safety_status()

            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.COMPLETED,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__stop_free_drive_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "is_ur_basic_running": self.__is_ur_basic_running
                })
            logging.info(log_text)
            self.__stop_free_drive_control_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    def stop_free_drive_control_response_handler(self, values):
        response_payload = json.dumps(self.__stop_free_drive_control_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    def start_cobot_iot_task_callback(self, values):
        try:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values
                })
            logging.info(log_text)
            self.__cobot_iot_lock = False
            self.__cobot_iot_task = CobotIotTask(self.__cobot_device)
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            event_loop.run_until_complete(self.__cobot_iot_task.connect())
            event_loop.close()
        except PipelineNotRunning:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "exception": "PipelineNotRunning"
                })
            logging.error(log_text)
            self.__start_iot_command_response_model \
                .set_response(status=Status.COBOT_CLIENT_ERROR, log_text=log_text)

    async def start_cobot_iot_command_handler(self, values):
        self.__start_iot_command_response_model = StartIotCommandRespondModel()
        if self.__cobot_iot_lock:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "cobot_iot_lock": self.__cobot_iot_lock
                })
            logging.info(log_text)
            self.__start_iot_command_response_model \
                .set_response(status=Status.COBOT_CLIENT_EXECUTED, log_text=log_text)
            self.__cobot_iot_thread = Thread(target=self.start_cobot_iot_task_callback, args=(values,))
            self.__cobot_iot_thread.start()
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "cobot_iot_lock": self.__cobot_iot_lock
                })
            logging.error(log_text)
            self.__start_iot_command_response_model \
                .set_response(status=Status.COMMAND_EXECUTION_SEQUENCE_ERROR, log_text=log_text)

    def start_cobot_iot_command_response_handler(self, values):
        response_payload = json.dumps(self.__start_iot_command_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload

            }))
        return response_payload

    async def stop_cobot_iot_command_handler(self, values):
        self.__stop_iot_command_response_model = StopIotCommandRespondModel()
        if not self.__cobot_iot_lock:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.RUNNING,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "cobot_iot_lock": self.__cobot_iot_lock
                })
            logging.info(log_text)
            self.__stop_iot_command_response_model.set_response(status=Status.COBOT_CLIENT_EXECUTED,
                                                                log_text=log_text)
            self.__cobot_iot_lock = True
            self.__cobot_iot_task.terminate()
            self.__cobot_iot_thread.join()
        else:
            log_text = self.__log_text_helper.get_log_text(
                status=LogTextStatus.ERROR,
                command_name=inspect.currentframe().f_code.co_name,
                input_dictionary={
                    "values": values,
                    "cobot_iot_lock": self.__cobot_iot_lock
                })
            logging.error(log_text)
            self.__stop_iot_command_response_model.set_response(status=Status.COMMAND_EXECUTION_SEQUENCE_ERROR,
                                                                log_text=log_text)

    def stop_cobot_iot_command_response_handler(self, values):
        response_payload = json.dumps(self.__stop_iot_command_response_model.get(),
                                      default=lambda o: o.__dict__, sort_keys=True)
        logging.info(self.__log_text_helper.get_log_text(
            status=LogTextStatus.COMPLETED,
            command_name=inspect.currentframe().f_code.co_name,
            input_dictionary={
                "values": values,
                "response_payload": response_payload,
            }))
        return response_payload

    async def connect_azure_iot(self, queue):
        self.__cobot_device = Device(model_id=self.__model_id,
                                     provisioning_host=self.__provisioning_host,
                                     id_scope=self.__id_scope,
                                     registration_id=self.__registration_id,
                                     symmetric_key=self.__symmetric_key)

        await self.__cobot_device.create_iot_hub_device_client()

        await self.__cobot_device.iot_hub_device_client.connect()

        command_listeners = asyncio.gather(
            self.__cobot_device.execute_command_listener(
                method_name="EnableControlCommand",
                user_command_handler=self.enable_control_command_handler,
                create_user_response_handler=self.enable_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="DisableControlCommand",
                user_command_handler=self.disable_control_command_handler,
                create_user_response_handler=self.disable_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="MoveJControlCommand",
                user_command_handler=self.move_j_control_command_handler,
                create_user_response_handler=self.move_j_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="MovePControlCommand",
                user_command_handler=self.move_p_control_command_handler,
                create_user_response_handler=self.move_p_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="MoveLControlCommand",
                user_command_handler=self.move_l_control_command_handler,
                create_user_response_handler=self.move_l_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="PauseControlCommand",
                user_command_handler=self.pause_control_command_handler,
                create_user_response_handler=self.pause_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="PlayControlCommand",
                user_command_handler=self.play_control_command_handler,
                create_user_response_handler=self.play_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="UnlockProtectiveStopControlCommand",
                user_command_handler=self.unlock_protective_stop_control_command_handler,
                create_user_response_handler=self.unlock_protective_stop_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="CloseSafetyPopupControlCommand",
                user_command_handler=self.close_safety_popup_control_command_handler,
                create_user_response_handler=self.close_safety_popup_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="OpenPopupControlCommand",
                user_command_handler=self.open_popup_control_command_handler,
                create_user_response_handler=self.open_popup_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="ClosePopupControlCommand",
                user_command_handler=self.close_popup_control_command_handler,
                create_user_response_handler=self.close_popup_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="PowerOnControlCommand",
                user_command_handler=self.power_on_control_command_handler,
                create_user_response_handler=self.power_on_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="PowerOffControlCommand",
                user_command_handler=self.power_off_control_command_handler,
                create_user_response_handler=self.power_off_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StartFreeDriveControlCommand",
                user_command_handler=self.start_free_drive_control_command_handler,
                create_user_response_handler=self.start_free_drive_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StopFreeDriveControlCommand",
                user_command_handler=self.stop_free_drive_control_command_handler,
                create_user_response_handler=self.stop_free_drive_control_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StartIotCommand",
                user_command_handler=self.start_cobot_iot_command_handler,
                create_user_response_handler=self.start_cobot_iot_command_response_handler,
            ),
            self.__cobot_device.execute_command_listener(
                method_name="StopIotCommand",
                user_command_handler=self.stop_cobot_iot_command_handler,
                create_user_response_handler=self.stop_cobot_iot_command_response_handler,
            ),
            self.__cobot_device.execute_property_listener(),
        )

        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)

        await user_finished

        if not command_listeners.done():
            command_listeners.set_result(["Cobot done"])

        command_listeners.cancel()

        await self.__cobot_device.iot_hub_device_client.shutdown()
        logging.info("cobot.connect_azure_iot:queue.put")
        await queue.put(None)

    @staticmethod
    def check_valid_literal(values):
        try:
            result = ast.literal_eval(values)
            if len(result) == 6:
                logging.info("cobot.check_valid_literal:Valid result={result} type={type}"
                             .format(result=result, type=str(type(values))))
                return True
            else:
                logging.info(
                    "cobot.check_valid_literal:Invalid result=Length should be minimum 6 values length={length}"
                    .format(length=str(len(result))))
                return False
        except (ValueError, SyntaxError) as e:
            logging.info("cobot.check_valid_literal:Invalid values={values} type={type} error={error}"
                         .format(values=values, type=str(type(values)), error=str(e)))
            return False

    def get_rtdl_dt_model(self):
        json_string = self.load_json_content()
        rtdl_dt_model = self.json_string_to_rtdl_dt_model(json_string)
        return rtdl_dt_model

    @staticmethod
    def json_string_to_rtdl_dt_model(json_string):
        parsed_data = json.loads(json_string)
        rtdl_dt_model = RtdlDtModel.get_from_parsed_data(parsed_data)
        return rtdl_dt_model

    def load_json_content(self):
        cache_json_file = open(self.__cache_json_path)
        json_content = json.load(cache_json_file)
        cache_json_file.close()
        return json_content
