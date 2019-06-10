from src.main.python.Automata.formaters import empty_formatter
from src.main.python.Parsers.ShiftReduceParser import ShiftReduceParser
from src.main.python.Parsers.tools import build_LR0_automaton
from src.main.python.Tools.first_follow import compute_firsts, compute_follows
from src.main.python.ll1 import is_register


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        grammar = self.grammar.AugmentedGrammar(True)
        firsts = compute_firsts(grammar)
        follows = compute_follows(grammar, firsts)

        automaton = build_LR0_automaton(grammar).to_deterministic(empty_formatter)

        assert automaton.recognize('E')
        assert automaton.recognize('T*F')
        assert automaton.recognize(['E', '+', 'int'])
        assert not automaton.recognize('E*F')

        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, node)
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state

                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == grammar.startSymbol:
                        is_register(self.action, idx, grammar.EOF, (ShiftReduceParser.OK, ''))
                    else:
                        for symbol in follows[prod.Left]:
                            is_register(self.action, idx, symbol, (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        is_register(self.action, idx, next_symbol,
                                    (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        is_register(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)
