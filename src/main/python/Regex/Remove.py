from src.main.python.Regex.Concat import regex_concat
from src.main.python.Regex.Star import regex_star
from src.main.python.Regex.Union import regex_union


def regex_remove(table, k, length):
    for i in range(1, length):
        for j in range(1, length):
            table[i][j] = regex_union(table[i][j],
                                      regex_concat(
                                          regex_concat(
                                              table[i][k],
                                              regex_star(table[k][k])),
                                          table[k][j])
                                      )

    return table

