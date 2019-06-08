import pydot

from src.main.python.Grammar.ContainerSet import ContainerSet


class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = {state: {} for state in range(states)}

        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)

        self.vocabulary.discard('')

    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass


nfa = NFA(states=3, finals=[2], transitions={
    (0, 'a'): [0],
    (0, 'b'): [0, 1],
    (1, 'a'): [2]
})


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
        for i in range(len(string)):
            try:
                self._move(string[i])
            except:
                return False

        return self.current in self.finals


automaton = DFA(states=3, finals=[2], transitions={
    (0, 'a'): 0,
    (0, 'b'): 1,
    (1, 'a'): 2,
    (1, 'b'): 1,
    (2, 'a'): 0,
    (2, 'b'): 1,
})

assert automaton.recognize('ba')
assert automaton.recognize('aababbaba')

assert not automaton.recognize('')
assert not automaton.recognize('aabaa')
assert not automaton.recognize('aababb')

automaton = NFA(states=6, finals=[3, 5], transitions={
    (0, ''): [ 1, 2 ],
    (1, ''): [ 3 ],
    (1,'b'): [ 4 ],
    (2,'a'): [ 4 ],
    (3,'c'): [ 3 ],
    (4, ''): [ 5 ],
    (5,'d'): [ 5 ]
})

def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            moves.update(automaton.transitions[state][symbol])
        except:
            pass
    return moves

assert move(automaton, [1], 'a') == set()
assert move(automaton, [2], 'a') == {4}
assert move(automaton, [1, 5], 'd') == {5}


def epsilon_closure(automaton, states):
    pending = [s for s in states]  # equivalente a list(states) pero me gusta así :p
    closure = {s for s in states}  # equivalente a  set(states) pero me gusta así :p

    while pending:
        state = pending.pop()
        for trans in automaton.epsilon_transitions(state):
            if not trans in closure:
                pending.append(trans)
                closure.add(trans)

    return ContainerSet(*closure)


assert epsilon_closure(automaton, [0]) == {0, 1, 2, 3}
assert epsilon_closure(automaton, [0, 4]) == {0, 1, 2, 3, 4, 5}
assert epsilon_closure(automaton, [1, 2, 4]) == {1, 2, 3, 4, 5}


def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [start]

    pending = [start]
    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            trans = epsilon_closure(automaton, move(automaton, state, symbol))

            if not trans:
                continue

            for s in states:
                if trans == s:
                    trans = s
                    break
            else:
                trans.id = len(states)
                trans.is_final = any(s in automaton.finals for s in trans)
                states.append(trans)
                pending.append(trans)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = trans.id

    finals = [state.id for state in states if state.is_final]
    dfa = DFA(len(states), finals, transitions)
    return dfa

dfa = nfa_to_dfa(automaton)

assert dfa.states == 4
assert len(dfa.finals) == 4

assert dfa.recognize('')
assert dfa.recognize('a')
assert dfa.recognize('b')
assert dfa.recognize('cccccc')
assert dfa.recognize('adddd')
assert dfa.recognize('bdddd')

assert not dfa.recognize('dddddd')
assert not dfa.recognize('cdddd')
assert not dfa.recognize('aa')
assert not dfa.recognize('ab')
assert not dfa.recognize('ddddc')