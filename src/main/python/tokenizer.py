import collections
import re

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
token_specification = [
    ('NO_TERMINAL', r'\w(?=-->)|\w([\t\r\f\v ])*(?=-->)'),  # Upper Case Letter
    ('ARROW', r'-->'),  # Arrow operator for productions
    ('PIPE', r'[|]'),  # Productions separator
    ('EPSILON', r'epsilon'),  # epsilon
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

        value = mo.group(kind) if kind != 'EPSILON' else 'ε'
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
