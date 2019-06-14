import re
from Tokens import Token, Tokens

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 0
        self.column = 0
        self.indents = []
        self.tokens = []

    def lex(self):
        """Tokenizes input into a list of tokens."""
        expressions = [(token, re.compile(pattern, re.I)) for token, pattern in Tokens.__annotations__.items()]
        while self.pos < len(self.text):
            self.pos += 1