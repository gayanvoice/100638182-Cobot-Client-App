import logging

from model.request.joint_position_model import JointPositionModel


class CobotControlTask:

    def __init__(self, robot):
        self.__robot = robot

    async def move_j(self, move_j_control_model):
        logging.info("cobot_control_task.move_j:Starting")
        logging.info("cobot_control_task.move_j:Length joint_position_array_length={joint_position_array_length}"
                     .format(joint_position_array_length=str(len(move_j_control_model.joint_position_model_array))))
        for index, joint_position_model in enumerate(move_j_control_model.joint_position_model_array):
            joint_position_array = JointPositionModel.get_position_array_from_joint_position_model(
                joint_position_model=joint_position_model)
            model_index = index + 1
            array_length = len(move_j_control_model.joint_position_model_array)

            logging.info('cobot_control_task.move_j:Execute joint_position_model {model_index}/{array_length}'
                         .format(model_index=model_index,
                                 array_length=array_length))
            self.__robot.movej(q=joint_position_array,
                               a=move_j_control_model.acceleration,
                               v=move_j_control_model.velocity,
                               t=move_j_control_model.time_s,
                               r=move_j_control_model.blend_radius)
            logging.info('cobot_control_task.move_j:Success joint_position_model_index={joint_position_model_index}, '
                         'joint_position_array={joint_position_array}, '
                         'acceleration={acceleration}, velocity={velocity}, time_s={time_s}, '
                         'blend_radius={blend_radius}'
                         .format(joint_position_model_index=model_index,
                                 joint_position_array=joint_position_array,
                                 acceleration=move_j_control_model.acceleration,
                                 velocity=move_j_control_model.velocity,
                                 time_s=move_j_control_model.time_s,
                                 blend_radius=move_j_control_model.blend_radius))
        logging.info("cobot_control_task.move_j:Complete")


    async def move_p(self, move_p_control_model):
        logging.info("cobot_control_task.move_p:Starting")
        logging.info("cobot_control_task.move_p:Length joint_position_array_length={joint_position_array_length}"
                     .format(joint_position_array_length=str(len(move_p_control_model.joint_position_model_array))))
        for index, joint_position_model in enumerate(move_p_control_model.joint_position_model_array):
            joint_position_array = JointPositionModel.get_position_array_from_joint_position_model(
                joint_position_model=joint_position_model)
            model_index = index + 1
            array_length = len(move_p_control_model.joint_position_model_array)

            logging.info('cobot_control_task.move_p:Execute joint_position_model {model_index}/{array_length}'
                         .format(model_index=model_index,
                                 array_length=array_length))
            self.__robot.movep(pose=joint_position_array,
                               a=move_p_control_model.acceleration,
                               v=move_p_control_model.velocity,
                               r=move_p_control_model.blend_radius)
            logging.info('cobot_control_task.move_p:Success joint_position_model_index={joint_position_model_index}, '
                         'joint_position_array={joint_position_array}, '
                         'acceleration={acceleration}, velocity={velocity}, '
                         'blend_radius={blend_radius}'
                         .format(joint_position_model_index=model_index,
                                 joint_position_array=joint_position_array,
                                 acceleration=move_p_control_model.acceleration,
                                 velocity=move_p_control_model.velocity,
                                 blend_radius=move_p_control_model.blend_radius))
        logging.info("cobot_control_task.move_p:Complete")


    async def move_l(self, move_l_control_model):
        logging.info("cobot_control_task.move_l:Starting")
        logging.info("cobot_control_task.move_l:Length joint_position_array_length={joint_position_array_length}"
                     .format(joint_position_array_length=str(len(move_l_control_model.joint_position_model_array))))
        for index, joint_position_model in enumerate(move_l_control_model.joint_position_model_array):
            joint_position_array = JointPositionModel.get_position_array_from_joint_position_model(
                joint_position_model=joint_position_model)
            model_index = index + 1
            array_length = len(move_l_control_model.joint_position_model_array)

            logging.info('cobot_control_task.move_l:Execute joint_position_model {model_index}/{array_length}'
                         .format(model_index=model_index,
                                 array_length=array_length))
            self.__robot.movel(pose=joint_position_array,
                               a=move_l_control_model.acceleration,
                               v=move_l_control_model.velocity,
                               t=move_l_control_model.time_s,
                               r=move_l_control_model.blend_radius)
            logging.info('cobot_control_task.move_p:Success joint_position_model_index={joint_position_model_index}, '
                         'joint_position_array={joint_position_array}, '
                         'acceleration={acceleration}, velocity={velocity}, '
                         'blend_radius={blend_radius}'
                         .format(joint_position_model_index=model_index,
                                 joint_position_array=joint_position_array,
                                 acceleration=move_l_control_model.acceleration,
                                 velocity=move_l_control_model.velocity,
                                 blend_radius=move_l_control_model.blend_radius))
        logging.info("cobot_control_task.move_l:Complete")

    # async def stop(self):
    #     logging.info("cobot_control_task.stop_j:Starting")
    #     self.__robot.(a=stop_j_control_model.acceleration)
    #     logging.info('cobot_control_task.stop_j:Success acceleration={acceleration}'
    #                  .format(acceleration=stop_j_control_model.acceleration))
    #     logging.info("cobot_control_task.move_j:Complete")

    # def terminate(self):
    #     self.__running = False

    # async def connect(self):
    #     logging.info("cobot_control_task.connect:Starting")
    #
    #     config_file = rtde_config.ConfigFile(self.__control_configuration_path)
    #     state_names, state_types = config_file.get_recipe("state")
    #     setp_names, setp_types = config_file.get_recipe("setp")
    #     watchdog_names, watchdog_types = config_file.get_recipe("watchdog")
    #
    #     self.__rtde_connection = rtde.RTDE(self.__rtde_host, self.__rtde_port)
    #     self.__rtde_connection.connect()
    #
    #     self.__rtde_connection.get_controller_version()
    #
    #     self.__rtde_connection.send_output_setup(state_names, state_types)
    #     set_position = self.__rtde_connection.send_input_setup(setp_names, setp_types)
    #     watchdog = self.__rtde_connection.send_input_setup(watchdog_names, watchdog_types)
    #
    #     watchdog.input_int_register_0 = 0
    #
    #     if not self.__rtde_connection.send_start():
    #         sys.exit()
    #
    #     await self.control_cobot(watchdog, set_position)
    #
    #     self.__rtde_connection.send_pause()
    #     self.__rtde_connection.disconnect()
    #
    # async def control_cobot(self, watchdog, set_position):
    #
    #     set_position.input_double_register_0 = 0
    #     set_position.input_double_register_1 = 0
    #     set_position.input_double_register_2 = 0
    #     set_position.input_double_register_3 = 0
    #     set_position.input_double_register_4 = 0
    #     set_position.input_double_register_5 = 0
    #
    #     self.__running = True
    #     move_completed = True
    #     set_position_index = 0
    #
    #     while self.__running:
    #         if set_position_index >= len(self.__set_position_array):
    #             set_position_index = 0
    #
    #         current_set_position = self.__set_position_array[set_position_index]
    #
    #         state = self.__rtde_connection.receive()
    #
    #         if state is None:
    #             break
    #
    #         start_time = datetime.now()
    #         if move_completed and state.output_int_register_0 == 1:
    #
    #             move_completed = False
    #             await self.list_to_set_p(set_position, current_set_position)
    #             logging.info(str(set_position_index)
    #                          + "/"
    #                          + str(len(self.__set_position_array))
    #                          + ": "
    #                          + str(start_time)
    #                          + " New pose = "
    #                          + str(current_set_position))
    #             self.__rtde_connection.send(set_position)
    #             watchdog.input_int_register_0 = 1
    #         elif not move_completed and state.output_int_register_0 == 0:
    #             end_time = datetime.now()
    #             elapsed_time = self.calculate_time_difference(start_time, end_time)
    #             logging.info(str(set_position_index)
    #                          + "/"
    #                          + str(len(self.__set_position_array)) + ": "
    #                          + str(start_time)
    #                          + "Move to confirmed pose = "
    #                          + str(state.target_q))
    #             logging.info(str(set_position_index)
    #                          + "/"
    #                          + str(len(self.__set_position_array))
    #                          + ": "
    #                          + "Time Elapsed = "
    #                          + str(elapsed_time))
    #             move_completed = True
    #             watchdog.input_int_register_0 = 0
    #             time.sleep(1)
    #         self.__rtde_connection.send(watchdog)
    #         set_position_index += 1
    #
    # @staticmethod
    # async def list_to_set_p(sp, list):
    #     for i in range(0, 6):
    #         sp.__dict__["input_double_register_%i" % i] = list[i]
    #     return sp
    #
    # @staticmethod
    # def calculate_time_difference(start, end):
    #     duration = end - start
    #     return duration
