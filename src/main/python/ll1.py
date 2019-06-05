def is_register(table, state, symbol, value):
    if state not in table:
        table[state] = dict()

    row = table[state]

    if symbol not in row:
        row[symbol] = []

    cell = row[symbol]

    if value not in cell:
        cell.append(value)

    return len(cell) == 1


def build_ll1_table(grammar, first, follow):
    table = {}
    is_ll1 = True

    for production in grammar.Productions:
        x = production.Left
        alpha = production.Right

        first_alpha = first[alpha]
        for symbol in first_alpha:
            is_ll1 = is_ll1 and is_register(table, x, symbol, production)

        if first_alpha.contains_epsilon:
            for symbol in follow[x]:
                is_ll1 = is_ll1 and is_register(table, x, symbol, production)

    return table, is_ll1
