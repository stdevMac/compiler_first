import collections
import json
import re

from Grammar.Grammar import Grammar

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
token_specification = [
    ('NO_TERMINAL', r'\w(?=-->)|\w([\t\r\f\v ])*(?=-->)'),  # Upper Case Letter
    ('ARROW', r'-->'),  # Arrow operator for productions
    ('PIPE', r'[|]'),  # Productions separator
    ('EPSILON', r'Epsilon'),  # epsilon
    ('PRODUCTION', r'([()[\]{}!"·%&/=*+-._?¿¡,;.:><a-zA-Z0-9_])+'),  # Production
    ('NEWLINE', r'\n'),  # Line endings
    ('WHITESPACE', r'[\t\r\f\v ]'),
]


def get_type(item):
    for name, pattern in token_specification:
        regs = re.compile(pattern)
        if regs.match(item):
            return name
    return 1


def tokenize(code: str):
    """
    input: Grammar like
                    Z --> Ax | epsilon
                    A --> epsilon | Ass | esa
    Return: Collection of tokens
    """
    tokens = []
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup

        value = mo.group(kind) if kind != 'EPSILON' else 'Epsilon'
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'WHITESPACE':
            pass
        else:
            column = mo.start() - line_start
            value = value.lstrip().rstrip()
            tokens.append(Token(kind, value, line_num, column))
    return tokens


def grammar_from_tokens(tokens):
    terminals = []
    non_terminals = []
    productions = []
    line_num = 1
    while True:
        line = [x for x in tokens if x.line == line_num]
        if len(line) == 0:
            break
        if line[0] not in non_terminals:
            non_terminals.append(line[0].value)
        current_body = []
        for i in range(2, len(line)):
            if line[i].typ == 'PIPE':
                productions.append({'Head': line[0].value, 'Body': current_body})
                terminals.extend(productions[-1]['Body'])
                current_body = []
                continue
            current_body.append(line[i].value)
        productions.append({'Head': line[0].value, 'Body': current_body})
        terminals.extend(productions[-1]['Body'])
        line_num += 1
    if 'Epsilon' in terminals:
        final_terminals, final_non_terminals = \
            set(terminals).difference(non_terminals), set(non_terminals)
    else:
        final_terminals, final_non_terminals = \
            set(terminals).difference(non_terminals + ['Epsilon']), set(non_terminals)

    data = json.dumps({
        'NonTerminals': [symbol for symbol in non_terminals if symbol in final_non_terminals
                         and final_non_terminals.discard(symbol) is None],
        'Terminals': [symbol for symbol in terminals if symbol in final_terminals
                      and final_terminals.discard(symbol) is None],
        'Productions': productions,
        'StartSymbol': non_terminals[0]
    })

    return Grammar.from_json(data)


def tokenize_input(code: str, grammar: Grammar=None):
    if grammar is None:
        return code.split(' ')
    terminal_tokens = []
    for token in code.split(' '):
        for terminal in grammar.terminals:
            if terminal.Name == token:
                terminal_tokens.append(terminal)
    terminal_tokens.append(grammar.EOF)
    return terminal_tokens
