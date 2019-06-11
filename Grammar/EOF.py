from Grammar.Terminal import Terminal


class EOF(Terminal):

    def __init__(self, grammar):
        super().__init__('$', grammar)
