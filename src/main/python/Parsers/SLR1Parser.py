from src.main.python.Automata.formaters import empty_formatter
from src.main.python.Parsers.ShiftReduceParser import ShiftReduceParser
from src.main.python.Parsers.tools import build_LR0_automaton
from src.main.python.Tools.first_follow import compute_firsts, compute_follows
from src.main.python.ll1 import is_register


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        self.is_slr1 = True
        grammar = self.grammar.AugmentedGrammar(True)
        firsts = compute_firsts(grammar)
        follows = compute_follows(grammar, firsts)

        self.automaton = build_LR0_automaton(grammar).to_deterministic(empty_formatter)

        for i, node in enumerate(self.automaton):
            if self.verbose:
                print(i, node)
            node.idx = i

        for node in self.automaton:
            idx = node.idx
            for state in node.state:
                item = state.state

                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == grammar.startSymbol:
                        self.is_slr1 &= is_register(self.action, idx, grammar.EOF, (ShiftReduceParser.OK, ''))
                    else:
                        for symbol in follows[prod.Left]:
                            self.is_slr1 &= is_register(self.action, idx, symbol, (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_slr1 &= is_register(self.action, idx, next_symbol,
                                                    (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        self.is_slr1 &= is_register(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)
