import re

class Token:
    """Raw tokens extracted from input stream."""
    def __init__(self, type_, value=''):
        self.type = type_
        self.value = value

    def __str__(self):
        if self.type in ['NEWLINE', 'INDENT', 'DEDENT']:
            return f'{self.value}'
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
        keywords = ['Rule', 'Event', 'Conditions', 'Actions']
        event_types = []#['Ongoing - Global', 'Ongoing - Each Player']
        conditions = ['All True', 'Has Spawned']
        arrays = ['All Players']
        expressions = [
            (r'\Z', 'EOF'),
            (r'^\s*.*:', 'COMMENT'),
            (r'[_a-zA-Z][_a-zA-Z0-9 \-]*[a-zA-Z0-9]', 'NAME'),
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
                    value = match.group(0)
                    token = Token(tag, value)
                    if tag == 'NEWLINE':
                        self.tokens.append(token)
                        self.find_indentation()
                        break
                    elif tag == 'NAME':
                        if value in keywords:
                            token = Token('KEYWORD', value)
                        elif value in event_types:
                            token = Token('EVENT_TYPE', value)
                        elif value in conditions:
                            token = Token('CONDITION', value)
                        elif value in arrays:
                            token = Token('ARRAY', value)
                    if tag not in ('COMMENT', 'WHITESPACE'):
                        self.tokens.append(token)
                    break
            else:
                print('No match.')
                self.cursor += 1
                self.column += 1
        while self.indents[-1] > 0:
            self.indents.pop()
            self.tokens.append(DEDENT)
        self.tokens.append(Token('EOF', None))
        return self.tokens