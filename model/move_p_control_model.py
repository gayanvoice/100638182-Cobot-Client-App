import json
from model.joint_position_model import JointPositionModel


class MovePControlModel:
    def __init__(self):
        self._acceleration = None
        self._velocity = None
        self._blend_radius = None
        self._joint_position_model_array = []

    @property
    def acceleration(self):
        return self._acceleration

    @property
    def velocity(self):
        return self._velocity

    @property
    def blend_radius(self):
        return self._blend_radius

    @property
    def joint_position_model_array(self):
        return self._joint_position_model_array

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    @velocity.setter
    def velocity(self, value):
        self._velocity = value


    @blend_radius.setter
    def blend_radius(self, value):
        self._blend_radius = value

    @joint_position_model_array.setter
    def joint_position_model_array(self, value):
        self._joint_position_model_array.append(value)

    @staticmethod
    def get_move_p_model_from_values(values):
        data = json.loads(values)
        move_p_control_model = MovePControlModel()
        move_p_control_model.acceleration = data["acceleration"]
        move_p_control_model.velocity = data["velocity"]
        move_p_control_model.blend_radius = data["blend_radius"]
        for joint_position_model_array_object in data["joint_position_model_array"]:
            joint_position_model = JointPositionModel.get_joint_position_model_from_joint_position_model_object(
                joint_position_model_array_object["joint_position_model"])
            move_p_control_model.joint_position_model_array = joint_position_model
        return move_p_control_model
