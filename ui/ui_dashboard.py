from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QListView, QPushButton,
                               QSizePolicy, QWidget)


class UiDashboard(object):
    def setupUi(self, Dashboard):
        if not Dashboard.objectName():
            Dashboard.setObjectName(u"Dashboard")
        Dashboard.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dashboard.sizePolicy().hasHeightForWidth())
        Dashboard.setSizePolicy(sizePolicy)
        Dashboard.setMinimumSize(QSize(800, 600))
        Dashboard.setMaximumSize(QSize(800, 600))
        icon = QIcon(QIcon.fromTheme(u"computer"))
        Dashboard.setWindowIcon(icon)
        self.pushButton = QPushButton(Dashboard)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(490, 30, 80, 24))
        self.label_cobot = QLabel(Dashboard)
        self.label_cobot.setObjectName(u"label_cobot")
        self.label_cobot.setGeometry(QRect(340, 20, 120, 30))
        font = QFont()
        font.setPointSize(14)
        self.label_cobot.setFont(font)
        self.label_cobot.setAlignment(Qt.AlignCenter)
        self.label_control_box = QLabel(Dashboard)
        self.label_control_box.setObjectName(u"label_control_box")
        self.label_control_box.setGeometry(QRect(40, 100, 120, 30))
        self.label_control_box.setFont(font)
        self.label_control_box.setAlignment(Qt.AlignCenter)
        self.label_joint_load = QLabel(Dashboard)
        self.label_joint_load.setObjectName(u"label_joint_load")
        self.label_joint_load.setGeometry(QRect(340, 100, 120, 30))
        self.label_joint_load.setFont(font)
        self.label_joint_load.setAlignment(Qt.AlignCenter)
        self.label_payload = QLabel(Dashboard)
        self.label_payload.setObjectName(u"label_payload")
        self.label_payload.setGeometry(QRect(640, 100, 120, 30))
        self.label_payload.setFont(font)
        self.label_payload.setAlignment(Qt.AlignCenter)
        self.label_cobot_param = QLabel(Dashboard)
        self.label_cobot_param.setObjectName(u"label_cobot_param")
        self.label_cobot_param.setGeometry(QRect(340, 50, 120, 30))
        self.label_cobot_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_control_box_param = QLabel(Dashboard)
        self.label_control_box_param.setObjectName(u"label_control_box_param")
        self.label_control_box_param.setGeometry(QRect(40, 130, 120, 90))
        self.label_control_box_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_payload_param = QLabel(Dashboard)
        self.label_payload_param.setObjectName(u"label_payload_param")
        self.label_payload_param.setGeometry(QRect(660, 130, 120, 90))
        self.label_payload_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_base = QLabel(Dashboard)
        self.label_base.setObjectName(u"label_base")
        self.label_base.setGeometry(QRect(160, 140, 120, 30))
        self.label_base.setFont(font)
        self.label_base.setAlignment(Qt.AlignCenter)
        self.label_shoulder = QLabel(Dashboard)
        self.label_shoulder.setObjectName(u"label_shoulder")
        self.label_shoulder.setGeometry(QRect(340, 140, 120, 30))
        self.label_shoulder.setFont(font)
        self.label_shoulder.setAlignment(Qt.AlignCenter)
        self.label_base_param = QLabel(Dashboard)
        self.label_base_param.setObjectName(u"label_base_param")
        self.label_base_param.setGeometry(QRect(160, 170, 120, 120))
        self.label_base_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_shoulder_param = QLabel(Dashboard)
        self.label_shoulder_param.setObjectName(u"label_shoulder_param")
        self.label_shoulder_param.setGeometry(QRect(340, 170, 120, 120))
        self.label_shoulder_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_elbow = QLabel(Dashboard)
        self.label_elbow.setObjectName(u"label_elbow")
        self.label_elbow.setGeometry(QRect(520, 140, 120, 30))
        self.label_elbow.setFont(font)
        self.label_elbow.setAlignment(Qt.AlignCenter)
        self.label_elbow_param = QLabel(Dashboard)
        self.label_elbow_param.setObjectName(u"label_elbow_param")
        self.label_elbow_param.setGeometry(QRect(520, 170, 120, 120))
        self.label_elbow_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_wrist1 = QLabel(Dashboard)
        self.label_wrist1.setObjectName(u"label_wrist1")
        self.label_wrist1.setGeometry(QRect(60, 290, 120, 30))
        self.label_wrist1.setFont(font)
        self.label_wrist1.setAlignment(Qt.AlignCenter)
        self.label_wrist1_param = QLabel(Dashboard)
        self.label_wrist1_param.setObjectName(u"label_wrist1_param")
        self.label_wrist1_param.setGeometry(QRect(60, 320, 120, 150))
        self.label_wrist1_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_wrist2 = QLabel(Dashboard)
        self.label_wrist2.setObjectName(u"label_wrist2")
        self.label_wrist2.setGeometry(QRect(240, 290, 120, 30))
        self.label_wrist2.setFont(font)
        self.label_wrist2.setAlignment(Qt.AlignCenter)
        self.label_wrist2_param = QLabel(Dashboard)
        self.label_wrist2_param.setObjectName(u"label_wrist2_param")
        self.label_wrist2_param.setGeometry(QRect(240, 320, 120, 150))
        self.label_wrist2_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_wrist3 = QLabel(Dashboard)
        self.label_wrist3.setObjectName(u"label_wrist3")
        self.label_wrist3.setGeometry(QRect(420, 290, 120, 30))
        self.label_wrist3.setFont(font)
        self.label_wrist3.setAlignment(Qt.AlignCenter)
        self.label_wrist3_param = QLabel(Dashboard)
        self.label_wrist3_param.setObjectName(u"label_wrist3_param")
        self.label_wrist3_param.setGeometry(QRect(420, 320, 120, 150))
        self.label_wrist3_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.listView_Log = QListView(Dashboard)
        self.listView_Log.setObjectName(u"listView_Log")
        self.listView_Log.setGeometry(QRect(10, 470, 780, 120))
        self.label_tool_param = QLabel(Dashboard)
        self.label_tool_param.setObjectName(u"label_tool_param")
        self.label_tool_param.setGeometry(QRect(600, 320, 120, 150))
        self.label_tool_param.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_tool = QLabel(Dashboard)
        self.label_tool.setObjectName(u"label_tool")
        self.label_tool.setGeometry(QRect(600, 290, 120, 30))
        self.label_tool.setFont(font)
        self.label_tool.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dashboard)

        QMetaObject.connectSlotsByName(Dashboard)

    # setupUi

    def retranslateUi(self, Dashboard):
        Dashboard.setWindowTitle(QCoreApplication.translate("Dashboard", u"Dashboard", None))
        self.pushButton.setText(QCoreApplication.translate("Dashboard", u"Start", None))
        self.label_cobot.setText(QCoreApplication.translate("Dashboard", u"Cobot", None))
        self.label_control_box.setText(QCoreApplication.translate("Dashboard", u"Control Box", None))
        self.label_joint_load.setText(QCoreApplication.translate("Dashboard", u"Joint Load", None))
        self.label_payload.setText(QCoreApplication.translate("Dashboard", u"Payload", None))
        self.label_cobot_param.setText(QCoreApplication.translate("Dashboard", u"ElapsedTime DOUBLE", None))
        self.label_control_box_param.setText(QCoreApplication.translate("Dashboard", u"Temperature DOUBLE\n"
                                                                                     "Voltage DOUBLE", None))
        self.label_payload_param.setText(QCoreApplication.translate("Dashboard", u"Mass DOUBLE\n"
                                                                                 "CoGx DOUBLE\n"
                                                                                 "CoGy DOUBLE\n"
                                                                                 "CoGz DOUBLE", None))
        self.label_base.setText(QCoreApplication.translate("Dashboard", u"Base", None))
        self.label_shoulder.setText(QCoreApplication.translate("Dashboard", u"Shoulder", None))
        self.label_base_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                              "Temperature DOUBLE\n"
                                                                              "Voltage DOUBLE\n"
                                                                              "X DOUBLE\n"
                                                                              "Y DOUBLE\n"
                                                                              "Z DOUBLE", None))
        self.label_shoulder_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                  "Temperature DOUBLE\n"
                                                                                  "Voltage DOUBLE\n"
                                                                                  "X DOUBLE\n"
                                                                                  "Y DOUBLE\n"
                                                                                  "Z DOUBLE", None))
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
                                                                                "Voltage DOUBLE\n"
                                                                                "X DOUBLE\n"
                                                                                "Y DOUBLE\n"
                                                                                "Z DOUBLE", None))
        self.label_wrist2.setText(QCoreApplication.translate("Dashboard", u"Wrist 2", None))
        self.label_wrist2_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                "Temperature DOUBLE\n"
                                                                                "Voltage DOUBLE\n"
                                                                                "X DOUBLE\n"
                                                                                "Y DOUBLE\n"
                                                                                "Z DOUBLE", None))
        self.label_wrist3.setText(QCoreApplication.translate("Dashboard", u"Wrist 3", None))
        self.label_wrist3_param.setText(QCoreApplication.translate("Dashboard", u"Position DOUBLE\n"
                                                                                "Temperature DOUBLE\n"
                                                                                "Voltage DOUBLE\n"
                                                                                "X DOUBLE\n"
                                                                                "Y DOUBLE\n"
                                                                                "Z DOUBLE", None))
        self.label_tool_param.setText(QCoreApplication.translate("Dashboard", u"Temperature DOUBLE\n"
                                                                              "Voltage DOUBLE\n"
                                                                              "X DOUBLE\n"
                                                                              "Y DOUBLE\n"
                                                                              "Z DOUBLE\n"
                                                                              "RX DOUBLE\n"
                                                                              "RY DOUBLE\n"
                                                                              "RZ DOUBLE", None))
        self.label_tool.setText(QCoreApplication.translate("Dashboard", u"Tool", None))
    # retranslateUi
