__author__ = "100638182"
__copyright__ = "University of Derby"


class TcpPositionModel:
    def __init__(self):
        self._x = None
        self._y = None
        self._z = None
        self._rx = None
        self._ry = None
        self._rz = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def rx(self):
        return self._rx

    @property
    def ry(self):
        return self._ry

    @property
    def rz(self):
        return self._rz

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @z.setter
    def z(self, value):
        self._z = value

    @rx.setter
    def rx(self, value):
        self._rx = value

    @ry.setter
    def ry(self, value):
        self._ry = value

    @rz.setter
    def rz(self, value):
        self._rz = value

    @staticmethod
    def get_tcp_position_model_from_tcp_position_model_object(tcp_position_model_object):
        tcp_position_model = TcpPositionModel()
        tcp_position_model.x = tcp_position_model_object["X"]
        tcp_position_model.y = tcp_position_model_object["Y"]
        tcp_position_model.z = tcp_position_model_object["Z"]
        tcp_position_model.rx = tcp_position_model_object["Rx"]
        tcp_position_model.ry = tcp_position_model_object["Ry"]
        tcp_position_model.rz = tcp_position_model_object["Rz"]
        return tcp_position_model

    @staticmethod
    def get_position_array_from_tcp_position_model(tcp_position_model):
        return (tcp_position_model.x,
                tcp_position_model.y,
                tcp_position_model.z,
                tcp_position_model.rx,
                tcp_position_model.ry,
                tcp_position_model.rz)
