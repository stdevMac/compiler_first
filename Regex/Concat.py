def regex_concat(first, second):
    if first is None or second is None:
        return None
    if first == 'Epsilon':
        if second == 'Epsilon':
            return 'Epsilon'
        else:
            return second
    else:
        if second == 'Epsilon':
            return first
        else:
            return first + second
