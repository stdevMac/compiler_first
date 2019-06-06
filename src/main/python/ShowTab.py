from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QTextEdit, QScrollArea)

from src.main.python import ll1
from src.main.python.Tools import Tokenizer, first_follow

# from src.main.python.GrammarWrapper import GrammarWrapper
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
        self.grammar_label = QLabel('Gramatica')
        self.grammar = QTextEdit()
        self.first_label = QLabel('First')
        self.first = QTextEdit()
        self.follow_label = QLabel('Follow')
        self.follow = QTextEdit()
        self.ll1_label = QLabel('Es LL1?')
        self.ll1 = QTextEdit()
        self.ll1_table_label = QLabel('Tabla LL1')
        self.ll1_table = QTextEdit()
        self.grammar_without_left_recursion_label = QLabel('Quitar la recursion Izquierda')
        self.grammar_without_left_recursion = QTextEdit()
        self.grammar_reduced_label = QLabel('Gramatica reducidad')
        self.grammar_reduced = QTextEdit()

        # Add tabs to widget
        scroll_layout.addWidget(self.grammar_label)
        scroll_layout.addWidget(self.grammar)
        scroll_layout.addWidget(self.first_label)
        scroll_layout.addWidget(self.first)
        scroll_layout.addWidget(self.follow_label)
        scroll_layout.addWidget(self.follow)
        scroll_layout.addWidget(self.ll1_label)
        scroll_layout.addWidget(self.ll1)
        scroll_layout.addWidget(self.ll1_table_label)
        scroll_layout.addWidget(self.ll1_table)
        scroll_layout.addWidget(self.grammar_without_left_recursion_label)
        scroll_layout.addWidget(self.grammar_without_left_recursion)
        scroll_layout.addWidget(self.grammar_reduced_label)
        scroll_layout.addWidget(self.grammar_reduced)
        self.scroll.setWidget(scroll_content)
        self.setLayout(self.layout)

    def compute_options(self, code):
        tokens = Tokenizer.tokenize(code)
        grammar = Tokenizer.grammar_from_tokens(tokens)

        first, follow = first_follow.compute_first_follow(grammar)

        ll1_table, is_ll1 = ll1.build_ll1_table(grammar, first, follow)

        self.first.setPlainText(str(first))

        self.ll1.setPlainText(str(is_ll1))
        self.ll1_table.setPlainText(str(ll1_table))
        self.ll1_table.show()
        if not is_ll1:
            self.ll1_table.setPlainText(str(ll1_table))
            self.ll1_table.hide()
            self.ll1_table_label.hide()
        grammar_without_common_prefixes = grammar.copy()
        rm_common_prefix(grammar_without_common_prefixes)
        grammar_without_immediate_left_recursion = grammar.copy()
        rm_immediate_left_recursion(grammar_without_immediate_left_recursion)
        self.grammar_reduced.setPlainText(str(grammar_without_common_prefixes))
        self.grammar_without_left_recursion.setPlainText(str(grammar_without_immediate_left_recursion))
        self.first.setPlainText(str(first))
        self.follow.setPlainText(str(follow))
        self.grammar.setPlainText(str(grammar))
