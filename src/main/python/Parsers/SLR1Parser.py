from src.main.python.Automata.State import State
from src.main.python.Automata.formaters import empty_formatter
from src.main.python.Grammar.Item import Item
from src.main.python.Parsers.ShiftReduceParser import ShiftReduceParser, ShiftReduceParser2, Action
from src.main.python.Parsers.tools import build_LR0_automaton
from src.main.python.Tools.first_follow import compute_firsts, compute_follows
from src.main.python.ll1 import is_register


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        grammar = self.grammar.AugmentedGrammar(True)
        firsts = compute_firsts(grammar)
        follows = compute_follows(grammar, firsts)

        automaton = build_LR0_automaton(grammar).to_deterministic(empty_formatter)
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


class SLR1Parser2(ShiftReduceParser2):
    def build_LR0_automaton(self):
        G = self.augmentedG = self.G.AugmentedGrammar(True)

        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0)

        automaton = State(start_item, True)

        pending = [start_item]
        visited = {start_item: automaton}

        while pending:
            current_item = pending.pop()
            if current_item.IsReduceItem:
                continue

            # (Decide which transitions to add)
            next_symbol = current_item.NextSymbol

            next_item = current_item.NextItem()
            if not next_item in visited:
                pending.append(next_item)
                visited[next_item] = State(next_item, True)

            if next_symbol.IsNonTerminal:
                for prod in next_symbol.productions:
                    next_item = Item(prod, 0)
                    if not next_item in visited:
                        pending.append(next_item)
                        visited[next_item] = State(next_item, True)

            current_state = visited[current_item]

            # (Add the decided transitions)
            current_state.add_transition(next_symbol.Name, visited[current_item.NextItem()])

            if next_symbol.IsNonTerminal:
                for prod in next_symbol.productions:
                    current_state.add_epsilon_transition(visited[Item(prod, 0)])

        self.automaton = automaton.to_deterministic(empty_formatter)

    def _build_parsing_table(self):
        self.is_slr1 = True
        self.build_LR0_automaton()

        firsts = compute_firsts(self.augmentedG)
        follows = compute_follows(self.augmentedG, firsts)

        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, node)
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for state in node.state:
                item = state.state

                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == self.augmentedG.startSymbol:
                        self.is_slr1 &= is_register(self.action, idx, self.augmentedG.EOF,
                                                               Action((Action.OK, '')))
                    else:
                        for symbol in follows[prod.Left]:
                            self.is_slr1 &= is_register(self.action, idx, symbol,
                                                                   Action((Action.REDUCE, prod)))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_slr1 &= is_register(self.action, idx, next_symbol,
                                                               Action((Action.SHIFT, node[next_symbol.Name][0].idx)))
                    else:
                        self.is_slr1 &= is_register(self.goto, idx, next_symbol,
                                                               node[next_symbol.Name][0].idx)
