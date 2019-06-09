class Item:

    def __init__(self, production, pos, lookaheads=[]):
        self.production = production
        self.pos = pos
        self.look_a_heads = tuple(look for look in lookaheads)

    def __str__(self):
        s = str(self.production.Left) + " -> "
        if len(self.production.Right) > 0:
            for i,c in enumerate(self.production.Right):
                if i == self.pos:
                    s += "."
                s += str(self.production.Right[i])
            if self.pos == len(self.production.Right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.look_a_heads)
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            (self.pos == other.pos) and
            (self.production == other.production) and
            (self.look_a_heads == other.lookaheads)
        )

    def __hash__(self):
        return hash((self.production,self.pos,self.look_a_heads))

    @property
    def IsReduceItem(self):
        return len(self.production.Right) == self.pos

    @property
    def NextSymbol(self):
        if self.pos < len(self.production.Right):
            return self.production.Right[self.pos]
        else:
            return None

    def NextItem(self):
        if self.pos < len(self.production.Right):
            return Item(self.production, self.pos + 1, self.look_a_heads)
        else:
            return None
