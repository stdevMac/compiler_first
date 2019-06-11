import json

from Grammar.AttributeProduction import AttributeProduction
from Grammar.EOF import EOF
from Grammar.Epsilon import Epsilon
from Grammar.NonTerminal import NonTerminal
from Grammar.Sentence import Sentence
from Grammar.Terminal import Terminal
from Tools.printer import pprint
from Automata.tools import *
from Automata.NFA import *


class Grammar:

    def __init__(self):

        self.Productions = []
        self.nonTerminals = []
        self.terminals = []
        self.startSymbol = None
        # production type
        self.pType = None
        self.Epsilon = Epsilon(self)
        self.EOF = EOF(self)

        self.symbDict = {'$': self.EOF}

    def NonTerminal(self, name, startSymbol=False):

        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = NonTerminal(name, self)

        if startSymbol:

            if self.startSymbol is None:
                self.startSymbol = term
                self.nonTerminals.insert(0, term)
            else:
                raise Exception("Cannot define more than one start symbol.")
        else:
            self.nonTerminals.append(term)
        self.symbDict[name] = term
        return term

    def NonTerminals(self, names):

        ans = tuple((self.NonTerminal(x) for x in names.strip().split()))

        return ans

    def Add_Production(self, production):

        if len(self.Productions) == 0:
            self.pType = type(production)

        assert type(production) == self.pType, "The Productions most be of only 1 type."

        # for avoid repeated productions
        if production not in production.Left.productions:
            production.Left.productions.append(production)
            self.Productions.append(production)

    def Terminal(self, name):

        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = Terminal(name, self)
        self.terminals.append(term)
        self.symbDict[name] = term
        return term

    def Terminals(self, names):

        ans = tuple((self.Terminal(x) for x in names.strip().split()))

        return ans

    def __str__(self):

        mul = '%s, '

        ans = 'Non-Terminals:\n'

        nonterminals = mul * (len(self.nonTerminals) - 1) + '%s\n'

        ans += nonterminals % tuple(self.nonTerminals)

        ans += 'Terminals:\n'

        terminals = mul * (len(self.terminals) - 1) + '%s\n'

        ans += terminals % tuple(self.terminals)

        ans += 'Productions:\n'

        ans += pprint(self.Productions)

        return ans

    def __getitem__(self, name):
        try:
            return self.symbDict[name]
        except KeyError:
            return None

    @property
    def to_json(self):

        productions = []

        for p in self.Productions:
            head = p.Left.Name

            body = []

            for s in p.Right:
                body.append(s.Name)

            productions.append({'Head': head, 'Body': body})

        d = {'NonTerminals': [symb.Name for symb in self.nonTerminals],
             'Terminals': [symb.Name for symb in self.terminals],
             'Productions': productions}

        # [{'Head':p.Left.Name, "Body": [s.Name for s in p.Right]} for p in self.Productions]
        return json.dumps(d)

    @staticmethod
    def from_json(data):
        data = json.loads(data)

        G = Grammar()
        dic = {'Epsilon': G.Epsilon}

        for term in data['Terminals']:
            dic[term] = G.Terminal(term)
        start_symbol = data['StartSymbol']
        for noTerm in data['NonTerminals']:
            if noTerm is start_symbol:
                dic[noTerm] = G.NonTerminal(noTerm, True)
                continue
            dic[noTerm] = G.NonTerminal(noTerm)

        for p in data['Productions']:
            head = p['Head']
            if 'Epsilon' in p['Body']:
                dic[head] %= Epsilon(G)
                continue
            dic[head] %= Sentence(*[dic[term] for term in p['Body']])

        # here is the automata !!!
        # aut = G.DFA()

        return G

    def copy(self):
        G = Grammar()
        # G.Productions = self.Productions.copy()
        G.Productions = []
        for p in self.Productions:
            G.Productions.append(p.copy())

        G.nonTerminals = self.nonTerminals.copy()

        G.terminals = self.terminals.copy()

        G.pType = self.pType
        G.startSymbol = self.startSymbol
        G.Epsilon = self.Epsilon
        G.EOF = self.EOF
        G.symbDict = self.symbDict.copy()

        return G

    @property
    def IsAugmentedGrammar(self):
        augmented = 0
        for left, right in self.Productions:
            if self.startSymbol == left:
                augmented += 1
        if augmented <= 1:
            return True
        else:
            return False

    def AugmentedGrammar(self, force=False):
        if not self.IsAugmentedGrammar or force:

            G = self.copy()
            # S, self.startSymbol, SS = self.startSymbol, None, self.NonTerminal('S\'', True)
            S = G.startSymbol
            G.startSymbol = None
            SS = G.NonTerminal('S\'', True)
            if G.pType is AttributeProduction:
                SS %= S + G.Epsilon, lambda x: x
            else:
                SS %= S + G.Epsilon

            return G
        else:
            return self.copy()

    def DFA(self):
        trans = {}
        map = {}
        finals = []

        for i in range(len(self.nonTerminals)):
            map[self.nonTerminals[i]] = i

        extra = False
        for j in self.Productions:
            if len(j.Right) == 1 and not j.IsEpsilon:
                extra = True
                break

        if extra:
            map['#'] = len(self.nonTerminals)
            map['f'] = len(self.nonTerminals) + 1
            trans[(map['#'], '$')] = [map['f']]
        else:
            map['f'] = len(self.nonTerminals)

        finals.append(map['f'])

        for j in self.Productions:
            s = j.Right[0]
            if len(j.Right) == 1:
               if j.IsEpsilon:
                   trans[(map[j.Left], '$')] = [map['f']]
               else:
                   trans[(map[j.Left], j.Right[0])] = [map['#']]
            else:
                trans[(map[j.Left], j.Right[0])] = [map[j.Right[1]]]

        automaton = NFA(states=len(map), finals=finals, transitions=trans)

        return nfa_to_dfa(automaton)
