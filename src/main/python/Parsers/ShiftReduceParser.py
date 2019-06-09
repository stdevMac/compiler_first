class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, grammar, verbose=False):
        self.grammar = grammar
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []

        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose:
                print(stack, w[cursor:])

            # Your code here!!! (Detect error)
            try:
                action, tag = self.action[state][lookahead][0]
                # Your code here!!! (Shift case)
                if action == ShiftReduceParser.SHIFT:
                    stack.append(tag)
                    cursor += 1
                # Your code here!!! (Reduce case)
                elif action == ShiftReduceParser.REDUCE:
                    for _ in range(len(tag.Right)):
                        stack.pop()
                    stack.append(self.goto[stack[-1], tag.Left])
                    output.append(tag)
                # Your code here!!! (OK case)
                elif action == ShiftReduceParser.OK:
                    output.reverse()
                    return output
                # Your code here!!! (Invalid case)
                else:
                    assert False, 'Must be something wrong!'
            except KeyError:
                return None


class Action(tuple):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __str__(self):
        try:
            action, tag = self
            return f"{'S' if action == Action.SHIFT else 'OK' if action == Action.OK else ''}{tag}"
        except:
            return str(tuple(self))

    __repr__ = __str__


class ShiftReduceParser2:
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []

        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, w[cursor:])

            # (Detect error)
            try:
                action, tag = self.action[state][lookahead][0]
                # (Shift case)
                if action == Action.SHIFT:
                    stack.append(tag)
                    cursor += 1
                # (Reduce case)
                elif action == Action.REDUCE:
                    for _ in range(len(tag.Right)): stack.pop()
                    stack.append(self.goto[stack[-1]][tag.Left][0])
                    output.append(tag)
                # (OK case)
                elif action == Action.OK:
                    output.reverse()
                    return output
                # (Invalid case)
                else:
                    assert False, 'Must be something wrong!'
            except KeyError:
                return None