from src.main.python.Parsers.ShiftReduceParser import ShiftReduceParser
from src.main.python.Parsers.tools import build_lr1_automaton
from src.main.python.ll1 import is_register


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        self.is_lr1 = True

        grammar = self.grammar.AugmentedGrammar(True)

        automaton = build_lr1_automaton(grammar)
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:

                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == grammar.startSymbol:
                        self.is_lr1 &= is_register(self.action, idx, grammar.EOF, (ShiftReduceParser.OK, ''))
                    else:
                        for lookahead in item.lookaheads:
                            self.is_lr1 &= is_register(self.action, idx, lookahead, (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal and not next_symbol.IsEpsilon:
                        try:
                            self.is_lr1 &= is_register(self.action, idx, next_symbol,
                                                   (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                        except:
                            self.is_lr1 = False
                    else:
                        if not next_symbol.IsEpsilon:
                            self.is_lr1 &= is_register(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)
                pass

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
