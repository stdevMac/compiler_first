def regex_star(exp):
    if exp is None or exp == 'Epsilon':
        return None
    return f'({exp})*'
