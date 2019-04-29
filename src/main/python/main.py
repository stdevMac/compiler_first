from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QPushButton, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QMainWindow)
import sys


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Primer Proyecto de Compilación'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.showMaximized()
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


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
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Gramática")
        self.tabs.addTab(self.tab2, "Resultados")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.textBox = QTextEdit()
        self.textBox.setPlainText("Twinkle, twinkle, little star,\n"
                                  "How I wonder what you are.\n"
                                  "Up above the world so high,\n"
                                  "Like a diamond in the sky.\n"
                                  "Twinkle, twinkle, little star,\n"
                                  "How I wonder what you are!\n")
        self.button = QPushButton('PyQt5 button', self)
        self.button.setToolTip('This is an example button')
        self.button.move(100, 70)
        self.button.clicked.connect(self.on_click_button)

        self.tab1.layout.addWidget(self.textBox)
        self.tab1.layout.addWidget(self.button)
        self.tab1.setLayout(self.tab1.layout)

        # self.setWindowState(Qt.WindowMaximized)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click_button(self):
        print('PyQt5 button click')
        self.tabs.setCurrentIndex(1)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
