def regex_pow(first):
    if first is None or first == 'Epsilon':
        return None
    return f'({first})*'
