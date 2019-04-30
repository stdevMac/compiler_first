import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from src.main.python.MyTableWidget import MyTableWidget


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
