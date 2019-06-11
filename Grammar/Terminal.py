from Grammar.Sentence import Symbol


class Terminal(Symbol):

    def __init__(self, name, grammar):
        super().__init__(name, grammar)

    @property
    def IsTerminal(self):
        return True

    @property
    def IsNonTerminal(self):
        return False

    @property
    def IsEpsilon(self):
        return True if self.Name == 'Epsilon' else False
