from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QPushButton, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QFileDialog, QLabel)


class ShowTable(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.resize(1028, 720)

        s = QFont('SansSerif', 25)
        self.setFont(s)

        # Initialize tab screen
        self.tabs = QLabel('Alguna Etiqueta')
        self.tags = QLabel('Otra Etiqueta')
        # self.tab1 = QWidget()
        # self.tab2 = QWidget()
        # self.tabs.resize(300, 200)
        #
        # # Add tabs
        # self.tabs.addTab(self.tab1, "Gramática")
        # self.tabs.addTab(self.tab2, "Resultados")
        #
        # # Create first tab
        # self.tab1.layout = QVBoxLayout(self)
        # self.textBox = QTextEdit()
        # self.textBox.setPlainText("Twinkle, twinkle, little star,\n"
        #                           "How I wonder what you are.\n"
        #                           "Up above the world so high,\n"
        #                           "Like a diamond in the sky.\n"
        #                           "Twinkle, twinkle, little star,\n"
        #                           "How I wonder what you are!\n")
        # self.button = QPushButton('Computar', self)
        # self.button.setToolTip('This is an example button')
        # self.button.move(100, 70)
        # self.button.clicked.connect(self.on_click_button)
        # self.load = QPushButton('Cargar Archivo', self)
        # self.load.setToolTip('Carga un archivo .grm')
        # self.load.move(100, 70)
        # self.load.clicked.connect(self.file_open)
        #
        # self.tab1.layout.addWidget(self.textBox)
        # self.tab1.layout.addWidget(self.button)
        # self.tab1.layout.addWidget(self.load)
        # self.tab1.setLayout(self.tab1.layout)
        #
        # # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.tags)
        self.setLayout(self.layout)

    @pyqtSlot()
    def file_open(self):
        name = QFileDialog.getOpenFileName(self, 'Open File', filter="grm(*.grm)")
        file = open(name[0], 'r')

        with file:
            text = file.read()
            self.textBox.setPlainText(text)

    @pyqtSlot()
    def on_click_button(self):
        print('PyQt5 button click')
        print(self.textBox.toPlainText())
        self.tabs.setCurrentIndex(1)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
