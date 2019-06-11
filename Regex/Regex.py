from Regex.Concat import regex_concat
from Regex.Remove import regex_remove
from Regex.Star import regex_star
from Regex.Union import regex_union


def regexp_from_automaton(automaton, alphabet):
    """
    Build the  regular expression for
    a NFA
    """
    table = [[None for _ in range(len(automaton) + 1)] for _ in range(len(automaton) + 1)]
    for i in range(0, len(automaton)):
        for j in range(0, len(automaton)):
            if i == j:
                table[i][j] = 'Epsilon'
            for symbol in alphabet:
                try:
                    if automaton[j] in automaton[i].transitions[symbol]:
                        table[i][j] = regex_union(table[i][j], symbol.Name)
                except:
                    try:
                        if automaton[j] in automaton[i].transitions[symbol.Name]:
                            table[i][j] = regex_union(table[i][j], '')
                    except:
                        continue

    final_states = []
    for i in range(0, len(automaton)):
        if automaton[i].final:
            final_states.append(i)
            continue
        if i != 0:
            table = regex_remove(table, i, len(automaton))

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
            regex_star(table[0][0]),
            table[0][final_states[0]]
        )
    else:
        re = 'complex'
    return re
