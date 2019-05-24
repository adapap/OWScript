import re
import Definitions
from Definitions import Entity, Condition

class Token:
    """Raw tokens extracted from input stream."""
    def __init__(self, type_, value='', definitions=[]):
        self.type = type_
        self.value = value
        self.definitions = definitions

    def __str__(self):
        if self.type in ['NEWLINE', 'INDENT', 'DEDENT']:
            return f'<{self.type}>'
        return f'<{self.type}: {self.value}>'
    __repr__ = __str__

INDENT = Token('INDENT', 'Indent')
DEDENT = Token('DEDENT', 'Dedent')

class Lexer:
    """Generates a list of tokens to be parsed."""
    def __init__(self, text):
        self.text = text
        self.cursor = 0
        self.tokens = []
        self.indents = []
        self.keywords = ['Rule', 'Event', 'Conditions', 'Actions']
        self.definitions = {cls: cls() for cls in Definitions.types}

    def find_indentation(self):
        """Parses the input text to find indents and dedents."""
        regex = re.compile(r'[ \t]+')
        match = regex.match(self.text, self.cursor)
        spaces = len(match.group(0)) if match else 0
        if spaces > self.indents[-1]:
            self.indents.append(spaces)
            self.tokens.append(INDENT)
        elif spaces < self.indents[-1]:
            while spaces < self.indents[-1]:
                self.indents.pop()
                self.tokens.append(DEDENT)
        self.cursor += spaces

    def lex(self):
        """Generates the tokens by using regular expressions."""
        expressions = [
            (r'\Z', 'EOF'),
            (r'^\s*.*:', 'COMMENT'),
            (r'->', 'MAP'),
            (r'[_a-zA-Z][_a-zA-Z0-9 \-]*', 'NAME'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r'\[', 'LBRACK'),
            (r'\]', 'RBRACK'),
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r':', 'COLON'),
            (r',', 'COMMA'),
            (r'(?<!=)=(?!=)|\+=|-=|\*=|\/=', 'ASSIGN'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MUL'),
            (r'\/', 'DIV'),
            (r'(<=?|>=?|!=|==)', 'COMPARE'),
            (r'(\"|\')((?<!\\)\\\1|.)*?\1', 'STRING'),
            (r'(True|False)', 'BOOLEAN'),
            (r'\d+\.\d*', 'FLOAT'),
            (r'\d+', 'INTEGER'),
            (r'[ \t]+', 'WHITESPACE'),
            (r'\n+', 'NEWLINE')
        ]
        assert not re.match(r'^[ \t]+', self.text)
        self.indents.append(0)
        while self.cursor < len(self.text):
            for expr in expressions:
                pattern, tag = expr
                regex = re.compile(pattern)
                match = regex.match(self.text, self.cursor)
                if match:
                    self.cursor = match.end()
                    value = match.group(0).strip()
                    token = Token(tag, value)
                    if tag == 'NEWLINE':
                        self.tokens.append(token)
                        self.find_indentation()
                        break
                    elif tag == 'NAME':
                        if value in self.keywords:
                            token = Token('KEYWORD', value)
                        for class_, obj in self.definitions.items():
                            params = obj.definitions
                            name = class_.__name__.upper()
                            if value in params.keys():
                                token = Token(type_=name,
                                    value=value,
                                    definitions=params.get(value))
                                break
                            elif value in obj.aliases.keys():
                                token = Token(type_=name,
                                    value=obj.aliases.get(value),
                                    definitions=params.get(obj.aliases.get(value)))
                                break
                    if tag not in ('COMMENT', 'WHITESPACE'):
                        self.tokens.append(token)
                    break
            else:
                print('No match.')
                self.cursor += 1
        while self.indents[-1] > 0:
            self.indents.pop()
            self.tokens.append(DEDENT)
        self.tokens.append(Token('EOF', None))
        return self.tokens