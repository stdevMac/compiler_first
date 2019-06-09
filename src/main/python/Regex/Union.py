def regex_union(first, second):
    if first is None:
        if second is None:
            return None
        else:
            return second
    else:
        if second is None or second == 'Epsilon':
            return first
        else:
            if first == 'Epsilon':
                return  second
            else:
                return f'({first}|{second})'
