from src.main.python.Grammar.AttributeProduction import AttributeProduction
from src.main.python.Grammar.Production import Production
from src.main.python.Grammar.Sentence import Sentence, SentenceList, Symbol


class NonTerminal(Symbol):

    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.productions = []

    def __imod__(self, other):

        if isinstance(other, Sentence):
            p = Production(self, other)
            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, tuple):
            assert len(other) > 1

            if len(other) == 2:
                other += (None,) * len(other[0])

            assert len(other) == len(other[0]) + 2, \
                "Debe definirse una, y solo una, regla por cada símbolo de la producción"

            if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
                p = AttributeProduction(self, other[0], other[1:])
            else:
                raise Exception("")

            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, Symbol):
            p = Production(self, Sentence(other))
            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, SentenceList):

            for s in other:
                p = Production(self, s)
                self.Grammar.Add_Production(p)

            return self

        raise TypeError(other)

    @property
    def IsTerminal(self):
        return False

    @property
    def IsNonTerminal(self):
        return True

    @property
    def IsEpsilon(self):
        return False
