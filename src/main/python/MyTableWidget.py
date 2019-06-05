from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QPushButton, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QFileDialog)

from src.main.python.ShowTab import ShowResults


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.resize(1028, 720)

        s = QFont('SansSerif', 25)
        self.setFont(s)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = ShowResults(self)
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Gramática")
        self.tabs.addTab(self.tab2, "Resultados")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.textBox = QTextEdit()
        self.textBox.setPlainText("Inserte su gramática")
        self.button = QPushButton('Computar', self)
        self.button.setToolTip('This is an example button')
        self.button.move(100, 70)
        self.button.clicked.connect(self.compute_button)
        self.load = QPushButton('Cargar Archivo', self)
        self.load.setToolTip('Carga un archivo .grm')
        self.load.move(100, 70)
        self.load.clicked.connect(self.file_open_button)

        self.tab1.layout.addWidget(self.textBox)
        self.tab1.layout.addWidget(self.button)
        self.tab1.layout.addWidget(self.load)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def file_open_button(self):
        name = QFileDialog.getOpenFileName(self, 'Open File', filter="grm(*.grm)")
        file = open(name[0], 'r')

        with file:
            text = file.read()
            self.textBox.setPlainText(text)

    @pyqtSlot()
    def compute_button(self):
        print('Compute button clicked')
        print(self.textBox.toPlainText())
        self.tab2.compute_options(self.textBox.toPlainText())
        self.tabs.setCurrentIndex(1)
