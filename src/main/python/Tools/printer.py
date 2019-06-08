def pprint(item, header=""):
    sol = ''
    if header:
        sol += header + '\n'
    if isinstance(item, dict):
        for key, value in item.items():
            sol += f'{key}  --->  {value}' + '\n'
    elif isinstance(item, list):
        sol += '[' + '\n'
        for x in item:
            sol += f'   {repr(x)}' + '\n'
        sol += ']' + '\n'
    else:
        sol += item + '\n'
    return sol
