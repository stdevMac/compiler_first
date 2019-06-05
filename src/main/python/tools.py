import collections
import json
import re
from queue import Queue

from src.main.python.Grammar import Grammar, Sentence

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

    final_terminals, final_non_terminals = set(terminals).difference(non_terminals + ['epsilon']), set(non_terminals)

    data = json.dumps({
        'NonTerminals': [symbol for symbol in non_terminals if symbol in final_non_terminals
                         and final_non_terminals.discard(symbol) is None],
        'Terminals': [symbol for symbol in terminals if symbol in final_terminals
                      and final_terminals.discard(symbol) is None],
        'Productions': productions
    })

    return Grammar.from_json(data)


def rm_immediate_left_recursion(grammar):
    grammar.Productions = []
    non_terminals = grammar.nonTerminals.copy()

    for non_terminal in non_terminals:
        recursion = [p.Right[1:] for p in non_terminal.productions if len(p.Right) > 0 and p.Right[0] == non_terminal]
        no_recursion = [p.Right for p in non_terminal.productions if len(p.Right) == 0 or p.Right[0] != non_terminal]

        if len(recursion) > 0:
            non_terminal.productions = []
            tmp = grammar.NonTerminal(f'{non_terminal.name}0')

            for p in no_recursion:
                non_terminal %= Sentence(*p) + tmp

            for p in recursion:
                tmp %= Sentence(*p) + tmp

            tmp %= grammar.Epsilon

        else:
            grammar.Productions.extend(non_terminal.productions)


def rm_common_prefix(grammar):
    grammar.Productions = []
    q = Queue()

    for non_terminal in grammar.nonTerminals:
        q.put(non_terminal)

    while not q.empty():
        non_terminal = q.get()
        visited = set()

        productions = non_terminal.productions.copy()
        non_terminal.productions = []

        for i in range(len(productions)):
            if productions[i] not in visited:
                length = len(productions[i].Right)

                common_prefixs = []
                for prodct in productions[i:]:
                    counter = 0

                    for index in range(min(len(productions[i].Right), len(prodct.Rigth))):
                        if productions[i].Right[index] == prodct.Rigth[index]:
                            counter += 1
                        else:
                            break
                    if counter > 0:
                        common_prefixs.append(prodct)
                        length = min(length, counter)
                if length(common_prefixs) > 1:
                    visited.update(common_prefixs)
                    tmp = grammar.NonTerminal(f'{non_terminal.Name}{i + 1}')

                    non_terminal %= Sentence(*productions[i].Right[:length]) + tmp
                    for prodct in common_prefixs:
                        if length == length(prodct.Rigth):
                            tmp %= grammar.Epsilon
                        else:
                            tmp %= Sentence(*prodct.Rigth[length:])

                    q.put(tmp)
                else:
                    visited.add(productions[i])
                    non_terminal %= productions[i].Right
