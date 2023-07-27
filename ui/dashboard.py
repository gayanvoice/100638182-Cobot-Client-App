import logging
import sys
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from model.rtdl.rtdl_dt_model import RtdlDtModel
from model.rtdl.rtdl_model import RtdlModel
from twin_writer import TwinWriter
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt, QThreadPool, QRunnable)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QLabel, QPushButton, QSizePolicy, QWidget, QListWidget)


class Runnable(QRunnable):
    def __init__(self, dashboard):
        super().__init__()
        self.dashboard = dashboard

    def run(self):
        host = "localhost"
        port = 30004
        config = "configuration.xml"
        frequency = 1

        config_file = rtde_config.ConfigFile(config)
        output_names, output_types = config_file.get_recipe("out")

        rtde_connection = rtde.RTDE(host, port)
        rtde_connection.connect()

        # get controller version
        rtde_connection.get_controller_version()

        # setup recipes
        if not rtde_connection.send_output_setup(output_names, output_types, frequency):
            logging.error("Unable to configure output")
            sys.exit()

        # start data synchronization
        if not rtde_connection.send_start():
            logging.error("Unable to start synchronization")
            sys.exit()

        twin_writer = TwinWriter(output_names, output_types)

        header_row = twin_writer.get_header_row()
        print("\n ".join(str(x) for x in header_row))

        while self.dashboard.robot_status:
            try:
                state = rtde_connection.receive()
                if state is not None:
                    data_row = twin_writer.get_data_row(state)
                    rtdl_model = RtdlModel.get_from_rows(header_row, data_row)
                    rtdl_dt_model = RtdlDtModel.get_from_rtdl_model(rtdl_model)
                    self.dashboard.update_label_cobot_param(rtdl_dt_model.cobot_model)
                    self.dashboard.update_label_control_box_param(rtdl_dt_model.control_box_model)
                    self.dashboard.update_label_payload_param(rtdl_dt_model.payload_model)
                    self.dashboard.update_label_base_param(rtdl_dt_model.base_model)
                    self.dashboard.update_label_shoulder_param(rtdl_dt_model.shoulder_model)
                    self.dashboard.update_label_elbow_param(rtdl_dt_model.elbow_model)
                    self.dashboard.update_label_wrist1_param(rtdl_dt_model.wrist1_model)
                    self.dashboard.update_label_wrist2_param(rtdl_dt_model.wrist2_model)
                    self.dashboard.update_label_wrist3_param(rtdl_dt_model.wrist3_model)
                    self.dashboard.update_label_tool_param(rtdl_dt_model.tool_model)
                    self.dashboard.update_list_widget_log_param(rtdl_dt_model)

            except rtde.RTDEException:
                rtde_connection.disconnect()
                sys.exit()

        sys.stdout.write("\rComplete!\n")

        rtde_connection.send_pause()
        rtde_connection.disconnect()


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_tool = None
        self.label_tool_param = None
        self.listWidget_Log = None
        self.label_wrist3_param = None
        self.label_wrist3 = None
        self.label_wrist2_param = None
        self.label_wrist2 = None
        self.label_wrist1_param = None
        self.label_wrist1 = None
        self.label_elbow_param = None
        self.label_elbow = None
        self.label_shoulder_param = None
        self.label_base_param = None
        self.label_shoulder = None
        self.label_base = None
        self.label_payload_param = None
        self.label_control_box_param = None
        self.label_cobot_param = None
        self.label_payload = None
        self.label_joint_load = None
        self.label_control_box = None
        self.label_cobot = None
        self.pushButton = None
        self.robot_status = True
        self.button_status = True
        self.pool = None
        self.setupUi()

    def setupUi(self):
        self.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(800, 600))
        icon = QIcon(QIcon.fromTheme(u"computer"))
        self.setWindowIcon(icon)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(490, 30, 80, 24))
        self.pushButton.clicked.connect(self.run_tasks)
        self.label_cobot = QLabel(self)
        self.label_cobot.setObjectName(u"label_cobot")
        self.label_cobot.setGeometry(QRect(340, 20, 120, 30))
        font = QFont()
        font.setPointSize(14)
        self.label_cobot.setFont(font)
        self.label_cobot.setAlignment(Qt.AlignCenter)
        self.label_control_box = QLabel(self)
        self.label_control_box.setObjectName(u"label_control_box")
        self.label_control_box.setGeometry(QRect(40, 100, 120, 30))
        self.label_control_box.setFont(font)
        self.label_control_box.setAlignment(Qt.AlignCenter)
        self.label_joint_load = QLabel(self)
        self.label_joint_load.setObjectName(u"label_joint_load")
        self.label_joint_load.setGeometry(QRect(340, 100, 120, 30))
        self.label_joint_load.setFont(font)
        self.label_joint_load.setAlignment(Qt.AlignCenter)
        self.label_payload = QLabel(self)
        self.label_payload.setObjectName(u"label_payload")
        self.label_payload.setGeometry(QRect(640, 100, 120, 30))
        self.label_payload.setFont(font)
        self.label_payload.setAlignment(Qt.AlignCenter)
        self.label_cobot_param = QLabel(self)
        self.label_cobot_param.setObjectName(u"label_cobot_param")
        self.label_cobot_param.setGeometry(QRect(340, 50, 120, 30))
        self.label_cobot_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_control_box_param = QLabel(self)
        self.label_control_box_param.setObjectName(u"label_control_box_param")
        self.label_control_box_param.setGeometry(QRect(40, 130, 120, 90))
        self.label_control_box_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_payload_param = QLabel(self)
        self.label_payload_param.setObjectName(u"label_payload_param")
        self.label_payload_param.setGeometry(QRect(660, 130, 120, 90))
        self.label_payload_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_base = QLabel(self)
        self.label_base.setObjectName(u"label_base")
        self.label_base.setGeometry(QRect(160, 140, 120, 30))
        self.label_base.setFont(font)
        self.label_base.setAlignment(Qt.AlignCenter)
        self.label_shoulder = QLabel(self)
        self.label_shoulder.setObjectName(u"label_shoulder")
        self.label_shoulder.setGeometry(QRect(340, 140, 120, 30))
        self.label_shoulder.setFont(font)
        self.label_shoulder.setAlignment(Qt.AlignCenter)
        self.label_base_param = QLabel(self)
        self.label_base_param.setObjectName(u"label_base_param")
        self.label_base_param.setGeometry(QRect(160, 170, 160, 120))
        self.label_base_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_shoulder_param = QLabel(self)
        self.label_shoulder_param.setObjectName(u"label_shoulder_param")
        self.label_shoulder_param.setGeometry(QRect(340, 170, 160, 120))
        self.label_shoulder_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_elbow = QLabel(self)
        self.label_elbow.setObjectName(u"label_elbow")
        self.label_elbow.setGeometry(QRect(520, 140, 120, 30))
        self.label_elbow.setFont(font)
        self.label_elbow.setAlignment(Qt.AlignCenter)
        self.label_elbow_param = QLabel(self)
        self.label_elbow_param.setObjectName(u"label_elbow_param")
        self.label_elbow_param.setGeometry(QRect(520, 170, 160, 120))
        self.label_elbow_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_wrist1 = QLabel(self)
        self.label_wrist1.setObjectName(u"label_wrist1")
        self.label_wrist1.setGeometry(QRect(60, 290, 120, 30))
        self.label_wrist1.setFont(font)
        self.label_wrist1.setAlignment(Qt.AlignCenter)
        self.label_wrist1_param = QLabel(self)
        self.label_wrist1_param.setObjectName(u"label_wrist1_param")
        self.label_wrist1_param.setGeometry(QRect(60, 320, 160, 150))
        self.label_wrist1_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_wrist2 = QLabel(self)
        self.label_wrist2.setObjectName(u"label_wrist2")
        self.label_wrist2.setGeometry(QRect(240, 290, 120, 30))
        self.label_wrist2.setFont(font)
        self.label_wrist2.setAlignment(Qt.AlignCenter)
        self.label_wrist2_param = QLabel(self)
        self.label_wrist2_param.setObjectName(u"label_wrist2_param")
        self.label_wrist2_param.setGeometry(QRect(240, 320, 160, 150))
        self.label_wrist2_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_wrist3 = QLabel(self)
        self.label_wrist3.setObjectName(u"label_wrist3")
        self.label_wrist3.setGeometry(QRect(420, 290, 120, 30))
        self.label_wrist3.setFont(font)
        self.label_wrist3.setAlignment(Qt.AlignCenter)
        self.label_wrist3_param = QLabel(self)
        self.label_wrist3_param.setObjectName(u"label_wrist3_param")
        self.label_wrist3_param.setGeometry(QRect(420, 320, 160, 150))
        self.label_wrist3_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.listWidget_Log = QListWidget(self)
        self.listWidget_Log.setObjectName(u"listWidget_Log")
        self.listWidget_Log.setGeometry(QRect(10, 470, 780, 120))
        self.label_tool_param = QLabel(self)
        self.label_tool_param.setObjectName(u"label_tool_param")
        self.label_tool_param.setGeometry(QRect(600, 320, 160, 150))
        self.label_tool_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_tool = QLabel(self)
        self.label_tool.setObjectName(u"label_tool")
        self.label_tool.setGeometry(QRect(600, 290, 120, 30))
        self.label_tool.setFont(font)
        self.label_tool.setAlignment(Qt.AlignCenter)

        self.load_ui()

        QMetaObject.connectSlotsByName(self)

    def run_tasks(self):
        if self.button_status:
            self.button_status = False
            self.robot_status = True
            self.pool = QThreadPool.globalInstance()
            runnable = Runnable(self)
            self.pool.start(runnable)
            self.pushButton.setText("Stop")
        else:
            self.button_status = True
            self.robot_status = False
            self.pushButton.setText("Start")

    def update_label_cobot_param(self, cobot_model):
        self.label_cobot_param.setText("")
        self.label_cobot_param.setText(u"ElapsedTime " + str(cobot_model.elapsed_time))

    def update_label_control_box_param(self, control_box_model):
        self.label_control_box_param.setText("")
        self.label_control_box_param.setText(u"Voltage " + str(control_box_model.voltage))

    def update_label_payload_param(self, payload_model):
        self.label_payload_param.setText("")
        self.label_payload_param.setText(u"Mass " + str(payload_model.mass) +
                                         "\nCoGx " + str(payload_model.cogx) +
                                         "\nCoGy " + str(payload_model.cogy) +
                                         "\nCoGz " + str(payload_model.cogz))

    def update_label_base_param(self, base_model):
        self.label_base_param.setText("")
        self.label_base_param.setText(u"Position " + str(base_model.position) + "\n"
                                                                                "Temperature " + str(
            base_model.temperature) + "\n"
                                      "Voltage " + str(base_model.voltage))

    def update_label_shoulder_param(self, shoulder_model):
        self.label_shoulder_param.setText("")
        self.label_shoulder_param.setText(u"Position " + str(shoulder_model.position) + "\n"
                                                                                        "Temperature " + str(
            shoulder_model.temperature) + "\n"
                                          "Voltage " + str(shoulder_model.voltage))

    def update_label_elbow_param(self, elbow_model):
        self.label_elbow_param.setText("")
        self.label_elbow_param.setText(u"Position " + str(elbow_model.position) + "\n"
                                                                                  "Temperature " + str(
            elbow_model.temperature) + "\n"
                                       "Voltage " + str(elbow_model.voltage) + "\n"
                                                                               "X " + str(elbow_model.x) + "\n"
                                                                                                           "Y " + str(
            elbow_model.y) + "\n"
                             "Z " + str(elbow_model.z))

    def update_label_wrist1_param(self, wrist1_model):
        self.label_wrist1_param.setText("")
        self.label_wrist1_param.setText(u"Position " + str(wrist1_model.position) + "\n"
                                                                                    "Temperature " + str(
            wrist1_model.temperature) + "\n"
                                        "Voltage " + str(wrist1_model.voltage))

    def update_label_wrist2_param(self, wrist2_model):
        self.label_wrist2_param.setText("")
        self.label_wrist2_param.setText(u"Position " + str(wrist2_model.position) + "\n"
                                                                                    "Temperature " + str(
            wrist2_model.temperature) + "\n"
                                        "Voltage " + str(wrist2_model.voltage))

    def update_label_wrist3_param(self, wrist3_model):
        self.label_wrist3_param.setText("")
        self.label_wrist3_param.setText(u"Position " + str(wrist3_model.position) + "\n"
                                                                                    "Temperature " + str(
            wrist3_model.temperature) + "\n"
                                        "Voltage " + str(wrist3_model.voltage))

    def update_label_tool_param(self, tool_model):
        self.label_tool_param.setText("")
        self.label_tool_param.setText(u"Temperature " + str(tool_model.temperature) + "\n"
                                                                                      "Voltage " + str(
            tool_model.voltage) + "\n"
                                  "X " + str(tool_model.x) + "\n"
                                                             "Y " + str(tool_model.y) + "\n"
                                                                                        "Z " + str(tool_model.z) + "\n"
                                                                                                                   "RX " + str(
            tool_model.rx) + "\n"
                             "RY " + str(tool_model.ry) + "\n"
                                                          "RZ " + str(tool_model.rz))

    def update_list_widget_log_param(self, rtdl_dt_model):
        self.listWidget_Log.addItem(str(rtdl_dt_model.cobot_model.__dict__) + str(rtdl_dt_model.elbow_model.__dict__))

    def load_ui(self):
        self.setWindowTitle(QCoreApplication.translate("Dashboard", u"Dashboard", None))
        self.pushButton.setText(QCoreApplication.translate("Dashboard", u"Start", None))
        self.label_cobot.setText(QCoreApplication.translate("Dashboard", u"Cobot", None))
        self.label_control_box.setText(QCoreApplication.translate("Dashboard", u"Control Box", None))
        self.label_joint_load.setText(QCoreApplication.translate("Dashboard", u"Joint Load", None))
        self.label_payload.setText(QCoreApplication.translate("Dashboard", u"Payload", None))
        self.label_cobot_param.setText(QCoreApplication.translate("Dashboard", u"ElapsedTime DOUBLE", None))
        self.label_control_box_param.setText(QCoreApplication.translate("Dashboard", "Voltage DOUBLE", None))
        self.label_payload_param.setText(QCoreApplication.translate("Dashboard", u"Mass DOUBLE\n"
                                                                                 "CoGx DOUBLE\n"
                                                                                 "CoGy DOUBLE\n"
                                                                                 "CoGz DOUBLE", None))
        self.label_base.setText(QCoreApplication.translate("Dashboard", u"Base", None))
        self.label_shoulder.setText(QCoreApplication.translate("Dashboard", u"Shoulder", None))
        self.label_base_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                              "Temperature DOUBLE\n"
                                                                              "Voltage DOUBLE", None))
        self.label_shoulder_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                  "Temperature DOUBLE\n"
                                                                                  "Voltage DOUBLE", None))
        self.label_elbow.setText(QCoreApplication.translate("Dashboard", u"Elbow", None))
        self.label_elbow_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                               "Temperature DOUBLE\n"
                                                                               "Voltage DOUBLE\n"
                                                                               "X DOUBLE\n"
                                                                               "Y DOUBLE\n"
                                                                               "Z DOUBLE", None))
        self.label_wrist1.setText(QCoreApplication.translate("Dashboard", u"Wrist 1", None))
        self.label_wrist1_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                "Temperature DOUBLE\n"
                                                                                "Voltage DOUBLE", None))
        self.label_wrist2.setText(QCoreApplication.translate("Dashboard", u"Wrist 2", None))
        self.label_wrist2_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                "Temperature DOUBLE\n"
                                                                                "Voltage DOUBLE", None))
        self.label_wrist3.setText(QCoreApplication.translate("Dashboard", u"Wrist 3", None))
        self.label_wrist3_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                "Temperature DOUBLE\n"
                                                                                "Voltage DOUBLE", None))
        self.label_tool_param.setText(QCoreApplication.translate("Dashboard", u"Temperature DOUBLE\n"
                                                                              "Voltage DOUBLE\n"
                                                                              "X DOUBLE\n"
                                                                              "Y DOUBLE\n"
                                                                              "Z DOUBLE\n"
                                                                              "RX DOUBLE\n"
                                                                              "RY DOUBLE\n"
                                                                              "RZ DOUBLE", None))
        self.label_tool.setText(QCoreApplication.translate("Dashboard", u"Tool", None))
