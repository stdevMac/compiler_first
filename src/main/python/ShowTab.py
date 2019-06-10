import pydot
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QTextEdit, QScrollArea)

from src.main.python import ll1
from src.main.python.Automata.State import State
from src.main.python.Grammar import Grammar
from src.main.python.Parsers.LR1Parser import LR1Parser
from src.main.python.Parsers.SLR1Parser import SLR1Parser
from src.main.python.Regex.Regex import regexp_from_automaton
from src.main.python.Tools import Tokenizer, first_follow

from src.main.python.Tools.RemoveCommonPrefix import rm_common_prefix
from src.main.python.Tools.RemoveImmediateLeftRecursion import rm_immediate_left_recursion
from src.main.python.Tools.Tokenizer import tokenize_input
from src.main.python.Tools.first_follow import build_parsing_table, method_predicted_non_recursive
from src.main.python.Tools.printer import pprint
from copy import deepcopy


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
        self.lr_graph_label = QLabel()
        self.lr1_graph_label = QLabel()
        self.slr1_graph_label = QLabel()
        self.image = None
        scroll_layout.addWidget(self.all_info)
        self.scroll.setWidget(scroll_content)
        self.setLayout(self.layout)

    @staticmethod
    def run_pipeline(tokens, parser):
        try:
            left_parse = parser(tokens)
        except Exception as error:
            left_parse = str(error)

        return left_parse

    @staticmethod
    def full_run_pipeline(grammar: Grammar, code, parser):
        info = ''
        if len(code) > 0:
            for line in str.split(code, '\n'):
                if len(line) == 0:
                    continue
                tokens = tokenize_input(line, grammar)
                output, productions = parser(tokens)
                if output is not None and productions is not None:
                    info += pprint(output, f'Parse para cadena -> {line}:') + '\n\n'

        return info

    @staticmethod
    def show_automaton(automaton: State, label: str, widget: QLabel, image_tag: str):
        try:
            import pygraphviz as pgv
            dot = automaton.graph()

            (graph,) = pydot.graph_from_dot_data(str(dot))
            graph.set_label(label)
            gr = pgv.AGraph().from_string(str(graph))
            gr.layout()
            gr.draw(image_tag)
            pix_map = QPixmap(image_tag)
            widget.setPixmap(pix_map)
            widget.show()
        except:
            return

    def compute_options(self, code, strings):
        if len(code) == 0:
            return
        tokens = Tokenizer.tokenize(code)
        grammar = Tokenizer.grammar_from_tokens(tokens)

        first, follow = first_follow.compute_first_follow(grammar)

        ll1_table, is_ll1 = ll1.build_ll1_table(grammar, first, follow)
        info = pprint(str(grammar), 'Gramatica:') + '\n\n'

        info += pprint(first, 'First:') + '\n\n'
        info += pprint(follow, 'Follow:') + '\n\n'
        info += pprint(str(is_ll1), 'Es LL1') + '\n\n'
        if is_ll1:
            info += pprint(ll1_table, 'Tabla ll1: ') + '\n\n'

            parsing_table = build_parsing_table(grammar, first, follow)
            parser = method_predicted_non_recursive(grammar, M=parsing_table)

            try:
                dfa = grammar.DFA()
                states = State.from_nfa(dfa, True)
                regex = regexp_from_automaton(states[1], grammar.terminals)
                info += pprint(str(True), 'Gramatica Regular: ') + '\n\n'
                info += pprint(regex, 'Expresion Regular Asociada: ') + '\n\n'
                try:
                    import pygraphviz as pgv
                    dot = states[0].graph()

                    (graph, ) = pydot.graph_from_dot_data(str(dot))
                    graph.set_label('Automata expresion Regular Asociada')
                    gr = pgv.AGraph().from_string(str(graph))
                    gr.layout()
                    gr.draw('graph.png')
                    self.image = QPixmap('graph.png')
                    self.lr_graph_label.setPixmap(self.image)
                    self.lr_graph_label.show()
                except:
                    info += 'No es posible mostrar el automata...Error' + '\n\n'

            except:
                info += pprint(str(False), 'Gramatica Regular: ') + '\n\n'

            if len(strings) > 0:
                for line in str.split(strings, '\n'):
                    if len(line) == 0:
                        continue
                    left_parse = self.run_pipeline(tokenize_input(line), parser)
                    print('Left parser')
                    print(left_parse)
                    info += pprint(left_parse, f'Parse para cadena -> {line}:') + '\n\n'

        parser_lr1 = LR1Parser(grammar, verbose=True)
        parser_slr1 = SLR1Parser(grammar, verbose=True)

        if parser_slr1.is_slr1:
            info += 'La Gramatica es SLR(1):' + '\n\n'
            info += pprint(parser_slr1.action, 'Tabla de Actions:') + '\n\n'
            info += pprint(parser_slr1.goto, 'Tabla de Goto:') + '\n\n'
            info += self.full_run_pipeline(grammar, strings, parser_slr1)
            self.show_automaton(parser_slr1.automaton, 'Automata SLR1', self.slr1_graph_label, 'slr.png')
        else:
            info += pprint(str(False), 'La Gramatica no es SLR(1):') + '\n\n'

        if parser_lr1.is_lr1:
            info += 'La Gramatica es LR(1):' + '\n\n'
            info += pprint(parser_lr1.action, 'Tabla de Actions:') + '\n\n'
            info += pprint(parser_lr1.goto, 'Tabla de Goto:') + '\n\n'
            info += self.full_run_pipeline(grammar, strings, parser_lr1)
            self.show_automaton(parser_lr1.automaton, 'Automata LR1', self.lr1_graph_label, 'lr.png')
        else:
            info += pprint(str(False), 'La Gramatica no es LR(1):') + '\n\n'

        grammar_without_common_prefixes = deepcopy(grammar)
        rm_common_prefix(grammar_without_common_prefixes)
        grammar_without_immediate_left_recursion = deepcopy(grammar)
        rm_immediate_left_recursion(grammar_without_immediate_left_recursion)
        info += pprint(str(grammar_without_common_prefixes), 'Gramatica sin prefijos comunes:') + '\n\n'
        info += pprint(str(grammar_without_immediate_left_recursion),
                       'Gramatica sin recursion inmediata izquierda:') + '\n\n'

        self.all_info.setPlainText(info)
        self.all_info.setReadOnly(True)
