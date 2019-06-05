from src.main.python.Grammar import ContainerSet
from src.main.python.automaton.DFA import DFA


def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            moves.update(automaton.transitions[state][symbol])
        except KeyError:
            pass
    return moves


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
                print(transitions[state.id, symbol])
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = trans.id

    finals = [state.id for state in states if state.is_final]
    dfa = DFA(len(states), finals, transitions)

    return dfa
