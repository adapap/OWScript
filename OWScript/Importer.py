from .Lexer import Lexer
from .Parser import Parser

def import_file(path):
    with open(path) as f:
        text = f.read() + '\n'
    try:
        lexer = Lexer(text=text)
        tokens = lexer.lex()
        parser = Parser(tokens=tokens)
        tree = parser.script()
        return tree
    except Exception as ex:
        raise ex