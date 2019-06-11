def multi_line_formatter(state):
    return '\n'.join(str(item) for item in state)


def lr0_formatter(state):
    try:
        return '\n'.join(str(item)[:-4] for item in state)
    except TypeError:
        return str(state)[:-4]


def empty_formatter(state):
    return ''
