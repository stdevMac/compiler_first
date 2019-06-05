from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QTextEdit)

from src.main.python import tools, first_follow


# from src.main.python.GrammarWrapper import GrammarWrapper


class ShowResults(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.resize(1028, 720)

        s = QFont('SansSerif', 25)
        self.setFont(s)
        # self.wrapper = GrammarWrapper()

        # Initialize tab screen
        self.grammar_label = QLabel('Gramatica')
        self.grammar = QTextEdit()
        self.first_label = QLabel('First')
        self.first = QTextEdit()
        self.follow_label = QLabel('First')
        self.follow = QTextEdit()
        # # Add tabs to widget
        self.layout.addWidget(self.grammar_label)
        self.layout.addWidget(self.first_label)
        self.layout.addWidget(self.follow_label)
        self.layout.addWidget(self.grammar)
        self.layout.addWidget(self.first)
        self.layout.addWidget(self.follow)
        self.setLayout(self.layout)

    def compute_options(self, code):
        tokens = tools.tokenize(code)
        grammar = tools.grammar_from_tokens(tokens)

        first, follow = first_follow.compute_first_follow(grammar)
        self.first.setPlainText(str(first))
        self.follow.setPlainText(str(follow))
        self.grammar.setPlainText(str(grammar))
