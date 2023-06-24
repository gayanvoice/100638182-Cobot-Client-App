import sys

import control
import control_async

from ui.dashboard import Dashboard
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # widget = Dashboard()
    # widget.show()
    # sys.exit(app.exec())
    control_async.run()
    # control.run()
