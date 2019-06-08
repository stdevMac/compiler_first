from src.main.python.Regex.Concat import regex_concat
from src.main.python.Regex.Pow import regex_pow
from src.main.python.Regex.Remove import regex_remove
from src.main.python.Regex.Star import regex_star
from src.main.python.Regex.Union import regex_union


def regexp_from_automaton(automaton, alphabet):
    """
    Build the  regular expression for
    a NFA
    """
    table = [[None for _ in range(len(automaton) + 1)] for _ in range(len(automaton) + 1)]
    pass
    for i in range(1, len(automaton)+1):
        for j in range(1, len(automaton)+1):
            if i == j:
                table[i][j] = 'Epsilon'
            for symbol in alphabet:
                if automaton[i - 1].has_transition(symbol):
                    table[i][j] = regex_union(table[i][j], symbol.Name)
    final_states = []
    for i in range(1, len(automaton)+1):
        if automaton[i - 1].final:
            final_states.append(i-1)
            continue
        if i != 1:
            table = regex_remove(table, i, len(automaton) + 1)

    if len(final_states) == 1:
        # e := #star(L[s,s]) .
        #      #L[s,f] .
        #      ##star(
        #      ##     #L[f,s] .
        #      ##     ##star(
        #      ##     ##    L[s,s]
        #      ##     ##    ) .
        #      ##     #L[s,f] +
        #      ##     # #   L[f,f]
        #      ##     #)
        re = regex_concat(
            regex_concat(
                regex_star(
                    regex_union(
                        regex_concat(
                            regex_concat(
                                regex_star(table[1][1]),
                                table[final_states[0]][1]),
                            table[1][final_states[0]]),
                        table[final_states[0]][final_states[0]])),
                table[1][final_states[0]]),
            table[1][1])
    else:
        re = 'complex'
    return re
