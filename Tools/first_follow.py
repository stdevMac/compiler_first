from Grammar.ContainerSet import ContainerSet
import copy

from Tools.printer import pprint


def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

    return first_alpha


# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
    firsts = {}
    change = True

    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    # init First(Vn)
    for non_terminal in G.nonTerminals:
        firsts[non_terminal] = ContainerSet()

    while change:
        change = False

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            # get current First(X)
            first_x = firsts[X]

            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except:
                first_alpha = firsts[alpha] = ContainerSet()

            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)

            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_x.hard_update(local_first)

    # First(Vt) + First(Vt) + First(RightSides)
    return firsts


def compute_follows(G, firsts):
    follows = {}
    change = True

    # init Follow(Vn)
    for non_terminal in G.nonTerminals:
        follows[non_terminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            for w in range(0, len(alpha)):
                if alpha[w].IsTerminal:
                    continue

                if w < len(alpha) - 1:
                    t = alpha[w + 1]
                else:
                    t = G.Epsilon
                    if w == len(alpha) - 1:
                        change = follows[alpha[w]].add(follows[X])
                        continue
                first = firsts[t]
                cop = copy.copy(first)
                cop.set_epsilon(False)
                change = follows[alpha[w]].add(cop)
                if first.contains_epsilon:
                    change = follows[alpha[w]].add(follows[X])

    return follows


def build_parsing_table(grammar, firsts, follows):
    # init parsing table
    m = {}
    terminals = grammar.terminals
    terminals.append(grammar.EOF)
    # P: X -> alpha
    for production in grammar.Productions:
        x = production.Left
        alpha = production.Right
        for term in grammar.terminals:

            f = firsts[alpha]
            if alpha.IsEpsilon:
                if term in follows[x].set:
                    m[x, str(term)] = []
                    m[x, str(term)].append(production)
            elif str(term) in f:
                m[x, str(term)] = []
                m[x, str(term)].append(production)

    return m


def method_predicted_non_recursive(G, M=None, firsts=None, follows=None):
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)

    # parser construction...
    def parser(w):

        stack = []
        output = []
        stack.append(G.startSymbol)
        cursor = 0
        while len(stack) > 0 and cursor < len(w):
            top = stack.pop()
            symbol = w[cursor]
            if top.IsTerminal:
                if top.Name == symbol:
                    cursor += 1
                    continue
                pp_output = pprint(output)
                joined = ' '.join(w)
                raise Exception(f"Malformed Expression {joined} {pp_output}")
            try:
                # Take the production top apply
                prod = M[top, symbol][0]
            except:
                raise Exception(f"Malformed Expression {w.join(' ')}" + pprint(output))
            output.append(prod)

            # cursor += 1
            if prod.Right.IsEpsilon:
                continue
            tmp = []
            for p in prod.Right:
                tmp.append(p)
            for i in reversed(tmp):
                stack.append(i)

        return output

    # parser is ready!!!
    return parser


def compute_first_follow(G):
    # Testing table
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    # M = build_parsing_table(G, firsts, follows)
    return firsts, follows
