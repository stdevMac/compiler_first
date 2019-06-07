from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QTextEdit, QScrollArea)

from src.main.python import ll1
from src.main.python.Tools import Tokenizer, first_follow

from src.main.python.Tools.RemoveCommonPrefix import rm_common_prefix
from src.main.python.Tools.RemoveImmediateLeftRecursion import rm_immediate_left_recursion


class ShowResults(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.resize(1028, 720)

        s = QFont('SansSerif', 25)
        self.setFont(s)

        self.scroll = QScrollArea(self)

        self.layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        scroll_content = QWidget(self.scroll)

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        # Initialize tab screen
        self.all_info = QTextEdit()

        # Add widgets
        scroll_layout.addWidget(self.all_info)
        self.scroll.setWidget(scroll_content)
        self.setLayout(self.layout)

    def compute_options(self, code):
        tokens = Tokenizer.tokenize(code)
        grammar = Tokenizer.grammar_from_tokens(tokens)

        first, follow = first_follow.compute_first_follow(grammar)

        ll1_table, is_ll1 = ll1.build_ll1_table(grammar, first, follow)
        info = 'First: \n'
        info += str(first) + '\n\n'
        info += 'Follow: \n' + str(follow) + '\n\n'
        info += 'Gramatica: \n' + str(grammar) + '\n\n'
        info += 'll1: \n' + str(is_ll1) + '\n\n'
        info += 'Tabla ll1: \n' + str(ll1_table) + '\n\n'

        grammar_without_common_prefixes = grammar.copy()
        rm_common_prefix(grammar_without_common_prefixes)
        grammar_without_immediate_left_recursion = grammar.copy()
        rm_immediate_left_recursion(grammar_without_immediate_left_recursion)
        info += 'Gramatica sin prefijos comunes: \n' + str(grammar_without_common_prefixes) + '\n\n'
        info += 'Gramatica sin recursion inmediata izquierda: \n' \
                + str(grammar_without_immediate_left_recursion) + '\n\n'
        self.all_info.setPlainText(info)
        self.all_info.setReadOnly(True)
