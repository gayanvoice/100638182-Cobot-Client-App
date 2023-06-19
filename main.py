import sys
from ui.dashboard import Dashboard
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Dashboard()
    widget.show()
    sys.exit(app.exec())
