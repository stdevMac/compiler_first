def regex_union(first, second):
    if first is None or second is None:
        return None
    if first is None or first == 'Epsilon':
        return second
    if second is None or second == 'Epsilon':
        return first
    return f'({first}|{second})'
