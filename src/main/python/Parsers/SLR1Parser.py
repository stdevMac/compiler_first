from src.main.python.Parsers.ShiftReduceParser import ShiftReduceParser
from src.main.python.Parsers.tools import build_LR0_automaton
from src.main.python.Tools.first_follow import compute_firsts, compute_follows


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, node)
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == G.startSymbol:
                        SLR1Parser._register(self.action, (idx, G.EOF), (ShiftReduceParser.OK, None))
                    else:
                        for symbol in follows[prod.Left]:
                            SLR1Parser._register(self.action, (idx, symbol), (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        SLR1Parser._register(self.action, (idx, next_symbol),
                                             (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        SLR1Parser._register(self.goto, (idx, next_symbol), node[next_symbol.Name][0].idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value