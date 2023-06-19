import json
import logging
import sys
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from model.base_model import BaseModel
from model.cobot_model import CobotModel
from model.control_box_model import ControlBoxModel
from model.elbow_model import ElbowModel
from model.payload_model import PayloadModel
from model.rtdl_dt_model import RtdlDtModel
from model.rtdl_model import RtdlModel
from model.wrist1_model import Wrist1Model
from model.wrist2_model import Wrist2Model
from model.wrist3_model import Wrist3Model
from twin_writer import TwinWriter
from ui.dashboard import Dashboard
from PySide6.QtWidgets import QApplication


def run_dashboard():
    app = QApplication(sys.argv)
    widget = Dashboard()
    widget.show()
    sys.exit(app.exec())


def run_robot(host, port, config, frequency):
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

    keep_running = True
    while keep_running:
        try:
            state = rtde_connection.receive()
            if state is not None:
                data_row = twin_writer.get_data_row(state)
                rtdl_model = RtdlModel.get_from_rows(header_row, data_row)
                rtdl_dt_model = RtdlDtModel.get_from_rtdl_model(rtdl_model)
                print("".join(str(json.dumps(rtdl_dt_model.cobot_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.control_box_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.payload_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.base_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.shoulder_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.elbow_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.wrist1_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.wrist2_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.wrist3_model.__dict__))))
                print("".join(str(json.dumps(rtdl_dt_model.tool_model.__dict__))))

        except KeyboardInterrupt:
            keep_running = False
        except rtde.RTDEException:
            rtde_connection.disconnect()
            sys.exit()

    sys.stdout.write("\rComplete!\n")

    rtde_connection.send_pause()
    rtde_connection.disconnect()

if __name__ == '__main__':
    run_robot("localhost", 30004, "configuration.xml", 1)
    # run_dashboard()
