from src.main.python.Grammar.Sentence import Sentence
from src.main.python.Grammar.Terminal import Terminal


class Epsilon(Terminal, Sentence):

    def __init__(self, grammar):
        super().__init__('Epsilon', grammar)
        self._symbols = [self]

    def __str__(self):
        return 'Epsilon'

    def __repr__(self):
        return 'Epsilon'

    def __iter__(self):
        yield from ()

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    def __getitem__(self, index):
        return self._symbols[index]

    @property
    def IsEpsilon(self):
        return True


class FakeEpsilon(Terminal, Sentence):

    def __init__(self, grammar):
        super().__init__('Epsilon', grammar)
        self._symbols = [self]

    def __str__(self):
        return 'Epsilon'

    def __repr__(self):
        return 'Epsilon'

    def __iter__(self):
        yield from ()

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    def __getitem__(self, index):
        return self._symbols[index]

    @property
    def IsEpsilon(self):
        return False

