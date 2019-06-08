from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QTextEdit, QScrollArea)

from src.main.python import ll1
from src.main.python.Tools import Tokenizer, first_follow

from src.main.python.Tools.RemoveCommonPrefix import rm_common_prefix
from src.main.python.Tools.RemoveImmediateLeftRecursion import rm_immediate_left_recursion
from src.main.python.Tools.printer import pprint


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
        info = pprint(str(grammar), 'Gramatica:') + '\n\n'
        # 'Gramatica: \n' + str(grammar) + '\n\n'
        info += pprint(first, 'First:') + '\n\n'
        info += pprint(follow, 'Follow:') + '\n\n'
        info += pprint(str(is_ll1), 'Es LL1') + '\n\n'
        if is_ll1:
            info += pprint(ll1_table, 'Tabla ll1: ') + '\n\n'

        grammar_without_common_prefixes = grammar.copy()
        rm_common_prefix(grammar_without_common_prefixes)
        grammar_without_immediate_left_recursion = grammar.copy()
        rm_immediate_left_recursion(grammar_without_immediate_left_recursion)
        info += pprint(str(grammar_without_common_prefixes), 'Gramatica sin prefijos comunes:') + '\n\n'
        info += pprint(str(grammar_without_immediate_left_recursion),
                       'Gramatica sin recursion inmediata izquierda:') + '\n\n'
        self.all_info.setPlainText(info)
        self.all_info.setReadOnly(True)
