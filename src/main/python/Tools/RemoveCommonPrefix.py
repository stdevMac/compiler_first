from queue import Queue

from src.main.python.Grammar.Sentence import Sentence


def rm_common_prefix(grammar):
    """

    :type grammar: Grammar
    """
    grammar.Productions = []
    q = Queue()

    for non_terminal in grammar.nonTerminals:
        q.put(non_terminal)

    while not q.empty():
        non_terminal = q.get()
        visited = set()

        productions = non_terminal.productions.copy()
        non_terminal.productions = []

        for i in range(len(productions)):
            if productions[i] not in visited:
                length = len(productions[i].Right)

                common_prefixes = []
                for prodct in productions[i:]:
                    counter = 0

                    for index in range(min(len(productions[i].Right), len(prodct.Right))):
                        if productions[i].Right[index] == prodct.Right[index]:
                            counter += 1
                        else:
                            break
                    if counter > 0:
                        common_prefixes.append(prodct)
                        length = min(length, counter)
                if len(common_prefixes) > 1:
                    visited.update(common_prefixes)
                    tmp = grammar.NonTerminal(f'{non_terminal.Name}{i + 1}')

                    non_terminal %= (Sentence(*productions[i].Right[:length]) + tmp)


                    for nt in grammar.nonTerminals:
                        if nt.Name == non_terminal.Name:
                            nt = non_terminal
                            for p in nt.productions:
                                grammar.Productions.append(p)
                            break


                    for prodct in common_prefixes:
                        if length == len(prodct.Right):
                            tmp %= grammar.Epsilon
                        else:
                            tmp %= Sentence(*prodct.Right[length:])

                else:
                    visited.add(productions[i])
                    grammar.Productions.append(productions[i])



