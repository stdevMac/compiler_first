from src.main.python.Grammar.Sentence import Sentence
from src.main.python.Grammar.Terminal import Terminal


class Epsilon(Terminal, Sentence):

    def __init__(self, grammar):
        super().__init__('epsilon', grammar)
        self._symbols = []

    def __str__(self):
        return "Epsilon"

    def __repr__(self):
        return 'epsilon'

    def __iter__(self):
        yield from ()

    def __len__(self):
        return 0

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    @property
    def IsEpsilon(self):
        return True
