import logging
import sys
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from model.base_model import BaseModel
from model.rtdl_model import RtdlModel
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
                base_model = BaseModel.get_from_rtdl_model(rtdl_model)

                # print("\n".join(str(x) for x in data_row))
                print("".join(str(base_model.position)))

        except KeyboardInterrupt:
            keep_running = False
        except rtde.RTDEException:
            rtde_connection.disconnect()
            sys.exit()

    sys.stdout.write("\rComplete!\n")

    rtde_connection.send_pause()
    rtde_connection.disconnect()


if __name__ == '__main__':
    run_robot("localhost", 30004, "configuration.xml", 2)
    # run_dashboard()
