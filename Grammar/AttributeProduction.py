from Grammar.Production import Production
from Grammar.Sentence import Sentence, Symbol


class AttributeProduction(Production):

    def __init__(self, nonTerminal, sentence, attributes):
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super(AttributeProduction, self).__init__(nonTerminal, sentence)

        self.attributes = attributes

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon

    # sintetizar en ingles??????, pending aggrement
    def syntetice(self):
        pass
