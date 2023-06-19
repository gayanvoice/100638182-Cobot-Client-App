import sys
from PySide6.QtWidgets import QWidget

from ui.ui_dashboard import UiDashboard


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiDashboard()
        self.ui.setupUi(self)
