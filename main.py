import sys

import control
import cobot_control_async
from cloud import cobot_control
from cloud import cobot

from ui.dashboard import Dashboard
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # widget = Dashboard()
    # widget.show()
    # sys.exit(app.exec())
    # cobot_control_async.run()
    cobot_control.run()
    # control.run()
    # cobot.run()
