from Grammar.Sentence import Sentence


def rm_immediate_left_recursion(grammar):
    grammar.Productions = []
    non_terminals = grammar.nonTerminals.copy()

    for non_terminal in non_terminals:
        recursion = [p.Right[1:] for p in non_terminal.productions if len(p.Right) > 0 and p.Right[0] == non_terminal]
        no_recursion = [p.Right for p in non_terminal.productions if len(p.Right) == 0 or p.Right[0] != non_terminal]

        if len(recursion) > 0:
            non_terminal.productions = []
            tmp = grammar.NonTerminal(f'{non_terminal.Name}0')

            for p in no_recursion:
                non_terminal %= Sentence(*p) + tmp

            for p in non_terminal.productions:
                if p not in grammar.Productions:
                    grammar.Productions.append(p)

            for p in recursion:
                tmp %= Sentence(*p) + tmp

            tmp %= grammar.Epsilon

        else:
            grammar.Productions.extend(non_terminal.productions)
