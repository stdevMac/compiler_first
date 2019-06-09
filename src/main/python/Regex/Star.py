def regex_star(exp):
    if exp is None:
        return None
    if exp == 'Epsilon':
        return 'Epsilon'
    return f'({exp})*'
