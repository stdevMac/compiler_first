def regex_concat(first, second):
    if first is None or first == 'Epsilon':
        return second
    if second is None or second == 'Epsilon':
        return first
    return first + second
