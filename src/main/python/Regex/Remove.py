from src.main.python.Regex.Concat import regex_concat
from src.main.python.Regex.Star import regex_star
from src.main.python.Regex.Union import regex_union
import copy


def regex_remove(table, k, length):
    table_copy = copy.deepcopy(table)
    for i in range(0, length):
        for j in range(0, length):
            if i == k or j == k:
                continue
            # L[i, i] += L[i, k].star(L[k, k]).L[k, i]
            table_copy[i][i] = regex_union(table[i][i],
                                           regex_concat(
                                               regex_concat(
                                                   table[i][k],
                                                   regex_star(table[k][k])),
                                               table[k][i])
                                           )
            # L[j, j] += L[j, k].star(L[k, k]).L[k, j]
            table_copy[j][j] = regex_union(table[j][j],
                                           regex_concat(
                                               regex_concat(
                                                   table[j][k],
                                                   regex_star(table[k][k])),
                                               table[k][j])
                                           )
            # L[i, j] += L[i, k].star(L[k, k]).L[k, j]
            table_copy[i][j] = regex_union(table[i][j],
                                           regex_concat(
                                               regex_concat(
                                                   table[i][k],
                                                   regex_star(table[k][k])),
                                               table[k][j])
                                           )
            # L[j, i] += L[j, k].star(L[k, k]).L[k, i]
            table_copy[j][i] = regex_union(table[j][i],
                                           regex_concat(
                                               regex_concat(
                                                   table[j][k],
                                                   regex_star(table[k][k])),
                                               table[k][i])
                                           )

    return table_copy
