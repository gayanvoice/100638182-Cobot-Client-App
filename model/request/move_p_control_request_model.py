__author__ = "100638182"
__copyright__ = "University of Derby"

from model.request.tcp_position_model import TcpPositionModel


class MovePControlRequestModel:
    def __init__(self):
        self._acceleration = None
        self._velocity = None
        self._blend_radius = None
        self._tcp_position_model_array = []

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
    def tcp_position_model_array(self):
        return self._tcp_position_model_array

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    @velocity.setter
    def velocity(self, value):
        self._velocity = value


    @blend_radius.setter
    def blend_radius(self, value):
        self._blend_radius = value

    @tcp_position_model_array.setter
    def tcp_position_model_array(self, value):
        self._tcp_position_model_array.append(value)

    @staticmethod
    def get_move_p_control_request_model_from_values(values):
        move_p_control_request_model = MovePControlRequestModel()
        move_p_control_request_model.acceleration = values["Acceleration"]
        move_p_control_request_model.velocity = values["Velocity"]
        move_p_control_request_model.blend_radius = values["BlendRadius"]
        for tcp_position_model_array_object in values["TcpPositionModelArray"]:
            tcp_position_model = TcpPositionModel.get_tcp_position_model_from_tcp_position_model_object(
                tcp_position_model_array_object["TcpPositionModel"])
            move_p_control_request_model.tcp_position_model_array = tcp_position_model
        return move_p_control_request_model
