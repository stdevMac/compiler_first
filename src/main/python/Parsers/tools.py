from src.main.python.Automata.State import State
from src.main.python.Automata.formaters import multi_line_formatter
from src.main.python.Grammar.ContainerSet import ContainerSet
from src.main.python.Grammar.Item import Item
from src.main.python.Parsers.ShiftReduceParser import ShiftReduceParser
from src.main.python.Tools.first_follow import compute_local_first, compute_firsts


def build_LR0_automaton(grammar):
    assert len(grammar.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = grammar.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [start_item]
    visited = {start_item: automaton}

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        next_symbol = current_item.NextSymbol

        next_item = current_item.NextItem()
        if not next_item in visited:
            pending.append(next_item)
            visited[next_item] = State(next_item, True)

        if next_symbol.IsNonTerminal:
            for prod in next_symbol.productions:
                next_item = Item(prod, 0)
                if not next_item in visited:
                    pending.append(next_item)
                    visited[next_item] = State(next_item, True)

        current_state = visited[current_item]

        current_state.add_transition(next_symbol.Name, visited[current_item.NextItem()])

        if next_symbol.IsNonTerminal:
            for prod in next_symbol.productions:
                current_state.add_epsilon_transition(visited[Item(prod, 0)])

    return automaton


def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return 'S' + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action == ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value


def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    look_a_heads = ContainerSet()

    for preview in item.Preview():
        look_a_heads.hard_update(compute_local_first(firsts, preview))

    assert not look_a_heads.contains_epsilon

    return [Item(prod, 0, look_a_heads) for prod in next_symbol.productions]


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            look_a_heads = centers[center]
        except KeyError:
            centers[center] = look_a_heads = set()
        look_a_heads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}


def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


def build_lr1_automaton(grammar):
    assert len(grammar.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(grammar)
    firsts[grammar.EOF] = ContainerSet(grammar.EOF)

    start_production = grammar.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(grammar.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in grammar.terminals + grammar.nonTerminals:

            kernels = goto_lr1(current_state.state, symbol, just_kernel=True)

            if not kernels:
                continue

            try:
                next_state = visited[kernels]
            except KeyError:
                pending.append(kernels)
                visited[pending[-1]] = next_state = State(frozenset(goto_lr1(current_state.state, symbol, firsts)),
                                                          True)

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multi_line_formatter)
    return automaton
