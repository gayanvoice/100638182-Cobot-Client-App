__author__ = "100638182"
__copyright__ = "University of Derby"

import logging
from model.request.joint_position_model import JointPositionModel
from model.request.tcp_position_model import TcpPositionModel


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
        logging.info("cobot_control_task.move_p:Length tcp_position_array_length={tcp_position_array_length}"
                     .format(tcp_position_array_length=str(len(move_p_control_model.tcp_position_model_array))))
        for index, tcp_position_model in enumerate(move_p_control_model.tcp_position_model_array):
            tcp_position_array = TcpPositionModel.get_position_array_from_tcp_position_model(
                tcp_position_model=tcp_position_model)
            model_index = index + 1
            array_length = len(move_p_control_model.tcp_position_model_array)

            logging.info('cobot_control_task.move_p:Execute joint_position_model {model_index}/{array_length}'
                         .format(model_index=model_index,
                                 array_length=array_length))
            self.__robot.movep(pose=tcp_position_array,
                               a=move_p_control_model.acceleration,
                               v=move_p_control_model.velocity,
                               r=move_p_control_model.blend_radius)
            logging.info('cobot_control_task.move_p:Success joint_position_model_index={joint_position_model_index}, '
                         'tcp_position_array={tcp_position_array}, '
                         'acceleration={acceleration}, velocity={velocity}, '
                         'blend_radius={blend_radius}'
                         .format(joint_position_model_index=model_index,
                                 tcp_position_array=tcp_position_array,
                                 acceleration=move_p_control_model.acceleration,
                                 velocity=move_p_control_model.velocity,
                                 blend_radius=move_p_control_model.blend_radius))
        logging.info("cobot_control_task.move_p:Complete")


    async def move_l(self, move_l_control_model):
        logging.info("cobot_control_task.move_l:Starting")
        logging.info("cobot_control_task.move_l:Length joint_position_array_length={joint_position_array_length}"
                     .format(joint_position_array_length=str(len(move_l_control_model.tcp_position_model_array))))
        for index, tcp_position_model in enumerate(move_l_control_model.tcp_position_model_array):
            tcp_position_array = TcpPositionModel.get_position_array_from_tcp_position_model(
                tcp_position_model=tcp_position_model)
            model_index = index + 1
            array_length = len(move_l_control_model.tcp_position_model_array)

            logging.info('cobot_control_task.move_l:Execute joint_position_model {model_index}/{array_length}'
                         .format(model_index=model_index,
                                 array_length=array_length))
            self.__robot.movel(pose=tcp_position_array,
                               a=move_l_control_model.acceleration,
                               v=move_l_control_model.velocity,
                               t=move_l_control_model.time_s,
                               r=move_l_control_model.blend_radius)
            logging.info('cobot_control_task.move_p:Success joint_position_model_index={joint_position_model_index}, '
                         'tcp_position_array={tcp_position_array}, '
                         'acceleration={acceleration}, velocity={velocity}, '
                         'blend_radius={blend_radius}'
                         .format(joint_position_model_index=model_index,
                                 tcp_position_array=tcp_position_array,
                                 acceleration=move_l_control_model.acceleration,
                                 velocity=move_l_control_model.velocity,
                                 blend_radius=move_l_control_model.blend_radius))
        logging.info("cobot_control_task.move_l:Complete")
