from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel)

from src.main.python.GrammarWrapper import GrammarWrapper


class ShowResults(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.resize(1028, 720)

        s = QFont('SansSerif', 25)
        self.setFont(s)
        self.wrapper = GrammarWrapper()

        # Initialize tab screen
        self.tabs = QLabel('Alguna Etiqueta')
        self.tags = QLabel('Otra Etiqueta')

        # # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.tags)
        self.setLayout(self.layout)
