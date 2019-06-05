from src.main.python.automaton.NFA import NFA


class DFA(NFA):

    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)

        transitions = {key: [value] for key, value in transitions.items()}
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start

    def epsilon_transitions(self):
        raise TypeError()

    def _move(self, symbol):
        self.current = self.transitions[self.current][symbol][0]

    def _reset(self):
        self.current = self.start

    def recognize(self, string):
        self._reset()
        for symbol in string:
            try:
                self._move(symbol)
            except KeyError:
                return False

        return self.current in self.finals
