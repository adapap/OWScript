"""Lexer rules to be interpreted by PLY."""
import re
from ply import lex

# Reserved
from Workshop import actions, values, types
reserved_list = []
reserved_list.extend([(x, 'ACTION') for x in actions])
reserved_list.extend([(x, 'VALUE') for x in values])
reserved_list.extend([(x, 'EVENT_TYPE') for x in types.get('EVENT').get('values')])
reserved_list.extend([(x, 'NUMBER') for x in types.get('NUMBER').get('values')])
reserved_list.extend([('EVENT', 'EVENT'), ('CONDITIONS', 'CONDITIONS'), ('ACTIONS', 'ACTIONS')])
reserved = dict(reserved_list)
aliases_list = [
    ('ROUND', 'ROUND TO INTEGER')
]
aliases = {k: reserved.get(v) for k, v in dict(aliases_list).items()}
reserved.update(aliases)

# Token Names
tokens = (
    'COMMENT',
    'ASSIGN',
    'MAP',
    'RULE',
    'QUOTE',
    'NAME',
    'BOOLEAN',
    'FLOAT',
    'INTEGER',
    'COMPARE',
    'WHITESPACE',
    'NEWLINE',
    'INDENT',
    'DEDENT',
    'EOF'
) + (
    'ACTION', 'VALUE', 'EVENT_TYPE', 'NUMBER',
    'FUNC', 'GLOBAL_VAR', 'PLAYER_VAR',
    'EVENT', 'CONDITIONS', 'ACTIONS'
)

literals = '+-*/%^:(),'

t_ASSIGN = r'(?<!=)=(?!=)|\+=|-=|\*=|\/=|\^='
t_MAP = r'\->'
t_QUOTE = r'(\'|\")'
t_BOOLEAN = r'(True|False)'
t_FLOAT = r'\d+\.\d*'
t_INTEGER = r'\d+'
t_COMPARE = r'(<=?|>=?|!=|==)'
t_WHITESPACE = r'[ \t]+'
t_NEWLINE = r'\n+'
# Ignore Whitespace
# t_ignore = r'[ \t\r]+'

def _new_token(type_, lineno, lexpos, value=None):
    tok = lex.LexToken()
    tok.type = type_
    tok.value = value
    tok.lineno = lineno
    tok.lexpos = lexpos
    return tok

def t_RULE(t):
    r'Rule\s+("[^"]+")'
    t.value = t.lexer.lexmatch.group(2)
    return t

def t_COMMENT(t):
    r'[^:\s]+:\s*'
    return t

def t_NAME(t):
    r'([_a-zA-Z][_a-zA-Z0-9\- ]*)\b'
    match = t.lexer.lexmatch.group(0)
    if match.startswith('gVar'):
        _, var = re.split(r'\s+', match)
        return _new_token('GLOBAL_VAR', t.lineno, t.lexpos, value=var)
    if match.startswith('pVar'):
        _, var = re.split(r'\s+', match)
        return _new_token('PLAYER_VAR', t.lineno, t.lexpos, value=var)
    t.type = reserved.get(t.value.upper(), 'NAME')
    return t

def t_eof(t):
    #if not t.lexer.eof:
    if t.lexer.indents[-1] > 0:
        t.lexer.indents.pop()
        return _new_token('DEDENT', t.lineno, t.lexpos)
        # t.lexer.eof = True
        # return _new_token('EOF', t.lineno, t.lexpos)
    return None

def t_error(t):
    print(f'Unrecognized character "{t.value[0]}"')
    t.lexer.skip(1)

class IndentLexer:
    def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
        self.lexer = lex.lex(debug=debug, optimize=optimize,
                             lextab=lextab, reflags=reflags)
        self.token_stream = None
        self.lexer.indents = [0]
        #self.lexer.eof = False

    def input(self, s):
        self.lexer.paren_count = 0
        self.lexer.input(s)
        self.token_stream = self.indentation()

    def indentation(self):
        tokens = iter(self.lexer.token, None)
        token_list = []
        for t in tokens:
            if t.type == 'NEWLINE':
                t.value = '\n'
                token_list.append(t)
                remaining = self.lexer.lexdata[self.lexer.lexpos:]
                whitespace = re.match(r'[ \t]+', remaining)
                if not whitespace and self.lexer.indents[-1] > 0:
                    while self.lexer.indents[-1] > 0:
                        self.lexer.indents.pop()
                        token_list.append(_new_token('DEDENT', t.lineno, t.lexpos))
            elif t.type == 'WHITESPACE' and token_list[-1].type == 'NEWLINE':
                indent = len(t.value)
                if indent > self.lexer.indents[-1]:
                    self.lexer.indents.append(indent)
                    token_list.append(_new_token('INDENT', t.lineno, t.lexpos))
                elif indent < self.lexer.indents[-1]:
                    while indent < self.lexer.indents[-1]:
                        self.lexer.indents.pop()
                        token_list.append(_new_token('DEDENT', t.lineno, t.lexpos))
            elif t.type == 'WHITESPACE':
                continue
            else:
                token_list.append(t)
        for token in token_list:
            yield token

    def token(self):
        try:
            return next(self.token_stream)
        except StopIteration:
            return None

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t
    __next__ = next
Lexer = IndentLexer()